#!/usr/bin/env python
import os
import sys
import django
from django.test import Client
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from membres.models import Membre, Bon

User = get_user_model()

def reinitialiser_mots_de_passe():
    """Réinitialise les mots de passe des utilisateurs de test"""
    print("🔑 RÉINITIALISATION DES MOTS DE PASSE")
    
    users_to_reset = ['test_agent', 'assureur_test', 'medecin_test', 'test_pharmacien']
    
    for username in users_to_reset:
        try:
            user = User.objects.get(username=username)
            user.password = make_password('pass123')
            user.save()
            print(f"✅ {username}: Mot de passe réinitialisé à 'pass123'")
        except User.DoesNotExist:
            print(f"❌ {username}: N'existe pas")

def test_complet_avec_mots_de_passe():
    print("🔄 TEST COMPLET AVEC MOTS DE PASSE CORRIGÉS")
    
    # 1. RÉINITIALISER LES MOTS DE PASSE
    reinitialiser_mots_de_passe()
    
    # 2. TEST DES CONNEXIONS
    print("\n1. 🔐 TEST DES CONNEXIONS")
    client = Client()
    
    tests = [
        ('test_agent', 'pass123', '/agents/tableau-de-bord/', 'Agent'),
        ('assureur_test', 'pass123', '/assureur/dashboard/', 'Assureur'),
        ('medecin_test', 'pass123', '/medecin/dashboard/', 'Médecin'),
        ('test_pharmacien', 'pass123', '/pharmacien/dashboard/', 'Pharmacien')
    ]
    
    for username, password, url, role in tests:
        print(f"   {role} ({username}):", end=" ")
        
        client.logout()
        login_success = client.login(username=username, password=password)
        
        if login_success:
            response = client.get(url)
            print(f"✅ {response.status_code}")
        else:
            print(f"❌ Échec connexion")
    
    # 3. TEST DES DONNÉES (CORRIGÉ)
    print("\n2. 📊 TEST DES DONNÉES")
    try:
        total_membres = Membre.objects.count()
        total_bons = Bon.objects.count()
        bons_avec_medecin = Bon.objects.filter(medecin_traitant__isnull=False).count()
        
        print(f"   👤 Membres totaux: {total_membres}")
        print(f"   🏥 Bons de soin totaux: {total_bons}")
        print(f"   👨‍⚕️ Bons avec médecin assigné: {bons_avec_medecin}")
        
        # CORRECTION: Utiliser date_inscription au lieu de date_adhesion
        derniers_membres = Membre.objects.order_by('-date_inscription')[:3]
        print("   📋 DERNIERS MEMBRES:")
        for membre in derniers_membres:
            print(f"      • {membre.nom} {membre.prenom} - {membre.date_inscription.strftime('%d/%m/%Y')}")
            
    except Exception as e:
        print(f"   ❌ Erreur données: {e}")

if __name__ == "__main__":
    test_complet_avec_mots_de_passe()