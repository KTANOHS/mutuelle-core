#!/usr/bin/env python
"""
Script de test manuel pour la connexion médecin
Usage: python test_connexion_manuel.py
"""

import os
import django
import sys
import requests
import json
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from medecin.models import MedecinProfile
from django.utils import timezone

User = get_user_model()

class TesteurConnexionMedecin:
    """Classe pour tester manuellement la connexion médecin"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.client = Client()
        self.base_url = base_url
        self.resultats = []
    
    def afficher_resultat(self, test_name, success, details=""):
        """Affiche le résultat d'un test"""
        statut = "✅ SUCCÈS" if success else "❌ ÉCHEC"
        print(f"{statut} {test_name}")
        if details:
            print(f"   Détails: {details}")
        print("-" * 50)
        
        self.resultats.append({
            'test': test_name,
            'success': success,
            'details': details,
            'timestamp': timezone.now().isoformat()
        })
    
    def test_connexion_valide(self):
        """Test de connexion avec des identifiants valides"""
        try:
            # Création d'un médecin de test si nécessaire
            user, created = User.objects.get_or_create(
                username='test.medecin',
                defaults={
                    'email': 'test.medecin@clinique.com',
                    'password': 'MedecinTest123!',
                    'first_name': 'Test',
                    'last_name': 'Medecin',
                    'is_active': True
                }
            )
            
            if created:
                user.set_password('MedecinTest123!')
                user.save()
                MedecinProfile.objects.create(
                    user=user,
                    numero_ordre='TEST123456',
                    specialite='Generaliste',
                    est_actif=True
                )
            
            # Test de connexion
            response = self.client.post('/medecin/connexion/', {
                'username': 'test.medecin',
                'password': 'MedecinTest123!'
            }, follow=True)
            
            success = response.status_code == 200 and response.context['user'].is_authenticated
            details = f"Utilisateur: {response.context['user'].username}" if success else "Échec authentification"
            
            self.afficher_resultat("Connexion valide", success, details)
            
        except Exception as e:
            self.afficher_resultat("Connexion valide", False, f"Erreur: {str(e)}")
    
    def test_connexion_invalide(self):
        """Test de connexion avec des identifiants invalides"""
        try:
            response = self.client.post('/medecin/connexion/', {
                'username': 'utilisateur.inexistant',
                'password': 'MauvaisPassword123!'
            })
            
            success = not response.context['user'].is_authenticated
            details = "Authentification correctement refusée" if success else "Authentification anormale"
            
            self.afficher_resultat("Connexion invalide", success, details)
            
        except Exception as e:
            self.afficher_resultat("Connexion invalide", False, f"Erreur: {str(e)}")
    
    def test_acces_protege_sans_login(self):
        """Test d'accès à une page protégée sans être connecté"""
        try:
            response = self.client.get('/medecin/dashboard/', follow=True)
            
            # Doit rediriger vers la page de login
            success = response.redirect_chain and 'connexion' in response.redirect_chain[0][0]
            details = f"Redirection vers: {response.redirect_chain[0][0] if response.redirect_chain else 'Aucune redirection'}"
            
            self.afficher_resultat("Accès protégé sans login", success, details)
            
        except Exception as e:
            self.afficher_resultat("Accès protégé sans login", False, f"Erreur: {str(e)}")
    
    def test_deconnexion(self):
        """Test de la déconnexion"""
        try:
            # Connexion d'abord
            self.client.login(username='test.medecin', password='MedecinTest123!')
            
            # Vérification connexion
            response = self.client.get('/medecin/dashboard/')
            est_connecte_avant = response.status_code == 200
            
            # Déconnexion
            response = self.client.get('/medecin/deconnexion/', follow=True)
            est_connecte_apres = response.context['user'].is_authenticated
            
            success = est_connecte_avant and not est_connecte_apres
            details = f"Connexion avant: {est_connecte_avant}, Après: {est_connecte_apres}"
            
            self.afficher_resultat("Déconnexion", success, details)
            
        except Exception as e:
            self.afficher_resultat("Déconnexion", False, f"Erreur: {str(e)}")
    
    def test_medecin_inactif(self):
        """Test de connexion avec un médecin inactif"""
        try:
            # Création médecin inactif
            user_inactif = User.objects.create_user(
                username='medecin.inactif',
                password='Medecin123!',
                is_active=True
            )
            profil_inactif = MedecinProfile.objects.create(
                user=user_inactif,
                numero_ordre='INACTIF123',
                specialite='Radiologie',
                est_actif=False
            )
            
            # Tentative de connexion
            response = self.client.post('/medecin/connexion/', {
                'username': 'medecin.inactif',
                'password': 'Medecin123!'
            })
            
            success = not response.context['user'].is_authenticated
            details = "Accès refusé pour médecin inactif" if success else "Accès anormal autorisé"
            
            # Nettoyage
            user_inactif.delete()
            
            self.afficher_resultat("Médecin inactif", success, details)
            
        except Exception as e:
            self.afficher_resultat("Médecin inactif", False, f"Erreur: {str(e)}")
    
    def executer_tous_tests(self):
        """Exécute tous les tests"""
        print("🚀 LANCEMENT DES TESTS DE CONNEXION MÉDECIN")
        print("=" * 50)
        
        self.test_connexion_valide()
        self.test_connexion_invalide()
        self.test_acces_protege_sans_login()
        self.test_deconnexion()
        self.test_medecin_inactif()
        
        # Résumé
        succes = sum(1 for r in self.resultats if r['success'])
        total = len(self.resultats)
        
        print("\n" + "=" * 50)
        print(f"📊 RÉSUMÉ: {succes}/{total} tests réussis")
        print("=" * 50)
        
        return all(r['success'] for r in self.resultats)

if __name__ == "__main__":
    testeur = TesteurConnexionMedecin()
    testeur.executer_tous_tests()