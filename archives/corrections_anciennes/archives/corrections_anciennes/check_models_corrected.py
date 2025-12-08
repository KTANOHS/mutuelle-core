# check_models_corrected.py
import os
import django
import sys

sys.path.append('/Users/koffitanohsoualiho/Documents/projet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import models
from medecin import models as medecin_models

print("📋 Modèles disponibles dans medecin.models:")
for attr_name in dir(medecin_models):
    attr = getattr(medecin_models, attr_name)
    try:
        if isinstance(attr, type) and issubclass(attr, models.Model) and attr != models.Model:
            print(f"✅ {attr_name}")
    except:
        pass

print("\n🔍 Vérification des imports spécifiques...")
try:
    from medecin.models import Medicament
    print("✅ Medicament existe")
except ImportError as e:
    print(f"❌ Medicament n'existe pas: {e}")

try:
    from medecin.models import Ordonnance
    print("✅ Ordonnance existe")
except ImportError as e:
    print(f"❌ Ordonnance n'existe pas: {e}")

try:
    from medecin.models import LigneOrdonnance
    print("✅ LigneOrdonnance existe")
except ImportError as e:
    print(f"❌ LigneOrdonnance n'existe pas: {e}")

print("\n📝 Vérification du contenu actuel du fichier models.py...")
try:
    with open('/Users/koffitanohsoualiho/Documents/projet/medecin/models.py', 'r') as f:
        content = f.read()
        if 'class Medicament' in content:
            print("✅ La classe Medicament est définie dans models.py")
        else:
            print("❌ La classe Medicament n'est PAS définie dans models.py")
            
        if 'class Ordonnance' in content:
            print("✅ La classe Ordonnance est définie dans models.py")
        else:
            print("❌ La classe Ordonnance n'est PAS définie dans models.py")
            
        if 'class LigneOrdonnance' in content:
            print("✅ La classe LigneOrdonnance est définie dans models.py")
        else:
            print("❌ La classe LigneOrdonnance n'est PAS définie dans models.py")
except Exception as e:
    print(f"❌ Erreur lecture fichier: {e}")