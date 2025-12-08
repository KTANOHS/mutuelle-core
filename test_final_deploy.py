# test_final_deploy.py
import os
import sys
import subprocess

def run_test():
    print("🧪 TEST FINAL POUR DÉPLOIEMENT RENDER")
    print("=" * 60)
    
    # 1. Vérifier l'environnement
    print("\n1. Configuration de l'environnement...")
    os.environ['DJANGO_ENV'] = 'production'
    os.environ['SECRET_KEY'] = 'test-secret-for-render-123456'
    os.environ['DEBUG'] = 'False'
    
    # 2. Tester les imports
    print("\n2. Vérification des imports...")
    try:
        import django
        import gunicorn
        import dj_database_url
        import whitenoise
        print("✅ Tous les imports critiques fonctionnent")
    except ImportError as e:
        print(f"❌ Import manquant: {e}")
        return False
    
    # 3. Tester Django en mode production
    print("\n3. Test Django production...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        import django
        django.setup()
        
        from django.conf import settings
        print(f"✅ Django configuré avec succès")
        print(f"   • Environnement: {os.environ.get('DJANGO_ENV')}")
        print(f"   • DEBUG: {settings.DEBUG}")
        print(f"   • STATIC_ROOT: {settings.STATIC_ROOT}")
        
        # Vérifier que DEBUG est False en production
        if settings.DEBUG:
            print("❌ ATTENTION: DEBUG=True en production! À corriger.")
            return False
            
    except Exception as e:
        print(f"❌ Erreur Django: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 4. Tester collectstatic
    print("\n4. Test collectstatic...")
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'collectstatic', '--dry-run', '--noinput'])
        print("✅ collectstatic fonctionne")
    except Exception as e:
        print(f"⚠ collectstatic avertissement: {str(e)[:100]}...")
    
    # 5. Vérifier les fichiers Render
    print("\n5. Fichiers pour Render...")
    render_files = ['runtime.txt', 'Procfile', 'build.sh', 'render.yaml', 'requirements.txt']
    all_ok = True
    for file in render_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size} bytes)")
        else:
            print(f"❌ {file} manquant")
            all_ok = False
    
    # 6. Résumé
    print("\n" + "=" * 60)
    print("🎯 RÉSUMÉ DU TEST")
    print("=" * 60)
    
    if all_ok:
        print("✅ Tous les tests sont PASSÉS !")
        print("\n🎉 Votre application est PRÊTE pour le déploiement sur Render !")
        print("\n📋 Étapes suivantes:")
        print("1. git add .")
        print("2. git commit -m 'Prêt pour déploiement Render'")
        print("3. git push origin main")
        print("4. Allez sur https://render.com et déployez")
        return True
    else:
        print("❌ Certains tests ont ÉCHOUÉ")
        print("\n🔧 Problèmes à résoudre:")
        if not os.path.exists('runtime.txt'):
            print("   • Créez runtime.txt: echo 'python-3.11.10' > runtime.txt")
        return False

if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)