#!/bin/bash
# correction_rapide.sh

echo "🔧 CORRECTION DES 3 ERREURS CRITIQUES"
echo "====================================="

# 1. Corriger SECRET_KEY
echo "1. 🔐 Génération d'une nouvelle SECRET_KEY..."
NEW_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(50))")
echo "Nouvelle clé générée: ${NEW_KEY:0:20}..."

# Mettre à jour .env
if [ -f ".env" ]; then
    # Vérifier si SECRET_KEY existe déjà
    if grep -q "SECRET_KEY=" .env; then
        sed -i '' "s|SECRET_KEY=.*|SECRET_KEY=$NEW_KEY|" .env
        echo "✅ SECRET_KEY mise à jour dans .env"
    else
        echo "SECRET_KEY=$NEW_KEY" >> .env
        echo "✅ SECRET_KEY ajoutée à .env"
    fi
else
    echo "⚠️  .env non trouvé, création..."
    cat > .env << EOF
# SECRET_KEY sécurisée
SECRET_KEY=$NEW_KEY
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EOF
    echo "✅ .env créé avec SECRET_KEY"
fi

# 2. Installer psycopg2-binary
echo "2. 📦 Installation de psycopg2-binary..."
pip install psycopg2-binary
echo "✅ psycopg2-binary installé"

# Mettre à jour requirements.txt
if ! grep -q "psycopg2" requirements.txt; then
    echo "psycopg2-binary==2.9.11" >> requirements.txt
    echo "✅ psycopg2 ajouté à requirements.txt"
fi

# 3. Corriger STATIC_ROOT dans settings.py
echo "3. 📁 Correction de STATIC_ROOT..."
SETTINGS_FILE="mutuelle_core/settings.py"

# Vérifier si STATIC_ROOT est déjà défini
if grep -q "STATIC_ROOT =" "$SETTINGS_FILE"; then
    echo "✅ STATIC_ROOT déjà défini"
else
    # Ajouter STATIC_ROOT après STATIC_URL
    sed -i '' '/STATIC_URL = .*/a\
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")' "$SETTINGS_FILE"
    echo "✅ STATIC_ROOT ajouté à settings.py"
fi

# S'assurer que le dossier existe
if [ ! -d "staticfiles" ]; then
    mkdir -p staticfiles
    echo "✅ Dossier staticfiles créé"
fi

# 4. Tester les corrections
echo "4. 🧪 Test des corrections..."
echo "   - Test collectstatic..."
python manage.py collectstatic --noinput --dry-run && echo "     ✅ collectstatic fonctionne"

echo "   - Test SECRET_KEY..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()
from django.conf import settings
key = settings.SECRET_KEY
if 'insecure' not in key and len(key) > 20:
    print('     ✅ SECRET_KEY sécurisée')
else:
    print('     ❌ SECRET_KEY toujours non sécurisée')
"

echo "   - Test psycopg2..."
python -c "import psycopg2; print('     ✅ psycopg2 importé avec succès')"

echo ""
echo "🎉 CORRECTIONS TERMINÉES !"
echo "=========================="
echo "Pour tester: python manage.py runserver"
echo "Pour déployer sur Render:"
echo "1. Changez DEBUG=False dans .env"
echo "2. Ajoutez votre domaine à DJANGO_ALLOWED_HOSTS"
echo "3. Poussez sur Git"
echo "4. Créez le service sur Render.com"