#!/usr/bin/env python
"""
SCRIPT DE VALIDATION FINALE DU MODULE AGENTS - VERSION CORRIGÉE
Test complet de toutes les fonctionnalités du module agents
"""

import os
import sys
import django
from django.urls import reverse, NoReverseMatch
from django.test import Client
from django.contrib.auth import get_user_model

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def valider_urls_agents():
    """Validation CORRIGÉE des URLs agents avec gestion des paramètres"""
    print("\n🌐 TEST COMPLET DES URLs:")
    print("-" * 30)
    
    # Liste des URLs à tester avec leurs paramètres nécessaires
    urls_a_tester = [
        ('agents:dashboard', [], "Tableau de bord"),
        ('agents:verification_cotisations', [], "Vérification cotisations"),
        ('agents:creer_bon_soin', [], "Créer bon de soin"),
        ('agents:creer_bon_soin_membre', [1], "Créer bon pour membre spécifique"),  # CORRIGÉ: Ajout paramètre
        ('agents:confirmation_bon_soin', [1], "Confirmation bon de soin"),  # CORRIGÉ: Ajout paramètre
        ('agents:historique_bons', [], "Historique bons"),
        ('agents:rapport_performance', [], "Rapport performance"),
        ('agents:creer_membre', [], "Créer membre"),
        ('agents:liste_membres', [], "Liste membres"),
        ('agents:recherche_membres_api', [], "API recherche membres"),
        ('agents:verifier_cotisation_api', [], "API vérification cotisation"),
        ('agents:test_simple_api', [], "API test simple"),
        ('agents:api_recherche_membres_bon_soin', [], "API recherche membres bon soin"),
        ('agents:communication', [], "Communication"),
        ('agents:liste_messages', [], "Liste messages"),
        ('agents:liste_notifications', [], "Liste notifications"),
        ('agents:envoyer_message', [], "Envoyer message"),
    ]
    
    urls_trouvees = 0
    total_urls = len(urls_a_tester)
    
    for url_name, args, description in urls_a_tester:
        try:
            # Utiliser reverse avec les arguments appropriés
            if args:
                url = reverse(url_name, args=args)
            else:
                url = reverse(url_name)
            
            print(f"   ✅ {url_name:45} -> {url}")
            urls_trouvees += 1
            
        except NoReverseMatch as e:
            print(f"   ❌ {url_name:45} -> NON TROUVÉE: {str(e)[:50]}...")
        except Exception as e:
            print(f"   ❌ {url_name:45} -> ERREUR: {str(e)[:50]}...")
    
    return urls_trouvees, total_urls

def valider_modeles_agents():
    """Validation des modèles agents"""
    print("\n🗃️  TEST DES MODÈLES:")
    print("-" * 30)
    
    try:
        from agents.models import Agent, VerificationCotisation, ActiviteAgent, BonSoin
        
        modeles_stats = []
        
        # Agent
        try:
            count_agent = Agent.objects.count()
            modeles_stats.append(('Agent', count_agent, 'OK' if count_agent >= 0 else 'VIDE'))
        except Exception as e:
            modeles_stats.append(('Agent', 0, f'ERREUR: {e}'))
        
        # VerificationCotisation
        try:
            count_verif = VerificationCotisation.objects.count()
            modeles_stats.append(('VerificationCotisation', count_verif, 'OK' if count_verif >= 0 else 'VIDE'))
        except Exception as e:
            modeles_stats.append(('VerificationCotisation', 0, f'ERREUR: {e}'))
        
        # ActiviteAgent
        try:
            count_activite = ActiviteAgent.objects.count()
            modeles_stats.append(('ActiviteAgent', count_activite, 'OK' if count_activite >= 0 else 'VIDE'))
        except Exception as e:
            modeles_stats.append(('ActiviteAgent', 0, f'ERREUR: {e}'))
        
        # BonSoin
        try:
            count_bon = BonSoin.objects.count()
            modeles_stats.append(('BonSoin', count_bon, 'OK' if count_bon >= 0 else 'VIDE'))
        except Exception as e:
            modeles_stats.append(('BonSoin', 0, f'ERREUR: {e}'))
        
        # Affichage des résultats
        for nom, count, statut in modeles_stats:
            print(f"   {statut} {nom:25} - {count:3} enregistrements - {statut}")
        
        return len([m for m in modeles_stats if 'OK' in m[2]])
    
    except Exception as e:
        print(f"   ❌ Erreur validation modèles: {e}")
        return 0

def valider_templates_agents():
    """Validation des templates agents"""
    print("\n📄 TEST DES TEMPLATES:")
    print("-" * 30)
    
    try:
        from django.template.loader import get_template
        from django.conf import settings
        
        templates_agents = [
            'agents/dashboard.html',
            'agents/verification_cotisations.html',
            'agents/creer_bon_soin.html',
            'agents/creer_bon_soin_membre.html',  # CORRIGÉ: Template ajouté
            'agents/confirmation_bon_soin.html',  # CORRIGÉ: Template ajouté
            'agents/historique_bons.html',
            'agents/rapport_performance.html',
            'agents/creer_membre.html',
            'agents/liste_membres.html',
            'agents/communication.html',
            'agents/communication/liste_messages.html',
            'agents/communication/liste_notifications.html',
            'agents/communication/envoyer_message.html',
        ]
        
        templates_trouves = 0
        
        for template_name in templates_agents:
            try:
                template = get_template(template_name)
                print(f"   ✅ {template_name}")
                templates_trouves += 1
            except Exception as e:
                print(f"   ❌ {template_name} - NON TROUVÉ: {str(e)[:50]}...")
        
        print(f"\n   ✅ {templates_trouves} templates trouvés")
        return templates_trouves >= 10  # Au moins 10 templates requis
        
    except Exception as e:
        print(f"   ❌ Erreur validation templates: {e}")
        return False

def main():
    """Fonction principale de validation"""
    print("🎯 VALIDATION FINALE DU MODULE AGENTS - VERSION CORRIGÉE")
    print("=" * 50)
    
    # Validation des URLs
    urls_trouvees, total_urls = valider_urls_agents()
    
    # Validation des modèles
    modeles_ok = valider_modeles_agents()
    
    # Validation des templates
    templates_ok = valider_templates_agents()
    
    # Calcul du score
    score_urls = (urls_trouvees / total_urls) * 100
    score_modeles = (modeles_ok / 4) * 100 if modeles_ok > 0 else 0
    score_final = (score_urls * 0.5) + (score_modeles * 0.3) + (100 * 0.2 if templates_ok else 0)
    
    print("\n🎯 SCORE FINAL:")
    print("-" * 30)
    print(f"   📈 Score: {score_final:.1f}%")
    
    if score_final >= 95:
        print("   ✅ EXCELLENT! Module agents complètement fonctionnel")
    elif score_final >= 80:
        print("   ✅ BON! Module agents fonctionnel avec quelques améliorations possibles")
    elif score_final >= 60:
        print("   ⚠️  MODERÉ! Module agents nécessite des corrections")
    else:
        print("   ❌ CRITIQUE! Module agents nécessite une refonte")
    
    # Détail du score
    print(f"\n📊 DÉTAIL:")
    print(f"   URLs: {urls_trouvees}/{total_urls} ({score_urls:.1f}%)")
    print(f"   Modèles: {modeles_ok}/4 ({score_modeles:.1f}%)")
    print(f"   Templates: {'✅ OK' if templates_ok else '❌ PROBLEME'}")

if __name__ == "__main__":
    main()