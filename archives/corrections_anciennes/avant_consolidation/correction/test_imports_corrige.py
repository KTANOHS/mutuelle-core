import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("🔍 TEST DES IMPORTS")
print("===================")

try:
    # Essayer différents noms d'apps
    from member.models import Membre
    print("✅ Membre importé depuis 'member.models'")
except ImportError:
    try:
        from membres.models import Membre
        print("✅ Membre importé depuis 'membres.models'")
    except ImportError:
        try:
            # Essayer l'import direct
            from mutuelle_core.member.models import Membre
            print("✅ Membre importé depuis 'mutuelle_core.member.models'")
        except ImportError as e:
            print(f"❌ Impossible d'importer Membre: {e}")

try:
    from bon_soin.models import BonDeSoin
    print("✅ BonDeSoin importé depuis 'bon_soin.models'")
except ImportError:
    try:
        from bons_soins.models import BonDeSoin
        print("✅ BonDeSoin importé depuis 'bons_soins.models'")
    except ImportError:
        try:
            from mutuelle_core.bon_soin.models import BonDeSoin
            print("✅ BonDeSoin importé depuis 'mutuelle_core.bon_soin.models'")
        except ImportError as e:
            print(f"❌ Impossible d'importer BonDeSoin: {e}")

try:
    from agents.models import Agent
    print("✅ Agent importé depuis 'agents.models'")
except ImportError as e:
    print(f"❌ Impossible d'importer Agent: {e}")

# Lister toutes les apps installées
from django.apps import apps
print("\n📦 APPS INSTALLÉES:")
for app_config in apps.get_app_configs():
    print(f"  - {app_config.name}")
    for model in app_config.get_models():
        print(f"    └─ {model.__name__}")