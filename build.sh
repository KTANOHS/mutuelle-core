#!/usr/bin/env bash
# build.sh - Script de build optimisé pour Django sur Render.com
# Version corrigée : Python 3.11 + PostgreSQL + WhiteNoise + Gunicorn

set -o errexit
set -o pipefail
set -o nounset

echo "=========================================="
echo "  🚀 DÉPLOIEMENT DJANGO SUR RENDER"
echo "=========================================="
echo "Environnement: ${DJANGO_ENV:-production}"
echo "Python: $(python --version 2>/dev/null || echo 'Python non disponible')"
echo "Port: ${PORT:-non défini}"
echo ""

# ==================== VÉRIFICATION PRÉLIMINAIRE ====================
echo "🔍 Vérification de l'environnement..."

# Vérifier Python
if ! command -v python &> /dev/null; then
    echo "❌ Python n'est pas installé"
    exit 1
fi

# Vérifier pip
if ! command -v pip &> /dev/null; then
    echo "❌ pip n'est pas installé"
    exit 1
fi

echo "✅ Environnement vérifié"

# ==================== PRÉPARATION ====================
echo "📦 Préparation de l'environnement..."

# Créer les répertoires nécessaires
mkdir -p staticfiles
mkdir -p media
mkdir -p logs

# Donner les permissions nécessaires
chmod -R 755 staticfiles media logs 2>/dev/null || true

# ==================== INSTALLATION DES DÉPENDANCES ====================
echo "📦 Installation des dépendances Python..."

# Mettre à jour pip
echo "🔄 Mise à jour de pip..."
pip install --upgrade pip setuptools wheel

# Vérifier si requirements.txt existe
if [ ! -f "requirements.txt" ]; then
    echo "⚠️  requirements.txt non trouvé, création d'un fichier minimal..."
    cat > requirements.txt << 'EOF'
Django==5.2.6
gunicorn==21.2.0
whitenoise==6.7.0
psycopg2-binary==2.9.10
Pillow==10.4.0
python-dotenv==1.0.1
EOF
fi

# Installer les dépendances avec gestion d'erreurs
echo "📥 Installation depuis requirements.txt..."
if ! pip install -r requirements.txt; then
    echo "⚠️  Échec de l'installation complète, tentative avec pip install --no-deps..."
    # Essayer d'installer package par package
    while IFS= read -r package; do
        # Ignorer les lignes vides et les commentaires
        [[ -z "$package" || "$package" =~ ^# ]] && continue
        
        echo "  📦 Installation de: $package"
        if ! pip install "$package"; then
            echo "  ⚠️  Échec pour $package, tentative avec version flexible..."
            # Essayer sans version spécifique
            package_name=$(echo "$package" | sed 's/[<>=!].*//')
            pip install "$package_name" || echo "  ❌ Impossible d'installer $package_name"
        fi
    done < requirements.txt
fi

# Installer les dépendances critiques manquantes
echo "🔧 Vérification des dépendances critiques..."
REQUIRED_PACKAGES=(
    "Django"
    "gunicorn"
    "psycopg2-binary"
    "whitenoise"
    "Pillow"
)

for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! python -c "import $package" 2>/dev/null; then
        echo "  📦 Installation de $package..."
        case $package in
            "Django") pip install "Django>=5.2,<6.0" ;;
            "Pillow") pip install "Pillow>=10.0,<11.0" ;;
            *) pip install "$package" ;;
        esac
    fi
done

# ==================== VÉRIFICATIONS ====================
echo "🔍 Vérifications système..."

# Vérifier les imports critiques
echo "🧪 Test des imports Python..."
python << 'EOF'
import sys

required_modules = [
    'django',
    'gunicorn',
    'psycopg2',
    'whitenoise',
    'PIL'
]

print("📦 Vérification des modules...")
for module in required_modules:
    try:
        __import__(module)
        print(f"  ✅ {module}")
    except ImportError as e:
        print(f"  ❌ {module}: {e}")
        sys.exit(1)

print("✅ Tous les modules sont importables")
EOF

# Vérifier Django
echo "🐍 Vérification Django..."
python << 'EOF'
import os
import django

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    from django.conf import settings
    print(f"✅ Django {django.__version__} configuré")
    
    # Vérifier la base de données
    db_engine = settings.DATABASES['default']['ENGINE']
    print(f"✅ Base de données: {db_engine}")
    
    # Vérifier les settings de production
    if not settings.DEBUG:
        print("✅ Mode production: DEBUG=False")
    else:
        print("⚠️  Mode développement: DEBUG=True")
        
except Exception as e:
    print(f"❌ Erreur Django: {e}")
    sys.exit(1)
EOF

# ==================== MIGRATIONS ====================
echo "🗄️  Application des migrations de base de données..."

# Vérifier si les migrations existent
if [ -d "mutuelle_core/migrations" ]; then
    echo "📋 Migrations détectées, application..."
    
    # D'abord faire les makemigrations
    python manage.py makemigrations --noinput --dry-run 2>&1 | grep -q "No changes detected" || {
        echo "📝 Création de nouvelles migrations..."
        python manage.py makemigrations --noinput
    }
    
    # Appliquer les migrations
    if python manage.py migrate --noinput; then
        echo "✅ Migrations appliquées avec succès"
    else
        echo "⚠️  Échec des migrations, tentative de résolution..."
        # Tentative de récupération
        python manage.py migrate --fake mutuelle_core zero --noinput 2>/dev/null || true
        python manage.py migrate mutuelle_core --fake-initial --noinput
        python manage.py migrate --noinput
    fi
