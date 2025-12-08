# tester_points_acces.py
import os
import django
from django.conf import settings
from django.test import Client
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def tester_points_acces():
    """Teste les points d'accès principaux de l'application"""
    
    client = Client()
    User = get_user_model()
    
    print("🧪 TEST DES POINTS D'ACCÈS PRINCIPAUX")
    print("=" * 50)
    
    # Créer un utilisateur de test si nécessaire
    try:
        user = User.objects.filter(is_staff=True).first()
        if not user:
            print("❌ Aucun utilisateur staff trouvé pour les tests")
            return
        
        # Tester la connexion
        client.force_login(user)
        
        # Points d'accès à tester
        urls_a_tester = [
            '/assureur/',
            '/medecin/dashboard/',
            '/pharmacien/dashboard/',
            '/membres/dashboard/',
            '/soins/',
            '/admin/'
        ]
        
        print("\n🔍 TEST DES URLs:")
        for url in urls_a_tester:
            try:
                response = client.get(url)
                if response.status_code == 200:
                    print(f"✅ {url} - OK (200)")
                elif response.status_code == 302:
                    print(f"⚠️  {url} - Redirection ({response.status_code})")
                elif response.status_code == 403:
                    print(f"🔒 {url} - Accès refusé ({response.status_code})")
                else:
                    print(f"❌ {url} - Erreur ({response.status_code})")
            except Exception as e:
                print(f"💥 {url} - Exception: {str(e)}")
    
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")

def verifier_modeles_critiques():
    """Vérifie l'état des modèles critiques"""
    
    from django.apps import apps
    
    print("\n🔍 ÉTAT DES MODÈLES CRITIQUES")
    print("=" * 40)
    
    modeles_critiques = ['Soin', 'Ordonnance', 'Bon', 'Membre', 'Paiement']
    
    for nom_modele in modeles_critiques:
        try:
            modele = apps.get_model('assureur', nom_modele)
            count = modele.objects.count()
            print(f"✅ {nom_modele}: {count} enregistrement(s)")
        except LookupError:
            try:
                modele = apps.get_model('soins', nom_modele)
                count = modele.objects.count()
                print(f"✅ {nom_modele}: {count} enregistrement(s)")
            except LookupError:
                try:
                    modele = apps.get_model('medecin', nom_modele)
                    count = modele.objects.count()
                    print(f"✅ {nom_modele}: {count} enregistrement(s)")
                except LookupError:
                    print(f"❌ {nom_modele}: Modèle non trouvé")

if __name__ == "__main__":
    tester_points_acces()
    verifier_modeles_critiques()