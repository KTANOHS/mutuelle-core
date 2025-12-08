# test_without_server_fixed.py
import os
import django
import sys

# Ajoutez le chemin du projet à sys.path
projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

# Configurez Django AVANT d'importer quoi que ce soit
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

# MAINTENANT vous pouvez importer les modèles Django
from django.test import Client
from django.contrib.auth.models import User

print("=== TEST SANS SERVEUR (Client Django) ===")
print(f"Chemin du projet: {projet_path}")

# 1. Créer un superutilisateur de test
try:
    # Supprimer d'abord l'utilisateur existant pour éviter la contrainte unique
    User.objects.filter(username='test_admin').delete()
    
    user = User.objects.create_superuser(
        username='test_admin',  # Changez le nom d'utilisateur pour éviter le conflit
        email='test_admin@test.com',
        password='test123'
    )
    print("✅ Superutilisateur de test créé")
except Exception as e:
    print(f"❌ Erreur création utilisateur: {e}")
    try:
        user = User.objects.get(username='admin')
        print("✅ Utilisation de l'admin existant")
    except Exception:
        print("❌ Aucun utilisateur disponible")
        user = None

# 2. Tester avec le client Django
client = Client()

# 2.1. Se connecter
if user:
    try:
        login = client.login(username=user.username, password='test123' if user.username == 'test_admin' else 'admin123')
        print(f"Connexion: {'✅ Réussie' if login else '❌ Échec'}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        login = False
else:
    print("❌ Impossible de se connecter - pas d'utilisateur")
    login = False

# 2.2. Tester la page de génération
if login:
    print(f"\n{'='*50}")
    print("1. Test de la page de génération")
    print(f"{'='*50}")
    
    try:
        response = client.get('/assureur/cotisations/generer/')
        print(f"URL: /assureur/cotisations/generer/")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Page accessible")
            
            content = response.content.decode('utf-8', errors='ignore')
            
            # Vérifications
            checks = [
                ('<title', 'Balise title présente'),
                ('csrfmiddlewaretoken', 'Token CSRF présent'),
                ('periode', 'Champ période présent'),
                ('générer', 'Texte "générer" présent'),
            ]
            
            for text, description in checks:
                if text.lower() in content.lower():
                    print(f"  ✓ {description}")
                else:
                    print(f"  ✗ {description} manquante")
            
            # Vérifier si c'est un formulaire
            if '<form' in content and 'method="post"' in content:
                print("  ✓ Formulaire POST détecté")
            else:
                print("  ✗ Aucun formulaire POST détecté")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            
    except Exception as e:
        print(f"❌ Exception lors du test: {e}")

# 2.3. Tester la prévisualisation (avec gestion d'erreur)
if login:
    print(f"\n{'='*50}")
    print("2. Test de la prévisualisation")
    print(f"{'='*50}")
    
    try:
        response = client.get('/assureur/cotisations/preview/?periode=2025-03')
        print(f"URL: /assureur/cotisations/preview/?periode=2025-03")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Prévisualisation fonctionnelle")
            
            content_type = response.get('Content-Type', '')
            print(f"Content-Type: {content_type}")
            
            content = response.content.decode('utf-8', errors='ignore')
            
            if len(content) > 0:
                if 'prévisualisation' in content.lower() or 'membres' in content.lower():
                    print("✓ Contenu pertinent détecté")
                else:
                    print("⚠ Contenu différent de ce qui était attendu")
                    print(f"Extrait (500 chars): {content[:500]}...")
            else:
                print("⚠ Contenu vide")
                
        elif response.status_code == 500:
            print("❌ Erreur serveur 500")
            content = response.content.decode('utf-8', errors='ignore')
            if 'TemplateDoesNotExist' in content:
                print("  ✗ Template manquant")
                print("  Solution: Créez le fichier assureur/templates/assureur/includes/preview_content.html")
            else:
                print(f"  Erreur: {content[:500]}...")
        else:
            print(f"❌ Statut inattendu: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception lors du test de prévisualisation: {e}")

# 2.4. Tester si l'application assureur est bien configurée
print(f"\n{'='*50}")
print("3. Vérification de l'application")
print(f"{'='*50}")

try:
    from django.conf import settings
    
    # Vérifier si assureur est dans INSTALLED_APPS
    if 'assureur' in settings.INSTALLED_APPS:
        print("✅ Application 'assureur' trouvée dans INSTALLED_APPS")
    else:
        print("❌ Application 'assureur' NON trouvée dans INSTALLED_APPS")
        
    # Vérifier les templates
    template_dirs = getattr(settings, 'TEMPLATES', [{}])[0].get('DIRS', [])
    print(f"Répertoires de templates: {template_dirs}")
    
    # Chercher le template manuel
    import os
    template_path = os.path.join(projet_path, 'assureur/templates/assureur/includes/preview_content.html')
    if os.path.exists(template_path):
        print(f"✅ Template trouvé: {template_path}")
    else:
        print(f"❌ Template NON trouvé: {template_path}")
        print("   Pour le créer :")
        print("   mkdir -p assureur/templates/assureur/includes")
        print("   touch assureur/templates/assureur/includes/preview_content.html")
        
except Exception as e:
    print(f"❌ Erreur lors de la vérification: {e}")

print(f"\n{'='*50}")
print("TEST TERMINÉ")
print(f"{'='*50}")