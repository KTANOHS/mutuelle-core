#!/usr/bin/env python
"""
SCRIPT POUR DÉCOUVRIR LA STRUCTURE DE VOTRE PROJET
"""

import os
import sys
import django
import inspect

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Essayer de trouver le settings module
settings_modules = [
    'votre_projet.settings', 
    'projet.settings',
    'core.settings', 
    'assurance.settings',
    'config.settings',
    'settings'
]

for settings_module in settings_modules:
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
        django.setup()
        print(f"✅ Settings module trouvé: {settings_module}")
        break
    except Exception as e:
        continue
else:
    # Dernier essai avec le répertoire courant
    try:
        project_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
        django.setup()
        print(f"✅ Settings module: {project_name}.settings")
    except Exception as e:
        print("❌ Impossible de trouver le settings module")
        print("📋 Modules essayés:", settings_modules)
        sys.exit(1)

from django.apps import apps

def decouvrir_structure():
    print("\n🔍 DÉCOUVERTE DE LA STRUCTURE DU PROJET")
    print("=" * 50)
    
    # Lister toutes les applications installées
    print("\n📦 APPLICATIONS INSTALLÉES:")
    for app_config in apps.get_app_configs():
        print(f"   - {app_config.name} (verbose: {app_config.verbose_name})")
    
    # Lister tous les modèles
    print("\n🏗️  MODÈLES DISPONIBLES:")
    for model in apps.get_models():
        app_label = model._meta.app_label
        print(f"\n   📋 {app_label}.{model.__name__}:")
        
        # Lister les champs du modèle
        fields = model._meta.fields
        for field in fields:
            print(f"      └ {field.name} ({field.get_internal_type()})")
    
    # Chercher des modèles spécifiques
    print("\n🎯 RECHERCHE DE MODÈLES SPÉCIFIQUES:")
    model_keywords = {
        'membre': ['Membre', 'Member', 'User', 'Client'],
        'cotisation': ['Cotisation', 'Payment', 'Subscription', 'Paiement'],
        'bon': ['Bon', 'Voucher', 'Ticket', 'Coupon'],
        'assureur': ['Assureur', 'Insurer', 'Agent']
    }
    
    for key, keywords in model_keywords.items():
        found_models = []
        for model in apps.get_models():
            for keyword in keywords:
                if keyword.lower() in model.__name__.lower():
                    found_models.append(model)
                    break
        
        if found_models:
            print(f"\n   ✅ {key.upper()} trouvé(s):")
            for model in found_models:
                print(f"      - {model._meta.app_label}.{model.__name__}")
                # Afficher quelques champs importants
                field_names = [f.name for f in model._meta.fields[:5]]
                print(f"        Champs: {', '.join(field_names)}...")
        else:
            print(f"   ❌ {key.upper()} non trouvé")
    
    # Vérifier la base de données
    print("\n🗃️  BASE DE DONNÉES:")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"   📊 {len(tables)} tables dans la base")
            
            # Afficher quelques tables
            for table in tables[:10]:
                print(f"      - {table[0]}")
            if len(tables) > 10:
                print(f"      ... et {len(tables) - 10} autres")
    except Exception as e:
        print(f"   ❌ Impossible d'accéder à la base: {e}")

def trouver_vues_assurance():
    """Essaie de trouver les vues liées à l'assurance"""
    print("\n🔎 RECHERCHE DES VUES ASSURANCE:")
    
    # Chercher dans le répertoire core
    core_path = os.path.join(os.path.dirname(__file__), 'core')
    if os.path.exists(core_path):
        print("   📁 Dossier 'core' trouvé")
        for file in os.listdir(core_path):
            if file.endswith('.py') and not file.startswith('__'):
                print(f"      - {file}")
    
    # Chercher des URLs
    urls_path = os.path.join(os.path.dirname(__file__), 'core', 'urls.py')
    if os.path.exists(urls_path):
        print("\n   🌐 URLs dans core/urls.py:")
        with open(urls_path, 'r') as f:
            for line in f.readlines()[:20]:  # Premières 20 lignes
                if 'path' in line or 'url' in line:
                    print(f"      {line.strip()}")

if __name__ == "__main__":
    decouvrir_structure()
    trouver_vues_assurance()
    
    print("\n🎯 PROCHAINES ÉTAPES:")
    print("1. Exécutez ce script pour voir votre structure")
    print("2. Notez les noms exacts de vos modèles")
    print("3. Je créerai les corrections adaptées")