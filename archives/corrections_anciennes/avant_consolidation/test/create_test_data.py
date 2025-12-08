# Créez un fichier create_test_data.py
import os
import django
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from soins.models import Soin
from django.contrib.auth.models import User

# Créer des soins de test pour chaque membre
def create_test_soins():
    membres = Membre.objects.all()[:5]  # Les 5 premiers membres
    
    for membre in membres:
        # Créer plusieurs soins par membre
        soin1 = Soin.objects.create(
            patient=membre,
            type_soin='Consultation générale',
            date_soin='2023-12-01',
            cout_reel=5000.00,
            statut='valide',
            created_by=User.objects.first()
        )
        print(f"✅ Soin créé: {soin1.id} - {soin1.type_soin} pour {membre.prenom} {membre.nom}")
        
        soin2 = Soin.objects.create(
            patient=membre,
            type_soin='Analyse sanguine',
            date_soin='2023-12-10',
            cout_reel=15000.00,
            statut='valide',
            created_by=User.objects.first()
        )
        print(f"✅ Soin créé: {soin2.id} - {soin2.type_soin} pour {membre.prenom} {membre.nom}")

if __name__ == "__main__":
    create_test_soins()