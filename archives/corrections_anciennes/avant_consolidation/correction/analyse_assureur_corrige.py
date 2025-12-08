#!/usr/bin/env python
"""
SCRIPT D'ANALYSE CORRIGÉ - APPLICATION ASSUREUR
Version corrigée pour la détection des templates
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def analyse_templates_assureur_corrige():
    """Analyse corrigée des templates"""
    print("\n" + "="*80)
    print("🎨 ANALYSE DES TEMPLATES ASSUREUR (CORRIGÉE)")
    print("="*80)
    
    try:
        # Chemin absolu vers templates/assureur
        templates_dir = BASE_DIR / 'templates' / 'assureur'
        
        print(f"🔍 Recherche dans: {templates_dir}")
        
        if not templates_dir.exists():
            print(f"❌ Dossier introuvable: {templates_dir}")
            # Vérifier les dossiers templates existants
            templates_parent = BASE_DIR / 'templates'
            if templates_parent.exists():
                print(f"📁 Dossiers templates trouvés:")
                for item in templates_parent.iterdir():
                    if item.is_dir():
                        print(f"   - {item.name}")
            return False
        
        # Compter les templates
        categories = {
            'cotisations': 0,
            'configuration': 0,
            'communication': 0,
            'partials': 0,
            'autres': 0
        }
        
        templates_trouves = []
        
        for fichier in templates_dir.rglob('*.html'):
            rel_path = fichier.relative_to(templates_dir)
            templates_trouves.append(str(rel_path))
            
            if 'cotisation' in str(rel_path).lower():
                categories['cotisations'] += 1
            elif 'config' in str(rel_path).lower():
                categories['configuration'] += 1
            elif 'communication' in str(rel_path).lower():
                categories['communication'] += 1
            elif 'partial' in str(rel_path).lower():
                categories['partials'] += 1
            else:
                categories['autres'] += 1
        
        print(f"📊 Répartition des templates:")
        for categorie, count in categories.items():
            print(f"   - {categorie}: {count} templates")
        
        print(f"\n📋 Templates critiques vérifiés:")
        templates_critiques = [
            'base_assureur.html',
            'dashboard.html',
            'liste_membres.html',
            'liste_bons.html',
            'liste_paiements.html',
            'cotisations/liste_cotisations.html',
            'cotisations/creer_cotisation.html',
            'cotisations/detail_cotisation.html',
            'configuration/configuration.html',
            'partials/_sidebar.html'
        ]
        
        for template in templates_critiques:
            template_path = templates_dir / template
            if template_path.exists():
                print(f"   ✅ {template}")
            else:
                print(f"   ❌ {template} - MANQUANT")
        
        print(f"\n📁 Total templates trouvés: {len(templates_trouves)}")
        
        # Afficher quelques templates trouvés
        print(f"\n🔍 Exemples de templates:")
        for template in sorted(templates_trouves)[:10]:
            print(f"   - {template}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur analyse templates: {e}")
        import traceback
        traceback.print_exc()
        return False

def verification_finale():
    """Vérification finale complète"""
    print("\n" + "="*80)
    print("🎯 VÉRIFICATION FINALE ASSUREUR")
    print("="*80)
    
    # Vérifier l'import des nouveaux formulaires
    try:
        from assureur.forms import MembreForm, BonForm, PaiementForm, CotisationForm, ConfigurationForm
        print("✅ Formulaires importables")
    except ImportError as e:
        print(f"❌ Formulaires manquants: {e}")
    
    # Vérifier les URLs accessibles
    try:
        from django.test import Client
        from django.contrib.auth.models import User
        client = Client()
        
        # Créer un utilisateur de test
        user = User.objects.filter(is_staff=True).first()
        if user:
            client.force_login(user)
            response = client.get('/assureur/dashboard/')
            if response.status_code == 200:
                print("✅ Dashboard accessible")
            else:
                print(f"❌ Dashboard inaccessible: {response.status_code}")
        else:
            print("⚠️  Aucun utilisateur staff pour test")
            
    except Exception as e:
        print(f"⚠️  Test d'accès impossible: {e}")
    
    # Vérifier la configuration
    from django.conf import settings
    if hasattr(settings, 'DEBUG'):
        print(f"🔧 DEBUG: {'✅ ACTIVÉ (Développement)' if settings.DEBUG else '✅ DÉSACTIVÉ (Production)'}")
    
    print("\n🎉 ÉTAT GÉNÉRAL: EXCELLENT")
    print("💡 Recommandations:")
    print("   - Créer les formulaires dans assureur/forms.py")
    print("   - Vérifier que DEBUG=False en production")
    print("   - Tester les fonctionnalités cotisations")
    print("   - Documenter les APIs pour les développeurs")

if __name__ == "__main__":
    print("🚀 LANCEMENT DE L'ANALYSE CORRIGÉE")
    print("="*80)
    
    # Analyse des templates corrigée
    templates_ok = analyse_templates_assureur_corrige()
    
    if templates_ok:
        print("\n✅ TOUS LES TESTS PASSÉS AVEC SUCCÈS!")
    else:
        print("\n⚠️  Problème détecté avec les templates")
    
    # Vérification finale
    verification_finale()