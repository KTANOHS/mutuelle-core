#!/bin/bash
# build_and_run.sh
# Script complet de build et démarrage pour Django sur Render
set -e

echo "========================================"
echo "🚀 DÉPLOIEMENT DJANGO SUR RENDER"
echo "========================================"

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "manage.py" ]; then
    echo "❌ ERREUR: Fichier manage.py non trouvé"
    echo "   Assurez-vous d'être dans le répertoire racine du projet Django"
    exit 1
fi

echo "✅ Répertoire Django détecté"

# === ÉTAPE 1 : DÉPENDANCES ===
echo ""
echo "1️⃣ INSTALLATION DES DÉPENDANCES"
echo "----------------------------------------"

# Mettre à jour pip
echo "🔧 Mise à jour de pip..."
python -m pip install --upgrade pip

# Installer les dépendances
echo "📦 Installation des dépendances depuis requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dependencies installées"
else
    echo "❌ Fichier requirements.txt non trouvé"
    exit 1
fi

# === ÉTAPE 2 : FICHIERS STATIQUES ===
echo ""
echo "2️⃣ FICHIERS STATIQUES"
echo "----------------------------------------"

# Créer des fichiers statiques par défaut si nécessaire
echo "📁 Création de fichiers statiques par défaut..."
mkdir -p static/mutuelle_core/images static/mutuelle_core/videos static/js static/img

# Créer un favicon par défaut
if [ ! -f "static/img/favicon.ico" ]; then
    echo "🎨 Création favicon par défaut..."
    echo "data:image/x-icon;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAA" > static/img/favicon.ico
fi

# Créer un logo par défaut
if [ ! -f "static/mutuelle_core/images/logo.jpg" ]; then
    echo "🎨 Création logo par défaut..."
    echo "LOGO PLACEHOLDER" > static/mutuelle_core/images/logo.jpg
fi

# Créer un fichier JS par défaut
if [ ! -f "static/js/messagerie-integration.js" ]; then
    echo "📝 Création fichier JS par défaut..."
    echo "// Fichier JavaScript de messagerie
console.log('Messagerie Mutuelle Core chargée');
" > static/js/messagerie-integration.js
fi

# Collecter les fichiers statiques Django
echo "📦 Collection des fichiers statiques Django..."
python manage.py collectstatic --noinput || {
    echo "⚠️  Attention: collectstatic a échoué, continuation..."
}

# === ÉTAPE 3 : BASE DE DONNÉES ===
echo ""
echo "3️⃣ BASE DE DONNÉES"
echo "----------------------------------------"

# Vérifier les migrations en attente
echo "🔍 Vérification des migrations..."
python manage.py makemigrations --check --dry-run || true

# Appliquer les migrations
echo "🚀 Application des migrations..."
python manage.py migrate --noinput
echo "✅ Migrations appliquées avec succès"

# === ÉTAPE 4 : SUPERUTILISATEUR ===
echo ""
echo "4️⃣ SUPERUTILISATEUR"
echo "----------------------------------------"

echo "👤 Création du superutilisateur par défaut..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()

# Créer l'admin par défaut
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@mutuelle.local', 'Admin123!')
    print('✅ Superutilisateur créé: admin / Admin123!')
else:
    print('✅ Superutilisateur existe déjà')

# Créer d'autres utilisateurs de test si besoin
test_users = [
    ('agent', 'agent@mutuelle.local', 'Agent123!'),
    ('medecin', 'medecin@mutuelle.local', 'Medecin123!'),
    ('pharmacien', 'pharmacien@mutuelle.local', 'Pharmacien123!'),
]

for username, email, password in test_users:
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username, email, password, is_staff=True)
        print(f'✅ Utilisateur créé: {username} / {password}')
" || echo "⚠️  Création des utilisateurs a échoué (peut être normal)"

# === ÉTAPE 5 : VÉRIFICATIONS ===
echo ""
echo "5️⃣ VÉRIFICATIONS FINALES"
echo "----------------------------------------"

# Vérifier que Django peut démarrer
echo "🔍 Vérification du serveur Django..."
python manage.py check --deploy || echo "⚠️  Avertissements de déploiement détectés"

# Afficher les informations du projet
echo ""
echo "📊 INFORMATIONS DU PROJET"
echo "----------------------------------------"
echo "📁 Répertoire: $(pwd)"
echo "🐍 Python: $(python --version)"
echo "🎯 Django: $(python -c 'import django; print(django.get_version())')"
echo "🌐 Port: ${PORT:-10000}"
echo "🔧 DEBUG: $(python -c 'import os; print(os.environ.get(\"DEBUG\", \"False\"))')"

# === ÉTAPE 6 : DÉMARRAGE ===
echo ""
echo "6️⃣ DÉMARRAGE DU SERVEUR"
echo "========================================"
echo "🚀 Lancement de Gunicorn..."
echo "📢 L'application sera disponible sur: http://0.0.0.0:\${PORT:-10000}"
echo "========================================"

# Démarrer Gunicorn
exec gunicorn mutuelle_core.wsgi:application \
    --bind 0.0.0.0:\${PORT:-10000} \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --capture-output