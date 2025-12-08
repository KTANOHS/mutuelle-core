#!/usr/bin/env python
"""
Script principal pour générer des cotisations de test
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from datetime import datetime, timedelta
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import transaction
from assureur.models import Cotisation, Membre
from django.db.models import Sum

print("🚀 GÉNÉRATION DE COTISATIONS DE TEST")
print("=" * 50)

# Vérifier l'utilisateur
user = User.objects.filter(username='matrix').first()
if not user:
    user = User.objects.first()
print(f"Utilisateur: {user.username}")

# Membres actifs
membres = Membre.objects.filter(statut='actif')
print(f"Membres actifs: {membres.count()}")

if membres.count() == 0:
    print("❌ Aucun membre actif")
    exit()

# Nettoyer les cotisations existantes (optionnel)
print("\n🧹 Nettoyage des cotisations existantes...")
cotisations_existantes = Cotisation.objects.count()
if cotisations_existantes > 0:
    reponse = input(f"Supprimer les {cotisations_existantes} cotisations existantes ? (o/n): ").strip().lower()
    if reponse == 'o':
        Cotisation.objects.all().delete()
        print("✅ Cotisations supprimées")

# Périodes à générer (6 derniers mois)
today = datetime.now().date()
periodes = []
for i in range(6):
    mois = today - timedelta(days=30*i)
    periode = mois.strftime('%Y-%m')
    periodes.append(periode)

print(f"\n📅 Périodes à générer: {periodes}")

with transaction.atomic():
    total_creees = 0
    
    for periode in periodes:
        print(f"\n🔄 Génération pour {periode}...")
        
        for membre in membres:
            # Vérifier si la cotisation existe déjà pour cette période
            if Cotisation.objects.filter(membre=membre, periode=periode).exists():
                print(f"  ⏭️  Existe déjà pour {membre.nom}")
                continue
            
            try:
                # Calculer les dates
                year, month = map(int, periode.split('-'))
                
                # Date d'émission (1er du mois)
                date_emission = datetime(year, month, 1).date()
                
                # Date d'échéance (fin du mois)
                if month == 12:
                    next_month = datetime(year+1, 1, 1).date()
                else:
                    next_month = datetime(year, month+1, 1).date()
                date_echeance = next_month - timedelta(days=1)
                
                # Déterminer le type et montant
                if membre.cmu_option:  # Vérifier cmu_option (True/False)
                    type_cotisation = 'femme_enceinte'
                    montant = Decimal('7500.00')
                else:
                    type_cotisation = 'normale'
                    montant = Decimal('5000.00')
                
                # Déterminer le statut
                if periode == periodes[0]:  # Période actuelle
                    statut = 'due'
                    date_paiement = None
                elif periode == periodes[1] or periode == periodes[2]:  # 1-2 mois avant
                    statut = 'en_retard'
                    date_paiement = None
                else:  # Plus ancien = payé
                    statut = 'payee'
                    date_paiement = date_echeance - timedelta(days=5)
                
                # Créer la référence
                ref_mois = periode.replace('-', '')
                reference = f"COT-{membre.numero_unique}-{ref_mois}"
                
                # Créer la cotisation
                cotisation = Cotisation.objects.create(
                    membre=membre,
                    periode=periode,
                    type_cotisation=type_cotisation,
                    montant=montant,
                    date_emission=date_emission,
                    date_echeance=date_echeance,
                    date_paiement=date_paiement,
                    statut=statut,
                    reference=reference,
                    notes=f"Générée automatiquement - {type_cotisation}",
                    enregistre_par=user,
                    montant_clinique=Decimal('0.00'),
                    montant_pharmacie=Decimal('0.00'),
                    montant_charges_mutuelle=Decimal('0.00'),
                )
                
                print(f"  ✅ {reference}: {montant} FCFA ({statut})")
                total_creees += 1
                
            except Exception as e:
                print(f"  ❌ Erreur pour {membre.nom}: {e}")
                import traceback
                traceback.print_exc()

print(f"\n📊 RÉSULTAT FINAL:")
print(f"✅ Total cotisations créées: {total_creees}")
print(f"📈 Total en base: {Cotisation.objects.count()}")

# Vérification
print("\n🔍 VÉRIFICATION:")
total_par_statut = {}
for statut in ['due', 'payee', 'en_retard']:
    count = Cotisation.objects.filter(statut=statut).count()
    if count > 0:
        total = Cotisation.objects.filter(statut=statut).aggregate(total=Sum('montant'))['total'] or 0
        total_par_statut[statut] = total
        print(f"  {statut}: {count} = {total} FCFA")

# Total général
total_general = sum(total_par_statut.values())
print(f"\n💰 TOTAL GÉNÉRAL: {total_general} FCFA")
print(f"👥 Par membre: {total_general / membres.count() if membres.count() > 0 else 0:.0f} FCFA")

print("\n🎉 Génération terminée !")
print("➡️  Vous pouvez maintenant vérifier les statistiques.")