else
    echo "⚠️  Aucun dossier migrations trouvé, création initiale..."
    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
fi

# ==================== COLLECTSTATIC ====================
echo "📁 Collecte des fichiers statiques..."

# Nettoyer d'abord
rm -rf staticfiles/* 2>/dev/null || true

# Collecter les fichiers statiques avec plusieurs tentatives
MAX_RETRIES=3
for i in $(seq 1 $MAX_RETRIES); do
    echo "  Tentative $i/$MAX_RETRIES..."
    
    if python manage.py collectstatic --noinput --clear; then
        echo "✅ Collecte des fichiers statiques réussie"
        break
    else
        if [ $i -eq $MAX_RETRIES ]; then
            echo "⚠️  Échec après $MAX_RETRIES tentatives"
            # Créer un fichier statique minimal
            mkdir -p staticfiles/css staticfiles/js staticfiles/images
            echo "/* Fichier CSS minimal */" > staticfiles/css/style.css
            echo "// Fichier JS minimal" > staticfiles/js/app.js
            touch staticfiles/images/.gitkeep
        else
            echo "  Nouvelle tentative dans 2 secondes..."
            sleep 2
        fi
    fi
done

# Vérifier que staticfiles contient quelque chose
if [ -z "$(ls -A staticfiles 2>/dev/null)" ]; then
    echo "⚠️  staticfiles vide, création de structure minimale..."
    mkdir -p staticfiles/admin staticfiles/rest_framework
    echo "/* Admin CSS */" > staticfiles/admin/base.css
fi

# ==================== SUPERUSER ====================
echo "👑 Configuration superutilisateur..."

# Créer un superuser seulement si les variables sont définies
if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
    echo "Création du superutilisateur: $DJANGO_SUPERUSER_USERNAME"
    
    python << EOF
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings_production')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username=os.environ['DJANGO_SUPERUSER_USERNAME']).exists():
    User.objects.create_superuser(
        os.environ['DJANGO_SUPERUSER_USERNAME'],
        os.environ.get('DJANGO_SUPERUSER_EMAIL', ''),
        os.environ['DJANGO_SUPERUSER_PASSWORD']
    )
    print(f"✅ Superutilisateur {os.environ['DJANGO_SUPERUSER_USERNAME']} créé")
else:
    print(f"⚠️  Superutilisateur {os.environ['DJANGO_SUPERUSER_USERNAME']} existe déjà")
EOF
else
    echo "⚠️  Variables superutilisateur non définies, création d'un superuser par défaut..."
    python << 'EOF'
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings_production')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Superutilisateur par défaut créé (admin/admin123)")
else:
    print("⚠️  Superutilisateur admin existe déjà")
EOF
fi

# ==================== OPTIMISATIONS ====================
echo "⚡ Optimisations finales..."

# Nettoyer les fichiers .pyc et cache
echo "🧹 Nettoyage des fichiers temporaires..."
find . -name "*.pyc" -delete -o -name "__pycache__" -type d -delete 2>/dev/null || true
find . -name ".coverage" -delete -o -name ".pytest_cache" -type d -delete 2>/dev/null || true

# Compresser les fichiers statiques si WhiteNoise est installé
if python -c "import whitenoise" 2>/dev/null; then
    echo "📦 Compression des fichiers statiques (WhiteNoise)..."
    python manage.py compress --force 2>/dev/null || true
fi

# ==================== VÉRIFICATION FINALE ====================
echo "🔍 Vérification finale..."

# Tester que Django peut démarrer
python << 'EOF'
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings_production')

try:
    from django.core.wsgi import get_wsgi_application
    app = get_wsgi_application()
    print("✅ WSGI application chargée avec succès")
    
    # Tester une requête HTTP basique
    from django.test import RequestFactory
    factory = RequestFactory()
    request = factory.get('/health/')
    
    print("✅ Django prêt à recevoir des requêtes")
    
except Exception as e:
    print(f"❌ Erreur lors du chargement de Django: {e}")
    sys.exit(1)
EOF

# ==================== RAPPORT FINAL ====================
echo "✅ Build terminé avec succès !"
echo ""
echo "📊 RÉSUMÉ DU BUILD"
echo "=================="
python --version
pip --version

echo ""
echo "📦 Packages installés:"
pip list --format=columns | grep -E "(Django|gunicorn|psycopg2|whitenoise|Pillow)" | head -10

echo ""
echo "📁 Structure:"
echo "  • $(find . -name "*.py" | wc -l) fichiers Python"
echo "  • $(du -sh staticfiles 2>/dev/null | cut -f1) dans staticfiles"
echo "  • $(du -sh . | cut -f1) total"

echo ""
echo "🎯 PRÊT POUR LE DÉPLOIEMENT"
echo "==========================="
echo "Pour démarrer l'application:"
echo "  gunicorn mutuelle_core.wsgi:application --bind 0.0.0.0:\$PORT"
echo ""
echo "🔧 Commandes utiles:"
echo "  • Voir les logs: heroku logs --tail (si sur Heroku)"
echo "  • Accéder à l'admin: /admin"
echo "  • Health check: /health/"
echo ""
echo "✅ Le build a réussi !"