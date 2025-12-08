# test_generation_web.py
import os
import django
import requests
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("=== TEST DE GÉNÉRATION VIA WEB ===")

# Créer une session
session = requests.Session()

# 1. Se connecter
login_url = 'http://127.0.0.1:8000/accounts/login/'
response = session.get(login_url)

if response.status_code != 200:
    print(f"❌ Impossible d'accéder à la page de login: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})

if not csrf_token:
    print("❌ Token CSRF non trouvé")
    # Essayer de trouver dans une autre balise
    csrf_token = soup.find('input', {'name': 'csrf_token'})
    if not csrf_token:
        print("❌ Aucun token CSRF trouvé")
        exit()

csrf_token = csrf_token['value']

# Données de connexion
login_data = {
    'username': 'admin',  # Remplacez par vos identifiants
    'password': 'admin123',  # Remplacez par votre mot de passe
    'csrfmiddlewaretoken': csrf_token
}

response = session.post(login_url, data=login_data, allow_redirects=True)

if 'login' in response.url:
    print("❌ Échec de la connexion - redirigé vers login")
    print(f"Contenu: {response.text[:500]}")
    exit()
else:
    print("✅ Connexion réussie")

# 2. Aller à la page de génération
gen_url = 'http://127.0.0.1:8000/assureur/cotisations/generer/'
response = session.get(gen_url)

if response.status_code != 200:
    print(f"❌ Impossible d'accéder à la page de génération: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

print(f"✅ Page de génération accessible")
print(f"✅ Token CSRF: {csrf_token[:20]}...")

# 3. Compter les cotisations avant
from assureur.models import Cotisation
avant = Cotisation.objects.count()
print(f"✅ Cotisations avant génération: {avant}")

# 4. Générer des cotisations
periode = '2025-03'  # Période de test
post_data = {
    'periode': periode,
    'csrfmiddlewaretoken': csrf_token
}

response = session.post(gen_url, data=post_data, allow_redirects=True)

if response.status_code == 200 or response.status_code == 302:
    print(f"✅ Génération envoyée - Status: {response.status_code}")
    
    # Vérifier les messages
    soup = BeautifulSoup(response.text, 'html.parser')
    messages = soup.find_all(class_='alert')
    
    if messages:
        for msg in messages:
            print(f"Message: {msg.text.strip()}")
    
    # Vérifier la redirection
    if response.history:  # Il y a eu une redirection
        print(f"✅ Redirection vers: {response.url}")
    
    # Compter les cotisations après
    apres = Cotisation.objects.count()
    print(f"✅ Cotisations après génération: {apres}")
    print(f"✅ Différence: {apres - avant}")
    
    if apres > avant:
        print(f"✅ SUCCÈS: {apres - avant} cotisation(s) créée(s)")
        nouvelles = Cotisation.objects.all().order_by('-id')[:apres-avant]
        for cot in nouvelles:
            print(f"  - {cot.reference}: {cot.membre.nom} - {cot.periode}")
    else:
        print("⚠ Aucune nouvelle cotisation créée")
else:
    print(f"❌ Erreur lors de la génération: {response.status_code}")
    print(f"Contenu: {response.text[:500]}")

print("\n=== TEST TERMINÉ ===")