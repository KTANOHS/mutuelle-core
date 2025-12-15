#!/bin/bash
echo "🚀 Mise à jour des variables Railway..."

# Variables nécessaires
VARS=(
  "RAILWAY=true"
  "DEBUG=False"
  "ALLOWED_HOSTS=web-production-555c.up.railway.app,*.railway.app,localhost,127.0.0.1"
  "CSRF_TRUSTED_ORIGINS=https://web-production-555c.up.railway.app,http://web-production-555c.up.railway.app,https://*.railway.app,http://*.railway.app"
  "CORS_ALLOWED_ORIGINS=https://web-production-555c.up.railway.app,http://web-production-555c.up.railway.app"
)

echo "📋 Variables à ajouter dans Railway:"
echo ""
for var in "${VARS[@]}"; do
  echo "  $var"
done

echo ""
echo "📝 Instructions:"
echo "1. Allez sur: https://railway.app/project/[votre-projet-id]/variables"
echo "2. Cliquez sur 'New Variable'"
echo "3. Ajoutez chaque variable ci-dessus"
echo "4. Redéployez manuellement ou attendez le redéploiement automatique"
echo ""
echo "⏳ Après l'ajout, l'application redémarrera automatiquement"
echo "🌐 Votre URL: https://web-production-555c.up.railway.app"
