#!/usr/bin/env python3
import os
import sys
import django

sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    # Vérifier la structure des modèles
    from pharmacien.models import OrdonnancePharmacien, Pharmacien
    
    print("=== STRUCTURE DU MODÈLE OrdonnancePharmacien ===")
    print("Champs disponibles:")
    for field in OrdonnancePharmacien._meta.fields:
        print(f"  - {field.name:25} ({field.get_internal_type()})")
    
    print("\n=== STRUCTURE DU MODÈLE Pharmacien ===")
    print("Champs disponibles:")
    for field in Pharmacien._meta.fields:
        print(f"  - {field.name:25} ({field.get_internal_type()})")
    
    print("\n=== RELATIONS ===")
    print("1. OrdonnancePharmacien.pharmacien_validateur ->", 
          OrdonnancePharmacien._meta.get_field('pharmacien_validateur').related_model.__name__)
    
    print("2. Pharmacien.user ->", 
          Pharmacien._meta.get_field('user').related_model.__name__)
    
    print("\n=== CONSEIL POUR LE FILTRE ===")
    print("Pour filtrer les OrdonnancePharmacien d'un utilisateur:")
    print("1. D'abord obtenir son profil Pharmacien:")
    print("   pharmacien = Pharmacien.objects.get(user=request.user)")
    print("2. Puis filtrer:")
    print("   OrdonnancePharmacien.objects.filter(pharmacien_validateur=pharmacien)")
    
except Exception as e:
    print(f"Erreur: {e}")
    import traceback
    traceback.print_exc()
