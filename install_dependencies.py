import os
import sys
import subprocess

def install_requirements():
    """Installe les dépendances depuis requirements.txt"""
    print("📦 Installation des dépendances...")
    
    try:
        # Vérifier si requirements.txt existe
        if not os.path.exists('requirements.txt'):
            print("❌ requirements.txt non trouvé")
            return False
        
        # Installer les dépendances
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dépendances installées avec succès")
            return True
        else:
            print(f"❌ Erreur lors de l'installation: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def create_missing_files():
    """Crée les fichiers manquants"""
    print("📁 Création des fichiers manquants...")
    
    files_to_create = {
        'constants.py': '''
"""
Constantes pour l'application mutuelle_core
"""

# Statuts des membres
class StatutMembre:
    ACTIF = 'ACTIF'
    INACTIF = 'INACTIF'
    SUSPENDU = 'SUSPENDU'
    CHOICES = [
        (ACTIF, 'Actif'),
        (INACTIF, 'Inactif'),
        (SUSPENDU, 'Suspendu'),
    ]

# Catégories de membres
class CategorieMembre:
    STANDARD = 'STANDARD'
    PREMIUM = 'PREMIUM'
    FAMILLE = 'FAMILLE'
    CHOICES = [
        (STANDARD, 'Standard'),
        (PREMIUM, 'Premium'),
        (FAMILLE, 'Famille'),
    ]

# Configuration de l'application
class Config:
    # Taux de remboursement par défaut
    TAUX_REMBOURSEMENT_DEFAULT = 80
    
    # Durée de validité des bons (en jours)
    DUREE_VALIDITE_BON = 30
    
    # Montant minimum de cotisation
    COTISATION_MINIMUM = 5000
    
    # Devise
    DEVISE = 'FCFA'

# URLs des dashboards
DASHBOARD_URLS = {
    'assureur': '/assureur-dashboard/',
    'medecin': '/medecin-dashboard/',
    'pharmacien': '/pharmacien-dashboard/',
    'membre': '/membre-dashboard/',
    'generic': '/generic-dashboard/',
}
''',
        'requirements.txt': '''Django>=4.2,<5.0
django-crispy-forms
crispy-bootstrap5
Pillow
python-decouple
django-debug-toolbar
django-extensions
whitenoise
gunicorn
psycopg2-binary
reportlab
openpyxl
python-dateutil
requests
'''
    }
    
    for filename, content in files_to_create.items():
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content.strip())
            print(f"✅ {filename} créé")
        else:
            print(f"⚠️  {filename} existe déjà")
    
    return True

def main():
    print("🚀 INSTALLATION DES DÉPENDANCES ET CRÉATION DES FICHIERS")
    print("=" * 60)
    
    # Créer les fichiers manquants
    if not create_missing_files():
        print("❌ Erreur lors de la création des fichiers")
        return
    
    # Installer les dépendances
    if not install_requirements():
        print("❌ Erreur lors de l'installation des dépendances")
        return
    
    print("\n🎉 INSTALLATION TERMINÉE AVEC SUCCÈS!")
    print("📋 Prochaines étapes:")
    print("   1. Vérifiez que utils.py existe")
    print("   2. Testez avec: python test_final_integration.py")
    print("   3. Démarrez le serveur: python manage.py runserver")

if __name__ == "__main__":
    main()