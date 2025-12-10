# deploy_check.py
#!/usr/bin/env python3
"""
Vérification finale avant déploiement Render
"""

import requests
import time
import sys

def check_deployment():
    """Teste l'application localement"""
    print("🧪 TEST DE DÉPLOIEMENT LOCAL")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    try:
        # Test 1: Health check
        print("1. Testing health check...")
        try:
            response = requests.get('http://localhost:8000/', timeout=5)
            if response.status_code in [200, 301, 302]:
                print(f"✅ Health check: {response.status_code} (OK)")
                tests_passed += 1
            else:
                print(f"⚠️  Health check: {response.status_code} (attendu 200, 301 ou 302)")
        except requests.exceptions.Timeout:
            print("❌ Health check: Timeout après 5s")
        except requests.exceptions.ConnectionError:
            print("❌ Health check: Impossible de se connecter au serveur")
        
        # Test 2: Static files
        print("\n2. Testing static files...")
        try:
            response = requests.get('http://localhost:8000/static/css/style.css', timeout=5)
            if response.status_code in [200, 304]:
                print(f"✅ Static files: {response.status_code} (OK)")
                tests_passed += 1
            else:
                print(f"⚠️  Static files: {response.status_code} (attendu 200 ou 304)")
        except requests.exceptions.Timeout:
            print("❌ Static files: Timeout après 5s")
        except requests.exceptions.ConnectionError:
            print("❌ Static files: Impossible de se connecter au serveur")
        
        # Test 3: Admin page
        print("\n3. Testing admin page...")
        try:
            response = requests.get('http://localhost:8000/admin/', timeout=5, allow_redirects=False)
            if response.status_code in [200, 301, 302]:
                print(f"✅ Admin page: {response.status_code} (redirection normale)")
                tests_passed += 1
            else:
                print(f"⚠️  Admin page: {response.status_code} (attendu 200, 301 ou 302)")
        except requests.exceptions.Timeout:
            print("❌ Admin page: Timeout après 5s")
        except requests.exceptions.ConnectionError:
            print("❌ Admin page: Impossible de se connecter au serveur")
        
        # Résumé
        print("\n" + "=" * 60)
        print(f"📊 RÉSULTAT: {tests_passed}/{total_tests} tests réussis")
        
        if tests_passed == total_tests:
            print("🎉 EXCELLENT! L'application est prête pour le déploiement!")
        elif tests_passed >= 1:
            print("⚠️  L'application répond, mais certains tests ont échoué")
            print("   Cela peut être normal si certains fichiers n'existent pas encore")
        else:
            print("❌ L'application ne répond pas. Vérifiez que le serveur est démarré")
        
        print("\n📋 ÉTAPES POUR DÉPLOYER SUR RENDER:")
        print("1. Démarrer le serveur localement: ./start_prod.sh")
        print("2. Vérifier qu'il répond sur http://localhost:8000/")
        print("3. Pousser sur GitHub: git push origin main")
        print("4. Aller sur https://render.com")
        print("5. Créer un nouveau 'Web Service'")
        print("6. Connecter votre repository GitHub")
        print("7. Render utilisera automatiquement render.yaml")
        print("8. Ajouter les variables d'environnement sur Render:")
        print("   • DEBUG=False")
        print("   • DJANGO_ENV=production")
        print("   • SECRET_KEY=votre-clé-secrète")
        print("   • ALLOWED_HOSTS=.onrender.com,localhost")
        
        return tests_passed == total_tests
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrompu par l'utilisateur")
        return False
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return False

if __name__ == "__main__":
    print("\n⚠️  IMPORTANT: Assurez-vous que le serveur est démarré avec ./start_prod.sh")
    print("   Ouvrez un autre terminal et exécutez: ./start_prod.sh\n")
    
    try:
        success = check_deployment()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Interruption")
        sys.exit(130)