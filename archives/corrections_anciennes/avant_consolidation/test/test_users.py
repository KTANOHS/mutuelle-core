# test_users.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User

print("👥 Utilisateurs existants :")
for user in User.objects.all():
    print(f"  ID: {user.id}, Username: {user.username}, Email: {user.email}")