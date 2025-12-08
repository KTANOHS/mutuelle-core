#!/usr/bin/env python
"""
Test de l'application médecin avec les templates existants
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

def verifier_templates_existants():
    """Vérifie que tous les templates médecin existent"""
    print("📁 VÉRIFICATION DES TEMPLATES EXISTANTS")
    print("=" * 50)
    
    templates_dir = "templates/medecin"
    templates_necessaires = [
        'base_medecin.html', 'dashboard.html', 'liste_ordonnances.html',
        'creer_ordonnance.html', 'historique_ordonnances.html', 'profil_medecin.html',
        'mes_rendez_vous.html', 'liste_bons.html'
    ]
    
    import os
    for template in templates_necessaires:
        path = os.path.join(templates_dir, template)
        if os.path.exists(path):
            print(f"✅ {template}")
        else:
            print(f"❌ {template} - MANQUANT")
    
    return True

def test_application_medecin():
    """Test complet de l'application médecin"""
    print("\n🚀 TEST APPLICATION MÉDECIN")
    print("=" * 50)
    
    client = Client()
    
    # 1. Créer un médecin de test
    print("1. Création médecin test...")
    specialite, _ = SpecialiteMedicale.objects.get_or_create(nom='Généraliste')
    etablissement, _ = EtablissementMedical.objects.get_or_create(nom='Clinique Test')
    
    user, created = User.objects.get_or_create(
        username='dr.existant',
        defaults={
            'email': 'dr.existant@test.com',
            'first_name': 'Docteur',
            'last_name': 'Existant',
            'is_active': True
        }
    )
    
    if created:
        user.set_password('Medecin123!')
        user.save()
        user.groups.add(Group.objects.get_or_create(name='medecin')[0])
        
        Medecin.objects.create(
            user=user,
            numero_ordre='MEDEXIST001',
            specialite=specialite,
            etablissement=etablissement,
            actif=True
        )
        print("   ✅ Médecin créé: dr.existant / Medecin123!")
    
    # 2. Test login central
    print("\n2. Test login central...")
    client.login(username='dr.existant', password='Medecin123!')
    
    # 3. Test toutes les pages médecin
    print("\n3. Test des pages médecin...")
    
    pages_a_tester = [
        ('/medecin/dashboard/', 'Tableau de bord'),
        ('/medecin/patients/', 'Liste patients'),
        ('/medecin/consultations/', 'Consultations'),
        ('/medecin/ordonnances/', 'Ordonnances'),
        ('/medecin/ordonnance/nouvelle/', 'Nouvelle ordonnance'),
        ('/medecin/ordonnances/historique/', 'Historique ordonnances'),
        ('/medecin/profil/', 'Profil médecin'),
    ]
    
    toutes_ok = True
    for url, nom in pages_a_tester:
        response = client.get(url)
        status = "✅" if response.status_code == 200 else "❌"
        print(f"   {status} {nom}: {response.status_code}")
        
        if response.status_code != 200:
            toutes_ok = False
            # Afficher l'erreur si template manquant
            if response.status_code == 500:
                print(f"      💥 Erreur template: vérifiez le template pour {url}")
    
    return toutes_ok

def test_redirection_apres_login():
    """Test de la redirection après login"""
    print("\n4. Test redirection après login...")
    
    client = Client()
    
    # Se déconnecter d'abord
    client.logout()
    
    # Se connecter via le login central
    response = client.post('/accounts/login/', {
        'username': 'dr.existant',
        'password': 'Medecin123!',
    }, follow=True)
    
    final_url = response.request['PATH_INFO']
    print(f"   URL après login: {final_url}")
    
    # Vérifier qu'on a accès à l'espace médecin
    response_dashboard = client.get('/medecin/dashboard/')
    if response_dashboard.status_code == 200:
        print("   ✅ Accès espace médecin réussi après login")
        return True
    else:
        print(f"   ❌ Problème accès espace médecin: {response_dashboard.status_code}")
        return False

if __name__ == "__main__":
    print("🔍 DIAGNOSTIC APPLICATION MÉDECIN")
    print("=" * 60)
    
    # Vérifier les templates
    templates_ok = verifier_templates_existants()
    
    # Tester l'application
    app_ok = test_application_medecin()
    
    # Tester la redirection
    redirection_ok = test_redirection_apres_login()
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS:")
    print(f"Templates existants: {'✅ OK' if templates_ok else '❌ PROBLÈME'}")
    print(f"Application fonctionnelle: {'✅ OK' if app_ok else '❌ PROBLÈME'}")
    print(f"Redirection après login: {'✅ OK' if redirection_ok else '❌ PROBLÈME'}")
    
    if all([templates_ok, app_ok, redirection_ok]):
        print("\n🎉 EXCELLENT! L'application médecin est opérationnelle!")
        print("\n🌐 POUR TESTER:")
        print("1. Allez sur: http://localhost:8000/accounts/login/")
        print("2. Connectez-vous avec: dr.existant / Medecin123!")
        print("3. Naviguez dans l'espace médecin")
    else:
        print("\n🔧 CORRECTIONS À APPLIQUER:")
        if not templates_ok:
            print("   • Vérifiez que tous les templates existent dans templates/medecin/")
        if not app_ok:
            print("   • Vérifiez les vues dans medecin/views.py")
            print("   • Vérifiez les URLs dans medecin/urls.py")
        if not redirection_ok:
            print("   • Vérifiez la configuration LOGIN_REDIRECT_URL dans settings.py")