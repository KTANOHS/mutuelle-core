#!/usr/bin/env python
"""
SCRIPT DE VALIDATION CORRIGÉ - VERSION AVEC GESTION DES ARGUMENTS
Test complet du module agents avec support des URLs paramétrées
"""

import os
import sys
import django
from django.urls import reverse, NoReverseMatch

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("🎯 VALIDATION FINALE DU MODULE AGENTS - VERSION CORRIGÉE")
    print("=" * 50)
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def test_agents_urls():
    """Tester toutes les URLs du module agents avec gestion des arguments"""
    
    print("🌐 TEST COMPLET DES URLs AVEC ARGUMENTS:")
    print("-" * 50)
    
    # Liste de toutes les URLs agents à tester
    agents_urls = [
        # Tableau de bord
        'agents:dashboard',
        'agents:verification_cotisations',
        'agents:rapport_performance',
        
        # Gestion membres
        'agents:creer_membre',
        'agents:liste_membres',
        
        # Bons de soin
        'agents:creer_bon_soin',
        'agents:creer_bon_soin_membre',  # Nécessite membre_id
        'agents:confirmation_bon_soin',  # Nécessite bon_id
        'agents:historique_bons',
        
        # APIs
        'agents:recherche_membres_api',
        'agents:verifier_cotisation_api',
        'agents:test_simple_api',
        'agents:api_recherche_membres_bon_soin',
        
        # Communication
        'agents:communication',
        'agents:liste_messages',
        'agents:liste_notifications',
        'agents:envoyer_message',
    ]
    
    working_urls = 0
    total_urls = len(agents_urls)
    
    for url_name in agents_urls:
        try:
            # Gestion des URLs avec paramètres
            if url_name == 'agents:creer_bon_soin_membre':
                url = reverse(url_name, args=[1])  # membre_id = 1
            elif url_name == 'agents:confirmation_bon_soin':
                url = reverse(url_name, args=[1])  # bon_id = 1
            else:
                url = reverse(url_name)
            
            print(f"   ✅ {url_name:45} -> {url}")
            working_urls += 1
            
        except NoReverseMatch as e:
            print(f"   ❌ {url_name:45} -> NON TROUVÉE: {e}")
        except Exception as e:
            print(f"   ❌ {url_name:45} -> ERREUR: {e}")
    
    print(f"\n📊 URLs: {working_urls}/{total_urls} fonctionnelles")
    
    # Calcul du score
    score = (working_urls / total_urls) * 100 if total_urls > 0 else 0
    print(f"\n🎯 SCORE FINAL: {score:.1f}%")
    
    if score == 100:
        print("   🎉 EXCELLENT! Module agents complètement fonctionnel")
    elif score >= 80:
        print("   ✅ TRÈS BON! Module agents fonctionnel")
    elif score >= 60:
        print("   ⚠️  ACCEPTABLE! Module agents avec quelques problèmes")
    else:
        print("   ❌ CRITIQUE! Module agents nécessite des corrections")
    
    return score

if __name__ == "__main__":
    test_agents_urls()
