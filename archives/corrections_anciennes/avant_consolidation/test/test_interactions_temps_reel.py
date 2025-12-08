# test_interactions_temps_reel.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_vue_acteur(utilisateur, url, nom_acteur):
    """Teste l'accès d'un acteur à une vue spécifique"""
    client = Client()
    
    # Simuler la connexion
    if client.login(username=utilisateur.username, password='test123'):
        response = client.get(url)
        if response.status_code == 200:
            print(f"   ✅ {nom_acteur} peut accéder à {url}")
            return True
        else:
            print(f"   ❌ {nom_acteur} ne peut pas accéder à {url} (Status: {response.status_code})")
            return False
    else:
        print(f"   ❌ {nom_acteur} - Échec connexion")
        return False

print("🔐 TEST DES PERMISSIONS EN TEMPS RÉEL")

# Test avec différents utilisateurs
try:
    # Récupérer un utilisateur de test pour chaque rôle
    test_agent = User.objects.filter(username__icontains='agent').first()
    test_assureur = User.objects.filter(username__icontains='assureur').first() 
    test_medecin = User.objects.filter(username__icontains='medecin').first()
    test_pharmacien = User.objects.filter(username__icontains='pharmacien').first()
    
    if test_agent:
        test_vue_acteur(test_agent, '/agents/tableau-de-bord/', 'Agent')
        test_vue_acteur(test_agent, '/agents/verification-cotisations/', 'Agent')
    
    if test_assureur:
        test_vue_acteur(test_assureur, '/assureur/dashboard/', 'Assureur')
        test_vue_acteur(test_assureur, '/assureur/cotisations/', 'Assureur')
        
    if test_medecin:
        test_vue_acteur(test_medecin, '/medecin/dashboard/', 'Médecin')
        test_vue_acteur(test_medecin, '/medecin/ordonnances/', 'Médecin')
        
    if test_pharmacien:
        test_vue_acteur(test_pharmacien, '/pharmacien/dashboard/', 'Pharmacien')
        test_vue_acteur(test_pharmacien, '/pharmacien/ordonnances/', 'Pharmacien')
        
except Exception as e:
    print(f"❌ Erreur test permissions: {e}")