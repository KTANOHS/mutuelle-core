#!/usr/bin/env python
"""
Diagnostic des problèmes de redirection médecin
"""

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from django.conf import settings

User = get_user_model()

def diagnostic_complet():
    print("🔍 DIAGNOSTIC COMPLET DES REDIRECTIONS")
    print("=" * 60)
    
    client = Client()
    
    # 1. Vérifier les URLs médecin
    print("1. VÉRIFICATION DES URLs MÉDECIN:")
    print("-" * 35)
    
    urls_medecin = [
        ('medecin:dashboard', 'Tableau de bord'),
        ('medecin:liste_patients', 'Liste patients'),
        ('medecin:liste_consultations', 'Consultations'),
        ('medecin:liste_ordonnances', 'Ordonnances'),
        ('medecin:creer_ordonnance', 'Nouvelle ordonnance'),
        ('medecin:historique_ordonnances', 'Historique ordonnances'),
        ('medecin:profil', 'Profil médecin'),
    ]
    
    for url_name, description in urls_medecin:
        try:
            url = reverse(url_name)
            print(f"✅ {description}: {url}")
        except Exception as e:
            print(f"❌ {description}: {e}")
    
    # 2. Vérifier la configuration login
    print(f"\n2. CONFIGURATION LOGIN:")
    print("-" * 25)
    print(f"LOGIN_REDIRECT_URL: {getattr(settings, 'LOGIN_REDIRECT_URL', 'Non défini')}")
    print(f"LOGIN_URL: {getattr(settings, 'LOGIN_URL', 'Non défini')}")
    
    # 3. Tester la redirection après login
    print(f"\n3. TEST REDIRECTION APRÈS LOGIN:")
    print("-" * 35)
    
    # Créer/chercher un médecin de test
    user, created = User.objects.get_or_create(
        username='dr.diagnostic',
        defaults={'password': 'Medecin123!', 'is_active': True}
    )
    if created:
        user.set_password('Medecin123!')
        user.save()
    
    # Tester le login
    response = client.post('/accounts/login/', {
        'username': 'dr.diagnostic',
        'password': 'Medecin123!',
    }, follow=True)
    
    print(f"Status final: {response.status_code}")
    print(f"URL finale: {response.request['PATH_INFO']}")
    print(f"Redirections: {response.redirect_chain}")
    
    # 4. Tester l'accès au dashboard
    print(f"\n4. TEST ACCÈS DASHBOARD:")
    print("-" * 25)
    
    # Se connecter d'abord
    client.login(username='dr.diagnostic', password='Medecin123!')
    
    # Tester l'accès direct
    response = client.get('/medecin/dashboard/')
    print(f"Dashboard - Status: {response.status_code}")
    
    if response.status_code == 302:
        print(f"Dashboard - Redirige vers: {response.url}")
    
    # 5. Vérifier le middleware de redirection
    print(f"\n5. MIDDLEWARE DE REDIRECTION:")
    print("-" * 30)
    
    middleware = getattr(settings, 'MIDDLEWARE', [])
    medecin_middleware = any('medecin' in str(mw) for mw in middleware)
    print(f"Middleware médecin détecté: {'✅ OUI' if medecin_middleware else '❌ NON'}")
    
    # 6. Solution recommandée
    print(f"\n6. SOLUTIONS RECOMMANDÉES:")
    print("-" * 25)
    print("Si la redirection ne fonctionne pas:")
    print("1. Vérifiez que LOGIN_REDIRECT_URL = 'core:redirect_after_login' dans settings.py")
    print("2. Vérifiez que la vue redirect_after_login existe dans core/views.py")
    print("3. Vérifiez que les URLs core sont incluses dans urls.py principal")
    print("4. Vérifiez que l'utilisateur a bien un profil médecin actif")

if __name__ == "__main__":
    diagnostic_complet()