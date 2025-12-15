#!/bin/bash
# final_check.sh

echo "🔍 Vérification finale avant déploiement..."

# 1. Test local
python manage.py check --deploy

# 2. Test de l'API
python manage.py runserver &
SERVER_PID=$!
sleep 3

curl -s http://localhost:8000/api/health/ | python -m json.tool

kill $SERVER_PID

# 3. Vérification des fichiers
echo -e "\n📁 Fichiers pour Railway:"
ls -la .nixpacks.toml Procfile requirements.txt

# 4. Génération d'une clé secrète
echo -e "\n🔑 Clé secrète pour Railway:"
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(50))"

echo -e "\n✅ Prêt pour le déploiement !"
echo "🌐 Allez sur: https://railway.app"
echo "📦 Votre dépôt: https://github.com/KTANOHS/mutuelle-core"