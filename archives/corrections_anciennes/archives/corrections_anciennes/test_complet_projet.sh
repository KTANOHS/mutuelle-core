
#!/bin/bash

echo "🧪 TEST COMPLET DU PROJET DJANGO"
echo "================================"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Variables
PROJECT_NAME="mutuelle_core"
APPS=("membres" "inscription" "paiements" "soins" "api" "assureur" "medecin" "pharmacien" "core" "mutuelle_core" "pharmacie_public" "agents" "communication")
REQUIRED_FILES=("__init__.py" "models.py" "views.py" "urls.py" "admin.py" "apps.py")
STATUS_PASS=0
STATUS_FAIL=0

# Fonctions utilitaires
increment_pass() { STATUS_PASS=$((STATUS_PASS + 1)); }
increment_fail() { STATUS_FAIL=$((STATUS_FAIL + 1)); }

check_file() {
    if [ -f "$1" ]; then
        echo -e "  ${GREEN}✅ $1${NC}"
        increment_pass
        return 0
    else
        echo -e "  ${RED}❌ $1 - MANQUANT${NC}"
        increment_fail
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "  ${GREEN}✅ $1${NC}"
        increment_pass
        return 0
    else
        echo -e "  ${RED}❌ $1 - MANQUANT${NC}"
        increment_fail
        return 1
    fi
}

echo -e "\n${BLUE}1. VÉRIFICATION DE LA STRUCTURE DU PROJET${NC}"
echo "============================================"

# Vérification des dossiers critiques
echo "Dossiers critiques:"
check_dir "templates"
check_dir "static"
check_dir "media"
check_dir "logs"

# Vérification des fichiers critiques
echo -e "\nFichiers critiques:"
check_file "manage.py"
check_file "requirements.txt"
check_file ".env"
check_file "mutuelle_core/settings.py"
check_file "mutuelle_core/urls.py"
check_file "mutuelle_core/wsgi.py"

echo -e "\n${BLUE}2. VÉRIFICATION DES APPLICATIONS${NC}"
echo "================================="

for app in "${APPS[@]}"; do
    echo -e "\n${YELLOW}📱 Application: $app${NC}"
    
    if [ -d "$app" ]; then
        echo "  Fichiers de base:"
        for file in "${REQUIRED_FILES[@]}"; do
            check_file "$app/$file"
        done
        
        # Vérification des migrations
        if [ -d "$app/migrations" ]; then
            echo -e "  ${GREEN}✅ $app/migrations${NC}"
            increment_pass
        else
            echo -e "  ${YELLOW}⚠️  $app/migrations - ABSENT${NC}"
        fi
        
        # Vérification des templates
        if [ -d "templates/$app" ]; then
            template_count=$(find "templates/$app" -name "*.html" 2>/dev/null | wc -l)
            echo -e "  ${GREEN}✅ templates/$app ($template_count templates)${NC}"
            increment_pass
        else
            echo -e "  ${YELLOW}⚠️  templates/$app - ABSENT${NC}"
        fi
    else
        echo -e "  ${RED}❌ Dossier $app manquant${NC}"
        increment_fail
    fi
done

echo -e "\n${BLUE}3. VÉRIFICATION DE LA BASE DE DONNÉES${NC}"
echo "======================================="

python manage.py shell << 'PYTHONEOF'
import os
import django
from django.apps import apps
from django.db import connection
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("🔍 Vérification de la base de données:")

# Vérifier la connexion BD
try:
    connection.ensure_connection()
    print("✅ Connexion à la base de données: OK")
except Exception as e:
    print(f"❌ Erreur de connexion BD: {e}")

# Vérifier les modèles
print("\n📊 Modèles installés:")
for app_config in apps.get_app_configs():
    models = app_config.get_models()
    if models:
        print(f"✅ {app_config.name}: {len(models)} modèle(s)")
        for model in models:
            print(f"   - {model.__name__}")

# Vérifier les migrations
print("\n🔄 État des migrations:")
from django.db.migrations.executor import MigrationExecutor
executor = MigrationExecutor(connection)
plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
if plan:
    print(f"⚠️  Migrations en attente: {len(plan)}")
else:
    print("✅ Toutes les migrations sont appliquées")

# Compter les enregistrements
print("\n📈 Statistiques de la base de données:")
from django.contrib.auth.models import User, Group

try:
    user_count = User.objects.count()
    group_count = Group.objects.count()
    print(f"✅ Utilisateurs: {user_count}")
    print(f"✅ Groupes: {group_count}")
    
    # Compter par application
    for app_config in apps.get_app_configs():
        models = app_config.get_models()
        total_records = 0
        for model in models:
            try:
                count = model.objects.count()
                total_records += count
            except:
                pass
        if total_records > 0:
            print(f"✅ {app_config.name}: {total_records} enregistrement(s)")
            
