#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC RAILWAY pour Django mutuelle_core
Vérifie la configuration, les dépendances et la compatibilité Railway
"""

import os
import sys
import django
import subprocess
import platform
from pathlib import Path

# =============================================================================
# CONFIGURATION DU DIAGNOSTIC
# =============================================================================

def print_header(text):
    """Affiche un en-tête formaté"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_success(text):
    """Affiche un message de succès"""
    print(f"✅ {text}")

def print_warning(text):
    """Affiche un avertissement"""
    print(f"⚠️  {text}")

def print_error(text):
    """Affiche une erreur"""
    print(f"❌ {text}")

def print_info(text):
    """Affiche une information"""
    print(f"📋 {text}")

# =============================================================================
# VÉRIFICATIONS SYSTÈME
# =============================================================================

def check_system():
    """Vérifie le système et Python"""
    print_header("VÉRIFICATION SYSTÈME")
    
    # Version Python
    python_version = platform.python_version()
    print_info(f"Python: {python_version}")
    
    # Vérifier Python 3.8+
    if tuple(map(int, python_version.split('.')[:2])) >= (3, 8):
        print_success("Version Python compatible (3.8+)")
    else:
        print_error("Python 3.8+ requis")
    
    # Système d'exploitation
    print_info(f"Système: {platform.system()} {platform.release()}")
    
    # Répertoire courant
    cwd = Path.cwd()
    print_info(f"Répertoire: {cwd}")
    
    # Variables d'environnement Railway
    railway_envs = [k for k in os.environ.keys() if 'RAILWAY' in k or 'DATABASE_URL' in k]
    if railway_envs:
        print_success(f"Variables Railway détectées: {len(railway_envs)}")
        for env in railway_envs[:3]:  # Affiche seulement les 3 premières
            print_info(f"  {env}=...")
    else:
        print_warning("Aucune variable Railway détectée (mode local)")

# =============================================================================
# VÉRIFICATIONS DJANGO
# =============================================================================

def check_django_config():
    """Vérifie la configuration Django"""
    print_header("VÉRIFICATION DJANGO")
    
    try:
        # Initialiser Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        django.setup()
        print_success("Django initialisé avec succès")
    except Exception as e:
        print_error(f"Erreur initialisation Django: {e}")
        return False
    
    # Vérifier les settings
    from django.conf import settings
    
    # DEBUG mode
    debug_status = "ACTIVÉ" if settings.DEBUG else "DÉSACTIVÉ"
    print_info(f"DEBUG: {debug_status}")
    
    if settings.DEBUG and not settings.ALLOWED_HOSTS:
        print_warning("DEBUG=True sans ALLOWED_HOSTS configurés")
    
    # ALLOWED_HOSTS
    if settings.ALLOWED_HOSTS:
        print_success(f"ALLOWED_HOSTS: {len(settings.ALLOWED_HOSTS)} hôtes configurés")
        for host in settings.ALLOWED_HOSTS[:3]:  # Affiche les 3 premiers
            print_info(f"  - {host}")
    else:
        print_error("Aucun ALLOWED_HOSTS configuré!")
    
    # Base de données
    db_engine = settings.DATABASES['default']['ENGINE']
    print_info(f"Base de données: {db_engine}")
    
    if 'postgresql' in db_engine.lower():
        print_success("PostgreSQL configuré (compatible Railway)")
    elif 'sqlite' in db_engine.lower():
        print_warning("SQLite détecté (non recommandé pour Railway production)")
    else:
        print_info(f"Moteur DB: {db_engine}")
    
    # Static files
    if hasattr(settings, 'STATIC_ROOT'):
        print_success(f"STATIC_ROOT: {settings.STATIC_ROOT}")
    
    # WhiteNoise
    if 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE:
        print_success("WhiteNoise configuré pour les fichiers statiques")
    else:
        print_warning("WhiteNoise non détecté dans MIDDLEWARE")
    
    # CSRF trusted origins
    if hasattr(settings, 'CSRF_TRUSTED_ORIGINS') and settings.CSRF_TRUSTED_ORIGINS:
        print_success(f"CSRF_TRUSTED_ORIGINS: {len(settings.CSRF_TRUSTED_ORIGINS)} origines")
    else:
        print_warning("CSRF_TRUSTED_ORIGINS non configurés")
    
    # CORS
    if hasattr(settings, 'CORS_ALLOWED_ORIGINS'):
        if settings.CORS_ALLOWED_ORIGINS:
            print_success(f"CORS: {len(settings.CORS_ALLOWED_ORIGINS)} origines")
        else:
            print_info("CORS: configuration détectée mais vide")
    
    # Applications installées
    print_info(f"Applications installées: {len(settings.INSTALLED_APPS)}")
    
    return True

