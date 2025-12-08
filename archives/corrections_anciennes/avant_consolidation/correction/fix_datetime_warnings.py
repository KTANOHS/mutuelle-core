# fix_datetime_warnings.py
import os
import sys
import django
from pathlib import Path
from datetime import datetime
from django.utils import timezone

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

django.setup()

print("🔧 CORRECTION DES WARNINGS DATETIME")
print("="*50)

from assureur.models import Membre, Bon, Paiement, Soin

def fix_naive_datetimes():
    print("1. Correction des dates naïves dans les modèles...")
    
    # Membre
    membres = Membre.objects.filter(created_at__isnull=False)
    for membre in membres:
        if membre.created_at and membre.created_at.tzinfo is None:
            membre.created_at = timezone.make_aware(membre.created_at)
            membre.save()
    print(f"   ✅ Membres: {membres.count()} vérifiés")
    
    # Bon
    bons = Bon.objects.filter(date_creation__isnull=False)
    for bon in bons:
        if bon.date_creation and bon.date_creation.tzinfo is None:
            bon.date_creation = timezone.make_aware(bon.date_creation)
            bon.save()
    print(f"   ✅ Bons: {bons.count()} vérifiés")
    
    # Paiement
    paiements = Paiement.objects.filter(date_paiement__isnull=False)
    for paiement in paiements:
        if paiement.date_paiement and paiement.date_paiement.tzinfo is None:
            paiement.date_paiement = timezone.make_aware(paiement.date_paiement)
            paiement.save()
    print(f"   ✅ Paiements: {paiements.count()} vérifiés")
    
    # Soin
    soins = Soin.objects.filter(date_soumission__isnull=False)
    for soin in soins:
        if soin.date_soumission and soin.date_soumission.tzinfo is None:
            soin.date_soumission = timezone.make_aware(soin.date_soumission)
            soin.save()
    print(f"   ✅ Soins: {soins.count()} vérifiés")
    
    print("\n✅ Toutes les dates ont été corrigées !")

if __name__ == "__main__":
    fix_naive_datetimes()