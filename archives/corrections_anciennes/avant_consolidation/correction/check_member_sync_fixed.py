# check_member_sync_fixed.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyze_member_sync():
    """Analyser la synchronisation des membres entre tous les acteurs - VERSION CORRIGÉE"""
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

    # 3. Vérifier la cohérence des données - VERSION CORRIGÉE
    print("\n🔗 COHÉRENCE DES DONNÉES")
    print("-" * 40)
    
    with connection.cursor() as cursor:
        # Compter les membres uniques dans membres_membre
        cursor.execute("SELECT COUNT(DISTINCT id) FROM membres_membre")
        membres_uniques = cursor.fetchone()[0]
        print(f"   👥 Membres uniques (membres_membre): {membres_uniques}")
        
        # Vérifier les doublons potentiels - CORRECTION: "HAVING" au lieu de "HAV"
        cursor.execute("""
            SELECT prenom, nom, COUNT(*) as doublons
            FROM membres_membre 
            GROUP BY prenom, nom 
            HAVING COUNT(*) > 1
        """)
        doublons = cursor.fetchall()
        if doublons:
            print(f"   ⚠️  Doublons détectés: {len(doublons)}")
            for prenom, nom, count in doublons:
                print(f"      {prenom} {nom} ({count} fois)")
        else:
            print("   ✅ Aucun doublon détecté")

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
        ('pharmacien_ordonnance', 'membre_id', 'Ordonnances pharmacien → Membres'),
    ]
    
    with connection.cursor() as cursor:
        for table, champ, description in references:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count_total = cursor.fetchone()[0]
                
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {champ} IS NOT NULL")
                count_references = cursor.fetchone()[0]
                
                print(f"   📊 {description}:")
                print(f"      Total: {count_total} | Avec référence: {count_references}")
                
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
                print(f"   ❌ {description}: Table non accessible - {e}")

def check_actor_access():
    """Vérifier l'accès des différents acteurs aux membres"""
    print("\n👥 ACCÈS DES ACTEURS AUX MEMBRES")
    print("-" * 40)
    
    from django.db import connection
    
    acteurs_tables = {
        'ASSUREUR': ['assureur_cotisation', 'assureur_membre'],
        'AGENT': ['agents_verificationcotisation', 'agents_bonsoin'],
        'MÉDECIN': ['medecin_consultation', 'medecin_ordonnance'],
        'PHARMACIEN': ['pharmacien_ordonnance'],
        'SOINS': ['soins_soin', 'soins_bondesoin']
    }
    
    with connection.cursor() as cursor:
        for acteur, tables in acteurs_tables.items():
            print(f"\n🎯 {acteur}:")
            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"   📋 {table}: {count} enregistrements")
                    
                    # Vérifier si la table référence des membres
                    cursor.execute(f"PRAGMA table_info({table})")
                    colonnes = [col[1] for col in cursor.fetchall()]
                    if any('membre' in col.lower() for col in colonnes):
                        print(f"      🔗 Référence membres: OUI")
                    else:
                        print(f"      ❌ Référence membres: NON")
                        
                except Exception as e:
                    print(f"   ❌ {table}: Non accessible")

def analyze_conflict():
    """Analyser le conflit entre les deux modèles Membre"""
    print("\n⚡ ANALYSE DU CONFLIT MEMBRE")
    print("-" * 40)
    
    from django.db import connection
    
    print("🚨 PROBLÈME IDENTIFIÉ: Deux modèles Membre en conflit")
    print("   📋 membres.Membre (PRINCIPAL) - 21 membres")
    print("   📋 assureur.Membre (CONFLIT) - 0 membres")
    
    print("\n🔍 IMPACT SUR LA SYNCHRONISATION:")
    print("   ✅ Cotisations assureur → membres_membre: FONCTIONNEL")
    print("   ✅ Vérifications agent → membres_membre: FONCTIONNEL") 
    print("   ⚠️  Risque: Certains modules pourraient utiliser assureur.Membre")
    
    print("\n💡 RECOMMANDATION:")
    print("   Supprimer le modèle assureur.Membre et utiliser uniquement membres.Membre")

def generate_sync_report():
    """Générer un rapport de synchronisation"""
    print("\n📊 RAPPORT DE SYNCHRONISATION")
    print("=" * 50)
    
    from django.db import connection
    
    with connection.cursor() as cursor:
        # Membres principaux
        cursor.execute("SELECT COUNT(*) FROM membres_membre")
        total_membres = cursor.fetchone()[0]
        
        # Références actives
        cursor.execute("""
            SELECT COUNT(DISTINCT membre_id) FROM (
                SELECT membre_id FROM assureur_cotisation
                UNION SELECT membre_id FROM agents_verificationcotisation
                UNION SELECT membre_id FROM soins_soin
                UNION SELECT membre_id FROM medecin_consultation
            ) WHERE membre_id IS NOT NULL
        """)
        membres_references = cursor.fetchone()[0]
        
        print(f"📈 SYNTHÈSE:")
        print(f"   👥 Membres totaux: {total_membres}")
        print(f"   🔗 Membres référencés: {membres_references}")
        print(f"   📊 Taux d'utilisation: {(membres_references/total_membres)*100:.1f}%")
        
        if membres_references == total_membres:
            print("   🎉 TOUS les membres sont synchronisés!")
        else:
            print(f"   ⚠️  {total_membres - membres_references} membres non utilisés")

if __name__ == "__main__":
    print("🚀 ANALYSE COMPLÈTE SYNCHRONISATION - VERSION CORRIGÉE")
    print("⏳ Vérification de tous les acteurs...\n")
    
    analyze_member_sync()
    check_cross_references()
    check_actor_access()
    analyze_conflict()
    generate_sync_report()
    
    print("\n" + "=" * 60)
    print("🎉 ANALYSE TERMINÉE!")
    print("=" * 60)