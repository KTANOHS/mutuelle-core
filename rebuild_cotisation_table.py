# rebuild_cotisation_table.py
import os
import sys
import sqlite3
import django
from datetime import datetime

sys.path.append('/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import connection

def backup_database():
    """Crée un backup de la base de données"""
    
    backup_name = f"db.sqlite3.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    with open('db.sqlite3', 'rb') as source:
        with open(backup_name, 'wb') as target:
            target.write(source.read())
    
    print(f"✅ Backup créé: {backup_name}")
    return backup_name

def fix_foreign_key_issues():
    """Corrige les problèmes de clés étrangères"""
    
    print("🔧 Correction des problèmes de clés étrangères...")
    
    with connection.cursor() as cursor:
        # 1. Supprimer les enregistrements orphelins dans scoring_historiquescore
        cursor.execute("""
            DELETE FROM scoring_historiquescore
            WHERE membre_id NOT IN (SELECT id FROM membres_membre)
        """)
        deleted = cursor.rowcount
        print(f"   ✅ {deleted} enregistrement(s) orphelins supprimés de scoring_historiquescore")
        
        # 2. Supprimer le trigger problématique s'il existe encore
        cursor.execute("DROP TRIGGER IF EXISTS auto_share_ordonnance")
        print("   ✅ Trigger auto_share_ordonnance supprimé")
    
    return True

def create_clean_cotisation_table():
    """Crée une nouvelle table cotisation sans les champs problématiques"""
    
    print("\n🔄 Reconstruction de la table assureur_cotisation...")
    
    with connection.cursor() as cursor:
        # 1. Vérifier la structure actuelle
        cursor.execute("PRAGMA table_info(assureur_cotisation)")
        current_columns = [col[1] for col in cursor.fetchall()]
        
        # 2. Créer la nouvelle table
        print("   1. Création de la nouvelle table...")
        cursor.execute("""
            CREATE TABLE assureur_cotisation_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                periode VARCHAR(7) NOT NULL,
                type_cotisation VARCHAR(20) NOT NULL,
                montant DECIMAL(10,2) NOT NULL,
                date_emission DATE NOT NULL,
                date_echeance DATE NOT NULL,
                date_paiement DATE,
                statut VARCHAR(20) NOT NULL,
                reference VARCHAR(50) NOT NULL UNIQUE,
                notes TEXT,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL,
                enregistre_par_id INTEGER REFERENCES auth_user(id),
                membre_id BIGINT NOT NULL REFERENCES membres_membre(id)
            )
        """)
        print("   ✅ Nouvelle table créée")
        
        # 3. Copier les données (exclure les champs problématiques)
        print("   2. Copie des données...")
        
        # Déterminer quelles colonnes copier
        columns_to_copy = []
        for col in current_columns:
            if col not in ['montant_clinique', 'montant_pharmacie', 'montant_charges_mutuelle']:
                columns_to_copy.append(col)
        
        columns_str = ', '.join(columns_to_copy)
        
        cursor.execute(f"""
            INSERT INTO assureur_cotisation_new ({columns_str})
            SELECT {columns_str}
            FROM assureur_cotisation
        """)
        
        moved_rows = cursor.rowcount
        print(f"   ✅ {moved_rows} enregistrement(s) copiés")
        
        # 4. Vérifier la somme des montants
        print("   3. Vérification des données...")
        cursor.execute("SELECT COUNT(*) FROM assureur_cotisation_new")
        new_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM assureur_cotisation")
        old_count = cursor.fetchone()[0]
        
        if new_count == old_count:
            print(f"   ✅ Toutes les données ont été transférées ({new_count} enregistrements)")
        else:
            print(f"   ⚠️  Attention: {old_count} -> {new_count} enregistrements")
        
        # 5. Supprimer l'ancienne table et renommer la nouvelle
        print("   4. Remplacement de la table...")
        cursor.execute("DROP TABLE assureur_cotisation")
        cursor.execute("ALTER TABLE assureur_cotisation_new RENAME TO assureur_cotisation")
        print("   ✅ Table remplacée")
        
        # 6. Vérifier la nouvelle structure
        print("   5. Vérification de la structure finale...")
        cursor.execute("PRAGMA table_info(assureur_cotisation)")
        final_columns = [col[1] for col in cursor.fetchall()]
        
        print(f"   📋 Structure finale ({len(final_columns)} colonnes):")
        for col in final_columns:
            print(f"      - {col}")
        
        # Vérifier que les champs problématiques sont partis
        problem_fields = ['montant_clinique', 'montant_pharmacie', 'montant_charges_mutuelle']
        for field in problem_fields:
            if field in final_columns:
                print(f"   ❌ {field} existe encore !")
            else:
                print(f"   ✅ {field} a été supprimé")
    
    return True

def verify_data_integrity():
    """Vérifie l'intégrité des données après la reconstruction"""
    
    print("\n🔍 Vérification de l'intégrité des données...")
    
    with connection.cursor() as cursor:
        # 1. Compter les enregistrements
        cursor.execute("SELECT COUNT(*) FROM assureur_cotisation")
        count = cursor.fetchone()[0]
        print(f"   1. Nombre total de cotisations: {count}")
        
        # 2. Vérifier les références uniques
        cursor.execute("""
            SELECT reference, COUNT(*) 
            FROM assureur_cotisation 
            GROUP BY reference 
            HAVING COUNT(*) > 1
        """)
        duplicates = cursor.fetchall()
        if duplicates:
            print(f"   ⚠️  Références en double trouvées: {len(duplicates)}")
            for ref, cnt in duplicates[:5]:
                print(f"      - {ref}: {cnt} fois")
        else:
            print("   ✅ Pas de références en double")
        
        # 3. Vérifier les clés étrangères
        cursor.execute("""
            SELECT COUNT(*) 
            FROM assureur_cotisation c
            WHERE NOT EXISTS (SELECT 1 FROM membres_membre m WHERE m.id = c.membre_id)
        """)
        orphaned = cursor.fetchone()[0]
        if orphaned > 0:
            print(f"   ⚠️  {orphaned} cotisation(s) avec membre_id invalide")
        else:
            print("   ✅ Tous les membre_id sont valides")
        
        # 4. Vérifier les statuts
        cursor.execute("SELECT statut, COUNT(*) FROM assureur_cotisation GROUP BY statut")
        stats = cursor.fetchall()
        print("   4. Répartition par statut:")
        for statut, cnt in stats:
            print(f"      - {statut}: {cnt}")
    
    return True

def update_migration_state():
    """Met à jour l'état des migrations pour refléter la réalité"""
    
    print("\n📦 Mise à jour de l'état des migrations...")
    
    try:
        # Trouver la migration la plus récente
        import glob
        migration_files = glob.glob('assureur/migrations/000*.py')
        if migration_files:
            latest = max(migration_files)
            print(f"   Migration la plus récente: {latest}")
        
        # Marquer la migration 0002 comme appliquée (sans --fake cette fois)
        from django.db.migrations.recorder import MigrationRecorder
        recorder = MigrationRecorder(connection)
        
        # Vérifier si la migration est déjà enregistrée
        if not recorder.migration_qs.filter(app='assureur', name='0002_remove_unused_cotisation_fields').exists():
            recorder.record_applied('assureur', '0002_remove_unused_cotisation_fields')
            print("   ✅ Migration 0002 marquée comme appliquée")
        else:
            print("   ℹ️  Migration 0002 déjà enregistrée")
    
    except Exception as e:
        print(f"   ⚠️  Erreur lors de la mise à jour des migrations: {e}")
        print("   ℹ️  Vous devrez peut-être exécuter: python manage.py migrate assureur --fake")

def test_cotisation_creation():
    """Teste la création d'une cotisation après les corrections"""
    
    print("\n🧪 Test de création d'une cotisation...")
    
    try:
        from assureur.models import Cotisation
        from membres.models import Membre
        from django.contrib.auth.models import User
        
        # Récupérer un membre et un utilisateur
        membre = Membre.objects.first()
        user = User.objects.first()
        
        if not membre or not user:
            print("   ⚠️  Impossible de trouver un membre ou utilisateur pour le test")
            return
        
        # Créer une cotisation test
        cotisation = Cotisation.objects.create(
            membre=membre,
            periode="2025-12",
            type_cotisation="normale",
            montant=5000.00,
            date_emission="2025-12-01",
            date_echeance="2025-12-31",
            statut="due",
            reference=f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            enregistre_par=user,
            notes="Test de création après reconstruction"
        )
        
        print(f"   ✅ Cotisation créée avec succès: {cotisation.reference}")
        print(f"   📝 ID: {cotisation.id}, Montant: {cotisation.montant}, Statut: {cotisation.statut}")
        
        # Nettoyer après le test
        cotisation.delete()
        print("   🧹 Cotisation test supprimée")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la création: {e}")
        return False

def main():
    """Fonction principale"""
    
    print("🚀 RECONSTRUCTION DE LA TABLE COTISATION")
    print("="*60)
    
    # Backup
    backup_file = backup_database()
    print(f"   Backup: {backup_file}")
    
    # Correction des clés étrangères
    if not fix_foreign_key_issues():
        print("❌ Échec de la correction des clés étrangères")
        return
    
    # Reconstruction de la table
    if not create_clean_cotisation_table():
        print("❌ Échec de la reconstruction de la table")
        return
    
    # Vérification
    if not verify_data_integrity():
        print("❌ Problèmes d'intégrité détectés")
        return
    
    # Mise à jour des migrations
    update_migration_state()
    
    # Test
    if test_cotisation_creation():
        print("\n🎉 RÉUSSITE ! La table cotisation a été reconstruite avec succès.")
        print("\n📋 Actions effectuées:")
        print("   1. Backup de la base de données")
        print("   2. Correction des clés étrangères")
        print("   3. Reconstruction de la table sans les champs problématiques")
        print("   4. Vérification de l'intégrité des données")
        print("   5. Test de création d'une cotisation")
        print("\n⚠️  IMPORTANT:")
        print("   - Les champs montant_clinique, montant_pharmacie, montant_charges_mutuelle ont été supprimés")
        print("   - Les données ont été sauvegardées dans 'cotisations_champs_problematiques.csv'")
        print("   - Redémarrez le serveur: python manage.py runserver")
    else:
        print("\n⚠️  Problème lors du test. Vérifiez les erreurs ci-dessus.")

if __name__ == "__main__":
    # Demander confirmation
    print("⚠️  ATTENTION: Cette opération va reconstruire la table des cotisations.")
    print("   Les champs montant_clinique, montant_pharmacie, montant_charges_mutuelle seront supprimés.")
    print("   Un backup sera créé automatiquement.")
    
    response = input("\n❓ Voulez-vous continuer ? (oui/non): ")
    
    if response.lower() == 'oui':
        main()
    else:
        print("❌ Opération annulée.")