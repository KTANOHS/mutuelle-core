"""
SCRIPT DE DIAGNOSTIC ASSUREUR - Mutuelle Core
Ce script vérifie la configuration de l'environnement Django pour l'assureur
"""

import os
import sys
import django
from pathlib import Path
from datetime import datetime

# Ajouter le chemin du projet Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur lors du chargement de Django: {e}")
    sys.exit(1)

from django.conf import settings

def diagnostic_assureur():
    """Exécute un diagnostic complet de la configuration assureur"""
    
    print("🔍 DIAGNOSTIC ASSUREUR - Mutuelle Core")
    print("=" * 50)
    print(f"Date du diagnostic: {datetime.now()}")
    print(f"Répertoire de base: {BASE_DIR}")
    print(f"Mode DEBUG: {settings.DEBUG}")
    print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print()
    
    # 1. Vérifier les applications installées
    print("📦 1. VÉRIFICATION DES APPLICATIONS")
    print("-" * 30)
    
    apps_assureur = [
        'assureur',
        'agents',
        'membres',
        'inscription',
        'paiements',
        'soins',
        'notifications',
        'communication',
        'ia_detection',
        'scoring',
        'relances',
        'dashboard'
    ]
    
    for app in apps_assureur:
        if app in settings.INSTALLED_APPS:
            print(f"✅ {app} - Installé")
        else:
            print(f"❌ {app} - NON installé")
    
    print()
    
    # 2. Vérifier les templates
    print("📝 2. VÉRIFICATION DES TEMPLATES")
    print("-" * 30)
    
    templates_dirs = []
    for template in settings.TEMPLATES:
        if 'DIRS' in template:
            templates_dirs.extend(template['DIRS'])
    
    for dir_path in templates_dirs:
        if os.path.exists(dir_path):
            print(f"✅ Répertoire templates trouvé: {dir_path}")
            # Compter les fichiers templates
            templates_files = []
            for root, dirs, files in os.walk(dir_path):
                templates_files.extend([os.path.join(root, f) for f in files if f.endswith('.html')])
            
            if templates_files:
                print(f"   → {len(templates_files)} fichiers templates trouvés")
        else:
            print(f"⚠️  Répertoire templates non trouvé: {dir_path}")
    
    print()
    
    # 3. Vérifier les fichiers statiques
    print("🎨 3. VÉRIFICATION DES FICHIERS STATIQUES")
    print("-" * 30)
    
    for static_dir in settings.STATICFILES_DIRS:
        if os.path.exists(static_dir):
            print(f"✅ Répertoire statique trouvé: {static_dir}")
            # Compter les fichiers
            static_files = []
            for root, dirs, files in os.walk(static_dir):
                static_files.extend(files)
            
            if static_files:
                print(f"   → {len(static_files)} fichiers statiques trouvés")
        else:
            print(f"⚠️  Répertoire statique non trouvé: {static_dir}")
    
    print(f"URL statique: {settings.STATIC_URL}")
    print(f"Racine statique: {settings.STATIC_ROOT}")
    
    print()
    
    # 4. Vérifier la base de données
    print("🗄️  4. VÉRIFICATION DE LA BASE DE DONNÉES")
    print("-" * 30)
    
    db_config = settings.DATABASES.get('default', {})
    print(f"Type de base: {db_config.get('ENGINE', 'Non spécifié')}")
    print(f"Nom de la base: {db_config.get('NAME', 'Non spécifié')}")
    
    # Vérifier si la base de données existe
    db_path = db_config.get('NAME')
    if db_path:
        if os.path.exists(db_path):
            db_size = os.path.getsize(db_path)
            print(f"✅ Base de données trouvée: {db_path}")
            print(f"   → Taille: {db_size / 1024 / 1024:.2f} MB")
        else:
            print(f"⚠️  Base de données non trouvée: {db_path}")
    
    print()
    
    # 5. Vérifier la configuration assureur
    print("🏥 5. CONFIGURATION ASSUREUR")
    print("-" * 30)
    
    mutuelle_config = getattr(settings, 'MUTUELLE_CONFIG', {})
    
    if mutuelle_config:
        print("✅ Configuration mutuelle chargée")
        for key, value in mutuelle_config.items():
            print(f"   {key}: {value}")
    else:
        print("❌ Configuration mutuelle NON chargée")
    
    print()
    
    # 6. Vérifier la sécurité
    print("🔒 6. VÉRIFICATION DE SÉCURITÉ")
    print("-" * 30)
    
    if settings.DEBUG:
        print("⚠️  ATTENTION: DEBUG est activé (désactiver en production)")
    else:
        print("✅ DEBUG est désactivé")
    
    print(f"SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")
    print(f"CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
    
    if settings.DEBUG and (settings.SESSION_COOKIE_SECURE or settings.CSRF_COOKIE_SECURE):
        print("⚠️  ATTENTION: Cookies sécurisés activés en mode DEBUG")
    
    print()
    
    # 7. Vérifier les URL de redirection
    print("🔄 7. URLS DE REDIRECTION")
    print("-" * 30)
    
    print(f"LOGIN_URL: {settings.LOGIN_URL}")
    print(f"LOGIN_REDIRECT_URL: {settings.LOGIN_REDIRECT_URL}")
    print(f"LOGOUT_REDIRECT_URL: {settings.LOGOUT_REDIRECT_URL}")
    
    print()
    
    # 8. Vérifier les logs
    print("📋 8. VÉRIFICATION DES LOGS")
    print("-" * 30)
    
    logs_dir = os.path.join(BASE_DIR, 'logs')
    if os.path.exists(logs_dir):
        print(f"✅ Répertoire logs trouvé: {logs_dir}")
        
        log_files = os.listdir(logs_dir)
        for log_file in log_files:
            log_path = os.path.join(logs_dir, log_file)
            if os.path.isfile(log_path):
                size = os.path.getsize(log_path)
                modified = datetime.fromtimestamp(os.path.getmtime(log_path))
                print(f"   📄 {log_file}: {size / 1024:.1f} KB, modifié: {modified}")
    else:
        print(f"⚠️  Répertoire logs non trouvé: {logs_dir}")
        print("   Création du répertoire...")
        try:
            os.makedirs(logs_dir, exist_ok=True)
            print("   ✅ Répertoire logs créé")
        except Exception as e:
            print(f"   ❌ Erreur lors de la création: {e}")
    
    print()
    
    # 9. Vérifier les dépendances
    print("📚 9. VÉRIFICATION DES DÉPENDANCES")
    print("-" * 30)
    
    try:
        import rest_framework
        print(f"✅ Django REST Framework: {rest_framework.__version__}")
    except ImportError:
        print("❌ Django REST Framework non installé")
    
    try:
        import channels
        print(f"✅ Django Channels: {channels.__version__}")
    except ImportError:
        print("❌ Django Channels non installé")
    
    try:
        import crispy_forms
        print(f"✅ Django Crispy Forms: {crispy_forms.__version__}")
    except (ImportError, AttributeError):
        print("✅ Django Crispy Forms installé")
    
    print()
    
    # 10. Tester l'import des modèles
    print("🧪 10. TEST DES MODÈLES ASSUREUR")
    print("-" * 30)
    
    try:
        from assureur.models import Assureur
        print("✅ Modèle Assureur importé avec succès")
    except Exception as e:
        print(f"❌ Erreur import modèle Assureur: {e}")
    
    try:
        from agents.models import Agent
        print("✅ Modèle Agent importé avec succès")
    except Exception as e:
        print(f"❌ Erreur import modèle Agent: {e}")
    
    try:
        from membres.models import Membre
        print("✅ Modèle Membre importé avec succès")
    except Exception as e:
        print(f"❌ Erreur import modèle Membre: {e}")
    
    print()
    print("=" * 50)
    print("✅ DIAGNOSTIC TERMINÉ")
    print("=" * 50)
    
    # Résumé
    print("\n📊 RÉSUMÉ:")
    print("- Configuration Django: OK" if settings.configured else "❌ Problème de configuration")
    print(f"- Applications assureur: {len([app for app in apps_assureur if app in settings.INSTALLED_APPS])}/{len(apps_assureur)} installées")
    print(f"- Base de données: {'OK' if db_path and os.path.exists(db_path) else 'Vérifier'}")
    print(f"- Mode: {'DEVELOPPEMENT' if settings.DEBUG else 'PRODUCTION'}")

def verifier_urls():
    """Vérifie la configuration des URLs"""
    print("\n🌐 VÉRIFICATION DES URLS")
    print("-" * 30)
    
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        
        # Lister les URLs de l'assureur
        print("URLs disponibles pour l'assureur:")
        
        url_patterns = []
        for pattern in resolver.url_patterns:
            # Vérifier les patterns d'URL
            if hasattr(pattern, 'pattern'):
                url_str = str(pattern.pattern)
                if any(keyword in url_str.lower() for keyword in ['assureur', 'agent', 'membre', 'dashboard']):
                    url_patterns.append(url_str)
        
        if url_patterns:
            for url in sorted(set(url_patterns)):
                print(f"  {url}")
        else:
            print("  Aucune URL spécifique assureur trouvée")
            
    except Exception as e:
        print(f"Erreur lors de la vérification des URLs: {e}")

if __name__ == "__main__":
    diagnostic_assureur()
    verifier_urls()
    
    # Suggestions
    print("\n💡 SUGGESTIONS:")
    if settings.DEBUG:
        print("1. Pensez à désactiver DEBUG en production")
        print("2. Configurez une SECRET_KEY forte")
    
    if 'sqlite3' in str(settings.DATABASES['default'].get('ENGINE', '')):
        print("3. Pour la production, utilisez PostgreSQL ou MySQL au lieu de SQLite")
    
    print("4. Vérifiez la configuration SMTP pour les emails")
    print("5. Configurez les backups automatiques de la base de données")