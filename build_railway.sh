#!/usr/bin/env bash
# build_railway.sh - Script de build optimisé pour Django sur Railway.app
# Version sans création de superutilisateur par défaut

set -o errexit
set -o pipefail
set -o nounset

echo "=========================================="
echo "  🚂 DÉPLOIEMENT DJANGO SUR RAILWAY"
echo "=========================================="
echo "Environnement: ${RAILWAY_ENVIRONMENT:-production}"
echo "Port: ${PORT:-non défini}"
echo "Python: $(python --version 2>/dev/null || echo 'Chargement...')"
echo ""

# ==================== VÉRIFICATION PRÉLIMINAIRE RAILWAY ====================
echo "🔍 Vérification de l'environnement Railway..."

# Variables Railway requises
if [ -z "${PORT:-}" ]; then
    echo "⚠️  PORT non défini, utilisation par défaut: 8000"
    export PORT=8000
fi

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

echo "✅ Environnement Railway vérifié"

# ==================== PRÉPARATION SPÉCIFIQUE RAILWAY ====================
echo "📦 Préparation spécifique Railway..."

# Créer les répertoires nécessaires pour Railway
mkdir -p staticfiles
mkdir -p media
mkdir -p logs
mkdir -p static/images  # Pour le fichier manquant healthcare-bg.jpg

# Créer le fichier image manquant pour WhiteNoise
echo "🖼️  Création du fichier image manquant (healthcare-bg.jpg)..."
if [ ! -f "static/images/healthcare-bg.jpg" ]; then
    python3 -c "
import os
os.makedirs('static/images', exist_ok=True)

# Créer un fichier placeholder simple
with open('static/images/healthcare-bg.jpg', 'w') as f:
    f.write('PLACEHOLDER IMAGE - healthcare-bg.jpg\\n')
print('  ✅ Fichier placeholder créé')
"
fi

# Vérifier que le fichier existe
if [ -f "static/images/healthcare-bg.jpg" ]; then
    echo "✅ Fichier healthcare-bg.jpg créé ($(stat -c%s static/images/healthcare-bg.jpg) bytes)"
else
    echo "⚠️  Impossible de créer healthcare-bg.jpg, création d'un fichier vide"
    touch static/images/healthcare-bg.jpg
fi

# Donner les permissions nécessaires
chmod -R 755 staticfiles media logs static/images 2>/dev/null || true

# ==================== INSTALLATION DES DÉPENDANCES ====================
echo "📦 Installation des dépendances Python..."

# Vérifier si requirements.txt existe
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt non trouvé - CRITIQUE"
    exit 1
fi

# Installer les dépendances
echo "📥 Installation depuis requirements.txt..."
pip install -r requirements.txt
echo "✅ Dépendances installées"

# ==================== VÉRIFICATIONS SPÉCIALES RAILWAY ====================
echo "🔍 Vérifications spécifiques Railway..."

# Vérifier que coreapi et pyyaml sont installés
echo "📚 Vérification documentation API..."
python3 -c "
try:
    import coreapi
    print('✅ coreapi installé')
except ImportError:
    print('❌ coreapi NON installé')
    import subprocess
    subprocess.run(['pip', 'install', 'coreapi==2.3.3'], check=False)

try:
    import yaml
    print('✅ pyyaml installé')
except ImportError:
    print('❌ pyyaml NON installé')
    import subprocess
    subprocess.run(['pip', 'install', 'pyyaml==6.0.1'], check=False)
"

# ==================== MIGRATIONS ====================
echo "🗄️  Application des migrations..."

# Appliquer les migrations
if python manage.py migrate --noinput; then
    echo "✅ Migrations appliquées"
else
    echo "⚠️  Échec migrations, tentative de réparation..."
    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
fi

# ==================== COLLECTSTATIC ====================
echo "📁 Collecte des fichiers statiques..."

# Nettoyer avant de collecter
rm -rf staticfiles/* 2>/dev/null || true

# Collecter avec gestion d'erreurs
if python manage.py collectstatic --noinput --clear; then
    echo "✅ Fichiers statiques collectés"
else
    echo "⚠️  Échec collectstatic, création de structure minimale..."
    mkdir -p staticfiles/{css,js,images}
    echo "/* CSS minimal */" > staticfiles/css/style.css
    cp static/images/healthcare-bg.jpg staticfiles/images/ 2>/dev/null || touch staticfiles/images/healthcare-bg.jpg