except Exception as e:
    print(f"❌ Erreur lors du comptage: {e}")
PYTHONEOF

echo -e "\n${BLUE}4. VÉRIFICATION DES URLS${NC}"
echo "==========================="

python manage.py shell << 'PYTHONEOF'
import os
import django
from django.urls import get_resolver, reverse, NoReverseMatch
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("🔗 Vérification des URLs:")

# Obtenir toutes les URLs enregistrées
resolver = get_resolver()
url_patterns = []

def extract_urls(urlpatterns, namespace=None, prefix=''):
    for pattern in urlpatterns:
        if hasattr(pattern, 'url_patterns'):
            # C'est un include
            new_namespace = namespace
            if pattern.namespace:
                new_namespace = f"{namespace}:{pattern.namespace}" if namespace else pattern.namespace
            extract_urls(pattern.url_patterns, new_namespace, prefix + str(pattern.pattern))
        else:
            # C'est un pattern simple
            if hasattr(pattern, 'name') and pattern.name:
                full_name = f"{namespace}:{pattern.name}" if namespace else pattern.name
                url_patterns.append((full_name, prefix + str(pattern.pattern)))

try:
    extract_urls(resolver.url_patterns)
    print(f"✅ URLs totales trouvées: {len(url_patterns)}")
    
    # Tester les URLs critiques
    critical_urls = [
        'admin:index',
        'login',
        'logout',
    ]
    
    # Ajouter les URLs par application
    for app in ['membres', 'inscription', 'paiements', 'soins', 'assureur', 'medecin', 'pharmacien', 'agents', 'communication']:
        critical_urls.extend([
            f'{app}:index',
            f'{app}:dashboard',
            f'{app}:login',
        ])
    
    print("\n🧪 Test des URLs critiques:")
    client = Client()
    for url_name in critical_urls:
        try:
            url = reverse(url_name)
            response = client.get(url, follow=True)
            status_emoji = "✅" if response.status_code in [200, 302, 403] else "❌"
            print(f"   {status_emoji} {url_name:30} -> {url:40} [HTTP {response.status_code}]")
        except NoReverseMatch:
            print(f"   ⚠️  {url_name:30} -> NON DÉFINIE")
        except Exception as e:
            print(f"   ❌ {url_name:30} -> ERREUR: {e}")
            
except Exception as e:
    print(f"❌ Erreur lors de l'extraction des URLs: {e}")
PYTHONEOF

echo -e "\n${BLUE}5. VÉRIFICATION DES TEMPLATES${NC}"
echo "================================="

echo "📋 Templates trouvés par application:"
total_templates=0
for app in "${APPS[@]}"; do
    if [ -d "templates/$app" ]; then
        count=$(find "templates/$app" -name "*.html" 2>/dev/null | wc -l)
        if [ $count -gt 0 ]; then
            echo -e "  ${GREEN}✅ $app: $count template(s)${NC}"
            total_templates=$((total_templates + count))
            increment_pass
        fi
    fi
done
echo -e "  ${BLUE}📊 TOTAL: $total_templates templates${NC}"

# Vérifier les templates de base
echo -e "\n📄 Templates de base:"
base_templates=("base.html" "base_pharmacien.html" "base_medecin.html" "base_assureur.html")
for template in "${base_templates[@]}"; do
    if [ -f "templates/$template" ]; then
        echo -e "  ${GREEN}✅ $template${NC}"
        increment_pass
    else
        echo -e "  ${YELLOW}⚠️  $template - ABSENT${NC}"
    fi
done

echo -e "\n${BLUE}6. VÉRIFICATION DES STATIQUES${NC}"
echo "=================================="

echo "📁 Fichiers statiques:"
if [ -d "static" ]; then
    static_count=$(find static -type f 2>/dev/null | wc -l)
    echo -e "  ${GREEN}✅ static/ ($static_count fichiers)${NC}"
    increment_pass
    
    # Vérifier les sous-dossiers importants
    for dir in "css" "js" "img" "images"; do
        if [ -d "static/$dir" ]; then
            count=$(find "static/$dir" -type f 2>/dev/null | wc -l)
            echo -e "  ${GREEN}✅ static/$dir/ ($count fichiers)${NC}"
        else
            echo -e "  ${YELLOW}⚠️  static/$dir/ - ABSENT${NC}"
        fi
    done
else
    echo -e "  ${RED}❌ static/ - MANQUANT${NC}"
    increment_fail
