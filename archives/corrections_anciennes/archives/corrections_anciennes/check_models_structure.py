import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import models

print("🔍 STRUCTURE DES MODÈLES:")
print("=" * 50)

# Vérifier le modèle Membre
try:
    from membres.models import Membre
    print("\n📋 MODÈLE MEMBRE:")
    for field in Membre._meta.fields:
        print(f"  - {field.name} ({field.get_internal_type()}) - {'OBLIGATOIRE' if not field.null and not field.blank else 'OPTIONNEL'}")
except Exception as e:
    print(f"❌ Erreur Membre: {e}")

# Vérifier le modèle Medecin
try:
    from medecin.models import Medecin
    print("\n📋 MODÈLE MEDECIN:")
    for field in Medecin._meta.fields:
        print(f"  - {field.name} ({field.get_internal_type()}) - {'OBLIGATOIRE' if not field.null and not field.blank else 'OPTIONNEL'}")
except Exception as e:
    print(f"❌ Erreur Medecin: {e}")

# Vérifier le modèle Pharmacien
try:
    from pharmacien.models import Pharmacien
    print("\n📋 MODÈLE PHARMACIEN:")
    for field in Pharmacien._meta.fields:
        print(f"  - {field.name} ({field.get_internal_type()}) - {'OBLIGATOIRE' if not field.null and not field.blank else 'OPTIONNEL'}")
except Exception as e:
    print(f"❌ Erreur Pharmacien: {e}")

# Vérifier le modèle SpecialiteMedicale
try:
    from medecin.models import SpecialiteMedicale
    print("\n📋 MODÈLE SPECIALITEMEDICALE:")
    for field in SpecialiteMedicale._meta.fields:
        print(f"  - {field.name} ({field.get_internal_type()}) - {'OBLIGATOIRE' if not field.null and not field.blank else 'OPTIONNEL'}")
        
    # Afficher les spécialités existantes
    specialites = SpecialiteMedicale.objects.all()
    print(f"\n  Spécialités existantes: {specialites.count()}")
    for spec in specialites:
        print(f"    - {spec.nom}")
except Exception as e:
    print(f"❌ Erreur SpecialiteMedicale: {e}")