#!/usr/bin/env python3
"""
SCRIPT D'ANALYSE DES MODÈLES DE DONNÉES
Analyse la cohérence et les relations entre les modèles
"""

import os
import sys
import django
from django.apps import apps
from django.db import models
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

class ModelAnalyzer:
    def __init__(self):
        self.models = apps.get_models()
    
    def analyze_all_models(self):
        """Analyse tous les modèles du projet"""
        print("=" * 60)
        print("📊 ANALYSE DES MODÈLES DE DONNÉES")
        print("=" * 60)
        
        for model in self.models:
            self.analyze_single_model(model)
    
    def analyze_single_model(self, model):
        """Analyse un modèle spécifique"""
        print(f"\n🔍 Modèle: {model._meta.label}")
        print(f"   Table: {model._meta.db_table}")
        print(f"   Champs: {len(model._meta.fields)}")
        
        # Analyse des champs
        for field in model._meta.fields:
            field_type = type(field).__name__
            field_name = field.name
            nullable = field.null
            unique = field.unique
            
            field_info = f"   📍 {field_name} ({field_type})"
            if nullable:
                field_info += " [NULLABLE]"
            if unique:
                field_info += " [UNIQUE]"
            if field.primary_key:
                field_info += " [PRIMARY KEY]"
                
            print(field_info)
        
        # Relations
        relations = model._meta.related_objects
        if relations:
            print("   🔗 Relations:")
            for rel in relations:
                print(f"      • {rel.name} -> {rel.related_model._meta.label}")
    
    def check_model_consistency(self):
        """Vérifie la cohérence des modèles"""
        print("\n" + "=" * 60)
        print("🔎 VÉRIFICATION DE COHÉRENCE")
        print("=" * 60)
        
        issues = []
        
        for model in self.models:
            # Vérifier si le modèle a un manager
            if not hasattr(model, 'objects'):
                issues.append(f"Modèle {model._meta.label} n'a pas de manager 'objects'")
            
            # Vérifier les clés étrangères
            for field in model._meta.fields:
                if isinstance(field, models.ForeignKey):
                    related_model = field.related_model
                    if not related_model:
                        issues.append(f"Clé étrangère {field.name} dans {model._meta.label} pointe vers un modèle inexistant")
        
        for issue in issues:
            print(f"❌ {issue}")
        
        if not issues:
            print("✅ Aucun problème de cohérence détecté")

def analyze_data_models():
    """Analyse les modèles de données"""
    analyzer = ModelAnalyzer()
    analyzer.analyze_all_models()
    analyzer.check_model_consistency()

if __name__ == "__main__":
    analyze_data_models()