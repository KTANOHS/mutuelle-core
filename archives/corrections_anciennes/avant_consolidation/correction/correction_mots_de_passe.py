
#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User

print("🔑 CORRECTION DES MOTS DE PASSE")
print("=" * 40)

users = [
    ("DOUA", "DOUA"),
    ("DOUA1", "DOUA1"), 
    ("ktanos", "ktanos"),
    ("ORNELLA", "ORNELLA"),
    ("Yacouba", "Yacouba"),
    ("GLORIA", "GLORIA"),
    ("ASIA", "ASIA"),
]

for username, password in users:
    try:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"✅ {username}: mot de passe défini sur '{password}'")
    except Exception as e:
        print(f"❌ {username}: erreur - {e}")

print("\n✅ Mots de passe mis à jour")
print("\n🔍 Vérification des utilisateurs:")
print("-" * 30)

for username, _ in users:
    try:
        user = User.objects.get(username=username)
        print(f"👤 {username}:")
        print(f"   is_staff: {user.is_staff}")
        print(f"   is_superuser: {user.is_superuser}")
        print(f"   Groupes: {[g.name for g in user.groups.all()]}")
    except:
        print(f"❌ {username}: non trouvé"