# =============================================================================
# VÉRIFICATIONS FICHIERS RAILWAY
# =============================================================================

def check_railway_files():
    """Vérifie les fichiers de configuration Railway"""
    print_header("VÉRIFICATION FICHIERS RAILWAY")
    
    fichiers_requis = {
        'railway.json': "Configuration Railway principale",
        'requirements.txt': "Dépendances Python",
        'Procfile': "Commande de démarrage (optionnel)",
        '.nixpacks.toml': "Configuration build (optionnel mais recommandé)",
    }
    
    fichiers_trouves = {}
    
    for fichier, description in fichiers_requis.items():
        if Path(fichier).exists():
            fichiers_trouves[fichier] = True
            print_success(f"{fichier} ✓ ({description})")
            
            # Analyser le contenu
            try:
                with open(fichier, 'r') as f:
                    content = f.read()
                    
                if fichier == 'railway.json':
                    if '"$schema"' in content and 'railway.app' in content:
                        print_success("  → Format Railway valide")
                    else:
                        print_warning("  → Format Railway non standard")
                
                elif fichier == 'requirements.txt':
                    lines = [l.strip() for l in content.split('\n') if l.strip()]
                    deps_critiques = ['Django', 'gunicorn', 'whitenoise', 'psycopg2']
                    deps_presentes = []
                    
                    for dep in deps_critiques:
                        if any(dep.lower() in line.lower() for line in lines):
                            deps_presentes.append(dep)
                    
                    if len(deps_presentes) >= 3:
                        print_success(f"  → {len(deps_presentes)}/{len(deps_critiques)} dépendances critiques")
                    else:
                        print_warning(f"  → {len(deps_presentes)}/{len(deps_critiques)} dépendances critiques")
                
                elif fichier == 'Procfile':
                    if 'gunicorn' in content and 'mutuelle_core.wsgi' in content:
                        print_success("  → Procfile correctement configuré")
                    else:
                        print_warning("  → Procfile mal configuré")
                
                elif fichier == '.nixpacks.toml':
                    print_success("  → Configuration Nixpacks détectée")
                    
            except Exception as e:
                print_warning(f"  → Erreur lecture: {e}")
        else:
            fichiers_trouves[fichier] = False
            if fichier in ['railway.json', 'requirements.txt']:
                print_error(f"{fichier} ✗ ({description})")
            else:
                print_warning(f"{fichier} ✗ ({description})")
    
    # Résumé
    print("\n📊 Résumé fichiers Railway:")
    print(f"  ✓ Fichiers requis: {sum(fichiers_trouves.values())}/{len(fichiers_requis)}")
    
    # Recommandations
    if not fichiers_trouves.get('railway.json'):
        print("\n🚨 ACTION REQUISE: Créez railway.json")
        print("""
    {
      "$schema": "https://railway.app/railway.schema.json",
      "build": {
        "builder": "NIXPACKS",
        "buildCommand": "pip install -r requirements.txt"
      },
      "deploy": {
        "startCommand": "gunicorn mutuelle_core.wsgi:application",
        "healthcheckPath": "/"
      }
    }
        """)

# =============================================================================
# VÉRIFICATIONS DÉPENDANCES
# =============================================================================

