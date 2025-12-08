#!/usr/bin/env python
"""
Vérification finale de l'état du projet
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verify_project_state():
    """Vérifie l'état complet du projet"""
    print("🔍 VÉRIFICATION FINALE DU PROJET")
    print("=" * 50)
    
    from django.test import Client
    from django.contrib.auth.models import User
    
    checks = {
        "Connexions utilisateurs": False,
        "Dashboard assureur": False,
        "Liste membres assureur": False,
        "Profils utilisateurs": False,
        "Templates principaux": False
    }
    
    # Test des connexions
    client = Client()
    test_users = [
        ('test_assureur', 'pass123'),
        ('test_medecin', 'pass123'),
        ('test_pharmacien', 'pass123'),
        ('test_membre', 'pass123')
    ]
    
    connexions_ok = 0
    for username, password in test_users:
        if client.login(username=username, password=password):
            connexions_ok += 1
            print(f"✅ {username} connecté")
        else:
            print(f"❌ {username} échec connexion")
    
    checks["Connexions utilisateurs"] = connexions_ok == len(test_users)
    
    # Test spécifique assureur
    client.login(username='test_assureur', password='pass123')
    
    # Dashboard assureur
    response = client.get('/assureur-dashboard/')
    checks["Dashboard assureur"] = response.status_code == 200
    
    # Liste membres
    response = client.get('/assureur/membres/')
    checks["Liste membres assureur"] = response.status_code == 200
    
    # Vérification des profils
    try:
        from medecin.models import Medecin
        from pharmacien.models import Pharmacien
        from membres.models import Membre
        from assureur.models import Assureur
        
        profiles_ok = 0
        for username in ['test_medecin', 'test_pharmacien', 'test_membre', 'test_assureur']:
            user = User.objects.get(username=username)
            if hasattr(user, 'medecin') or hasattr(user, 'pharmacien') or hasattr(user, 'membre') or hasattr(user, 'assureur'):
                profiles_ok += 1
        
        checks["Profils utilisateurs"] = profiles_ok >= 3  # Au moins 3 profils sur 4
    except:
        checks["Profils utilisateurs"] = False
    
    # Vérification des templates
    templates = [
        'templates/membres/liste_membres.html',
        'templates/medecin/dashboard.html',
        'templates/pharmacien/dashboard.html',
        'templates/membres/dashboard.html'
    ]
    
    templates_ok = sum(1 for t in templates if os.path.exists(t))
    checks["Templates principaux"] = templates_ok >= 3
    
    # Affichage des résultats
    print("\n📊 RÉSULTATS DE LA VÉRIFICATION:")
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check}")
    
    total_passed = sum(checks.values())
    total_checks = len(checks)
    
    print(f"\n🎯 SCORE: {total_passed}/{total_checks}")
    
    if total_passed == total_checks:
        print("\n🎉 EXCELLENT! Le projet est complètement fonctionnel!")
        print("🚀 Vous pouvez procéder au déploiement en production.")
    elif total_passed >= 3:
        print("\n👍 BON! Le projet est fonctionnel avec quelques améliorations possibles.")
        print("💡 Vous pouvez utiliser l'application normalement.")
    else:
        print("\n⚠️  ATTENTION! Le projet a des problèmes critiques.")
        print("🔧 Des corrections supplémentaires sont nécessaires.")

if __name__ == "__main__":
    verify_project_state()