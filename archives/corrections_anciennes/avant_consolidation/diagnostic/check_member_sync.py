# check_member_sync.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyze_member_sync():
    """Analyser la synchronisation des membres entre tous les acteurs"""
    print("🔍 ANALYSE COMPLÈTE SYNCHRONISATION MEMBRES")
    print("=" * 60)
    
    from django.db import connection
    
    # 1. Vérifier tous les modèles Membre dans le système
    print("\n📦 MODÈLES MEMBRE DANS LE SYSTÈME")
    print("-" * 40)
    
    from django.apps import apps
    membre_models = []
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            if 'membre' in model.__name__.lower():
                membre_models.append(f"{app_config.name}.{model.__name__}")
    
    print("Modèles trouvés:")
    for model in membre_models:
        print(f"   📋 {model}")

    # 2. Analyser les tables de membres
    print("\n🗃️  TABLES MEMBRE DANS LA BASE")
    print("-" * 40)
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%membre%'")
        tables = [row[0] for row in cursor.fetchall()]
        
        for table in tables:
            print(f"\n📊 Table: {table}")
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   👥 Nombre d'enregistrements: {count}")
            
            # Afficher quelques colonnes
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cursor.fetchall()[:5]]  # 5 premières colonnes
            print(f"   📋 Colonnes: {', '.join(columns)}...")

    # 3. Vérifier la cohérence des données
    print("\n🔗 COHÉRENCE DES DONNÉES")
    print("-" * 40)
    
    with connection.cursor() as cursor:
        # Compter les membres uniques dans membres_membre
        cursor.execute("SELECT COUNT(DISTINCT id) FROM membres_membre")
        membres_uniques = cursor.fetchone()[0]
        print(f"   👥 Membres uniques (membres_membre): {membres_uniques}")
        
        # Vérifier les doublons potentiels
        cursor.execute("""
            SELECT prenom, nom, COUNT(*) as doublons
            FROM membres_membre 
            GROUP BY prenom, nom 
            HAV COUNT(*) > 1
        """)
        doublons = cursor.fetchall()
        if doublons:
            print(f"   ⚠️  Doublons détectés: {len(doublons)}")
            for prenom, nom, count in doublons:
                print(f"      {prenom} {nom} ({count} fois)")
        else:
            print("   ✅ Aucun doublon détecté")

    # 4. Vérifier l'accès aux membres par différents acteurs
    print("\n👥 ACCÈS PAR DIFFÉRENTS ACTEURS")
    print("-" * 40)
    
    # Acteurs à vérifier
    acteurs = ['assureur', 'agents', 'medecin', 'pharmacien']
    
    for acteur in acteurs:
        try:
            with connection.cursor() as cursor:
                # Vérifier si l'acteur a une relation avec membres_membre
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' 
                    AND name LIKE ? 
                    AND sql LIKE '%membre%'
                """, [f'%{acteur}%'])
                
                tables_acteur = cursor.fetchall()
                if tables_acteur:
                    print(f"   ✅ {acteur.upper()}: a accès aux membres")
                    for table in tables_acteur:
                        print(f"      📋 Table: {table[0]}")
                else:
                    print(f"   ⚠️  {acteur.upper()}: accès limité aux membres")
                    
        except Exception as e:
            print(f"   ❌ {acteur.upper()}: erreur vérification")

def check_cross_references():
    """Vérifier les références croisées entre acteurs"""
    print("\n🔗 RÉFÉRENCES CROISÉES")
    print("-" * 40)
    
    from django.db import connection
    
    references = [
        ('assureur_cotisation', 'membre_id', 'Cotisations assureur → Membres'),
        ('agents_verificationcotisation', 'membre_id', 'Vérifications agent → Membres'),
        ('soins_soin', 'membre_id', 'Soins → Membres'),
        ('medecin_consultation', 'membre_id', 'Consultations médecin → Membres'),
    ]
    
    with connection.cursor() as cursor:
        for table, champ, description in references:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {champ} IS NOT NULL")
                count = cursor.fetchone()[0]
                print(f"   📊 {description}: {count} références")
                
                # Vérifier l'intégrité des références
                cursor.execute(f"""
                    SELECT COUNT(*) FROM {table} t
                    LEFT JOIN membres_membre m ON t.{champ} = m.id
                    WHERE m.id IS NULL AND t.{champ} IS NOT NULL
                """)
                references_cassées = cursor.fetchone()[0]
                if references_cassées > 0:
                    print(f"      ⚠️  {references_cassées} références cassées")
                else:
                    print(f"      ✅ Toutes les références valides")
                    
            except Exception as e:
                print(f"   ❌ {description}: Table non accessible")

def verify_data_flow():
    """Vérifier le flux de données entre acteurs"""
    print("\n🔄 FLUX DE DONNÉES ENTRE ACTEURS")
    print("-" * 40)
    
    print("🎯 SCÉNARIO IDÉAL:")
    print("   1. ✅ MEMBRES créés dans membres_membre (source unique)")
    print("   2. ✅ ASSUREURS accèdent aux membres pour les cotisations") 
    print("   3. ✅ AGENTS vérifient les cotisations des membres")
    print("   4. ✅ MÉDECINS accèdent aux membres pour les consultations")
    print("   5. ✅ PHARMACIENS accèdent aux membres pour les ordonnances")
    
    print("\n🔍 ÉTAT ACTUEL:")
    with connection.cursor() as cursor:
        # Vérifier l'utilisation réelle
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM assureur_cotisation) as cotisations,
                (SELECT COUNT(*) FROM agents_verificationcotisation) as verifications,
                (SELECT COUNT(*) FROM soins_soin) as soins,
                (SELECT COUNT(*) FROM medecin_consultation) as consultations
        """)
        stats = cursor.fetchone()
        print(f"   💰 Cotisations: {stats[0]}")
        print(f"   ✅ Vérifications: {stats[1]}")
        print(f"   🏥 Soins: {stats[2]}")
        print(f"   👨‍⚕️ Consultations: {stats[3]}")

def generate_recommendations():
    """Générer des recommandations"""
    print("\n💡 RECOMMANDATIONS POUR LA SYNCHRONISATION")
    print("-" * 40)
    
    recommendations = [
        "1. 🎯 UTILISER membres_membre COMME SOURCE UNIQUE DE VÉRITÉ",
        "2. 🔗 TOUS LES ACTEURS DOIVENT RÉFÉRENCER membres_membre.id",
        "3. 📱 CRÉER UNE API CENTRALE POUR LA GESTION DES MEMBRES", 
        "4. 🔄 IMPLÉMENTER UN SYSTÈME DE SYNCHRONISATION TEMPS RÉEL",
        "5. 📊 TABLEAU DE BORD UNIFIÉ POUR TOUS LES ACTEURS"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")

if __name__ == "__main__":
    print("🚀 ANALYSE DE LA SYNCHRONISATION DES MEMBRES")
    print("⏳ Vérification de tous les acteurs...\n")
    
    analyze_member_sync()
    check_cross_references()
    verify_data_flow()
    generate_recommendations()
    
    print("\n" + "=" * 60)
    print("🎉 ANALYSE TERMINÉE!")
    print("=" * 60)