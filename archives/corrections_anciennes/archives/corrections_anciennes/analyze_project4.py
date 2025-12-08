#!/usr/bin/env python3
"""
SCRIPT D'ANALYSE DES MODÈLES ET RELATIONS
"""

import os
import sys
import django
from django.apps import apps
from django.db import models

def analyze_models_detailed():
    """Analyse détaillée des modèles et relations"""
    
    print("🔍 ANALYSE DÉTAILLÉE DES MODÈLES")
    print("=" * 50)
    
    all_models = apps.get_models()
    
    for model in all_models:
        print(f"\n📊 {model._meta.app_label}.{model.__name__}")
        print(f"   DB Table: {model._meta.db_table}")
        
        # Champs du modèle
        fields = model._meta.get_fields()
        field_count = len([f for f in fields if not f.is_relation])
        relation_count = len([f for f in fields if f.is_relation])
        
        print(f"   Champs: {field_count}, Relations: {relation_count}")
        
        # Liste des champs
        for field in model._meta.fields:
            field_type = type(field).__name__
            print(f"   - {field.name} ({field_type})")
        
        # Relations
        for field in model._meta.related_objects:
            print(f"   → Relation: {field.name} -> {field.related_model.__name__}")

def check_model_consistency():
    """Vérifie la cohérence des modèles"""
    
    print("\n🔧 VÉRIFICATION DE LA COHÉRENCE")
    print("=" * 50)
    
    issues = []
    
    for model in apps.get_models():
        # Vérifie les modèles sans verbose_name
        if not model._meta.verbose_name:
            issues.append(f"Modèle {model.__name__} sans verbose_name")
        
        # Vérifie les champs sans help_text
        for field in model._meta.fields:
            if not field.help_text and not field.primary_key:
                issues.append(f"Champ {model.__name__}.{field.name} sans help_text")
    
    if issues:
        for issue in issues:
            print(f"⚠️  {issue}")
    else:
        print("✅ Tous les modèles sont bien documentés")

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    django.setup()
    
    analyze_models_detailed()
    check_model_consistency()