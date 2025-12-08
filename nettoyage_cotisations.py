# nettoyage_cotisations.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Cotisation
from django.utils import timezone
from datetime import datetime, timedelta

print("="*70)
print("🔧 NETTOYAGE ET CORRECTION DES COTISATIONS")
print("="*70)

# 1. Analyser l'état actuel
cotisations = Cotisation.objects.all()
print(f"📊 ÉTAT ACTUEL:")
print(f"   Total cotisations: {cotisations.count()}")
print(f"   En retard: {cotisations.filter(statut='retard').count()}")
print(f"   Payées: {cotisations.filter(statut='payee').count()}")
print(f"   Annulées: {cotisations.filter(statut='annulee').count()}")

# 2. Vérifier les dates
print(f"\n📅 VÉRIFICATION DES DATES:")
aujourdhui = timezone.now().date()
for cotisation in cotisations.filter(statut='retard')[:5]:  # Limiter à 5 pour l'affichage
    date_creation = cotisation.date_creation.date() if cotisation.date_creation else "N/A"
    print(f"   {cotisation.reference}: créée le {date_creation}, période {cotisation.periode}")

# 3. Proposition de correction
print(f"\n🔄 OPTIONS DE CORRECTION:")
print("   1. Marquer toutes les cotisations anciennes comme 'payées'")
print("   2. Mettre à jour uniquement celles de plus de 30 jours")
print("   3. Ne rien changer (statut actuel)")
print("   4. Réinitialiser les statuts")

choix = input("\n👉 Votre choix (1-4): ")

if choix == "1":
    # Option 1: Marquer tout comme payé
    cotisations.filter(statut='retard').update(statut='payee')
    print("✅ Toutes les cotisations marquées comme payées")
    
elif choix == "2":
    # Option 2: Marquer comme payées celles de plus de 30 jours
    date_limite = aujourdhui - timedelta(days=30)
    anciennes = cotisations.filter(statut='retard', date_creation__lt=date_limite)
    anciennes.update(statut='payee')
    print(f"✅ {anciennes.count()} cotisations anciennes marquées comme payées")
    
elif choix == "3":
    print("ℹ️ Aucun changement effectué")
    
elif choix == "4":
    # Option 4: Réinitialiser les statuts
    print(f"\n🔄 Réinitialisation des statuts:")
    for cotisation in cotisations:
        # Logique: si la période est ancienne, marquer comme payée
        periode_date = datetime.strptime(cotisation.periode + "-01", "%Y-%m-%d").date()
        if periode_date < (aujourdhui - timedelta(days=60)):
            cotisation.statut = 'payee'
        elif periode_date < aujourdhui:
            cotisation.statut = 'retard'
        else:
            cotisation.statut = 'due'
        cotisation.save()
    print("✅ Statuts réinitialisés selon la logique métier")

# 4. Afficher le nouvel état
print(f"\n📊 NOUVEL ÉTAT:")
cotisations = Cotisation.objects.all()  # Recharger
for statut_code, statut_label in Cotisation.STATUT_CHOICES:
    nb = cotisations.filter(statut=statut_code).count()
    print(f"   {statut_label}: {nb}")

print("\n" + "="*70)
print("NETTOYAGE TERMINÉ ✅")
print("="*70)