#!/usr/bin/env python3
"""
TEST IMMÉDIAT - Mutuelle Core
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

print("🔧 TEST IMMÉDIAT DU SYSTÈME")
print("=" * 50)

# Test 1: Vérifier Django
try:
    sys.path.insert(0, str(BASE_DIR))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    import django
    django.setup()
    print("✅ Django configuré")
except Exception as e:
    print(f"❌ Erreur Django: {e}")

# Test 2: Vérifier les modèles
print("\n2. Test des modèles:")
try:
    from soins.models import BonDeSoin
    print(f"   ✅ BonDeSoin: {BonDeSoin.objects.count()} enregistrements")
except ImportError:
    try:
        from soins.models import BonSoin
        print(f"   ✅ BonSoin: {BonSoin.objects.count()} enregistrements")
    except ImportError as e:
        print(f"   ❌ Erreur: {e}")

# Test 3: Vérifier les répertoires
print("\n3. Répertoires:")
dirs = ['media', 'staticfiles', 'logs']
for d in dirs:
    path = BASE_DIR / d
    if path.exists():
        print(f"   ✅ {d}: Existe")
    else:
        print(f"   ⚠️  {d}: Absent (créer avec: mkdir {d})")

# Test 4: Vérifier la base de données
print("\n4. Base de données:")
db_path = BASE_DIR / 'db.sqlite3'
if db_path.exists():
    size_mb = db_path.stat().st_size / (1024 * 1024)
    print(f"   ✅ db.sqlite3: {size_mb:.2f} MB")
else:
    print("   ❌ db.sqlite3: Non trouvé")

print("\n" + "=" * 50)
print("🎯 ACTIONS IMMÉDIATES:")
print("1. Créer répertoires manquants:")
print("   mkdir -p media staticfiles logs backups")
print("\n2. Lancer le serveur:")
print("   python manage.py runserver")
print("\n3. Tester les URLs:")
print("   • http://127.0.0.1:8000/admin/")
print("   • http://127.0.0.1:8000/agents/tableau-de-bord/")