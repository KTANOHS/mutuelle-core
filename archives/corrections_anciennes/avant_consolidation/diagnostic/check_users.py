# Créer un fichier de vérification

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()

from django.contrib.auth.models import User

print("=== VÉRIFICATION DES UTILISATEURS ===")

# Vérifier DOUA
try:
    doua = User.objects.get(username='DOUA')
    print(f"✓ DOUA existe")
    print(f"  Email: {doua.email}")
    print(f"  Groupes: {[g.name for g in doua.groups.all()]}")
except User.DoesNotExist:
    print("✗ DOUA n'existe pas")

# Vérifier admin
try:
    admin = User.objects.get(username='admin')
    print(f"✓ Admin existe")
    print(f"  Email: {admin.email}")
    print(f"  Superuser: {admin.is_superuser}")
except User.DoesNotExist:
    print("✗ Admin n'existe pas")

print("\n=== TOUS LES UTILISATEURS ===")
for user in User.objects.all():
    groups = [g.name for g in user.groups.all()]
    print(f"- {user.username} (Email: {user.email}, Superuser: {user.is_superuser}, Groupes: {groups})")

