# tester_avec_auth.py
import os
import django
from django.conf import settings
from django.test import Client
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def tester_avec_utilisateur():
    """Teste les points d'accès avec différents types d'utilisateurs"""
    
    client = Client()
    User = get_user_model()
    
    print("👤 TEST AVEC AUTHENTIFICATION")
    print("=" * 50)
    
    # Trouver différents types d'utilisateurs
    try:
        # Utilisateur staff (assureur)
        staff_user = User.objects.filter(is_staff=True).first()
        if staff_user:
            print(f"\n🔧 Test avec staff user: {staff_user.username}")
            client.force_login(staff_user)
            tester_urls_par_role(client, "Staff/Assureur")
        
        # Utilisateur médecin
        medecin_user = User.objects.filter(groups__name='Medecin').first()
        if medecin_user:
            print(f"\n🥼 Test avec médecin: {medecin_user.username}")
            client.force_login(medecin_user)
            tester_urls_par_role(client, "Medecin")
        
        # Utilisateur membre
        membre_user = User.objects.filter(groups__name='Membre').first()
        if membre_user:
            print(f"\n👤 Test avec membre: {membre_user.username}")
            client.force_login(membre_user)
            tester_urls_par_role(client, "Membre")
            
        # Utilisateur pharmacien
        pharmacien_user = User.objects.filter(groups__name='Pharmacien').first()
        if pharmacien_user:
            print(f"\n💊 Test avec pharmacien: {pharmacien_user.username}")
            client.force_login(pharmacien_user)
            tester_urls_par_role(client, "Pharmacien")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

def tester_urls_par_role(client, role):
    """Teste les URLs appropriées pour chaque rôle"""
    
    urls_par_role = {
        "Staff/Assureur": [
            '/assureur/',
            '/assureur/dashboard/',
            '/assureur/membres/',
            '/assureur/bons/',
            '/assureur/soins/',
            '/assureur/paiements/'
        ],
        "Medecin": [
            '/medecin/dashboard/',
            '/medecin/bons/',
            '/medecin/ordonnances/',
            '/medecin/rendez-vous/'
        ],
        "Membre": [
            '/membres/dashboard/',
            '/membres/mes-soins/',
            '/membres/mon-profil/'
        ],
        "Pharmacien": [
            '/pharmacien/dashboard/',
            '/pharmacien/ordonnances/'
        ]
    }
    
    urls = urls_par_role.get(role, [])
    
    for url in urls:
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"  ✅ {url} - OK")
            elif response.status_code == 403:
                print(f"  🔒 {url} - Accès refusé (normal pour {role})")
            elif response.status_code == 404:
                print(f"  ❓ {url} - Non trouvé")
            else:
                print(f"  ⚠️  {url} - Code: {response.status_code}")
        except Exception as e:
            print(f"  💥 {url} - Exception: {str(e)}")

if __name__ == "__main__":
    tester_avec_utilisateur()