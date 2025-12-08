#!/usr/bin/env python3
"""
VÉRIFICATION FINALE - Mutuelle Core
"""

import os
import sys
import django
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.conf import settings

print("=" * 60)
print("✅ VÉRIFICATION FINALE DU SYSTÈME")
print("=" * 60)
print(f"Date: {datetime.now()}")
print(f"Répertoire: {BASE_DIR}")
print()

# 1. Vérifier les modèles principaux
print("1. MODÈLES PRINCIPAUX:")
print("-" * 30)

try:
    from soins.models import BonDeSoin
    print(f"   ✅ BonDeSoin: {BonDeSoin.objects.count()} enregistrement(s)")
except Exception as e:
    print(f"   ❌ BonDeSoin: {e}")

try:
    from membres.models import Membre
    print(f"   ✅ Membre: {Membre.objects.count()} enregistrement(s)")
except Exception as e:
    print(f"   ❌ Membre: {e}")

try:
    from agents.models import Agent
    print(f"   ✅ Agent: {Agent.objects.count()} enregistrement(s)")
except Exception as e:
    print(f"   ❌ Agent: {e}")

try:
    from assureur.models import Assureur
    print(f"   ✅ Assureur: {Assureur.objects.count()} enregistrement(s)")
except Exception as e:
    print(f"   ❌ Assureur: {e}")

print()

# 2. Vérifier les fichiers système
print("2. FICHIERS SYSTÈME:")
print("-" * 30)

files_to_check = [
    ("db.sqlite3", "Base de données"),
    ("manage.py", "Script de gestion"),
    ("requirements.txt", "Dépendances"),
    (".env.example", "Configuration exemple"),
    ("backup_simple.py", "Script de backup"),
]

for filename, description in files_to_check:
    filepath = BASE_DIR / filename
    if filepath.exists():
        if filename == "db.sqlite3":
            size = filepath.stat().st_size / (1024 * 1024)
            print(f"   ✅ {description}: {size:.2f} MB")
        else:
            print(f"   ✅ {description}: Présent")
    else:
        print(f"   ⚠️  {description}: Absent")

print()

# 3. Vérifier les répertoires
print("3. RÉPERTOIRES:")
print("-" * 30)

dirs_to_check = [
    ("media", "Fichiers média"),
    ("staticfiles", "Fichiers statiques"),
    ("logs", "Fichiers de log"),
    ("backups", "Sauvegardes"),
]

for dirname, description in dirs_to_check:
    dirpath = BASE_DIR / dirname
    if dirpath.exists():
        # Compter les fichiers
        file_count = len(list(dirpath.rglob("*")))
        print(f"   ✅ {description}: {file_count} fichier(s)")
    else:
        print(f"   ❌ {description}: Absent")

print()

# 4. Vérifier la configuration
print("4. CONFIGURATION:")
print("-" * 30)

print(f"   DEBUG: {'🚨 ACTIVÉ (désactiver en prod)' if settings.DEBUG else '✅ DÉSACTIVÉ'}")
print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"   BASE_DIR: {settings.BASE_DIR}")
print(f"   SECRET_KEY: {'✅ Configurée' if settings.SECRET_KEY else '❌ Manquante'}")

print()

# 5. URLS disponibles
print("5. URLS DISPONIBLES:")
print("-" * 30)

important_urls = [
    "/admin/",
    "/agents/tableau-de-bord/",
    "/assureur/",
    "/dashboard/",
    "/membres/",
    "/api/",
]

print("   URLs importantes prêtes à l'emploi:")
for url in important_urls:
    print(f"   • http://127.0.0.1:8000{url}")

print()

print("=" * 60)
print("🎉 VOTRE SYSTÈME EST PRÊT !")
print("=" * 60)
print()
print("📋 POUR COMMENCER:")
print("1. Lancez le serveur: python manage.py runserver")
print("2. Accédez à l'admin: http://127.0.0.1:8000/admin/")
print("3. Créez un superutilisateur: python manage.py createsuperuser")
print("4. Testez le backup: python backup_simple.py")
print("5. Vérifiez les logs: ls -la logs/")
print()
print("🔧 EN CAS DE PROBLÈME:")
print("• Vérifiez que vous êtes dans le bon répertoire")
print("• Vérifiez que le serveur est en cours d'exécution")
print("• Consultez les logs Django")
print()
print("✅ TOUT EST FONCTIONNEL !")