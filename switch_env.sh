#!/bin/bash
# switch_env.sh

echo "🔄 Changement d'environnement"
echo "1. Développement (local)"
echo "2. Production (Render)"
echo "3. Test"

read -p "Choix [1/2/3]: " choice

case $choice in
    1)
        echo "🔧 Passage en mode développement..."
        cp .env.development .env
        echo "✅ Environnement développement activé"
        echo "   DEBUG=True"
        echo "   DATABASE_URL=sqlite:///db.sqlite3"
        ;;
    2)
        echo "🚀 Passage en mode production..."
        echo "📝 Configuration pour Render.com..."
        
        # Générer une nouvelle SECRET_KEY si nécessaire
        if [ ! -f ".env.production" ]; then
            cat > .env.production << 'EOF'
# Configuration Django - Environnement de Production
DEBUG=False
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(50))")

# Configuration Render.com
DJANGO_ALLOWED_HOSTS=.onrender.com

# Configuration Email (à adapter)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@mutuelle.com

# Configuration CORS
CORS_ALLOWED_ORIGINS=https://votre-app.onrender.com
CORS_ALLOW_CREDENTIALS=True

# Variables Render
RENDER=True
EOF
        fi
        
        cp .env.production .env
        echo "✅ Environnement production activé"
        echo "   DEBUG=False"
        echo "   DJANGO_ALLOWED_HOSTS=.onrender.com"
        ;;
    3)
        echo "🧪 Passage en mode test..."
        cat > .env.test << 'EOF'
# Configuration Django - Environnement de Test
DEBUG=True
SECRET_KEY=test-key-for-testing-only

# Configuration Base de données test
DATABASE_URL=sqlite:///test_db.sqlite3

# Configuration Allowed Hosts test
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Configuration Email test
EMAIL_BACKEND=django.core.mail.backends.locmem.EmailBackend
DEFAULT_FROM_EMAIL=test@mutuelle.test

# Configuration CORS test
CORS_ALLOWED_ORIGINS=http://localhost:3000
EOF
        cp .env.test .env
        echo "✅ Environnement test activé"
        ;;
    *)
        echo "❌ Choix invalide"
        ;;
esac

echo ""
echo "📋 Configuration actuelle:"
grep -E "^(DEBUG|SECRET_KEY|DJANGO_ALLOWED_HOSTS|DATABASE_URL)=" .env | head -5