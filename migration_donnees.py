#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Paiement
from django.db import transaction

print("🔄 MIGRATION DES DONNÉES EXISTANTES")
print("=" * 50)

# 1. Correction 'especes' -> 'espece'
with transaction.atomic():
    updated = Paiement.objects.filter(mode_paiement='especes').update(mode_paiement='espece')
    print(f"✅ {updated} paiement(s) 'especes' -> 'espece'")

# 2. Correction 'mobile' -> 'mobile_money'
with transaction.atomic():
    updated = Paiement.objects.filter(mode_paiement='mobile').update(mode_paiement='mobile_money')
    print(f"✅ {updated} paiement(s) 'mobile' -> 'mobile_money'")

# 3. Vérification
print("\n📊 Statut après migration:")
for mode, label in Paiement._meta.get_field('mode_paiement').choices:
    count = Paiement.objects.filter(mode_paiement=mode).count()
    print(f"  - {mode}: {count} paiement(s)")