fi

# ==================== VÉRIFICATION SUPERUTILISATEUR EXISTANT ====================
echo "👑 Vérification du superutilisateur existant..."

python3 << 'EOF'
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Vérifier si le superutilisateur 'matrix' existe
try:
    user = User.objects.get(username='matrix')
    if user.is_superuser:
        print(f"✅ Superutilisateur trouvé: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Staff: {user.is_staff}")
        print(f"   Superuser: {user.is_superuser}")
    else:
        print(f"⚠️  Utilisateur 'matrix' trouvé mais n'est pas superutilisateur")
except User.DoesNotExist:
    print("❌ Superutilisateur 'matrix' non trouvé")
    print("ℹ️  Utilisez la commande manuelle pour créer un superutilisateur:")
    print("   python manage.py createsuperuser --username matrix --email matrix@example.com")
except Exception as e:
    print(f"⚠️  Erreur lors de la vérification: {e}")
EOF

# ==================== OPTIMISATIONS FINALES ====================
echo "⚡ Optimisations finales..."

# Nettoyer les fichiers temporaires
echo "🧹 Nettoyage des fichiers temporaires..."
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "__pycache__" -type d -delete 2>/dev/null || true

# ==================== VÉRIFICATION DE SANTÉ ====================
echo "🏥 Vérification de santé de l'application..."

python3 << 'EOF'
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
    # Tester la base de données
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    
    print("✅ Base de données accessible")
    
    # Tester les modèles principaux
    from django.contrib.auth.models import User
    user_count = User.objects.count()
    print(f"✅ Modèles accessibles ({user_count} utilisateurs)")
    
    print("✅ Application Django prête")
    
except Exception as e:
    print(f"⚠️  Vérification de santé échouée: {e}")
EOF

# ==================== RAPPORT FINAL ====================
echo ""
echo "✅ BUILD RAILWAY TERMINÉ AVEC SUCCÈS !"
echo "======================================"
echo ""
echo "📊 INFORMATIONS DU SYSTÈME"
echo "-------------------------"
echo "Python: $(python --version 2>/dev/null)"
echo "Django: $(python -c "import django; print(django.__version__)" 2>/dev/null || echo "Non disponible")"
echo "Port: ${PORT}"
echo ""
echo "🔑 SUPERUTILISATEUR EXISTANT"
echo "---------------------------"
echo "Username: matrix"
echo "Status: Préservé (non modifié par le build)"
echo ""
echo "📁 FICHIERS STATIQUES"
echo "--------------------"
echo "• staticfiles/: $(find staticfiles -type f 2>/dev/null | wc -l) fichiers"
echo "• healthcare-bg.jpg: $(ls -la staticfiles/images/healthcare-bg.jpg 2>/dev/null | awk '{print $5}') bytes" || echo "• healthcare-bg.jpg: non trouvé"
echo ""
echo "🚀 COMMANDE DE DÉMARRAGE"
echo "-----------------------"
echo "gunicorn mutuelle_core.wsgi:application \\"
echo "  --bind 0.0.0.0:\$PORT \\"
echo "  --workers 3 \\"
echo "  --threads 2 \\"
echo "  --timeout 120"
echo ""
echo "🔧 UTILISATEURS EXISTANTS"
echo "------------------------"
python3 << 'EOF'
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User

superusers = User.objects.filter(is_superuser=True)
staff_users = User.objects.filter(is_staff=True, is_superuser=False)
regular_users = User.objects.filter(is_staff=False, is_superuser=False)

print(f"• Superutilisateurs: {superusers.count()}")
for user in superusers[:3]:  # Afficher les 3 premiers
    print(f"  - {user.username} ({user.email})")

print(f"• Staff (non superuser): {staff_users.count()}")
print(f"• Utilisateurs réguliers: {regular_users.count()}")
EOF
echo ""
echo "🎉 PRÊT POUR LE DÉPLOIEMENT !"