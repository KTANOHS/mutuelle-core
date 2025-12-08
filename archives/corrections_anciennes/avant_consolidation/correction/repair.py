import os
import sys
import subprocess

def run_command(cmd):
    """Exécute une commande et retourne le résultat"""
    print(f"➤ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"✗ Erreur: {result.stderr}")
    else:
        print(f"✓ Succès: {result.stdout}")
    return result.returncode

def main():
    print("="*60)
    print("RÉPARATION COMPLÈTE DU PROJET DJANGO")
    print("="*60)
    
    # 1. Nettoyer les fichiers de cache
    print("\n1. Nettoyage des fichiers de cache...")
    os.system('find . -name "__pycache__" -type d -exec rm -rf {} +')
    os.system('find . -name "*.pyc" -delete')
    os.system('find . -name ".pytest_cache" -type d -exec rm -rf {} +')
    os.system('find . -name ".coverage" -delete')
    
    # 2. Corriger le fichier forms.py problématique
    print("\n2. Correction du fichier forms.py...")
    forms_content = '''class FiltreBonsForm(forms.Form):
    STATUT_CHOICES = [
        ('', 'Tous les statuts'),
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
        ('paye', 'Payé'),
    ]
    
    TYPE_SOIN_CHOICES = [
        ('', 'Tous les types'),
        ('consultation', 'Consultation'),
        ('hospitalisation', 'Hospitalisation'),
        ('pharmacie', 'Pharmacie'),
        ('radiologie', 'Radiologie'),
        ('laboratoire', 'Laboratoire'),
        ('dentaire', 'Dentaire'),
        ('optique', 'Optique'),
    ]

    numero = forms.CharField(required=False, label="Numéro de bon")
    membre = forms.CharField(required=False, label="Nom du membre")
    date_debut = forms.DateField(
        required=False, 
        label="Date de début",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    date_fin = forms.DateField(
        required=False, 
        label="Date de fin",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    statut = forms.ChoiceField(choices=STATUT_CHOICES, required=False, label="Statut")
    type_soin = forms.ChoiceField(choices=TYPE_SOIN_CHOICES, required=False, label="Type de soin")
'''
    
    # Mettre à jour le fichier forms.py
    forms_path = "assureur/forms.py"
    if os.path.exists(forms_path):
        with open(forms_path, 'r') as f:
            content = f.read()
        
        # Remplacer la classe problématique
        import re
        pattern = r'class FiltreBonsForm\(forms\.Form\):.*?def __init__'
        new_content = re.sub(pattern, forms_content + '\n\n    def __init__', content, flags=re.DOTALL)
        
        with open(forms_path, 'w') as f:
            f.write(new_content)
        print("✓ Fichier forms.py corrigé")
    
    # 3. Réinitialiser et recréer les migrations
    print("\n3. Réinitialisation des migrations...")
    run_command("python manage.py migrate --fake")
    run_command("python manage.py makemigrations")
    run_command("python manage.py migrate")
    
    # 4. Créer un superutilisateur
    print("\n4. Création du superutilisateur...")
    run_command('''python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('Superutilisateur créé: admin / admin123')
    else:
        print('Superutilisateur existe déjà')
except Exception as e:
    print('Erreur lors de la création:', str(e))
"''')
    
    # 5. Vérifier que tout fonctionne
    print("\n5. Vérification finale...")
    run_command("python manage.py check")
    
    print("\n" + "="*60)
    print("RÉPARATION TERMINÉE !")
    print("="*60)
    print("\nPour démarrer le serveur :")
    print("python manage.py runserver")
    print("\nIdentifiants par défaut :")
    print("Utilisateur: admin")
    print("Mot de passe: admin123")

if __name__ == "__main__":
    main()