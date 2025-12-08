# test_without_server.py
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

# 1. Créer un superutilisateur de test
try:
    user = User.objects.create_superuser(
        username='admin',
        email='admin@test.com',
        password='admin123'
    )
    print("✅ Superutilisateur créé")
except Exception as e:
    try:
        user = User.objects.get(username='admin')
        print("✅ Superutilisateur existant")
    except Exception:
        print(f"❌ Erreur avec l'utilisateur: {e}")
        user = None

# 2. Tester avec le client Django
client = Client()

# 2.1. Se connecter
if user:
    login = client.login(username='admin', password='admin123')
    print(f"Connexion: {'✅ Réussie' if login else '❌ Échec'}")
else:
    print("❌ Impossible de se connecter - pas d'utilisateur")
    login = False

# 2.2. Tester la page de génération
if login:
    response = client.get('/assureur/cotisations/generer/')
    print(f"\n1. Page génération - Status: {response.status_code}")

    if response.status_code == 200:
        print("✅ Page accessible")
        
        # Vérifier le contenu
        content = response.content.decode('utf-8')
        
        # Vérifier les éléments clés
        checks = [
            ('<h1', 'Titre présent'),
            ('periode', 'Champ période présent'),
            ('csrfmiddlewaretoken', 'Token CSRF présent'),
            ('Générer', 'Texte "Générer" présent'),
        ]
        
        for text, description in checks:
            if text in content:
                print(f"✅ {description}")
            else:
                print(f"⚠ {description} non trouvé")
        
        # Vérifier les statistiques dans le contexte
        if hasattr(response, 'context') and response.context:
            context = response.context
            print(f"\n✅ Contexte disponible:")
            print(f"   Membres actifs: {context.get('membres_actifs_count', 'N/A')}")
            print(f"   Cotisations ce mois: {context.get('cotisations_mois_count', 'N/A')}")
            print(f"   À générer: {context.get('a_generer_count', 'N/A')}")
        else:
            print("\n⚠ Contexte non disponible")
    else:
        print(f"❌ Erreur: {response.status_code}")
        if response.content:
            print(f"Contenu (500 premiers caractères):")
            try:
                print(response.content[:500].decode('utf-8', errors='ignore'))
            except:
                print("Impossible de décoder le contenu")
else:
    print("\n❌ Test page génération sauté - pas connecté")

# 2.3. Tester la prévisualisation
if login:
    print("\n2. Prévisualisation - Test GET:")
    response = client.get('/assureur/cotisations/preview/?periode=2025-03')

    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Prévisualisation fonctionnelle")
        
        # Vérifier si c'est du HTML ou du JSON
        content_type = response.get('Content-Type', '')
        if 'application/json' in content_type:
            print("✅ Retour JSON")
            import json
            try:
                data = json.loads(response.content)
                print(f"   Données: {data}")
            except:
                print("   Impossible de parser JSON")
        else:
            print("✅ Retour HTML")
            try:
                content = response.content.decode('utf-8', errors='ignore')
                if 'Prévisualisation' in content or 'membres' in content.lower():
                    print("✅ Contenu valide")
                else:
                    print(f"   Contenu: {content[:200]}...")
            except:
                print("   Impossible de décoder le contenu")
    else:
        print(f"❌ Erreur prévisualisation: {response.status_code}")

# 2.4. Tester la génération (POST)
if login:
    print("\n3. Génération - Test POST:")
    
    try:
        from assureur.models import Cotisation
        
        # Compter avant
        avant = Cotisation.objects.count()
        print(f"   Cotisations avant: {avant}")
        
        # Obtenir le token CSRF depuis la page GET
        response = client.get('/assureur/cotisations/generer/')
        if response.status_code == 200:
            try:
                content = response.content.decode('utf-8')
                # Extraire le token CSRF
                import re
                csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', content)
                
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                    print(f"✅ Token CSRF obtenu: {csrf_token[:20]}...")
                    
                    # Envoyer la requête POST
                    response = client.post('/assureur/cotisations/generer/', {
                        'periode': '2025-03',
                        'csrfmiddlewaretoken': csrf_token
                    })
                    
                    print(f"   POST Status: {response.status_code}")
                    
                    # Compter après
                    apres = Cotisation.objects.count()
                    print(f"   Cotisations après: {apres}")
                    print(f"   Différence: {apres - avant}")
                    
                    if response.status_code == 302:
                        print("✅ Redirection (succès probable)")
                        print(f"   Redirection vers: {response.url}")
                    elif response.status_code == 200:
                        print("⚠ Pas de redirection (vérifiez les messages d'erreur)")
                        
                        try:
                            # Pour récupérer les messages dans un script standalone
                            from django.contrib import messages
                            from django.contrib.messages import get_messages
                            
                            # Cette approche peut ne pas fonctionner dans tous les cas
                            # car la requête n'est pas passée par le middleware complet
                            print("   (Les messages peuvent ne pas être accessibles dans ce contexte)")
                        except Exception as e:
                            print(f"   Erreur avec les messages: {e}")
                else:
                    print("❌ Impossible d'obtenir le token CSRF")
            except Exception as e:
                print(f"❌ Erreur lors du décodage: {e}")
        else:
            print("❌ Impossible d'accéder à la page pour obtenir le token CSRF")
    except Exception as e:
        print(f"❌ Erreur lors de l'import du modèle Cotisation: {e}")
        print("   Vérifiez que l'application 'assureur' est dans INSTALLED_APPS")

print("\n=== TEST TERMINÉ ===")