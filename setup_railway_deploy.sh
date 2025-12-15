#!/bin/bash
# setup_railway_deploy.sh

echo "🚀 Configuration du déploiement Railway..."

# 1. Mettre à jour Procfile
echo "📝 Création du Procfile..."
cat > Procfile << 'EOF'
web: python manage.py migrate && gunicorn mutuelle_core.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
release: python manage.py migrate
EOF

# 2. Mettre à jour .nixpacks.toml
echo "📝 Mise à jour de .nixpacks.toml..."
cat > .nixpacks.toml << 'EOF'
[phases.setup]
nixPkgs = ["python311", "postgresql", "libpqxx"]

[phases.build]
cmds = [
    "pip install --upgrade pip",
    "pip install -r requirements.txt",
    "python manage.py collectstatic --noinput"
]

[start]
cmd = "python manage.py migrate && gunicorn mutuelle_core.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --threads 2 --timeout 120 --keep-alive 2"

[build.args]
PYTHON_VERSION = "3.11.10"
EOF

# 3. Vérifier les fichiers
echo "🔍 Vérification des fichiers..."
ls -la Procfile .nixpacks.toml

# 4. Générer une clé secrète
echo "🔑 Génération d'une clé secrète..."
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(50))"

echo "✅ Configuration terminée !"
echo "📦 Poussez sur GitHub: git add . && git commit -m 'Update Railway config' && git push"