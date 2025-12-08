#!/usr/bin/env python
"""
DÉCOUVERTE COMPLÈTE DE MUTUELLE_CORE
"""

import os
import sys
import django

# Configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django configuré avec mutuelle_core.settings")
except Exception as e:
    print(f"❌ Erreur configuration: {e}")
    sys.exit(1)

from django.apps import apps

def explorer_structure_complete():
    """Explore complètement la structure du projet"""
    print("\n🔍 EXPLORATION COMPLÈTE")
    print("=" * 50)
    
    # Lister toutes les applications
    print("\n📦 APPLICATIONS INSTALLÉES:")
    for app_config in apps.get_app_configs():
        models = list(app_config.get_models())
        print(f"\n🏷️  {app_config.verbose_name} ({app_config.name}):")
        print(f"   📁 Chemin: {app_config.path}")
        print(f"   📊 {len(models)} modèles:")
        
        for model in models:
            print(f"\n   📋 {model.__name__}:")
            print(f"      🗃️  Table: {model._meta.db_table}")
            
            # Afficher les champs
            fields_info = []
            for field in model._meta.fields:
                field_info = f"{field.name} ({field.get_internal_type()})"
                if field.primary_key:
                    field_info += " 🔑"
                fields_info.append(field_info)
            
            # Afficher par groupes de 3
            for i in range(0, len(fields_info), 3):
                print(f"      └ {' | '.join(fields_info[i:i+3])}")

def trouver_modeles_par_nom():
    """Cherche les modèles par nom"""
    print("\n🎯 RECHERCHE PAR NOMS:")
    
    recherches = {
        'Membre': ['membre', 'member', 'user', 'client', 'assure', 'beneficiaire', 'patient'],
        'Cotisation': ['cotisation', 'payment', 'paiement', 'subscription', 'abonnement', 'frais'],
        'Bon': ['bon', 'voucher', 'ticket', 'coupon', 'note', 'remboursement', 'claim'],
        'Assureur': ['assureur', 'insurer', 'agent', 'gestionnaire']
    }
    
    for nom_recherche, termes in recherches.items():
        print(f"\n   🔍 {nom_recherche}:")
        trouves = []
        
        for model in apps.get_models():
            for terme in termes:
                if terme in model.__name__.lower():
                    trouves.append(model)
                    break
        
        if trouves:
            for model in trouves:
                print(f"      ✅ {model._meta.app_label}.{model.__name__}")
                # Afficher les méthodes
                methodes = [m for m in dir(model) if not m.startswith('_') and callable(getattr(model, m))]
                print(f"        📝 Méthodes: {', '.join(methodes[:5])}...")
        else:
            print(f"      ❌ Non trouvé")

def lister_toutes_les_tables():
    """Lister toutes les tables de la base"""
    print("\n🗃️  TABLES DE LA BASE DE DONNÉES:")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            if 'sqlite' in connection.settings_dict['ENGINE']:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            else:
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            
            tables = [row[0] for row in cursor.fetchall()]
            
            for table in sorted(tables):
                print(f"   📋 {table}")
                
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

def verifier_fichiers_projet():
    """Vérifie la structure des fichiers"""
    print("\n📁 STRUCTURE DES FICHIERS:")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Lister les dossiers importants
    dossiers = ['core', 'assurance', 'mutuelle', 'members', 'users', 'app']
    
    for dossier in dossiers:
        dossier_path = os.path.join(current_dir, dossier)
        if os.path.exists(dossier_path):
            print(f"\n📁 {dossier}/")
            # Lister les fichiers Python
            for file in os.listdir(dossier_path):
                if file.endswith('.py') and not file.startswith('__'):
                    print(f"   📄 {file}")

if __name__ == "__main__":
    explorer_structure_complete()
    trouver_modeles_par_nom()
    lister_toutes_les_tables()
    verifier_fichiers_projet()
    
    print("\n🎯 COPIEZ TOUTE LA SORTIE DE CE SCRIPT ET COLLEZ-LA DANS VOTRE RÉPONSE")