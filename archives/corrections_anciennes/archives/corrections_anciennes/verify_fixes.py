#!/usr/bin/env python
"""
Vérification des correctifs appliqués
"""

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

from django.template.loader import get_template
from django.urls import get_resolver
from django.test import Client
from django.contrib.auth.models import User

def verify_fixes():
    print("🔍 VÉRIFICATION DES CORRECTIONS APPLIQUÉES")
    print("=" * 50)
    
    issues_fixed = 0
    remaining_issues = []
    
    # 1. Vérifier les templates
    print("\n1. VÉRIFICATION DES TEMPLATES:")
    templates_to_check = [
        'agents/base.html',
        'agents/creer_bon_soin.html',
        'agents/dashboard.html',
        'agents/liste_membres.html',
        'agents/notifications.html'
    ]
    
    for template_name in templates_to_check:
        try:
            template = get_template(template_name)
            print(f"   ✅ {template_name} - ACCESSIBLE")
            issues_fixed += 1
        except Exception as e:
            print(f"   ❌ {template_name} - ERREUR: {e}")
            remaining_issues.append(f"Template {template_name}: {e}")
    
    # 2. Vérifier l'utilisateur de test
    print("\n2. VÉRIFICATION UTILISATEUR TEST:")
    try:
        user = User.objects.get(username='test_agent')
        print(f"   ✅ Utilisateur test_agent trouvé")
        
        # Vérifier le profil agent
        if hasattr(user, 'agent'):
            print(f"   ✅ Profil agent associé trouvé")
            issues_fixed += 1
        else:
            print(f"   ❌ Aucun profil agent associé")
            remaining_issues.append("Profil agent manquant pour test_agent")
            
    except User.DoesNotExist:
        print(f"   ❌ Utilisateur test_agent non trouvé")
        remaining_issues.append("Utilisateur test_agent non créé")
    
    # 3. Vérifier l'accès aux URLs principales
    print("\n3. TEST D'ACCÈS AUX URLs:")
    client = Client()
    
    # Essayer de se connecter avec l'utilisateur test
    try:
        user = User.objects.get(username='test_agent')
        client.force_login(user)
        
        urls_to_test = [
            '/agents/dashboard/',
            '/agents/bons/creer/',
            '/agents/membres/',
            '/agents/notifications/',
        ]
        
        for url in urls_to_test:
            try:
                response = client.get(url)
                if response.status_code in [200, 302]:
                    print(f"   ✅ {url} - Accès {response.status_code}")
                    issues_fixed += 1
                else:
                    print(f"   ❌ {url} - Code {response.status_code}")
                    remaining_issues.append(f"URL {url} retourne {response.status_code}")
            except Exception as e:
                print(f"   💥 {url} - Erreur: {e}")
                remaining_issues.append(f"URL {url} erreur: {e}")
                
    except User.DoesNotExist:
        print("   ⚠️ Impossible de tester les URLs: utilisateur test_agent non trouvé")
    
    # 4. Vérifier les filtres de template
    print("\n4. VÉRIFICATION DES FILTRES:")
    try:
        from agents.templatetags import custom_filters
        print("   ✅ Filtres personnalisés chargés")
        issues_fixed += 1
    except ImportError as e:
        print(f"   ❌ Filtres personnalisés non chargés: {e}")
        remaining_issues.append(f"Filtres personnalisés: {e}")
    
    # Résumé
    print("\n" + "=" * 50)
    print("RAPPORT FINAL")
    print("=" * 50)
    
    print(f"✅ Problèmes résolus: {issues_fixed}")
    
    if remaining_issues:
        print(f"❌ Problèmes restants: {len(remaining_issues)}")
        for issue in remaining_issues:
            print(f"   - {issue}")
    else:
        print("🎉 Tous les problèmes ont été résolus !")
    
    return len(remaining_issues) == 0

if __name__ == "__main__":
    success = verify_fixes()
    sys.exit(0 if success else 1)