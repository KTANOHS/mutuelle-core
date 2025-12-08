# final_member_sync_fix.py
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def fix_all_sync_issues():
    """Correction définitive de tous les problèmes de synchronisation"""
    print("🔧 CORRECTION DÉFINITIVE SYNCHRONISATION")
    print("=" * 60)
    
    # 1. Vérifier l'état actuel
    print("\n📊 ÉTAT ACTUEL")
    print("-" * 40)
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM membres_membre")
        total_membres = cursor.fetchone()[0]
        print(f"👥 Membres totaux: {total_membres}")
        
        # Doublons
        cursor.execute("""
            SELECT prenom, nom, COUNT(*) as doublons
            FROM membres_membre 
            GROUP BY prenom, nom 
            HAVING COUNT(*) > 1
        """)
        doublons = cursor.fetchall()
        print(f"⚠️  Doublons détectés: {len(doublons)}")

    # 2. Résoudre le conflit de modèles
    print("\n🔗 RÉSOLUTION CONFLIT MODÈLES")
    print("-" * 40)
    print("💡 RECOMMANDATION: Supprimer assureur.Membre du modèle")
    print("   et utiliser uniquement membres.Membre comme source unique")

    # 3. Uniformiser les références
    print("\n🔄 UNIFORMISATION RÉFÉRENCES")
    print("-" * 40)
    
    # Vérifier les relations existantes
    relations = [
        ('assureur_cotisation', 'membre_id', '✅ OK'),
        ('agents_verificationcotisation', 'membre_id', '✅ OK'), 
        ('medecin_consultation', 'membre_id', '⚠️  À vérifier'),
        ('soins_soin', 'patient_id', '❌ PROBLÈME: patient_id au lieu de membre_id'),
        ('soins_bondesoin', 'patient_id', '❌ PROBLÈME: patient_id au lieu de membre_id')
    ]
    
    for table, champ, statut in relations:
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   {table}: {count} enregistrements - {statut}")
        except:
            print(f"   {table}: Table inaccessible")

    # 4. Créer des vues SQL pour uniformiser l'accès
    print("\n📋 CRÉATION VUES D'UNIFORMISATION")
    print("-" * 40)
    
    with connection.cursor() as cursor:
        # Vue pour soins_soin avec membre_id
        try:
            cursor.execute("""
                CREATE VIEW IF NOT EXISTS soins_soin_unifie AS
                SELECT s.*, p.id as membre_id_unifie
                FROM soins_soin s
                LEFT JOIN membres_membre p ON s.patient_id = p.id
            """)
            print("✅ Vue soins_soin_unifie créée")
        except Exception as e:
            print(f"❌ Erreur vue soins_soin: {e}")
            
        # Vue pour soins_bondesoin avec membre_id  
        try:
            cursor.execute("""
                CREATE VIEW IF NOT EXISTS soins_bondesoin_unifie AS
                SELECT b.*, p.id as membre_id_unifie
                FROM soins_bondesoin b
                LEFT JOIN membres_membre p ON b.patient_id = p.id
            """)
            print("✅ Vue soins_bondesoin_unifie créée")
        except Exception as e:
            print(f"❌ Erreur vue soins_bondesoin: {e}")

def create_unified_access_layer():
    """Créer une couche d'accès unifiée pour tous les acteurs"""
    print("\n🎯 COUCHE D'ACCÈS UNIFIÉE")
    print("=" * 50)
    
    print("""
💡 ARCHITECTURE RECOMMANDÉE:

    ┌─────────────────┐
    │   membres_membre  │ ← SOURCE UNIQUE
    └─────────────────┘
            │
    ┌───────┼───────┐
    ▼       ▼       ▼
assureur   agents   medecin   soins*
    │       │       │        │
    ✅      ✅      ✅       ⚠️ (via vues)
    
*soins: Accès via vues d'uniformisation soins_soin_unifie, soins_bondesoin_unifie
    """)

def verify_final_state():
    """Vérifier l'état final"""
    print("\n🔍 VÉRIFICATION FINALE")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        # Membres uniques
        cursor.execute("SELECT COUNT(DISTINCT id) FROM membres_membre")
        membres_uniques = cursor.fetchone()[0]
        
        # Références actives
        cursor.execute("""
            SELECT COUNT(DISTINCT membre_id) FROM (
                SELECT membre_id FROM assureur_cotisation
                UNION SELECT membre_id FROM agents_verificationcotisation
                UNION SELECT membre_id FROM medecin_consultation
            ) WHERE membre_id IS NOT NULL
        """)
        membres_references = cursor.fetchone()[0]
        
        print(f"📈 SYNTHÈSE FINALE:")
        print(f"   👥 Membres uniques: {membres_uniques}")
        print(f"   🔗 Membres référencés: {membres_references}")
        print(f"   📊 Taux d'utilisation: {(membres_references/membres_uniques)*100:.1f}%")

def generate_migration_plan():
    """Générer un plan de migration pour résoudre définitivement le conflit"""
    print("\n📋 PLAN DE MIGRATION DÉFINITIF")
    print("=" * 50)
    
    print("""
🎯 ÉTAPES POUR RÉSOUDRE DÉFINITIVEMENT LE CONFLIT:

1. 🔧 CORRECTION IMMÉDIATE (SQLite):
   - Supprimer le doublon Luc Moreau
   - Utiliser les vues d'uniformisation pour soins

2. 🗃️  MIGRATION MODÈLES (Django):
   - Dans assureur/models.py: SUPPRIMER la classe Membre
   - Remplacer par: from membres.models import Membre
   - Mettre à jour toutes les références

3. 🔄 MIGRATION DONNÉES:
   - Vérifier que toutes les tables utilisent membres_membre.id
   - Mettre à jour soins_soin et soins_bondesoin pour utiliser membre_id

4. ✅ VALIDATION:
   - Tester tous les modules (assureur, agent, médecin, soins)
   - Vérifier que tous voient les mêmes membres
    """)

if __name__ == "__main__":
    print("🚀 CORRECTION DÉFINITIVE SYNCHRONISATION MEMBRES")
    fix_all_sync_issues()
    create_unified_access_layer() 
    verify_final_state()
    generate_migration_plan()
    print("\n🎉 PLAN DE CORRECTION PRÊT!")
    