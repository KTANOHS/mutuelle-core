#!/bin/bash
echo "🔄 SOLUTION ALTERNATIVE SI VOUS NE POUVEZ PAS ACCÉDER À RAILWAY"
echo ""

echo "1. Créez un fichier .env dans votre projet :"
cat > .env << 'ENVFILE'
# Variables d'environnement pour Railway
RAILWAY=true
DEBUG=True
SECRET_KEY=505eee0974d43543d48e51924fd7aba63f76cca9d56277a00687aaace82a99ef
ALLOWED_HOSTS=web-production-555c.up.railway.app,*.railway.app,localhost,127.0.0.1,*,0.0.0.0,[::1]
CSRF_TRUSTED_ORIGINS=https://web-production-555c.up.railway.app,http://web-production-555c.up.railway.app,https://*.railway.app,http://*.railway.app
CORS_ALLOWED_ORIGINS=https://web-production-555c.up.railway.app,http://web-production-555c.up.railway.app,https://*.railway.app,http://*.railway.app
RAILWAY_PUBLIC_DOMAIN=web-production-555c.up.railway.app
SECURE_PROXY_SSL_HEADER=true
USE_X_FORWARDED_HOST=true
USE_X_FORWARDED_PORT=true
DISABLE_COLLECTSTATIC=1
CSRF_COOKIE_DOMAIN=none
SESSION_COOKIE_DOMAIN=none
ENVFILE

echo "✅ Fichier .env créé"
echo ""
echo "2. Poussez ce fichier sur Railway :"
echo "   git add .env"
echo "   git commit -m 'Add environment variables'"
echo "   git push railway main"
echo ""
echo "3. Railway devrait automatiquement utiliser ces variables"
echo ""
echo "⚠️  Note : Railway préfère les variables configurées via l'interface web"
echo "   mais le fichier .env peut fonctionner comme solution temporaire"
