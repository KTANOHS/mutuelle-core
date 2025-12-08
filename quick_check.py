#!/usr/bin/env python
"""
VÉRIFICATION RAPIDE DU MODULE AGENTS - VERSION CORRIGÉE DES CHEMINS
"""

import os
import sys
from pathlib import Path

# CORRECTION : Chemin de base correct
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

def quick_check():
    print("🚀 VÉRIFICATION RAPIDE DU MODULE AGENTS")
    print("=" * 50)
    
    # CORRECTION : Chemins relatifs corrects
    agents_dir = BASE_DIR / 'agents'
    templates_dir = BASE_DIR / 'templates' / 'agents'
    
    print(f"📍 BASE_DIR: {BASE_DIR}")
    print(f"📍 Agents dir: {agents_dir}")
    print(f"📍 Templates dir: {templates_dir}")
    
    # Vérifier les fichiers essentiels dans agents/
    essential_files = [
        ('__init__.py', 'Package Python'),
        ('admin.py', 'Configuration Admin'),
        ('urls.py', 'Routes URLs'),
        ('views.py', 'Vues Django'),
        ('models.py', 'Modèles Django'),
    ]
    
    print("\n📁 FICHIERS ESSENTIELS DANS agents/:")
    for file_name, description in essential_files:
        file_path = agents_dir / file_name
        if file_path.exists():
            size_kb = file_path.stat().st_size / 1024
            print(f"   ✅ {description:25} - PRÉSENT ({size_kb:.1f} KB)")
        else:
            print(f"   ❌ {description:25} - MANQUANT")
    
    # Vérifier les templates
    if templates_dir.exists():
        templates = list(templates_dir.glob('*.html'))
        print(f"\n📄 TEMPLATES: {len(templates)} trouvés dans templates/agents/")
        for template in templates[:10]:  # Afficher les 10 premiers
            print(f"   📋 {template.name}")
        if len(templates) > 10:
            print(f"   ... et {len(templates) - 10} autres")
    else:
        print(f"\n📄 TEMPLATES: ❌ Dossier {templates_dir} manquant")
    
    # Vérifier les migrations
    migrations_dir = agents_dir / 'migrations'
    if migrations_dir.exists():
        migrations = list(migrations_dir.glob('*.py'))
        print(f"\n🔄 MIGRATIONS: {len(migrations)} fichiers")
        for migration in migrations[:5]:  # Afficher les 5 premiers
            print(f"   📦 {migration.name}")
    else:
        print(f"\n🔄 MIGRATIONS: ❌ Dossier manquant")
    
    # Tester l'import des modèles
    print(f"\n🗃️  MODÈLES:")
    try:
        from agents.models import Agent, VerificationCotisation, ActiviteAgent, BonSoin
        print("   ✅ Tous les modèles importables")
        
        # Vérifier si les modèles sont enregistrés en base
        from django.apps import apps
        for model in [Agent, VerificationCotisation, ActiviteAgent, BonSoin]:
            try:
                count = model.objects.count()
                print(f"   📊 {model.__name__:25} - {count} enregistrements")
            except Exception as e:
                print(f"   ⚠️  {model.__name__:25} - Erreur accès BD: {e}")
                
    except ImportError as e:
        print(f"   ❌ Erreur import modèles: {e}")
    
    # Tester les URLs
    print(f"\n🌐 URLs:")
    try:
        from django.urls import reverse, NoReverseMatch
        
        test_urls = [
            'agents:dashboard',
            'agents:verification_cotisations',
            'agents:creer_bon_soin',
            'agents:recherche_membres_api',
            'agents:verifier_cotisation_api',
            'agents:historique_bons',
            'agents:rapport_performance',
        ]
        
        for url_name in test_urls:
            try:
                url = reverse(url_name)
                print(f"   ✅ {url_name:35} -> {url}")
            except NoReverseMatch:
                print(f"   ❌ {url_name:35} -> NON TROUVÉE")
                
    except Exception as e:
        print(f"   ❌ Erreur test URLs: {e}")

if __name__ == '__main__':
    quick_check()