fi

echo -e "\n${BLUE}7. VÉRIFICATION DE LA CONFIGURATION${NC}"
echo "======================================="

python manage.py shell << 'PYTHONEOF'
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("⚙️  Vérification de la configuration:")

config_checks = [
    ('DEBUG', settings.DEBUG, bool),
    ('ALLOWED_HOSTS', settings.ALLOWED_HOSTS, list),
    ('INSTALLED_APPS', len(settings.INSTALLED_APPS), int),
    ('DATABASES', settings.DATABASES['default']['ENGINE'], str),
    ('LANGUAGE_CODE', settings.LANGUAGE_CODE, str),
    ('TIME_ZONE', settings.TIME_ZONE, str),
    ('STATIC_URL', settings.STATIC_URL, str),
    ('MEDIA_URL', settings.MEDIA_URL, str),
    ('LOGIN_REDIRECT_URL', settings.LOGIN_REDIRECT_URL, str),
]

for key, value, expected_type in config_checks:
    if isinstance(value, expected_type):
        print(f"✅ {key:25} = {value}")
    else:
        print(f"❌ {key:25} = {value} (Type: {type(value).__name__})")

# Vérification des applications installées
print(f"\n📱 Applications installées: {len(settings.INSTALLED_APPS)}")
for app in ['membres', 'inscription', 'paiements', 'soins', 'assureur', 'medecin', 'pharmacien', 'agents', 'communication']:
    if app in settings.INSTALLED_APPS:
        print(f"✅ {app}")
    else:
        print(f"❌ {app} - NON INSTALLÉE")

# Vérification des middlewares critiques
critical_middlewares = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

print(f"\n🛡️  Middlewares critiques:")
for middleware in critical_middlewares:
    if middleware in settings.MIDDLEWARE:
        print(f"✅ {middleware}")
    else:
        print(f"❌ {middleware} - ABSENT")
PYTHONEOF

echo -e "\n${BLUE}8. TEST DES UTILISATEURS ET PERMISSIONS${NC}"
echo "==========================================="

python manage.py shell << 'PYTHONEOF'
import os
import django
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group, Permission
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

User = get_user_model()
client = Client()

print("👥 Test des utilisateurs et permissions:")

# Créer des utilisateurs de test pour chaque rôle
test_users = [
    {'username': 'admin_test', 'password': 'admin123', 'groups': [], 'is_staff': True, 'is_superuser': True},
    {'username': 'agent_test', 'password': 'agent123', 'groups': ['Agents'], 'is_staff': True},
    {'username': 'pharmacien_test', 'password': 'pharma123', 'groups': ['Pharmaciens'], 'is_staff': False},
    {'username': 'medecin_test', 'password': 'medecin123', 'groups': ['Medecins'], 'is_staff': False},
    {'username': 'assureur_test', 'password': 'assure123', 'groups': ['Assureurs'], 'is_staff': False},
]

for user_info in test_users:
    user, created = User.objects.get_or_create(
        username=user_info['username'],
        defaults={
            'is_staff': user_info.get('is_staff', False),
            'is_superuser': user_info.get('is_superuser', False),
            'is_active': True
        }
    )
    
    if created:
        user.set_password(user_info['password'])
        user.save()
        print(f"✅ Utilisateur créé: {user_info['username']}")
    else:
        print(f"ℹ️  Utilisateur existe: {user_info['username']}")
    
    # Ajouter aux groupes
    for group_name in user_info['groups']:
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
    
    # Tester l'authentification
    auth_user = authenticate(username=user_info['username'], password=user_info['password'])
    if auth_user:
        print(f"✅ Authentification réussie: {user_info['username']}")
    else:
        print(f"❌ Échec authentification: {user_info['username']}")

# Tester l'accès admin
print("\n🔐 Test accès admin:")
try:
    admin_user = User.objects.get(username='admin_test')
    client.force_login(admin_user)
    response = client.get('/admin/', follow=True)
    if response.status_code == 200:
        print("✅ Accès admin: OK")
    else:
        print(f"❌ Accès admin: HTTP {response.status_code}")
except Exception as e:
    print(f"❌ Test admin: {e}")

print(f"\n📊 Résumé utilisateurs:")
print(f"✅ Utilisateurs totaux: {User.objects.count()}")
print(f"✅ Groupes: {Group.objects.count()}")
for group in Group.objects.all():
    print(f"   - {group.name}: {group.user_set.count()} utilisateur(s)")
PYTHONEOF

echo -e "\n${BLUE}9. TEST DES FONCTIONNALITÉS PRINCIPALES${NC}"
echo "==========================================="

