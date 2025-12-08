#!/usr/bin/env python
"""
TEST MANUEL CORRIGÉ - VERSION COMPLÈTE
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth.models import User
from membres.models import Membre
from medecin.models import Ordonnance
from datetime import date, timedelta

def test_est_valide():
    """Test de la méthode est_valide des ordonnances"""
    print("🧪 TEST MANUEL - est_valide")
    print("=" * 50)
    
    try:
        # Créer un utilisateur de test
        user, created = User.objects.get_or_create(
            username='test_manuel_user',
            defaults={
                'first_name': 'Test',
                'last_name': 'Manuel',
                'email': 'test@manuel.com'
            }
        )
        
        # Créer une ordonnance valide (date récente)
        ordonnance_valide = Ordonnance.objects.create(
            patient=user,
            diagnostic="Test ordonnance valide",
            date_prescription=date.today() - timedelta(days=15),  # 15 jours
            medecin_prescripteur="Dr Test"
        )
        
        # Créer une ordonnance expirée
        ordonnance_expiree = Ordonnance.objects.create(
            patient=user,
            diagnostic="Test ordonnance expirée", 
            date_prescription=date.today() - timedelta(days=45),  # 45 jours
            medecin_prescripteur="Dr Test"
        )
        
        # Tester les ordonnances
        print(f"✅ Ordonnance valide (15 jours): {ordonnance_valide.est_valide}")
        print(f"✅ Ordonnance expirée (45 jours): {ordonnance_expiree.est_valide}")
        
        # Vérifications
        assert ordonnance_valide.est_valide == True, "L'ordonnance récente devrait être valide"
        assert ordonnance_expiree.est_valide == False, "L'ordonnance ancienne devrait être expirée"
        
        print("✅ Test est_valide: TOUS LES TESTS PASSÉS")
        
        # Nettoyer
        ordonnance_valide.delete()
        ordonnance_expiree.delete()
        if created:
            user.delete()
            
    except Exception as e:
        print(f"❌ Erreur test est_valide: {e}")

def test_nom_complet():
    """Test de la propriété nom_complet des membres"""
    print("\n🧪 TEST MANUEL - nom_complet")
    print("=" * 50)
    
    try:
        # Tester avec un membre existant
        membres = Membre.objects.all()[:3]  # Prendre les 3 premiers
        
        if not membres:
            print("❌ Aucun membre trouvé pour le test")
            return
            
        for i, membre in enumerate(membres, 1):
            print(f"Membre {i}:")
            print(f"  ID: {membre.id}")
            print(f"  User: {membre.user.username}")
            print(f"  First name: '{membre.user.first_name}'")
            print(f"  Last name: '{membre.user.last_name}'")
            print(f"  Nom complet: '{membre.nom_complet}'")
            print()
        
        print("✅ Test nom_complet terminé")
        
    except Exception as e:
        print(f"❌ Erreur test nom_complet: {e}")

def test_vue_ordonnances():
    """Test de la vue mes_ordonnances"""
    print("\n🧪 TEST MANUEL - Vue mes_ordonnances")
    print("=" * 50)
    
    try:
        # Importer la vue
        from membres.views import mes_ordonnances
        from django.test import RequestFactory
        
        # Créer un utilisateur avec des ordonnances
        user, created = User.objects.get_or_create(
            username='test_vue_user',
            defaults={'first_name': 'Vue', 'last_name': 'Test'}
        )
        
        # Créer quelques ordonnances pour cet utilisateur
        for i in range(2):
            Ordonnance.objects.create(
                patient=user,
                diagnostic=f"Diagnostic test vue {i}",
                date_prescription=date.today() - timedelta(days=i*10),
                medecin_prescripteur=f"Dr Vue {i}"
            )
        
        # Tester la vue
        factory = RequestFactory()
        request = factory.get('/mes-ordonnances/')
        request.user = user
        
        response = mes_ordonnances(request)
        
        print(f"✅ Statut de la vue: {response.status_code}")
        print(f"✅ Ordonnances trouvées: {Ordonnance.objects.filter(patient=user).count()}")
        
        # Nettoyer
        Ordonnance.objects.filter(patient=user).delete()
        if created:
            user.delete()
            
    except Exception as e:
        print(f"❌ Erreur test vue ordonnances: {e}")

def test_acces_assureur():
    """Test d'accès à la fonctionnalité assureur"""
    print("\n🧪 TEST MANUEL - Accès Assureur")
    print("=" * 50)
    
    try:
        from django.test import Client
        from django.contrib.auth.models import User
        
        client = Client()
        
        # 1. Se connecter avec l'utilisateur assureur_complet
        user = User.objects.get(username='assureur_complet')
        client.force_login(user)
        
        # 2. Tester l'accès à la création de bon pour le membre 5
        url = '/assureur/bons/creer/5/'
        response = client.get(url)
        
        print(f"✅ URL testée: {url}")
        print(f"✅ Statut: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ ACCÈS AUTORISÉ - La page fonctionne!")
        elif response.status_code == 302:
            print(f"⚠️  Redirection vers: {response.url}")
        else:
            print(f"❌ Accès refusé: {response.status_code}")
            
    except User.DoesNotExist:
        print("❌ Utilisateur assureur_complet non trouvé")
    except Exception as e:
        print(f"❌ Erreur test accès assureur: {e}")

if __name__ == "__main__":
    print("🎯 DÉMARRAGE DES TESTS MANUELS CORRIGÉS")
    print("=" * 60)
    
    test_est_valide()
    test_nom_complet() 
    test_vue_ordonnances()
    test_acces_assureur()
    
    print("\n" + "=" * 60)
    print("🎉 TESTS MANUELS TERMINÉS")