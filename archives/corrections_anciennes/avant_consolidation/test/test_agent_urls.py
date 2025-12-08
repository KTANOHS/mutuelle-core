#!/usr/bin/env python
"""
Test complet de toutes les URLs agents
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(str(Path(__file__).parent))

django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

def test_all_agent_urls():
    """Teste toutes les URLs agents avec un utilisateur connecté"""
    print("🔍 TEST COMPLET DES URLs AGENTS")
    print("=" * 60)
    
    client = Client()
    
    # Trouver un utilisateur agent pour se connecter
    User = get_user_model()
    agent_user = User.objects.filter(
        groups__name='Agents', 
        is_active=True
    ).first()
    
    if not agent_user:
        print("❌ Aucun utilisateur agent trouvé pour les tests")
        # Essayer avec un utilisateur staff comme fallback
        agent_user = User.objects.filter(is_staff=True, is_active=True).first()
        if agent_user:
            print(f"⚠️  Utilisation d'un utilisateur staff comme fallback: {agent_user.username}")
        else:
            print("❌ Aucun utilisateur disponible pour les tests")
            return
    
    print(f"👤 Utilisateur de test: {agent_user.username}")
    client.force_login(agent_user)
    
    # Liste des URLs à tester
    urls_to_test = [
        ('/agents/', 'Accueil agents'),
        ('/agents/tableau-de-bord/', 'Tableau de bord'),
        ('/agents/dashboard/', 'Dashboard (redirection)'),
        ('/agents/membres/', 'Liste membres'),
        ('/agents/membres/creer/', 'Créer membre'),
        ('/agents/bons/creer/', 'Créer bon de soin'),
        ('/agents/bons/historique/', 'Historique bons'),
        ('/agents/cotisations/verification/', 'Vérification cotisations'),
        ('/agents/messages/', 'Messages'),
        ('/agents/notifications/', 'Notifications'),
        ('/agents/rapports/performance/', 'Rapport performance'),
    ]
    
    results = []
    
    for url, description in urls_to_test:
        try:
            response = client.get(url)
            
            if response.status_code == 200:
                status = "✅"
                # Vérifier si le template est correct
                if hasattr(response, 'template_name'):
                    template = response.template_name
                    if template and 'error' not in str(template).lower():
                        status = "✅"
                    else:
                        status = "⚠️"
            elif response.status_code == 302:
                status = "🔄"
            elif response.status_code == 404:
                status = "❌"
            else:
                status = "⚠️"
            
            results.append({
                'url': url,
                'description': description,
                'status': status,
                'code': response.status_code,
                'template': getattr(response, 'template_name', 'N/A')
            })
            
            print(f"{status} {description} - {url} (Code: {response.status_code})")
            
        except Exception as e:
            print(f"❌ {description} - {url} (Erreur: {e})")
            results.append({
                'url': url,
                'description': description, 
                'status': '❌',
                'code': 'ERROR',
                'template': str(e)
            })
    
    # Rapport final
    print(f"\n{'='*60}")
    print("📊 RAPPORT FINAL")
    print(f"{'='*60}")
    
    success_count = sum(1 for r in results if r['status'] == '✅')
    redirect_count = sum(1 for r in results if r['status'] == '🔄')
    error_count = sum(1 for r in results if r['status'] in ['❌', '⚠️'])
    
    print(f"✅ URLs réussies: {success_count}")
    print(f"🔄 Redirections: {redirect_count}") 
    print(f"❌/⚠️ Erreurs: {error_count}")
    print(f"📊 Total testé: {len(results)}")
    
    # Détails des erreurs
    if error_count > 0:
        print(f"\n🔍 DÉTAILS DES PROBLÈMES:")
        for result in results:
            if result['status'] in ['❌', '⚠️']:
                print(f"   {result['status']} {result['description']}")
                print(f"      URL: {result['url']}")
                print(f"      Code: {result['code']}")
                if 'template' in result:
                    print(f"      Template: {result['template']}")

def main():
    print("🎯 TEST COMPLET DE L'ESPACE AGENT")
    print("Cette vérifie que toutes les URLs agents fonctionnent correctement")
    print("=" * 60)
    
    test_all_agent_urls()
    
    print(f"\n💡 RECOMMANDATIONS:")
    print("   • Les URLs avec ✅ sont opérationnelles")
    print("   • Les URLs avec 🔄 redirigent (normal pour certaines)")
    print("   • Les URLs avec ❌/⚠️ nécessitent une investigation")
    print(f"\n🚀 Prochaines étapes:")
    print("   • Testez manuellement les URLs dans le navigateur")
    print("   • Vérifiez les logs Django pour les erreurs détaillées")
    print("   • Consultez les vues agents/views.py pour les problèmes")

if __name__ == "__main__":
    main()