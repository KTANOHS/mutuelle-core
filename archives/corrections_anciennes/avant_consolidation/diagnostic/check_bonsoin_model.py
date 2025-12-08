# check_bonsoin_model.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("="*70)
print("🔍 VÉRIFICATION DÉTAILLÉE DU MODÈLE BONSOIN")
print("="*70)

from agents.models import BonSoin

print("✅ Modèle BonSoin importé avec succès")

# Afficher tous les champs
print("\n📋 TOUS LES CHAMPS DU MODÈLE BONSOIN:")
for field in BonSoin._meta.fields:
    field_type = field.get_internal_type()
    is_required = "REQUIS" if not field.null and not field.blank else "OPTIONNEL"
    print(f"  • {field.name}: {field_type} ({is_required})")

# Vérifier spécifiquement les champs de date
print("\n🔍 CHAMPS DE DATE SPÉCIFIQUEMENT:")
date_fields = [f for f in BonSoin._meta.fields if f.get_internal_type() in ['DateTimeField', 'DateField']]
for field in date_fields:
    print(f"  • {field.name}: {field.get_internal_type()}")

# Vérifier les champs créés/modifiés
print("\n🎯 VÉRIFICATION DES CHAMPS STANDARD:")
date_creation_exists = hasattr(BonSoin, 'date_creation')
created_at_exists = hasattr(BonSoin, 'created_at')
updated_at_exists = hasattr(BonSoin, 'updated_at')

print(f"  date_creation: {'✅ EXISTE' if date_creation_exists else '❌ ABSENT'}")
print(f"  created_at: {'✅ EXISTE' if created_at_exists else '❌ ABSENT'}")
print(f"  updated_at: {'✅ EXISTE' if updated_at_exists else '❌ ABSENT'}")

# Vérifier un exemple de données
print("\n📊 EXEMPLE DE DONNÉES BONSOIN:")
if BonSoin.objects.exists():
    bon = BonSoin.objects.first()
    print(f"  ID: {bon.id}")
    print(f"  Référence: {bon.reference}")
    print(f"  Statut: {bon.statut}")
    
    if date_creation_exists and bon.date_creation:
        print(f"  date_creation: {bon.date_creation}")
    elif created_at_exists and bon.created_at:
        print(f"  created_at: {bon.created_at}")
    
    # Afficher quelques autres champs importants
    if hasattr(bon, 'date_emission'):
        print(f"  date_emission: {bon.date_emission}")
    if hasattr(bon, 'date_paiement'):
        print(f"  date_paiement: {bon.date_paiement}")
else:
    print("  Aucun BonSoin dans la base de données")

# Vérifier aussi le modèle Cotisation pour comparaison
print("\n🔍 COMPARAISON AVEC MODÈLE COTISATION:")
from assureur.models import Cotisation

print("  Champs de date pour Cotisation:")
for field in Cotisation._meta.fields:
    if field.get_internal_type() in ['DateTimeField', 'DateField']:
        print(f"    • {field.name}: {field.get_internal_type()}")

print("\n" + "="*70)
print("🎯 CONCLUSION POUR LES CORRECTIONS")
print("="*70)

# Déterminer quelle correction appliquer
if date_creation_exists:
    print("""
    Le modèle BonSoin utilise 'date_creation'.
    
    ✅ CONSERVER 'date_creation' pour BonSoin:
       - BonSoin.objects.order_by('-date_creation') → CORRECT
       - BonSoin.objects.filter(date_creation__gte=...) → CORRECT
    """)
elif created_at_exists:
    print("""
    Le modèle BonSoin utilise 'created_at'.
    
    ✅ CHANGER 'date_creation' en 'created_at' pour BonSoin:
       - BonSoin.objects.order_by('-date_creation') → order_by('-created_at')
       - BonSoin.objects.filter(date_creation__gte=...) → filter(created_at__gte=...)
    """)

print("\n" + "="*70)