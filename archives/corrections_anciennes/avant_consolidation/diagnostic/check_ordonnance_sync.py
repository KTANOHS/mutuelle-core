# check_ordonnance_sync.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyze_ordonnance_flow():
    """Analyser le flux ordonnances médecin → pharmacien"""
    print("🔍 ANALYSE FLUX ORDONNANCES MÉDECIN→PHARMACIEN")
    print("=" * 60)
    
    from django.db import connection
    
    # 1. Vérifier l'existence des tables
    print("\n📦 TABLES ORDONNANCES DANS LE SYSTÈME")
    print("-" * 40)
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%ordonnance%'")
        tables_ordonnance = [row[0] for row in cursor.fetchall()]
        
        print("Tables ordonnances trouvées:")
        for table in tables_ordonnance:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   📋 {table}: {count} enregistrements")

    # 2. Analyser la structure des tables d'ordonnances
    print("\n🏗️  STRUCTURE DES TABLES ORDONNANCES")
    print("-" * 40)
    
    tables_to_analyze = ['medecin_ordonnance', 'pharmacien_ordonnance', 'ordonnance_medicament']
    
    for table in tables_to_analyze:
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                print(f"\n📊 {table}:")
                for col in columns[:8]:  # Afficher 8 premières colonnes
                    print(f"   {col[1]} ({col[2]})")
        except Exception as e:
            print(f"❌ {table}: Table non accessible - {e}")

    # 3. Vérifier les relations entre médecins et pharmaciens
    print("\n🔗 RELATIONS MÉDECIN-PHARMACIEN")
    print("-" * 40)
    
    with connection.cursor() as cursor:
        # Vérifier si les ordonnances médecins sont liées aux pharmaciens
        try:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM medecin_ordonnance mo
                LEFT JOIN pharmacien_ordonnance po ON mo.id = po.ordonnance_medecin_id
            """)
            relation_count = cursor.fetchone()[0]
            print(f"📊 Ordos médecins liées à pharmaciens: {relation_count}")
        except Exception as e:
            print(f"❌ Relation médecin-pharmacien: {e}")

    # 4. Vérifier le système de partage
    print("\n🔄 SYSTÈME DE PARTAGE ORDONNANCES")
    print("-" * 40)
    
    # Vérifier les champs de partage dans les tables
    sharing_fields = {
        'medecin_ordonnance': ['est_partagee', 'date_partage', 'pharmacien_id'],
        'pharmacien_ordonnance': ['ordonnance_medecin_id', 'date_reception']
    }
    
    for table, champs in sharing_fields.items():
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"PRAGMA table_info({table})")
                colonnes_existantes = [col[1] for col in cursor.fetchall()]
                
                print(f"\n📋 {table}:")
                for champ in champs:
                    if champ in colonnes_existantes:
                        print(f"   ✅ {champ}: PRÉSENT")
                    else:
                        print(f"   ❌ {champ}: ABSENT")
        except:
            print(f"❌ {table}: Table non accessible")

def test_ordonnance_visibility():
    """Tester la visibilité réelle des ordonnances"""
    print("\n👁️  TEST DE VISIBILITÉ ORDONNANCES")
    print("=" * 50)
    
    from django.db import connection
    
    print("🎯 SCÉNARIO IDÉAL:")
    print("   1. 👨‍⚕️ Médecin crée une ordonnance")
    print("   2. 🔄 Système la rend visible aux pharmaciens")
    print("   3. 💊 Pharmacien peut consulter et traiter")
    
    print("\n🔍 ÉTAT ACTUEL:")
    
    # Vérifier les données existantes
    with connection.cursor() as cursor:
        # Ordos médecins
        cursor.execute("SELECT COUNT(*) FROM medecin_ordonnance")
        ordos_medecins = cursor.fetchone()[0]
        
        # Ordos pharmaciens
        try:
            cursor.execute("SELECT COUNT(*) FROM pharmacien_ordonnance")
            ordos_pharmaciens = cursor.fetchone()[0]
        except:
            ordos_pharmaciens = 0
        
        print(f"   📝 Ordos médecins créées: {ordos_medecins}")
        print(f"   💊 Ordos visibles pharmaciens: {ordos_pharmaciens}")
        
        # Vérifier le lien direct
        try:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM medecin_ordonnance mo
                WHERE EXISTS (
                    SELECT 1 FROM pharmacien_ordonnance po 
                    WHERE po.ordonnance_medecin_id = mo.id
                )
            """)
            ordos_liees = cursor.fetchone()[0]
            print(f"   🔗 Ordos liées médecin→pharmacien: {ordos_liees}")
        except:
            print("   ❌ Impossible de vérifier les liens")

