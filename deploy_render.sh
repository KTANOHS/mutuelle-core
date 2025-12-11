#!/bin/bash
# Script de déploiement pour Render.com

echo "🚀 PRÉPARATION DU DÉPLOIEMENT RENDER"
echo "===================================="

# 1. Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

# 2. Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# 3. Appliquer les migrations (seulement en local pour test)
echo "🔄 Test des migrations..."
python manage.py migrate --noinput

# 4. Créer un superutilisateur si nécessaire
echo "👤 Vérification du superutilisateur..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = 'admin'
email = 'admin@mutuelle.com'
password = 'Admin123!'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'✅ Superutilisateur créé: {username} / {password}')
else:
    print(f'✅ Superutilisateur existe déjà: {username}')
"

# 5. Tester l'application localement
echo "🔗 Test local de l'application..."
timeout 5 python manage.py runserver 0.0.0.0:8000 &
SERVER_PID=$!
sleep 3

# Tester quelques URLs
echo "🌐 Test des URLs principales..."
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ && echo " - Accueil OK" || echo " - Accueil ÉCHEC"
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/admin/ && echo " - Admin OK" || echo " - Admin ÉCHEC"

# Arrêter le serveur
kill $SERVER_PID 2>/dev/null

echo ""
echo "✅ PRÉPARATION TERMINÉE !"
echo ""
echo "📝 POUR DÉPLOYER SUR RENDER :"
echo "1. git add ."
echo "2. git commit -m 'Prêt pour déploiement Render'"
echo "3. git push origin main"
echo "4. Render déploiera automatiquement"