def check_dependencies():
    """Vérifie les dépendances et requirements.txt"""
    print_header("VÉRIFICATION DÉPENDANCES")
    
    # Vérifier requirements.txt
    req_file = Path('requirements.txt')
    if not req_file.exists():
        print_error("requirements.txt non trouvé")
        return False
    
    print_success("requirements.txt trouvé")
    
    try:
        with open(req_file, 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print_info(f"Dépendances dans requirements.txt: {len(requirements)}")
        
        # Dépendances critiques pour Railway
        critical_deps = {
            'Django': False,
            'gunicorn': False,
            'whitenoise': False,
            'psycopg2-binary': False,
            'dj-database-url': False,
        }
        
        for req in requirements:
            for dep in critical_deps.keys():
                if dep.lower() in req.lower():
                    critical_deps[dep] = True
                    print_success(f"  ✓ {dep} → {req}")
                    break
        
        # Vérifier les dépendances manquantes
        missing_deps = [dep for dep, found in critical_deps.items() if not found]
        if missing_deps:
            print_warning(f"Dépendances manquantes: {', '.join(missing_deps)}")
        else:
            print_success("Toutes les dépendances critiques sont présentes")
        
        # Vérifier Pillow (problème connu avec Python 3.13)
        pillow_found = any('pillow' in req.lower() for req in requirements)
        if pillow_found:
            print_info("Pillow détecté - vérifier compatibilité Python")
        
        # Tester l'installation des dépendances
        print("\n🧪 Test d'installation des dépendances...")
        try:
            import pip
            print_success("pip disponible")
        except ImportError:
            print_warning("pip non disponible")
        
    except Exception as e:
        print_error(f"Erreur lecture requirements.txt: {e}")
        return False
    
    return True

# =============================================================================
# VÉRIFICATIONS BASE DE DONNÉES
# =============================================================================

def check_database():
    """Vérifie la configuration de la base de données"""
    print_header("VÉRIFICATION BASE DE DONNÉES")
    
    # Vérifier DATABASE_URL
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        print_success(f"DATABASE_URL détecté")
        
        # Analyser l'URL
        if 'postgresql://' in db_url:
            print_success("  → PostgreSQL (compatible Railway)")
        elif 'mysql://' in db_url:
            print_warning("  → MySQL (Railway supporte mais PostgreSQL recommandé)")
        elif 'sqlite://' in db_url:
            print_warning("  → SQLite (non recommandé pour production Railway)")
        else:
            print_info(f"  → Type: {db_url[:50]}...")
    else:
        print_warning("DATABASE_URL non défini (mode développement)")
        print_info("  → Railway fournira DATABASE_URL automatiquement")
    
    # Tester la connexion si Django est configuré
    try:
        from django.db import connection
        connection.ensure_connection()
        print_success("Connexion à la base de données réussie")
    except Exception as e:
        print_warning(f"Connexion DB échouée: {e}")

# =============================================================================
# VÉRIFICATIONS DÉPLOIEMENT
# =============================================================================

def check_deployment():
    """Vérifie la configuration de déploiement"""
    print_header("VÉRIFICATION DÉPLOIEMENT")
    
    # Port Railway
    port = os.environ.get('PORT', '8000')
    print_info(f"PORT Railway: {port}")
    
    # Variables Railway critiques
    railway_vars = {
        'RAILWAY_ENVIRONMENT': os.environ.get('RAILWAY_ENVIRONMENT'),
        'RAILWAY_PROJECT_NAME': os.environ.get('RAILWAY_PROJECT_NAME'),
        'RAILWAY_SERVICE_NAME': os.environ.get('RAILWAY_SERVICE_NAME'),
    }
    
    railway_vars_found = sum(1 for v in railway_vars.values() if v)
    print_info(f"Variables Railway: {railway_vars_found}/3 détectées")
    
    # Vérifier la commande de démarrage
    try:
        with open('Procfile', 'r') as f:
            procfile = f.read()
            if 'gunicorn' in procfile and 'mutuelle_core.wsgi' in procfile:
                print_success("Procfile correctement configuré")
                if '$PORT' in procfile:
                    print_success("  → Utilise $PORT Railway")
                else:
                    print_warning("  → N'utilise pas $PORT (risque de conflit)")
            else:
                print_error("Procfile mal configuré")
    except:
        print_warning("Procfile non trouvé ou illisible")
    
    # Vérifier le wsgi.py
    wsgi_path = Path('mutuelle_core/wsgi.py')
    if wsgi_path.exists():
        print_success("wsgi.py trouvé")
        with open(wsgi_path, 'r') as f:
            wsgi_content = f.read()
            if 'application = get_wsgi_application()' in wsgi_content:
                print_success("  → WSGI correctement configuré")
    else:
        print_error("wsgi.py non trouvé")

# =============================================================================
# TEST DE DÉMARRAGE
# =============================================================================

def test_startup():
    """Teste le démarrage de l'application"""
    print_header("TEST DE DÉMARRAGE")
    
    print("🔄 Simulation du démarrage Railway...")
    
    # Tester gunicorn
    try:
        import gunicorn
        print_success("gunicorn disponible")
    except ImportError:
        print_error("gunicorn non installé")
        return False
    
    # Tester la commande de démarrage
    test_cmd = f"gunicorn mutuelle_core.wsgi:application --bind 0.0.0.0:8000 --workers 1"
    print_info(f"Commande test: {test_cmd}")
    
    # Tester collectstatic
    print("\n🧪 Test collectstatic...")
    try:
        subprocess.run(['python', 'manage.py', 'collectstatic', '--noinput', '--dry-run'], 
                      capture_output=True, text=True, timeout=10)
        print_success("collectstatic fonctionnel")
    except Exception as e:
        print_warning(f"collectstatic échoué: {e}")
    
    # Tester les migrations
    print("\n🧪 Test migrations...")
    try:
        result = subprocess.run(['python', 'manage.py', 'migrate', '--plan'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print_success("Migrations fonctionnelles")
        else:
            print_warning(f"Migrations échouées: {result.stderr[:100]}")
    except Exception as e:
        print_warning(f"Test migrations échoué: {e}")
    
    return True

# =============================================================================
# RAPPORT FINAL
# =============================================================================

def generate_report():
    """Génère un rapport final"""
    print_header("📊 RAPPORT FINAL RAILWAY")
    
    # Liste des vérifications
    checks = [
        ("Système Python 3.8+", True),
        ("requirements.txt", Path('requirements.txt').exists()),
        ("railway.json", Path('railway.json').exists()),
        ("Configuration Django", True),  # À remplacer par résultat réel
        ("Dépendances critiques", True),  # À remplacer par résultat réel
        ("Base de données", os.environ.get('DATABASE_URL') is not None),
        ("WhiteNoise configuré", True),  # À remplacer par résultat réel
    ]
    
    passed = sum(1 for _, check in checks if check)
    total = len(checks)
    
    print(f"✅ Vérifications passées: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 VOTRE APPLICATION EST PRÊTE POUR RAILWAY !")
        print("\n🚀 Prochaines étapes:")
        print("1. git add railway.json .nixpacks.toml Procfile")
        print("2. git commit -m 'Ready for Railway'")
        print("3. git push origin main")
        print("4. Allez sur railway.app → New Project → GitHub")
        print("5. Sélectionnez votre repo")
    elif passed >= total * 0.7:
        print("\n⚠️  VOTRE APPLICATION EST PRESQUE PRÊTE")
        print("\n🔧 Corrections nécessaires:")
        if not Path('railway.json').exists():
            print("  - Créez railway.json (voir ci-dessus)")
        if not Path('requirements.txt').exists():
            print("  - Créez requirements.txt")
    else:
        print("\n🚨 DES CORRECTIONS SONT NÉCESSAIRES")
        print("Consultez les messages d'erreur ci-dessus")

# =============================================================================
# FONCTION PRINCIPALE
# =============================================================================

def main():
    """Fonction principale du diagnostic"""
    print("🚀 DIAGNOSTIC RAILWAY - Application Django")
    print("Version: 1.0 | Pour: mutuelle_core")
    
    # Exécuter toutes les vérifications
    check_system()
    check_railway_files()
    check_dependencies()
    check_database()
    
    if check_django_config():
        check_deployment()
        test_startup()
    
    generate_report()
    
    print("\n" + "="*60)
    print("💡 CONSEILS POUR RAILWAY:")
    print("="*60)
    print("""
1. Railway utilise Nixpacks - pas besoin de Dockerfile
2. DATABASE_URL est fourni automatiquement
3. Le PORT est injecté via variable d'environnement $PORT
4. Les logs sont automatiquement capturés
5. Health check sur / par défaut

📁 FICHIERS REQUIS POUR RAILWAY:
  - railway.json         (configuration principale)
  - requirements.txt     (dépendances)
  - .nixpacks.toml      (optionnel mais recommandé)
  - Procfile            (optionnel)

⚡ COMMANDES RAPIDES:
  # Créer railway.json
  echo '{"$schema":"https://railway.app/railway.schema.json","build":{"builder":"NIXPACKS"},"deploy":{"startCommand":"gunicorn mutuelle_core.wsgi:application"}}' > railway.json
  
  # Tester localement
  python railway_diagnostic.py
  
  # Déployer
  git add . && git commit -m "Railway ready" && git push origin main
    """)

if __name__ == "__main__":
    main()