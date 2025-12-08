# debug_groups.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

def debug_user_groups():
    users = ['test_membre', 'test_agent', 'test_assureur', 'test_medecin', 'test_pharmacien']
    
    for username in users:
        user = User.objects.get(username=username)
        print(f"\n=== {username} ===")
        print(f"Groups: {[g.name for g in user.groups.all()]}")
        print(f"Has agent profile: {hasattr(user, 'agent')}")
        print(f"Has medecin profile: {hasattr(user, 'medecin')}")
        print(f"Has assureur profile: {hasattr(user, 'assureur')}")
        print(f"Has pharmacien profile: {hasattr(user, 'pharmacien')}")
        print(f"Has membre profile: {hasattr(user, 'membre')}")

if __name__ == "__main__":
    debug_user_groups()