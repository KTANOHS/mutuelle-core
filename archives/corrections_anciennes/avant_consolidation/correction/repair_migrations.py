# repair_migrations_v2.py - SCRIPT AMÉLIORÉ
import os
import shutil
import sys
import subprocess

def run_command(cmd, description):
    """Exécute une commande avec gestion d'erreur"""
    print(f"\n{description}...")
    print(f"Commande: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERREUR: {result.stderr}")
        return False
    print(f"  SUCCÈS: {result.stdout[:200]}...")
    return True

def fix_forms_file():
    """Corrige le fichier forms.py problématique"""
    forms_path = "assureur/forms.py"
    if not os.path.exists(forms_path):
        return True
    
    print("\nCorrection du fichier forms.py...")
    
    # Faire une sauvegarde
    shutil.copy2(forms_path, f"{forms_path}.backup")
    
    # Lire le contenu
    with open(forms_path, 'r') as f:
        content = f.read()
    
    # Remplacer la ligne problématique
    old_line = "choices=[('', 'Tous les statuts')] + [(s, s) for s in Membre.objects.values_list('statut', flat=True).distinct()],"
    new_line = "choices=[('', 'Tous les statuts'), ('actif', 'Actif'), ('en_retard', 'En retard de paiement'), ('inactif', 'Inactif')],"
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        with open(forms_path, 'w') as f:
            f.write(content)
        print("  Ligne corrigée dans forms.py")
        return True
    else:
        print("  La ligne problématique n'a pas été trouvée")
        return True

def repair_migrations():
    print("=== DÉBUT DE LA RÉPARATION DES MIGRATIONS V2 ===")
    
    # 1. Corriger le fichier forms.py
    fix_forms_file()
    
    # 2. Nettoyer les migrations
    print("\n1. Nettoyage des anciennes migrations...")
    migrations_dirs = [
        "membres/migrations/",
        "agents/migrations/",
        "assureur/migrations/",
        "medecin/migrations/",
    ]
    
    for dir_path in migrations_dirs:
        if os.path.exists(dir_path):
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                if item != "__init__.py":
                    try:
                        if os.path.isfile(item_path):
                            print(f"  Suppression fichier: {item_path}")
                            os.remove(item_path)
                        elif os.path.isdir(item_path):
                            print(f"  Suppression dossier: {item_path}")
                            shutil.rmtree(item_path)
                    except Exception as e:
                        print(f"  Erreur suppression {item_path}: {e}")
        else:
            os.makedirs(dir_path, exist_ok=True)
    
    # 3. Créer les fichiers __init__.py
    for dir_path in migrations_dirs:
        init_file = os.path.join(dir_path, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                f.write("")
    
    # 4. Supprimer la base de données
    print("\n2. Nettoyage de la base de données...")
    if os.path.exists("db.sqlite3"):
        os.remove("db.sqlite3")
        print("  Base de données supprimée.")
    else:
        print("  Base de données non trouvée.")
    
    # 5. Créer les migrations en mode silencieux
    print("\n3. Création des migrations (mode silencieux)...")
    
    # D'abord, créons les migrations de base sans charger les vues problématiques
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mutuelle_core.settings'
    
    # Créer une migration minimale d'abord
    success = run_command("python manage.py makemigrations membres --name initial_migration", "Création migration membres")
    if not success:
        print("Tentative de création de migration sans chargement complet...")
        # Essayer avec --empty
        run_command("python manage.py makemigrations membres --empty --name initial", "Création migration vide")
    
    # Puis les autres apps
    for app in ["agents", "assureur", "medecin"]:
        run_command(f"python manage.py makemigrations {app} --name initial", f"Création migration {app}")
    
    # 6. Appliquer les migrations
    print("\n4. Application des migrations...")
    success = run_command("python manage.py migrate", "Application des migrations")
    
    if not success:
        print("\nÉchec de l'application des migrations. Tentative de reset...")
        # Supprimer et recréer la base de données
        if os.path.exists("db.sqlite3"):
            os.remove("db.sqlite3")
        
        # Essayer avec migrate --run-syncdb
        run_command("python manage.py migrate --run-syncdb", "Sync DB")
    
    # 7. Créer un superutilisateur
    print("\n5. Création d'un superutilisateur...")
    create_superuser = """
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superutilisateur créé: admin / admin123')
else:
    print('Superutilisateur existe déjà')
"""
    
    process = subprocess.run(
        ["python", "manage.py", "shell", "-c", create_superuser],
        capture_output=True,
        text=True
    )
    print(process.stdout)
    if process.stderr:
        print("Erreur:", process.stderr)
    
    print("\n=== RÉPARATION TERMINÉE ===")
    print("Vous pouvez maintenant démarrer le serveur:")
    print("python manage.py runserver")

if __name__ == "__main__":
    repair_migrations()