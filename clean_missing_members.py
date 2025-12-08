# clean_missing_members.py
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

django.setup()

print("🧹 NETTOYAGE DES RELATIONS MEMBRE CASSÉES")
print("="*50)

from assureur.models import Membre, Bon, Soin, Paiement, Cotisation

def check_and_fix_missing_members():
    print("1. Vérification des Bons avec membres manquants...")
    bons_problemes = []
    for bon in Bon.objects.all():
        try:
            # Essayer d'accéder au membre
            _ = bon.membre
        except Membre.DoesNotExist:
            bons_problemes.append(bon)
            print(f"   ❌ Bon {bon.id} ({bon.numero_bon}) a un membre manquant")
    
    if bons_problemes:
        print(f"\n   {len(bons_problemes)} bons avec problèmes")
        reponse = input("   Supprimer ces bons ? (o/n): ")
        if reponse.lower() == 'o':
            for bon in bons_problemes:
                bon.delete()
            print("   ✅ Bons supprimés")
    else:
        print("   ✅ Aucun problème trouvé")
    
    print("\n2. Vérification des Soins avec membres manquants...")
    soins_problemes = []
    for soin in Soin.objects.all():
        try:
            _ = soin.membre
        except Membre.DoesNotExist:
            soins_problemes.append(soin)
            print(f"   ❌ Soin {soin.id} a un membre manquant")
    
    if soins_problemes:
        print(f"\n   {len(soins_problemes)} soins avec problèmes")
        reponse = input("   Supprimer ces soins ? (o/n): ")
        if reponse.lower() == 'o':
            for soin in soins_problemes:
                soin.delete()
            print("   ✅ Soins supprimés")
    else:
        print("   ✅ Aucun problème trouvé")
    
    print("\n3. Vérification des Paiements avec membres manquants...")
    paiements_problemes = []
    for paiement in Paiement.objects.all():
        try:
            _ = paiement.membre
        except Membre.DoesNotExist:
            paiements_problemes.append(paiement)
            print(f"   ❌ Paiement {paiement.id} ({paiement.reference}) a un membre manquant")
    
    if paiements_problemes:
        print(f"\n   {len(paiements_problemes)} paiements avec problèmes")
        reponse = input("   Supprimer ces paiements ? (o/n): ")
        if reponse.lower() == 'o':
            for paiement in paiements_problemes:
                paiement.delete()
            print("   ✅ Paiements supprimés")
    else:
        print("   ✅ Aucun problème trouvé")
    
    print("\n4. Vérification des Cotisations avec membres manquants...")
    cotisations_problemes = []
    for cotisation in Cotisation.objects.all():
        try:
            _ = cotisation.membre
        except Membre.DoesNotExist:
            cotisations_problemes.append(cotisation)
            print(f"   ❌ Cotisation {cotisation.id} ({cotisation.reference}) a un membre manquant")
    
    if cotisations_problemes:
        print(f"\n   {len(cotisations_problemes)} cotisations avec problèmes")
        reponse = input("   Supprimer ces cotisations ? (o/n): ")
        if reponse.lower() == 'o':
            for cotisation in cotisations_problemes:
                cotisation.delete()
            print("   ✅ Cotisations supprimées")
    else:
        print("   ✅ Aucun problème trouvé")
    
    print("\n" + "="*50)
    print("🎯 NETTOYAGE TERMINÉ !")
    print(f"Résumé des problèmes trouvés :")
    print(f"  - Bons: {len(bons_problemes)}")
    print(f"  - Soins: {len(soins_problemes)}")
    print(f"  - Paiements: {len(paiements_problemes)}")
    print(f"  - Cotisations: {len(cotisations_problemes)}")

if __name__ == "__main__":
    check_and_fix_missing_members()