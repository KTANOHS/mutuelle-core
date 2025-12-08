#!/usr/bin/env python
"""
ANALYSE DÉTAILLÉE DES MODÈLES AGENTS
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

from django.apps import apps
from django.db import models

def analyze_models():
    print("🗃️ ANALYSE DÉTAILLÉE DES MODÈLES AGENTS")
    print("=" * 50)
    
    try:
        # Obtenir tous les modèles de l'app agents
        app_models = apps.get_app_config('agents').get_models()
        
        print(f"📊 Modèles trouvés: {len(app_models)}")
        print("-" * 30)
        
        for model in app_models:
            print(f"\n🔹 {model.__name__}:")
            print(f"   📋 Table: {model._meta.db_table}")
            print(f"   📝 Champs: {len(model._meta.fields)}")
            
            # Lister les champs
            for field in model._meta.fields:
                field_type = type(field).__name__
                print(f"      • {field.name:20} ({field_type})")
                
            # Vérifier les relations
            related_objects = [
                f for f in model._meta.get_fields() 
                if f.auto_created and not f.concrete
            ]
            if related_objects:
                print(f"   🔗 Relations:")
                for rel in related_objects:
                    print(f"      • {rel.name} -> {rel.related_model.__name__}")
                    
    except LookupError:
        print("❌ Application 'agents' non trouvée")

def check_model_consistency():
    """Vérifie la cohérence des modèles avec les autres composants"""
    print("\n🔍 VÉRIFICATION DE COHÉRENCE")
    print("=" * 30)
    
    # Vérifier si les modèles sont utilisés dans les vues
    views_file = BASE_DIR / 'agents' / 'views.py'
    if views_file.exists():
        with open(views_file, 'r') as f:
            content = f.read()
            
        models_used = []
        for model in ['Agent', 'VerificationCotisation', 'ActiviteAgent', 'BonSoin']:
            if model in content:
                models_used.append(model)
                print(f"✅ Modèle {model} utilisé dans les vues")
            else:
                print(f"⚠️  Modèle {model} non référencé dans les vues")

if __name__ == '__main__':
    analyze_models()
    check_model_consistency()