#!/usr/bin/env python
"""
SCRIPT DE DÉBUGUAGE - Analyse complète des modèles
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def debug_models():
    """Analyse détaillée de tous les modèles"""
    print("🔍 DÉBUGUAGE COMPLET DES MODÈLES")
    print("=" * 50)
    
    # Analyse Membre
    try:
        from membres.models import Membre
        print("\n📋 MODÈLE MEMBRE:")
        for field in Membre._meta.fields:
            print(f"   {field.name}: {field.get_internal_type()} {'(NULL)' if field.null else '(NOT NULL)'}")
    except Exception as e:
        print(f"❌ Membre: {e}")
    
    # Analyse Assureur
    try:
        from assureur.models import Assureur
        print("\n📋 MODÈLE ASSUREUR:")
        for field in Assureur._meta.fields:
            print(f"   {field.name}: {field.get_internal_type()} {'(NULL)' if field.null else '(NOT NULL)'}")
    except Exception as e:
        print(f"❌ Assureur: {e}")
    
    # Analyse Medecin
    try:
        from medecin.models import Medecin
        print("\n📋 MODÈLE MEDECIN:")
        for field in Medecin._meta.fields:
            null_info = '(NULL)' if field.null else '(NOT NULL)'
            default_info = f" default={field.default}" if field.default != django.db.models.NOT_PROVIDED else ""
            print(f"   {field.name}: {field.get_internal_type()} {null_info}{default_info}")
            
            # Info spéciale pour les ForeignKey
            if field.get_internal_type() == 'ForeignKey':
                print(f"      → Relation vers: {field.related_model.__name__ if field.related_model else '???'}")
    except Exception as e:
        print(f"❌ Medecin: {e}")
    
    # Analyse Pharmacien
    try:
        from pharmacien.models import Pharmacien
        print("\n📋 MODÈLE PHARMACIEN:")
        for field in Pharmacien._meta.fields:
            print(f"   {field.name}: {field.get_internal_type()} {'(NULL)' if field.null else '(NOT NULL)'}")
    except Exception as e:
        print(f"❌ Pharmacien: {e}")
    
    # Analyse Agent
    try:
        from agents.models import Agent
        print("\n📋 MODÈLE AGENT:")
        for field in Agent._meta.fields:
            print(f"   {field.name}: {field.get_internal_type()} {'(NULL)' if field.null else '(NOT NULL)'}")
    except Exception as e:
        print(f"❌ Agent: {e}")
    
    print("\n🎯 CONSEILS:")
    print("• Les champs 'NOT NULL' doivent avoir une valeur par défaut")
    print("• Les ForeignKey doivent pointer vers des modèles existants")
    print("• Utilisez l'admin Django pour créer les données de test")

if __name__ == "__main__":
    debug_models()