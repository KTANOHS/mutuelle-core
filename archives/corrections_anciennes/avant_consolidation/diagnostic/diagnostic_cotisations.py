#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

import logging
from django.utils import timezone
from datetime import timedelta

# Configuration du logger
logger = logging.getLogger('diagnostic')

print("🔍 ===== DIAGNOSTIC SYSTÈME COTISATIONS =====")
print()

# 1. VÉRIFICATION DES MODÈLES
print("1. 📊 VÉRIFICATION DES MODÈLES DISPONIBLES")
try:
    from membres.models import Membre
    print("   ✅ Modèle Membre importé avec succès")
    
    # Test d'un membre spécifique
    try:
        membre_test = Membre.objects.get(id=6)
        print(f"   ✅ Membre trouvé: ID={membre_test.id}, {membre_test.prenom} {membre_test.nom}")
        print(f"   📅 Date inscription: {getattr(membre_test, 'date_inscription', 'Non définie')}")
        print(f"   💰 Est à jour: {getattr(membre_test, 'est_a_jour', 'Non défini')}")
    except Membre.DoesNotExist:
        print("   ❌ Membre ID=6 non trouvé")
    except Exception as e:
        print(f"   ❌ Erreur récupération membre: {e}")
        
except ImportError as e:
    print(f"   ❌ Modèle Membre non disponible: {e}")

print()

# 2. VÉRIFICATION DES FONCTIONS DANS LE FICHIER VIEWS
print("2. 🔧 VÉRIFICATION DES FONCTIONS DANS agents/views.py")

def test_fonctions_views():
    """Teste si les fonctions sont bien définies dans views.py"""
    try:
        # Essayer d'importer les fonctions
        from agents.views import verifier_statut_cotisation_simple, verifier_cotisation_membre_simplifiee
        
        print("   ✅ verifier_statut_cotisation_simple importée")
        print("   ✅ verifier_cotisation_membre_simplifiee importée")
        
        # Tester la fonction avec un membre
        try:
            membre = Membre.objects.get(id=6)
            resultat = verifier_statut_cotisation_simple(membre)
            print(f"   ✅ Test fonction simple: {resultat}")
            
            resultat_complet = verifier_cotisation_membre_simplifiee(membre)
            print(f"   ✅ Test fonction complète: {resultat_complet[0]}")
            
        except Exception as e:
            print(f"   ❌ Erreur test fonctions: {e}")
            
    except ImportError as e:
        print(f"   ❌ Fonctions non importables: {e}")
        print("   💡 Le problème est l'ordre des fonctions dans views.py")
        
    except Exception as e:
        print(f"   ❌ Erreur importation: {e}")

test_fonctions_views()
print()

# 3. VÉRIFICATION DE L'ORDRE DES FONCTIONS
print("3. 📝 ANALYSE DE L'ORDRE DES FONCTIONS")

def analyser_ordre_fonctions():
    """Analyse l'ordre des fonctions dans le fichier views.py"""
    try:
        views_path = "agents/views.py"
        with open(views_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Chercher les positions des fonctions
        pos_simple = content.find("def verifier_statut_cotisation_simple")
        pos_simplifiee = content.find("def verifier_cotisation_membre_simplifiee")
        pos_verifier_api = content.find("def verifier_cotisation_api")
        
        print(f"   📍 Position verifier_statut_cotisation_simple: {pos_simple}")
        print(f"   📍 Position verifier_cotisation_membre_simplifiee: {pos_simplifiee}")
        print(f"   📍 Position verifier_cotisation_api: {pos_verifier_api}")
        
        if pos_simple == -1:
            print("   ❌ verifier_statut_cotisation_simple NON TROUVÉE dans le fichier")
        if pos_simplifiee == -1:
            print("   ❌ verifier_cotisation_membre_simplifiee NON TROUVÉE dans le fichier")
            
        # Vérifier l'ordre
        if pos_simple > 0 and pos_simplifiee > 0:
            if pos_simple < pos_simplifiee:
                print("   ✅ Ordre correct: simple AVANT simplifiee")
            else:
                print("   ❌ Ordre INCORRECT: simple APRÈS simplifiee")
                
        if pos_verifier_api > 0 and pos_simple > 0:
            if pos_simple < pos_verifier_api:
                print("   ✅ Ordre correct: simple AVANT API")
            else:
                print("   ❌ Ordre INCORRECT: simple APRÈS API")
                
    except FileNotFoundError:
        print("   ❌ Fichier agents/views.py non trouvé")
    except Exception as e:
        print(f"   ❌ Erreur analyse fichier: {e}")

analyser_ordre_fonctions()
print()

# 4. TEST DIRECT DES FONCTIONS
print("4. 🧪 TEST DIRECT DES FONCTIONS")

def test_fonctions_locales():
    """Teste les fonctions avec une définition locale"""
    
    # Définition locale pour test
    def verifier_statut_cotisation_simple_test(membre):
        try:
            print(f"   🔍 Test local - Membre: {membre.prenom} {membre.nom}")
            
            aujourd_hui = timezone.now().date()
            
            if hasattr(membre, 'date_inscription') and membre.date_inscription:
                if hasattr(membre.date_inscription, 'date'):
                    date_inscription = membre.date_inscription.date()
                else:
                    date_inscription = membre.date_inscription
                    
                delai_creation = aujourd_hui - date_inscription
                if delai_creation.days < 30:
                    print(f"   ❌ Nouveau membre ({delai_creation.days} jours) - NON À JOUR")
                    return False
            
            print("   ⚠️ Aucune donnée - Statut par défaut: NON À JOUR")
            return False
            
        except Exception as e:
            print(f"   ❌ Erreur test local: {e}")
            return False
    
    def verifier_cotisation_membre_simplifiee_test(membre):
        try:
            print(f"   🔍 Test simplifié local - Membre: {membre.id}")
            
            est_a_jour = verifier_statut_cotisation_simple_test(membre)
            
            if est_a_jour:
                return True, {'message': 'À jour'}
            else:
                return False, {'message': 'Non à jour'}
                
        except Exception as e:
            print(f"   ❌ Erreur test simplifié local: {e}")
            return False, {'message': f'Erreur: {e}'}
    
    # Exécuter le test
    try:
        membre = Membre.objects.get(id=6)
        resultat = verifier_cotisation_membre_simplifiee_test(membre)
        print(f"   ✅ Test local réussi: {resultat}")
    except Exception as e:
        print(f"   ❌ Test local échoué: {e}")

test_fonctions_locales()
print()

# 5. RECOMMANDATIONS
print("5. 🎯 RECOMMANDATIONS")
print("   🔧 SOLUTION 1: Réorganiser l'ordre des fonctions dans views.py")
print("      - verifier_statut_cotisation_simple DOIT être définie EN PREMIER")
print("      - verifier_cotisation_membre_simplifiee EN DEUXIÈME") 
print("      - verifier_cotisation_api APRÈS")
print()
print("   🔧 SOLUTION 2: Redémarrer le serveur Django après modifications")
print("      Commande: python manage.py runserver")
print()
print("   🔧 SOLUTION 3: Vérifier l'import dans verifier_cotisation_api")
print("      S'assurer qu'elle utilise bien les fonctions corrigées")

print()
print("🔍 ===== DIAGNOSTIC TERMINÉ =====")