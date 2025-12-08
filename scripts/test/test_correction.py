#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Paiement, Membre
from assureur.forms import PaiementForm
from django.utils import timezone

print("🧪 TEST APRÈS CORRECTION")
print("=" * 50)

# Vérifier les choix du modèle
print("\n📦 Choix du modèle Paiement:")
mode_field = Paiement._meta.get_field('mode_paiement')
statut_field = Paiement._meta.get_field('statut')

print(f"Mode paiement: {dict(mode_field.choices)}")
print(f"Statut: {dict(statut_field.choices)}")

# Tester avec un membre existant
membre = Membre.objects.first()
if not membre:
    print("❌ Aucun membre trouvé!")
    exit()

# Données de test VALIDES
form_data = {
    'membre': membre.id,
    'date_paiement': timezone.now().date(),
    'montant': 150.00,
    'mode_paiement': 'espece',  # Maintenant sans 's'
    'statut': 'valide',  # Doit être dans les choix du modèle
    'reference': 'TEST-001',
}

form = PaiementForm(data=form_data)

print(f"\n📝 Test du formulaire avec 'espece':")
print(f"  Formulaire valide: {form.is_valid()}")
if not form.is_valid():
    print(f"  Erreurs: {form.errors}")

# Tester toutes les valeurs de mode_paiement
print("\n🔍 Test de tous les modes de paiement:")
modes = ['espece', 'cheque', 'virement', 'carte', 'mobile_money', 'autre']

for mode in modes:
    form_data['mode_paiement'] = mode
    form = PaiementForm(data=form_data)
    if form.is_valid():
        print(f"  ✅ '{mode}': VALIDE")
    else:
        error = form.errors.get('mode_paiement', '')
        print(f"  ❌ '{mode}': {error}")