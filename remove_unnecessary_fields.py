# remove_unnecessary_fields.py
import os
import sys
import django
import sqlite3

sys.path.append('/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import connection

def analyze_cotisation_structure():
    """Analyse la structure de la table cotisation"""
    
    print("🔍 Analyse de la table assureur_cotisation")
    print("="*60)
    
    with connection.cursor() as cursor:
        # 1. Voir les colonnes actuelles
        cursor.execute("PRAGMA table_info(assureur_cotisation)")
        columns = cursor.fetchall()
        
        print("📋 Colonnes actuelles:")
        essential_columns = ['id', 'membre_id', 'periode', 'type_cotisation', 'montant', 
                           'date_emission', 'date_echeance', 'date_paiement', 'statut',
                           'reference', 'enregistre_par_id', 'notes', 'created_at', 'updated_at']
        
        unnecessary_columns = []
        
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            
            if col_name in essential_columns:
                print(f"  ✅ {col_name:30} ({col_type}) - Essentiel")
            elif col_name in ['montant_clinique', 'montant_pharmacie', 'montant_charges_mutuelle']:
                print(f"  ❌ {col_name:30} ({col_type}) - INUTILE (à supprimer)")
                unnecessary_columns.append(col_name)
            else:
                print(f"  ⚠️  {col_name:30} ({col_type}) - Autre")
        
        # 2. Vérifier s'il y a des données dans ces colonnes
        print(f"\n📊 Vérification des données dans les colonnes inutiles...")
        for col in unnecessary_columns:
            cursor.execute(f"SELECT COUNT(*) FROM assureur_cotisation WHERE {col} != 0")
            count = cursor.fetchone()[0]
            if count > 0:
                print(f"  ⚠️  {col}: {count} enregistrement(s) avec des données (vérifiez avant suppression)")
            else:
                print(f"  ✅ {col}: 0 enregistrement avec des données (peut être supprimée)")
        
        return unnecessary_columns

def create_clean_migration():
    """Crée une migration pour nettoyer les champs inutiles"""
    
    print("\n" + "="*60)
    print("🛠️  Création de la migration de nettoyage")
    print("="*60)
    
    # 1. Créer une migration vide
    print("1. Création de la migration...")
    os.system('python manage.py makemigrations --empty assureur --name remove_unused_cotisation_fields')
    
    # Trouver le fichier de migration
    import glob
    migration_files = glob.glob('assureur/migrations/000*.py')
    if migration_files:
        latest_migration = max(migration_files)
        print(f"   Migration créée: {latest_migration}")
        
        # 2. Créer le contenu de la migration
        migration_content = '''"""
Migration pour supprimer les champs inutiles de la table Cotisation.
Ces champs ne devraient pas être dans une cotisation de membre.
"""
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('assureur', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cotisation',
            name='montant_charges_mutuelle',
        ),
        migrations.RemoveField(
            model_name='cotisation',
            name='montant_clinique',
        ),
        migrations.RemoveField(
            model_name='cotisation',
            name='montant_pharmacie',
        ),
    ]
'''
        
        # 3. Écrire la migration
        with open(latest_migration, 'w') as f:
            f.write(migration_content)
        
        print("   ✅ Migration écrite")
        
        return latest_migration
    else:
        print("   ❌ Aucune migration trouvée")
        return None

def check_and_fix_views():
    """Vérifie et corrige les vues qui utilisent ces champs"""
    
    print("\n" + "="*60)
    print("🔧 Vérification des vues")
    print("="*60)
    
    # Vérifier le fichier views.py
    views_path = 'assureur/views.py'
    
    with open(views_path, 'r') as f:
        content = f.read()
    
    # Rechercher les références aux champs problématiques
    problematic_fields = ['montant_clinique', 'montant_pharmacie', 'montant_charges_mutuelle']
    
    print("Recherche des références dans views.py:")
    for field in problematic_fields:
        count = content.count(field)
        if count > 0:
            print(f"  ⚠️  {field}: {count} occurrence(s) - À corriger")
        else:
            print(f"  ✅ {field}: 0 occurrence")
    
    # Afficher les lignes problématiques
    print("\n📝 Lignes à corriger dans views.py:")
    lines = content.split('\n')
    for i, line in enumerate(lines):
        for field in problematic_fields:
            if field in line:
                print(f"  Ligne {i+1}: {line.strip()}")

def quick_fix_views():
    """Correction rapide des vues pour enlever les champs problématiques"""
    
    print("\n" + "="*60)
    print("⚡ Correction rapide des vues")
    print("="*60)
    
    views_path = 'assureur/views.py'
    
    with open(views_path, 'r') as f:
        content = f.read()
    
    # Correction 1: Fonction creer_cotisation_membre
    old_code_1 = """    # Créer la cotisation
    cotisation = Cotisation(
        membre=membre,
        periode=periode,
        montant=montant,
        statut='due',
        date_emission=date_emission,
        date_echeance=date_echeance,
        type_cotisation=type_cotisation,
        reference=reference,
        enregistre_par=request.user,
        notes=notes,
        # Champs obligatoires avec valeurs par défaut
        montant_clinique=Decimal('0.00'),
        montant_pharmacie=Decimal('0.00'),
        montant_charges_mutuelle=Decimal('0.00'),
    )"""
    
    new_code_1 = """    # Créer la cotisation
    cotisation = Cotisation(
        membre=membre,
        periode=periode,
        montant=montant,
        statut='due',
        date_emission=date_emission,
        date_echeance=date_echeance,
        type_cotisation=type_cotisation,
        reference=reference,
        enregistre_par=request.user,
        notes=notes,
    )"""
    
    # Correction 2: Fonction generer_cotisations
    old_code_2 = """        # Créer la cotisation
        cotisation = Cotisation(
            membre=membre,
            periode=periode,
            montant=montant,
            statut='due',
            date_emission=date_emission,
            date_echeance=date_echeance,
            type_cotisation=type_cotisation,
            reference=reference,
            enregistre_par=request.user if request.user.is_authenticated else None,
            notes='Générée automatiquement',
            # Champs obligatoires avec valeurs par défaut
            montant_clinique=Decimal('0.00'),
            montant_pharmacie=Decimal('0.00'),
            montant_charges_mutuelle=Decimal('0.00'),
        )"""
    
    new_code_2 = """        # Créer la cotisation
        cotisation = Cotisation(
            membre=membre,
            periode=periode,
            montant=montant,
            statut='due',
            date_emission=date_emission,
            date_echeance=date_echeance,
            type_cotisation=type_cotisation,
            reference=reference,
            enregistre_par=request.user if request.user.is_authenticated else None,
            notes='Générée automatiquement',
        )"""
    
    # Appliquer les corrections
    if old_code_1 in content:
        content = content.replace(old_code_1, new_code_1)
        print("✅ Correction 1 appliquée (creer_cotisation_membre)")
    
    if old_code_2 in content:
        content = content.replace(old_code_2, new_code_2)
        print("✅ Correction 2 appliquée (generer_cotisations)")
    
    # Sauvegarder
    with open(views_path, 'w') as f:
        f.write(content)
    
    print("📁 Fichier views.py mis à jour")

def main():
    """Fonction principale"""
    
    print("🚀 Nettoyage des champs inutiles de Cotisation")
    print("="*60)
    
    # 1. Analyser la structure
    unnecessary_columns = analyze_cotisation_structure()
    
    if not unnecessary_columns:
        print("\n✅ Aucun champ inutile trouvé")
        return
    
    # 2. Vérifier les vues
    check_and_fix_views()
    
    # 3. Demander confirmation
    print("\n" + "="*60)
    response = input("❓ Voulez-vous corriger automatiquement les vues ? (o/n): ")
    
    if response.lower() == 'o':
        quick_fix_views()
    
    # 4. Demander pour la migration
    print("\n" + "="*60)
    response = input("❓ Voulez-vous créer une migration pour supprimer ces champs ? (o/n): ")
    
    if response.lower() == 'o':
        migration_file = create_clean_migration()
        if migration_file:
            print(f"\n📋 Migration créée: {migration_file}")
            print("\n⚠️  AVANT D'APPLIQUER LA MIGRATION:")
            print("1. Assurez-vous d'avoir une sauvegarde de la base de données")
            print("2. Vérifiez que ces champs ne contiennent pas de données importantes")
            print("3. Lancez: python manage.py migrate assureur")
            print("\n🔧 Si la migration échoue à cause du trigger, exécutez d'abord:")
            print("   python repair_database.py")
    
    print("\n" + "="*60)
    print("📋 Récapitulatif des actions:")
    print("1. Les champs inutiles ont été identifiés")
    print("2. Les vues ont été corrigées (si demandé)")
    print("3. Une migration de nettoyage a été créée (si demandé)")
    print("\n⚠️  N'oubliez pas:")
    print("   - Vérifiez que le modèle Cotisation n'a pas ces champs")
    print("   - Lancez les migrations après vérification")
    print("   - Testez la création de cotisation")

if __name__ == "__main__":
    main()