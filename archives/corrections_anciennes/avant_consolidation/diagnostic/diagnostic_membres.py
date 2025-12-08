#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC - MEMBRE INTROUVABLE
Version 1.0 - Diagnostic complet de la recherche membres
"""

import os
import sys
import django
from django.db.models import Q

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    django.setup()
    
    from membres.models import Membre
    from agents.models import Agent
    from django.contrib.auth import get_user_model
    from django.utils import timezone
    import logging
    
    # Configuration logging
    logging.basicConfig(level=logging.INFO, format='🔍 %(message)s')
    logger = logging.getLogger('diagnostic')

except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def diagnostic_complet():
    """Diagnostic complet du problème des membres introuvables"""
    
    print("=" * 80)
    print("🔍 DIAGNOSTIC COMPLET - MEMBRES INTROUVABLES")
    print("=" * 80)
    
    # 1. COMPTAGE DES MEMBRES
    print("\n1. 📊 ANALYSE DE LA BASE DE DONNÉES")
    print("-" * 40)
    
    try:
        total_membres = Membre.objects.count()
        print(f"✅ Total membres dans la base: {total_membres}")
        
        # Derniers membres créés
        derniers_membres = Membre.objects.all().order_by('-id')[:5]
        print(f"📋 5 derniers membres (ID décroissant):")
        for membre in derniers_membres:
            print(f"   • ID: {membre.id} | {membre.prenom} {membre.nom} | Tel: {getattr(membre, 'telephone', 'N/A')}")
            
    except Exception as e:
        print(f"❌ Erreur comptage membres: {e}")
        return

    # 2. TEST DE RECHERCHE AVEC DIFFÉRENTS TERMES
    print("\n2. 🔍 TEST DES RECHERCHES")
    print("-" * 40)
    
    termes_test = ['glo', 'gloria', 'kou', 'roger', 'kouakou']
    
    for terme in termes_test:
        try:
            resultats = Membre.objects.filter(
                Q(nom__icontains=terme) |
                Q(prenom__icontains=terme) |
                Q(telephone__icontains=terme)
            )
            
            print(f"🔎 Recherche '{terme}': {resultats.count()} résultat(s)")
            
            for membre in resultats:
                print(f"   ✅ Trouvé: ID {membre.id} - {membre.prenom} {membre.nom}")
                
        except Exception as e:
            print(f"❌ Erreur recherche '{terme}': {e}")

    # 3. ANALYSE DES CHAMPS DISPONIBLES
    print("\n3. 📝 STRUCTURE DU MODÈLE MEMBRE")
    print("-" * 40)
    
    try:
        if total_membres > 0:
            premier_membre = Membre.objects.first()
            champs = [attr for attr in dir(premier_membre) if not attr.startswith('_') and not callable(getattr(premier_membre, attr))]
            
            print("Champs disponibles dans le modèle Membre:")
            for champ in sorted(champs)[:15]:  # Afficher les 15 premiers
                valeur = getattr(premier_membre, champ, 'N/A')
                print(f"   • {champ}: {valeur}")
                
    except Exception as e:
        print(f"❌ Erreur analyse structure: {e}")

    # 4. TEST DE CRÉATION D'UN MEMBRE TEST
    print("\n4. 🧪 TEST DE CRÉATION ET RECHERCHE")
    print("-" * 40)
    
    try:
        # Vérifier si un membre test existe déjà
        membre_test_existe = Membre.objects.filter(nom="TEST_DIAG", prenom="Diagnostic").exists()
        
        if not membre_test_existe:
            print("🧪 Création d'un membre test...")
            membre_test = Membre.objects.create(
                nom="TEST_DIAG",
                prenom="Diagnostic", 
                telephone="0102030405",
                statut="actif"
            )
            print(f"✅ Membre test créé - ID: {membre_test.id}")
            
            # Test recherche immédiate
            print("🔍 Test recherche immédiate après création...")
            resultats = Membre.objects.filter(
                Q(nom__icontains="TEST") |
                Q(prenom__icontains="Diagnostic") |
                Q(telephone__icontains="0102030405")
            )
            print(f"📊 Résultats recherche: {resultats.count()} membre(s) trouvé(s)")
            
        else:
            print("ℹ️  Membre test existe déjà")
            
    except Exception as e:
        print(f"❌ Erreur création membre test: {e}")

    # 5. COMPARAISON AVEC LA RECHERCHE API
    print("\n5. 🔄 COMPARAISON AVEC L'API")
    print("-" * 40)
    
    try:
        from agents.views import recherche_membres_api
        from django.test import RequestFactory
        
        factory = RequestFactory()
        
        for terme in ['glo', 'test']:
            print(f"\n🔍 Simulation API recherche: '{terme}'")
            request = factory.get(f'/agents/api/recherche-membres/?q={terme}')
            request.user = get_user_model().objects.first()  # Premier utilisateur
            
            # Simulation manuelle de la logique API
            if len(terme) < 2:
                print("   ⚠️  Terme trop court (API retourne vide)")
                continue
                
            membres_api = Membre.objects.filter(
                Q(nom__icontains=terme) |
                Q(prenom__icontains=terme) |
                Q(telephone__icontains=terme)
            )[:10]
            
            print(f"   📊 API trouverait: {membres_api.count()} résultat(s)")
            for membre in membres_api:
                print(f"   ✅ API: ID {membre.id} - {membre.prenom} {membre.nom}")
                
    except Exception as e:
        print(f"❌ Erreur comparaison API: {e}")

    # 6. VÉRIFICATION DES AGENTS
    print("\n6. 👥 ANALYSE DES AGENTS")
    print("-" * 40)
    
    try:
        total_agents = Agent.objects.count()
        print(f"📊 Total agents: {total_agents}")
        
        agents = Agent.objects.all()[:3]
        for agent in agents:
            user_info = getattr(agent, 'user', None)
            username = getattr(user_info, 'username', 'N/A') if user_info else 'N/A'
            print(f"   • Agent: {username} | ID: {agent.id}")
            
    except Exception as e:
        print(f"❌ Erreur analyse agents: {e}")

    # 7. RAPPORT FINAL
    print("\n" + "=" * 80)
    print("🎯 RAPPORT DE DIAGNOSTIC")
    print("=" * 80)
    
    print("\n📋 POINTS À VÉRIFIER:")
    print("   1. ✅ Vérifier que les membres créés sont bien enregistrés en BDD")
    print("   2. ✅ Comparer les champs de recherche entre liste_membres et verification_cotisations") 
    print("   3. ✅ Vérifier les filtres appliqués dans chaque vue")
    print("   4. ✅ Tester la création/récherche en temps réel")
    print("   5. ✅ Vérifier les permissions d'accès aux données")
    
    print("\n🔧 ACTIONS RECOMMANDÉES:")
    print("   • Créer un membre via l'interface et vérifier son ID")
    print("   • Rechercher immédiatement ce membre par son ID exact")
    print("   • Comparer les requêtes SQL générées")
    print("   • Vérifier les logs Django pour les erreurs cachées")
    
    print(f"\n⏰ Diagnostic terminé à: {timezone.now()}")

if __name__ == "__main__":
    diagnostic_complet()