# verifier_modeles.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps

def verifier_champs_modeles():
    print("🔍 STRUCTURE DES MODÈLES")
    print("=" * 50)
    
    modeles = ['Ordonnance', 'Bon', 'Soin']
    
    for nom_modele in modeles:
        try:
            modele = apps.get_model('assureur', nom_modele)
            if modele:
                print(f"\n📦 Modèle: {nom_modele}")
                print("Champs disponibles:")
                for champ in modele._meta.get_fields():
                    print(f"  - {champ.name} ({champ.__class__.__name__})")
        except LookupError:
            try:
                modele = apps.get_model('soins', nom_modele)
                if modele:
                    print(f"\n📦 Modèle: {nom_modele}")
                    print("Champs disponibles:")
                    for champ in modele._meta.get_fields():
                        print(f"  - {champ.name} ({champ.__class__.__name__})")
            except LookupError:
                print(f"\n❌ Modèle {nom_modele} non trouvé")

if __name__ == "__main__":
    verifier_champs_modeles()