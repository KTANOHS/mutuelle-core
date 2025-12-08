#!/usr/bin/env python
"""
Script pour tester spécifiquement la redirection après connexion médecin
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

def tester_redirection_medecin():
    """Test spécifique de la redirection après connexion médecin"""
    print("🎯 TEST REDIRECTION MÉDECIN")
    print("=" * 50)
    
    client = Client()
    
    # 1. Créer un médecin de test
    print("1. Préparation du médecin de test...")
    specialite, _ = SpecialiteMedicale.objects.get_or_create(nom='Généraliste')
    etablissement, _ = EtablissementMedical.objects.get_or_create(nom='Clinique Test')
    
    user, created = User.objects.get_or_create(
        username='dr.redirection',
        defaults={
            'email': 'dr.redirection@test.com',
            'first_name': 'Docteur',
            'last_name': 'Redirection',
            'is_active': True
        }
    )
    
    if created:
        user.set_password('Medecin123!')
        user.save()
        user.groups.add(Group.objects.get_or_create(name='medecin')[0])
        
        Medecin.objects.create(
            user=user,
            numero_ordre='MEDREDIR001',
            specialite=specialite,
            etablissement=etablissement,
            actif=True
        )
        print("   ✅ Médecin de test créé")
    
    # 2. Test de connexion
    print("2. Test de connexion...")
    response = client.post('/medecin/connexion/', {
        'username': 'dr.redirection',
        'password': 'Medecin123!'
    }, follow=True)  # follow=True pour suivre les redirections
    
    # 3. Vérifier la redirection
    print("3. Vérification de la redirection...")
    
    # Afficher l'historique des redirections
    print(f"   Historique des redirections: {response.redirect_chain}")
    
    # Vérifier l'URL finale
    final_url = response.request['PATH_INFO']
    print(f"   URL finale: {final_url}")
    
    # Vérifier le contexte
    if response.context and 'user' in response.context:
        user = response.context['user']
        print(f"   Utilisateur connecté: {user.username}")
        print(f"   Est authentifié: {user.is_authenticated}")
        
        if hasattr(user, 'medecin_profile'):
            print(f"   Profil médecin: ✅ (Dr {user.get_full_name()})")
        else:
            print(f"   Profil médecin: ❌")
    
    # Vérifier si on est sur le bon dashboard
    if '/medecin/dashboard/' in final_url:
        print("   ✅ SUCCÈS: Redirection vers dashboard médecin")
        return True
    elif '/membres/' in final_url:
        print("   ❌ ÉCHEC: Redirection vers dashboard membre")
        return False
    else:
        print(f"   ⚠️  Redirection inattendue: {final_url}")
        return False

def tester_acces_direct_dashboard():
    """Test d'accès direct au dashboard médecin"""
    print("\n4. Test accès direct au dashboard...")
    
    client = Client()
    
    # Essayer d'accéder sans être connecté
    response = client.get('/medecin/dashboard/', follow=True)
    print(f"   Accès non authentifié: {response.status_code}")
    
    if response.redirect_chain:
        print(f"   Redirigé vers: {response.redirect_chain[0][0]}")
    
    # Se connecter
    client.login(username='dr.redirection', password='Medecin123!')
    
    # Essayer d'accéder après connexion
    response = client.get('/medecin/dashboard/', follow=True)
    print(f"   Accès après connexion: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ Accès dashboard réussi")
        return True
    else:
        print("   ❌ Accès dashboard échoué")
        return False

if __name__ == "__main__":
    print("🚀 TEST COMPLET DE REDIRECTION MÉDECIN")
    print("=" * 60)
    
    # Test 1: Redirection après connexion
    test1 = tester_redirection_medecin()
    
    # Test 2: Accès direct
    test2 = tester_acces_direct_dashboard()
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS:")
    print(f"Redirection après connexion: {'✅ SUCCÈS' if test1 else '❌ ÉCHEC'}")
    print(f"Accès direct au dashboard: {'✅ SUCCÈS' if test2 else '❌ ÉCHEC'}")
    
    if not test1:
        print("\n🔧 SOLUTIONS:")
        print("1. Vérifier que la vue connexion_medecin redirige bien vers 'medecin:dashboard'")
        print("2. Vérifier qu'il n'y a pas de paramètre 'next' qui override la redirection")
        print("3. Vérifier les middlewares de redirection")
        print("4. Vérifier la configuration LOGIN_REDIRECT_URL")