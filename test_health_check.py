#!/usr/bin/env python
"""
Test de la health check pour Render
"""
import requests
import sys
import subprocess
import time
import threading

def test_health_check():
    """Tester la health check localement"""
    print("🧪 TEST HEALTH CHECK POUR RENDER")
    print("="*50)
    
    # Démarrer le serveur en arrière-plan
    print("1. Démarrage du serveur Django...")
    server_process = subprocess.Popen(
        ['python', 'manage.py', 'runserver', '--noreload'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Attendre que le serveur démarre
    print("2. Attente du démarrage du serveur...")
    time.sleep(5)
    
    try:
        # Tester la health check
        print("3. Test de la route /health/...")
        response = requests.get('http://localhost:8000/health/', timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Contenu: {response.text[:100]}")
        
        if response.status_code == 200 and 'OK' in response.text:
            print("✅ Health check fonctionnelle!")
        else:
            print("❌ Health check échouée")
            return False
        
        # Tester d'autres routes importantes
        print("\n4. Test des routes principales...")
        routes_to_test = [
            ('/', 'Page d\'accueil'),
            ('/admin/', 'Admin (login required)'),
            ('/api/', 'API'),
        ]
        
        for route, description in routes_to_test:
            try:
                resp = requests.get(f'http://localhost:8000{route}', timeout=5)
                print(f"   {route} ({description}): HTTP {resp.status_code}")
            except Exception as e:
                print(f"   {route}: ❌ {str(e)[:50]}")
        
        return True
        
    except requests.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
        
    finally:
        # Arrêter le serveur
        print("\n5. Arrêt du serveur...")
        server_process.terminate()
        server_process.wait()
        print("✅ Serveur arrêté")

def quick_deploy_check():
    """Vérification rapide pour déploiement"""
    print("\n⚡ VÉRIFICATION RAPIDE POUR RENDER")
    print("="*50)
    
    checks = []
    
    # 1. Fichiers obligatoires
    required = ['render.yaml', 'build.sh', 'Procfile', 'requirements.txt']
    for file in required:
        if os.path.exists(file):
            print(f"✅ {file}")
            checks.append(True)
        else:
            print(f"❌ {file} MANQUANT")
            checks.append(False)
    
    # 2. Permissions build.sh
    if os.path.exists('build.sh'):
        if os.access('build.sh', os.X_OK):
            print("✅ build.sh exécutable")
            checks.append(True)
        else:
            print("⚠️  build.sh non exécutable (chmod +x build.sh)")
            checks.append(False)
    
    # 3. Vérifier requirements.txt
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            deps = f.read()
            required_deps = ['gunicorn', 'whitenoise', 'psycopg2']
            for dep in required_deps:
                if dep in deps.lower():
                    print(f"✅ {dep}")
                    checks.append(True)
                else:
                    print(f"⚠️  {dep} manquant")
                    checks.append(False)
    
    # Résumé
    success_rate = sum(checks) / len(checks) * 100
    print(f"\n📊 Résumé: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("✅ Prêt pour le déploiement!")
    else:
        print("❌ Corrigez les problèmes avant le déploiement")
    
    return success_rate >= 80

if __name__ == '__main__':
    import os
    
    # Vérifier qu'on est dans le bon répertoire
    if not os.path.exists('manage.py'):
        print("Exécutez depuis la racine du projet Django")
        sys.exit(1)
    
    # Exécuter les tests
    health_ok = test_health_check()
    deploy_ok = quick_deploy_check()
    
    if health_ok and deploy_ok:
        print("\n🎉 TOUS LES TESTS ONT RÉUSSI!")
        print("Votre application est prête pour Render.com 🚀")
        sys.exit(0)
    else:
        print("\n⚠️  DES PROBLÈMES ONT ÉTÉ DÉTECTÉS")
        sys.exit(1)