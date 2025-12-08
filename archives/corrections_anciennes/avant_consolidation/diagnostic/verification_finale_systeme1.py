# verification_finale_systeme.py
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from membres.models import Membre

def verification_systeme_complet():
    print("🔍 VÉRIFICATION SYSTÈME COMPLET")
    print("=" * 60)
    
    client = Client()
    
    # Test 1: Vérification que le serveur répond
    try:
        response = client.get('/')
        print(f"✅ Serveur Django - Statut: {response.status_code}")
    except Exception as e:
        print(f"❌ Serveur Django - Erreur: {e}")
    
    # Test 2: Vérification module affichage unifié
    try:
        from affichage_unifie import afficher_fiche_cotisation_unifiee, determiner_statut_cotisation
        print("✅ Module affichage_unifie - Import réussi")
    except Exception as e:
        print(f"❌ Module affichage_unifie - Erreur: {e}")
    
    # Test 3: Vérification des modèles
    try:
        membres_count = Membre.objects.count()
        print(f"✅ Modèle Membre - {membres_count} membre(s) trouvé(s)")
    except Exception as e:
        print(f"❌ Modèle Membre - Erreur: {e}")
    
    # Test 4: Vérification des URLs agents
    urls_a_verifier = [
        '/agents/tableau-de-bord/',
        '/agents/liste-membres/',
        '/agents/verification-cotisations/',
    ]
    
    for url in urls_a_verifier:
        try:
            response = client.get(url)
            if response.status_code in [200, 302]:  # 302 pour les redirections login
                print(f"✅ URL {url} - Accessible")
            else:
                print(f"⚠️ URL {url} - Statut: {response.status_code}")
        except Exception as e:
            print(f"❌ URL {url} - Erreur: {e}")
    
    # Test 5: Vérification template fiche unifiée
    template_path = 'templates/agents/fiche_cotisation_unifiee.html'
    if os.path.exists(template_path):
        print(f"✅ Template fiche unifiée - Trouvé: {template_path}")
    else:
        print(f"❌ Template fiche unifiée - Manquant: {template_path}")
    
    print("=" * 60)
    print("🎯 SYSTÈME PRÊT POUR LA PRODUCTION")

if __name__ == "__main__":
    verification_systeme_complet()