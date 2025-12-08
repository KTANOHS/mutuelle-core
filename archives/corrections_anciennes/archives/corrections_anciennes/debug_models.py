#!/usr/bin/env python
import os
import sys
import django
from django.apps import apps
from django.db import models

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyze_model_fields():
    """Analyse tous les modèles et leurs champs"""
    print("=" * 80)
    print("ANALYSE COMPLÈTE DES MODÈLES DJANGO")
    print("=" * 80)
    
    all_models = apps.get_models()
    
    for model in all_models:
        print(f"\n📊 MODÈLE: {model.__name__}")
        print(f"📁 Application: {model._meta.app_label}")
        print(f"🗂️ Table: {model._meta.db_table}")
        
        # Champs locaux
        local_fields = model._meta.local_fields
        if local_fields:
            print("📋 Champs locaux:")
            for field in local_fields:
                field_type = type(field).__name__
                print(f"   - {field.name} ({field_type})")
        
        # Relations
        related_objects = model._meta.related_objects
        if related_objects:
            print("🔗 Relations:")
            for rel in related_objects:
                print(f"   - {rel.name} -> {rel.related_model.__name__}")
        
        # Champs many-to-many
        many_to_many = model._meta.many_to_many
        if many_to_many:
            print("🔗 Relations Many-to-Many:")
            for field in many_to_many:
                print(f"   - {field.name} -> {field.related_model.__name__}")

def find_field_across_models(field_name):
    """Recherche un champ spécifique dans tous les modèles"""
    print(f"\n🔍 RECHERCHE DU CHAMP: '{field_name}'")
    print("=" * 50)
    
    found = False
    all_models = apps.get_models()
    
    for model in all_models:
        # Vérifier les champs locaux
        for field in model._meta.local_fields:
            if field.name == field_name:
                print(f"✅ TROUVÉ dans {model.__name__}.{field.name}")
                found = True
        
        # Vérifier les relations
        for rel in model._meta.related_objects:
            if rel.name == field_name:
                print(f"✅ TROUVÉ (relation) dans {model.__name__}.{rel.name}")
                found = True
        
        # Vérifier les many-to-many
        for field in model._meta.many_to_many:
            if field.name == field_name:
                print(f"✅ TROUVÉ (many-to-many) dans {model.__name__}.{field.name}")
                found = True
    
    if not found:
        print(f"❌ CHAMP '{field_name}' INTROUVABLE dans tous les modèles")

def analyze_specific_models():
    """Analyse spécifique des modèles problématiques"""
    print("\n" + "=" * 80)
    print("ANALYSE DES MODÈLES PROBLÉMATIQUES")
    print("=" * 80)
    
    models_to_check = ['Ordonnance', 'Bon', 'Medecin', 'Patient']
    
    for model_name in models_to_check:
        try:
            model = apps.get_model('soins', model_name)
            if not model:
                model = apps.get_model('membres', model_name)
            
            print(f"\n🔍 {model_name}:")
            if model:
                fields = [f.name for f in model._meta.get_fields()]
                print(f"   Champs disponibles: {', '.join(fields)}")
            else:
                print(f"   ❌ Modèle {model_name} non trouvé")
        except LookupError:
            print(f"   ❌ Modèle {model_name} non trouvé dans soins ou membres")

def check_views_using_problematic_fields():
    """Vérifie les vues qui utilisent des champs problématiques"""
    print("\n" + "=" * 80)
    print("ANALYSE DES VUES PROBLÉMATIQUES")
    print("=" * 80)
    
    # Ces sont les champs qui causent des erreurs
    problematic_fields = ['medecin', 'date_emission', 'date_validation']
    
    # Analyse manuelle des vues (à adapter selon votre structure)
    views_to_check = {
        'pharmacien.views.dashboard_pharmacien': 'Utilise Ordonnance.objects.filter()',
        'pharmacien.views.liste_ordonnances_attente': 'Utilise Ordonnance.objects.filter()',
        'medecin.views.dashboard_medecin': 'Peut utiliser medecin field',
    }
    
    print("Vues à vérifier manuellement:")
    for view, description in views_to_check.items():
        print(f"   - {view}: {description}")

def generate_fix_recommendations():
    """Génère des recommandations de correction"""
    print("\n" + "=" * 80)
    print("RECOMMANDATIONS DE CORRECTION")
    print("=" * 80)
    
    recommendations = [
        "1. ✅ Le modèle Ordonnance n'a pas de champ 'medecin' direct",
        "2. ✅ Utiliser Bon.medecin au lieu de Ordonnance.medecin",
        "3. ✅ Remplacer Ordonnance.date_validation par Bon.date_soin",
        "4. ✅ Remplacer Ordonnance.objects par Bon.objects dans les vues",
        "5. ✅ Utiliser select_related() pour les relations patient/medecin",
        "6. ✅ Vérifier que tous les champs utilisés existent dans les modèles",
    ]
    
    for rec in recommendations:
        print(f"   {rec}")

def check_database_consistency():
    """Vérifie la cohérence de la base de données"""
    print("\n" + "=" * 80)
    print("VÉRIFICATION DE LA BASE DE DONNÉES")
    print("=" * 80)
    
    try:
        from django.core.management import execute_from_command_line
        print("📋 Vérification des migrations...")
        execute_from_command_line(['manage.py', 'makemigrations', '--dry-run'])
        
        print("📋 Vérification de la cohérence des modèles...")
        execute_from_command_line(['manage.py', 'check'])
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

if __name__ == "__main__":
    print("🚀 LANCEMENT DU DIAGNOSTIC DJANGO")
    print("=" * 80)
    
    # 1. Analyse complète des modèles
    analyze_model_fields()
    
    # 2. Recherche des champs problématiques
    find_field_across_models('medecin')
    find_field_across_models('date_emission')
    find_field_across_models('date_validation')
    find_field_across_models('pharmacien')
    
    # 3. Analyse spécifique
    analyze_specific_models()
    
    # 4. Vérification des vues
    check_views_using_problematic_fields()
    
    # 5. Recommandations
    generate_fix_recommendations()
    
    # 6. Vérification base de données
    check_database_consistency()
    
    print("\n" + "=" * 80)
    print("📋 DIAGNOSTIC TERMINÉ")
    print("=" * 80)