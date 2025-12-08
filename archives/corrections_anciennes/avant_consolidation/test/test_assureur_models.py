# test_assureur_models.py
import os
import django
import sys

# Configuration Django
sys.path.append('/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import *
from django.contrib.auth.models import User

print("🔍 Diagnostic des modèles assureur")
print("="*50)

# Vérifier les modèles existants
try:
    # Liste tous les modèles de l'application assureur
    from django.apps import apps
    assureur_app = apps.get_app_config('assureur')
    print(f"📊 Modèles dans l'app 'assureur':")
    for model in assureur_app.get_models():
        print(f"  ✅ {model.__name__}: {model._meta.db_table}")
        print(f"     Champs: {[f.name for f in model._meta.fields]}")
except Exception as e:
    print(f"  ❌ Erreur: {e}")

print("\n👥 Vérification des utilisateurs assureur:")
try:
    assureurs = User.objects.filter(username__icontains='assureur')
    for user in assureurs:
        print(f"  - {user.id}: {user.username} ({user.email})")
except Exception as e:
    print(f"  ❌ Erreur: {e}")