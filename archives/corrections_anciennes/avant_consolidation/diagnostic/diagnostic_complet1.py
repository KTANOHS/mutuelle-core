import requests
import json
import subprocess
import sys
import os
import time
from urllib.error import URLError

def check_server_status():
    """Vérifie si le serveur Django est en cours d'exécution"""
    print("🔍 Vérification du serveur Django...")
    
    ports_to_check = [8000, 8080, 8001, 9000]
    
    for port in ports_to_check:
        url = f"http://127.0.0.1:{port}"
        try:
            response = requests.get(url, timeout=3)
            print(f"   ✅ Serveur trouvé sur le port {port}")
            print(f"      Statut: {response.status_code}")
            print(f"      Réponse: {response.text[:100]}...")
            return port
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Port {port}: Aucun serveur")
        except Exception as e:
            print(f"   ⚠️  Port {port}: Erreur - {e}")
    
    return None

def check_django_process():
    """Vérifie les processus Django en cours d'exécution"""
    print("\n🔍 Recherche de processus Django...")
    
    try:
        # Pour Mac/Linux
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        django_processes = [line for line in result.stdout.split('\n') if 'python' in line and ('manage.py' in line or 'django' in line.lower())]
        
        if django_processes:
            print("   ✅ Processus Django trouvés:")
            for proc in django_processes[:3]:  # Afficher seulement les 3 premiers
                print(f"      - {proc[:80]}")
        else:
            print("   ❌ Aucun processus Django trouvé")
            
    except Exception as e:
        print(f"   ⚠️  Erreur lors de la recherche des processus: {e}")

def check_database():
    """Vérifie l'état de la base de données"""
    print("\n🔍 Vérification de la base de données...")
    
    try:
        # Essayer de lancer un check de migration
        result = subprocess.run(
            ['python', 'manage.py', 'check', '--database', 'default'],
            capture_output=True,
            text=True,
            cwd=os.getcwd()  # Utiliser le répertoire courant
        )
        
        if result.returncode == 0:
            print("   ✅ Base de données: OK")
        else:
            print(f"   ❌ Problème de base de données:")
            print(f"      {result.stderr}")
            
    except FileNotFoundError:
        print("   ⚠️  Fichier manage.py non trouvé dans le répertoire courant")
    except Exception as e:
        print(f"   ⚠️  Erreur: {e}")

def start_test_server():
    """Propose de démarrer le serveur de test"""
    print("\n🚀 Voulez-vous démarrer le serveur Django?")
    print("   Options:")
    print("   1. Démarrer le serveur de développement (python manage.py runserver)")
    print("   2. Vérifier les migrations")
    print("   3. Quitter")
    
    choice = input("\n   Votre choix (1-3): ")
    
    if choice == "1":
        print("\n   Démarrage du serveur...")
        try:
            # Démarrer le serveur en arrière-plan
            subprocess.Popen(
                ['python', 'manage.py', 'runserver'],
                cwd=os.getcwd(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("   ✅ Serveur démarré. Patientez 5 secondes...")
            time.sleep(5)
            return True
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            return False
            
    elif choice == "2":
        print("\n   Vérification des migrations...")
        try:
            result = subprocess.run(
                ['python', 'manage.py', 'migrate', '--check'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            if result.returncode == 0:
                print("   ✅ Toutes les migrations sont appliquées")
            else:
                print("   ❌ Migrations en attente:")
                print(result.stdout)
                print("\n   Appliquer les migrations? (o/n): ")
                if input().lower() == 'o':
                    subprocess.run(['python', 'manage.py', 'migrate'], cwd=os.getcwd())
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    return False

def run_api_test(port=8000):
    """Teste l'API une fois le serveur démarré"""
    BASE_URL = f"http://127.0.0.1:{port}"
    CONVERSATION_ID = 5
    
    print(f"\n📊 Test de l'API sur {BASE_URL}")
    
    endpoints = [
        ("/", "Page d'accueil"),
        ("/admin/", "Admin Django"),
        (f"/communication/conversations/{CONVERSATION_ID}/", f"Conversation {CONVERSATION_ID}"),
        (f"/communication/conversations/{CONVERSATION_ID}/messages/", f"Messages conversation {CONVERSATION_ID}")
    ]
    
    for endpoint, description in endpoints:
        print(f"\n   Testing {description}...")
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            print(f"      ✅ Code: {response.status_code}")
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'application/json' in content_type:
                    try:
                        data = response.json()
                        if endpoint == f"/communication/conversations/{CONVERSATION_ID}/":
                            print(f"      📝 Titre: {data.get('title', 'N/A')}")
                            print(f"      👤 Utilisateur: {data.get('user', 'N/A')}")
                        elif endpoint == f"/communication/conversations/{CONVERSATION_ID}/messages/":
                            if isinstance(data, list):
                                print(f"      📨 Messages: {len(data)}")
                                if data:
                                    for msg in data[-3:]:  # Afficher les 3 derniers
                                        msg_id = msg.get('id', 'N/A')
                                        content = msg.get('content', '')[:50]
                                        print(f"         - ID {msg_id}: {content}")
                    except json.JSONDecodeError:
                        print(f"      ⚠️  Réponse non-JSON: {response.text[:100]}")
                else:
                    print(f"      📄 Content-Type: {content_type}")
            elif response.status_code == 404:
                print(f"      ❌ Endpoint non trouvé")
            elif response.status_code == 403:
                print(f"      🔒 Accès refusé (authentification requise)")
            elif response.status_code == 500:
                print(f"      💥 Erreur serveur interne")
                
        except requests.exceptions.ConnectionError:
            print(f"      ❌ Impossible de se connecter")
            break
        except Exception as e:
            print(f"      ⚠️  Erreur: {e}")

def main():
    print("=" * 60)
    print("DIAGNOSTIC COMPLET DJANGO")
    print("=" * 60)
    
    # Vérifier l'environnement
    print(f"\n📁 Répertoire courant: {os.getcwd()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    
    # Vérifier si nous sommes dans un environnement virtuel
    if 'VIRTUAL_ENV' in os.environ:
        print(f"🎯 Environnement virtuel: {os.environ['VIRTUAL_ENV']}")
    else:
        print("⚠️  Pas d'environnement virtuel détecté")
    
    # Vérifier les processus Django
    check_django_process()
    
    # Vérifier la base de données
    check_database()
    
    # Vérifier le serveur
    port = check_server_status()
    
    if port is None:
        print("\n❌ Aucun serveur Django n'est en cours d'exécution")
        
        # Proposer de démarrer le serveur
        if start_test_server():
            port = 8000  # Port par défaut
            time.sleep(3)  # Donner du temps au serveur pour démarrer
    else:
        print(f"\n✅ Serveur trouvé sur le port {port}")
    
    # Tester l'API si un port est disponible
    if port:
        run_api_test(port)
    else:
        print("\n💡 Conseils de dépannage:")
        print("   1. Démarrer le serveur: python manage.py runserver")
        print("   2. Vérifier le port: python manage.py runserver 8001")
        print("   3. Vérifier les erreurs: python manage.py check")
        print("   4. Appliquer les migrations: python manage.py migrate")
    
    print("\n" + "=" * 60)
    print("DIAGNOSTIC TERMINÉ")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Diagnostic interrompu")
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")