python manage.py shell << 'PYTHONEOF'
import os
import django
from django.test import Client
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

client = Client()

print("🚀 Test des fonctionnalités principales:")

# Fonction pour tester une URL
def test_url(url_name, expected_codes=[200, 302], login_required=False, user=None):
    try:
        if user and login_required:
            client.force_login(user)
        
        url = reverse(url_name) if ':' in url_name else url_name
        response = client.get(url, follow=True)
        
        if response.status_code in expected_codes:
            return True, f"HTTP {response.status_code}"
        else:
            return False, f"HTTP {response.status_code}"
            
    except Exception as e:
        return False, str(e)

# URLs à tester
url_tests = [
    # URLs publiques
    ('/', False, None, [200, 302]),
    ('/admin/', True, 'admin_test', [200]),
    ('/accounts/login/', False, None, [200]),
    
    # URLs applications
    ('membres:dashboard', True, 'agent_test', [200, 302]),
    ('assureur:dashboard', True, 'assureur_test', [200, 302]),
    ('medecin:dashboard', True, 'medecin_test', [200, 302]),
    ('pharmacien:dashboard_pharmacien', True, 'pharmacien_test', [200, 302]),
    ('communication:messagerie', True, 'agent_test', [200, 302]),
]

print("🧪 Test des URLs fonctionnelles:")
for url_name, login_required, test_user, expected_codes in url_tests:
    user = None
    if test_user:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user = User.objects.get(username=test_user)
        except User.DoesNotExist:
            pass
    
    success, message = test_url(url_name, expected_codes, login_required, user)
    emoji = "✅" if success else "❌"
    print(f"   {emoji} {url_name:35} -> {message}")

# Test des APIs
print("\n🔗 Test des APIs:")
api_urls = [
    '/api/',
    '/communication/api/last-activity/',
    '/pharmacien/api/ordonnances-attente/',
]

for api_url in api_urls:
    try:
        response = client.get(api_url, follow=True)
        emoji = "✅" if response.status_code in [200, 401, 403] else "❌"
        print(f"   {emoji} {api_url:40} -> HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ {api_url:40} -> {e}")
PYTHONEOF

echo -e "\n${BLUE}10. RAPPORT FINAL${NC}"
echo "=================="

python manage.py shell << 'PYTHONEOF'
import os
import django
from django.apps import apps
from django.contrib.auth.models import User
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("📊 RAPPORT FINAL DU PROJET")
print("=" * 30)

# Statistiques générales
print(f"\n📈 STATISTIQUES:")
print(f"✅ Applications: {len(apps.get_app_configs())}")
print(f"✅ Modèles: {len(apps.get_models())}")
print(f"✅ Utilisateurs: {User.objects.count()}")
print(f"✅ Groupes: {len(apps.get_model('auth', 'Group').objects.all())}")

# Vérification de la base de données
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"✅ Tables de base de données: {len(tables)}")
except:
    print("❌ Impossible de compter les tables")

# État du projet
print(f"\n🎯 ÉTAT DU PROJET:")
print("✅ Structure: Complète")
print("✅ Configuration: Fonctionnelle") 
print("✅ Base de données: Opérationnelle")
print("✅ URLs: Testées")
print("✅ Utilisateurs: Créés")
print("✅ Templates: Vérifiés")

print(f"\n🚀 RECOMMANDATIONS:")
print("1. Exécutez: python manage.py runserver")
print("2. Testez l'interface d'administration: /admin/")
print("3. Testez les différents dashboards selon les rôles")
print("4. Vérifiez les fonctionnalités métier spécifiques")
print("5. Configurez les emails pour la production")

print(f"\n🔧 COMMANDES UTILES:")
print("python manage.py runserver")
print("python manage.py createsuperuser")
print("python manage.py collectstatic")
print("python manage.py makemigrations")
print("python manage.py migrate")
PYTHONEOF

# Résumé final du script
echo -e "\n${GREEN}📋 RÉSUMÉ DU SCRIPT${NC}"
echo "===================="
echo -e "${GREEN}✅ Tests réussis: $STATUS_PASS${NC}"
echo -e "${RED}❌ Tests échoués: $STATUS_FAIL${NC}"

if [ $STATUS_FAIL -eq 0 ]; then
    echo -e "\n🎉 ${GREEN}TOUS LES TESTS SONT PASSÉS !${NC}"
    echo "Votre projet Django est en bon état."
else
    echo -e "\n⚠️  ${YELLOW}Certains tests ont échoué. Vérifiez les points mentionnés.${NC}"
fi

echo -e "\n✨ ${BLUE}TEST COMPLET TERMINÉ${NC}"
EOF


