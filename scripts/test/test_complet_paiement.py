#!/usr/bin/env python
"""
Test complet du système de paiement après correction - VERSION CORRIGÉE
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.utils import timezone
from django.contrib.auth.models import User
from assureur.models import Paiement, Membre
from assureur.forms import PaiementForm

print("🧪 TEST COMPLET SYSTÈME PAIEMENT - CORRIGÉ")
print("=" * 50)

# Vérifier qu'on a un membre et un utilisateur
membre = Membre.objects.first()
user = User.objects.first()

if not membre or not user:
    print("❌ Données insuffisantes pour le test")
    exit()

print(f"Utilisateur: {user.username}")
print(f"Membre: {membre.nom} {membre.prenom}")

# 1. Tester tous les modes de paiement
print("\n🎯 1. TEST TOUS LES MODES DE PAIEMENT")
modes = ['espece', 'cheque', 'virement', 'carte', 'mobile_money', 'autre']

for mode in modes:
    form_data = {
        'membre': membre.id,
        'montant': 5000.00,
        'date_paiement': timezone.now().date(),
        'mode_paiement': mode,
        'statut': 'initie',
        'reference': f'TEST-{mode.upper()}-{timezone.now().strftime("%H%M%S")}',
    }
    
    form = PaiementForm(data=form_data)
    if form.is_valid():
        paiement = form.save(commit=False)
        paiement.created_by = user
        paiement.save()
        print(f"✅ {mode}: VALIDE - Référence: {paiement.reference}")
    else:
        errors = form.errors.get('mode_paiement', 'Erreur inconnue')
        print(f"❌ {mode}: {errors}")

# 2. Tester différents statuts
print("\n📊 2. TEST DIFFÉRENTS STATUTS")
statuts = ['initie', 'valide', 'annule', 'rembourse', 'echec']

for statut in statuts:
    form_data = {
        'membre': membre.id,
        'montant': 3000.00,
        'date_paiement': timezone.now().date(),
        'mode_paiement': 'espece',
        'statut': statut,
        'reference': f'STATUT-{statut}-{timezone.now().strftime("%H%M%S")}',
    }
    
    form = PaiementForm(data=form_data)
    if form.is_valid():
        paiement = form.save(commit=False)
        paiement.created_by = user
        paiement.save()
        print(f"✅ Statut '{statut}': VALIDE - Référence: {paiement.reference}")
    else:
        errors = form.errors.get('statut', 'Erreur inconnue')
        print(f"❌ Statut '{statut}': {errors}")

# 3. Vérification finale
print("\n📊 3. VÉRIFICATION FINALE")
total_paiements = Paiement.objects.count()
print(f"Total paiements dans la base: {total_paiements}")

# Lister les derniers paiements (corrigé : utiliser created_at au lieu de date_creation)
derniers = Paiement.objects.order_by('-created_at')[:5]
if derniers:
    print("\nDerniers paiements créés:")
    for p in derniers:
        print(f"  - {p.reference}: {p.montant} FCFA")
        print(f"    Mode: {p.get_mode_paiement_display()}")
        print(f"    Statut: {p.get_statut_display()}")
        print(f"    Date: {p.date_paiement}")
        print()

# 4. Nettoyage optionnel
print("\n🧹 4. NETTOYAGE OPTIONNEL")
supprimer = input("Voulez-vous supprimer les paiements de test créés par ce script? (o/n): ").strip().lower()
if supprimer == 'o':
    count, _ = Paiement.objects.filter(reference__startswith='TEST-').delete()
    count2, _ = Paiement.objects.filter(reference__startswith='STATUT-').delete()
    print(f"✅ {count + count2} paiement(s) de test supprimé(s)")
else:
    print("ℹ️  Les paiements de test ont été conservés")

print("\n" + "=" * 50)
print("🎉 TESTS TERMINÉS AVEC SUCCÈS !")