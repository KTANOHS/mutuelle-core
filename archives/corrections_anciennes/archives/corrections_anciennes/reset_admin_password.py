# reset_admin_password.py
import os
import django
import sys

# Configuration Django
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User

def reset_admin_password():
    print("🔧 RÉINITIALISATION DU MOT DE PASSE ADMIN")
    print("=" * 50)
    
    # Liste des noms d'utilisateur admin courants
    admin_usernames = ['admin', 'administrator', 'superuser', 'root']
    
    for username in admin_usernames:
        try:
            user = User.objects.get(username=username)
            if user.is_superuser:
                nouveau_mdp = "Almoravide1084"  # Changez ce mot de passe
                user.set_password(nouveau_mdp)
                user.save()
                print(f"✅ {username}: Mot de passe réinitialisé -> {nouveau_mdp}")
                return
        except User.DoesNotExist:
            continue
    
    # Si aucun admin trouvé, créer un nouveau
    print("ℹ️ Aucun superutilisateur trouvé, création d'un nouveau...")
    nouveau_mdp = "Almoravide1084"
    User.objects.create_superuser('admin', 'admin@example.com', nouveau_mdp)
    print(f"✅ Nouvel admin créé: admin / {nouveau_mdp}")

if __name__ == "__main__":
    reset_admin_password()