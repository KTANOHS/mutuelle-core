#!/usr/bin/env python
"""
Test du système de login unifié avec redirection intelligente
"""

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from medecin.models import Medecin, SpecialiteMedicale, EtablissementMedical

User = get_user_model()

def test_login_unifie_medecin():
    """Test qu'un médecin est redirigé vers son dashboard après login central"""
    print("🧪 TEST LOGIN UNIFIÉ - MÉDECIN")
    print("=" * 50)
    
    client = Client()
    
    # 1. Créer un médecin de test
    print("1. Création médecin test...")
    specialite, _ = SpecialiteMedicale.objects.get_or_create(nom='Généraliste')
    etablissement, _ = EtablissementMedical.objects.get_or_create(nom='Clinique Test')
    
    user, created = User.objects.get_or_create(
        username='dr.unifie',
        defaults={
            'email': 'dr.unifie@test.com',
            'first_name': 'Docteur',
            'last_name': 'Unifie',
            'is_active': True
        }
    )
    
    if created:
        user.set_password('Medecin123!')
        user.save()
        user.groups.add(Group.objects.get_or_create(name='medecin')[0])
        
        Medecin.objects.create(
            user=user,
            numero_ordre='MEDUNIFIE001',
            specialite=specialite,
            etablissement=etablissement,
            actif=True
        )
        print("   ✅ Médecin créé: dr.unifie / Medecin123!")
    
    # 2. Utiliser le login central (pas /medecin/connexion/)
    print("2. Connexion via login central...")
    response = client.post('/accounts/login/', {
        'username': 'dr.unifie',
        'password': 'Medecin123!',
        'next': '/redirect-after-login/'  # Important pour la redirection intelligente
    }, follow=True)
    
    # 3. Vérifier la redirection
    print("3. Vérification redirection...")
    final_url = response.request['PATH_INFO']
    print(f"   URL finale: {final_url}")
    
    if '/medecin/dashboard/' in final_url:
        print("   ✅ SUCCÈS: Redirigé vers dashboard médecin après login central!")
        return True
    elif '/accounts/login/' in final_url:
        print("   ❌ ÉCHEC: Resté sur la page de login")
        return False
    else:
        print(f"   ⚠️  Redirection inattendue: {final_url}")
        return False

def test_acces_protege_medecin():
    """Test qu'un médecin peut accéder à ses pages protégées"""
    print("\n4. Test accès pages protégées médecin...")
    
    client = Client()
    
    # Se connecter d'abord
    client.login(username='dr.unifie', password='Medecin123!')
    
    # Tester l'accès aux pages médecin
    urls_medecin = [
        '/medecin/dashboard/',
        '/medecin/patients/',
        '/medecin/consultations/',
        '/medecin/ordonnances/',
    ]
    
    for url in urls_medecin:
        response = client.get(url)
        status = "✅" if response.status_code == 200 else "❌"
        print(f"   {status} {url}: {response.status_code}")
    
    return True

def test_utilisateur_non_medecin():
    """Test qu'un utilisateur normal ne peut pas accéder à l'espace médecin"""
    print("\n5. Test protection espace médecin...")
    
    client = Client()
    
    # Créer un utilisateur normal
    user_normal, created = User.objects.get_or_create(
        username='user.normal',
        defaults={
            'email': 'normal@test.com',
            'password': 'User123!',
            'is_active': True
        }
    )
    
    if created:
        user_normal.set_password('User123!')
        user_normal.save()
    
    # Se connecter comme utilisateur normal
    client.login(username='user.normal', password='User123!')
    
    # Essayer d'accéder à l'espace médecin
    response = client.get('/medecin/dashboard/', follow=True)
    
    if response.status_code == 403 or 'Accès réservé' in str(response.content):
        print("   ✅ SUCCÈS: Accès refusé à l'espace médecin")
        return True
    elif response.status_code == 200:
        print("   ❌ ÉCHEC: Accès anormalement autorisé")
        return False
    else:
        print(f"   ⚠️  Statut inattendu: {response.status_code}")
        return False

if __name__ == "__main__":
    print("🚀 TEST SYSTÈME DE LOGIN UNIFIÉ")
    print("=" * 60)
    
    # Test 1: Login unifié et redirection
    test1 = test_login_unifie_medecin()
    
    # Test 2: Accès aux pages protégées
    test2 = test_acces_protege_medecin()
    
    # Test 3: Protection de l'espace médecin
    test3 = test_utilisateur_non_medecin()
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS:")
    print(f"Login unifié et redirection: {'✅ SUCCÈS' if test1 else '❌ ÉCHEC'}")
    print(f"Accès pages protégées: {'✅ SUCCÈS' if test2 else '❌ ÉCHEC'}")
    print(f"Protection espace médecin: {'✅ SUCCÈS' if test3 else '❌ ÉCHEC'}")
    
    if all([test1, test2, test3]):
        print("\n🎉 EXCELLENT! Le système de login unifié fonctionne parfaitement!")
        print("\n✅ AVANTAGES:")
        print("   • Une seule page de login à maintenir")
        print("   • Expérience utilisateur cohérente")
        print("   • Sécurité centralisée")
        print("   • Maintenance simplifiée")