def check_access_control():
    """Vérifier le contrôle d'accès entre médecins et pharmaciens"""
    print("\n🔐 CONTRÔLE D'ACCÈS")
    print("=" * 50)
    
    print("🎯 PERMISSIONS NÉCESSAIRES:")
    print("   ✅ Médecin: Peut créer/modifier ses ordonnances")
    print("   ✅ Pharmacien: Peut voir les ordonnances partagées")
    print("   ❌ Accès croisé: Médecin A ne voit pas ordos Médecin B")
    
    print("\n🔍 VÉRIFICATION MODÈLES:")
    
    # Vérifier les modèles Django pour les permissions
    try:
        from medecin.models import Ordonnance as OrdoMedecin
        from pharmacien.models import Ordonnance as OrdoPharmacien
        
        print("   ✅ Modèle Ordonnance médecin: EXISTE")
        print("   ✅ Modèle Ordonnance pharmacien: EXISTE")
        
        # Vérifier les méthodes de partage
        medecin_methods = [method for method in dir(OrdoMedecin) if 'partage' in method.lower()]
        pharmacien_methods = [method for method in dir(OrdoPharmacien) if 'medecin' in method.lower()]
        
        print(f"   🔄 Méthodes partage médecin: {len(medecin_methods)}")
        print(f"   🔄 Méthodes lien pharmacien: {len(pharmacien_methods)}")
        
    except ImportError as e:
        print(f"   ❌ Modèles non accessibles: {e}")

def simulate_ordonnance_flow():
    """Simuler le flux complet d'une ordonnance"""
    print("\n🎭 SIMULATION FLUX ORDONNANCE")
    print("=" * 50)
    
    print("""
👨‍⚕️  MÉDECIN (Dr Diallo):
    1. Crée ordonnance pour Membre ID 1
    2. Prescrit: Paracétamol, Amoxicilline
    3. Système: Marque comme "partagée"

💊 PHARMACIEN (Pharmacie Centrale):
    1. Voir liste ordonnances partagées
    2. Sélectionne ordonnance Dr Diallo
    3. Prépare médicaments
    4. Marque comme "dispensée"

🔍 RÉSULTAT:
    - ✅ Médecin voit statut "dispensée"
    - ✅ Pharmacien voit prescription complète
    - ✅ Membre peut récupérer médicaments
    """)

def generate_recommendations():
    """Générer des recommandations d'amélioration"""
    print("\n💡 RECOMMANDATIONS POUR LE FLUX ORDONNANCES")
    print("=" * 50)
    
    recommendations = [
        "1. 🔄 IMPLÉMENTER SYSTÈME DE PARTAGE AUTOMATIQUE",
        "2. 📱 NOTIFICATION TEMPS RÉPEL POUR NOUVELLES ORDONNANCES", 
        "3. 🔒 CONTRÔLE D'ACCÈS GRANULAIRE (médecin→pharmacien spécifique)",
        "4. 📊 TABLEAU DE BORD ORDONNANCES POUR PHARMACIENS",
        "5. ⚠️  ALERTES INTERACTIONS MÉDICAMENTEUSES",
        "6. 📋 HISTORIQUE ORDONNANCES PAR MEMBRE"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")

if __name__ == "__main__":
    print("🚀 ANALYSE COMPLÈTE FLUX ORDONNANCES")
    print("⏳ Vérification médecin → pharmacien...\n")
    
    analyze_ordonnance_flow()
    test_ordonnance_visibility()
    check_access_control()
    simulate_ordonnance_flow()
    generate_recommendations()
    
    print("\n" + "=" * 60)
    print("🎉 ANALYSE TERMINÉE!")
    print("=" * 60)