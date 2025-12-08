#!/usr/bin/env python
"""
EXPLORATION SPÉCIFIQUE DE L'APPLICATION CORE
"""

import os
import sys
import django

# Configuration de base
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Essayer différents settings
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
    SETTINGS_MODULE = 'core.settings'
except:
    try:
        project_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
        django.setup()
        SETTINGS_MODULE = f'{project_name}.settings'
    except Exception as e:
        print(f"❌ Impossible de configurer Django: {e}")
        sys.exit(1)

print(f"✅ Settings module: {SETTINGS_MODULE}")

from django.apps import apps

def explorer_core():
    print("\n🔍 EXPLORATION DE L'APPLICATION CORE")
    print("=" * 50)
    
    # Vérifier si core existe
    try:
        core_config = apps.get_app_config('core')
        print("✅ Application 'core' trouvée")
        
        # Lister tous les modèles de core
        print("\n🏗️  MODÈLES DANS CORE:")
        core_models = core_config.get_models()
        
        if not core_models:
            print("   ❌ Aucun modèle dans core")
            return
            
        for model in core_models:
            print(f"\n   📋 {model.__name__}:")
            print(f"      Table: {model._meta.db_table}")
            
            # Afficher les champs
            for field in model._meta.fields:
                required = " (required)" if not field.null and not field.blank else ""
                print(f"      └ {field.name}: {field.get_internal_type()}{required}")
                
    except LookupError:
        print("❌ Application 'core' non trouvée")
        
        # Lister toutes les applications
        print("\n📦 Applications disponibles:")
        for app_config in apps.get_app_configs():
            models_count = len(app_config.get_models())
            print(f"   - {app_config.name}: {models_count} modèles")

def trouver_model_equivalent():
    """Trouve les modèles équivalents à Membre, Cotisation, Bon"""
    print("\n🎯 RECHERCHE DE MODÈLES ÉQUIVALENTS:")
    
    equivalences = {
        'Membre': ['Membre', 'Member', 'User', 'Client', 'Patient', 'Assure', 'Beneficiaire'],
        'Cotisation': ['Cotisation', 'Payment', 'Paiement', 'Subscription', 'Abonnement', 'Contribution'],
        'Bon': ['Bon', 'Voucher', 'Ticket', 'Coupon', 'Note', 'Document', 'Facture']
    }
    
    for nom_recherche, noms_possibles in equivalences.items():
        print(f"\n   🔍 Recherche: {nom_recherche}")
        trouve = False
        
        for model in apps.get_models():
            for nom_possible in noms_possibles:
                if nom_possible.lower() in model.__name__.lower():
                    print(f"      ✅ TROUVÉ: {model._meta.app_label}.{model.__name__}")
                    
                    # Afficher la structure
                    print(f"        📋 Champs: {[f.name for f in model._meta.fields]}")
                    trouve = True
                    break
            if trouve:
                break
        
        if not trouve:
            print(f"      ❌ Non trouvé")

if __name__ == "__main__":
    explorer_core()
    trouver_model_equivalent()