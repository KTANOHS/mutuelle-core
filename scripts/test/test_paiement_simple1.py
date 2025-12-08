#!/usr/bin/env python
"""
Test simple du système de paiement
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.utils import timezone
from django.contrib.auth.models import User
from assureur.models import Paiement, Membre
from assureur.forms import PaiementForm

print("🧪 TEST SIMPLE PAIEMENT")
print("=" * 50)

# Récupérer un membre et un utilisateur
membre = Membre.objects.first()
user = User.objects.first()

if not membre or not user:
    print("❌ Données insuffisantes pour le test")
    exit()

print(f"Utilisateur: {user.username}")
print(f"Membre: {membre.nom} {membre.prenom}")

# Test avec 'espece' (le problème original)
print("\n🎯 TEST AVEC 'ESPECE' (problème original):")
form_data = {
    'membre': membre.id,
    'montant': 10000.00,
    'date_paiement': timezone.now().date(),
    'mode_paiement': 'espece',
    'statut': 'initie',
}

form = PaiementForm(data=form_data)

if form.is_valid():
    print("✅ FORMULAIRE VALIDE !")
    print("   'espece' est maintenant accepté !")
    
    # Créer le paiement
    paiement = form.save(commit=False)
    paiement.created_by = user
    paiement.save()
    
    print(f"\n📄 Paiement créé:")
    print(f"   Référence: {paiement.reference}")
    print(f"   Montant: {paiement.montant} FCFA")
    print(f"   Mode: {paiement.get_mode_paiement_display()}")
    print(f"   Statut: {paiement.get_statut_display()}")
else:
    print("❌ FORMULAIRE INVALIDE")
    print(f"   Erreurs: {form.errors}")

print("\n" + "=" * 50)
print("✅ Test terminé")