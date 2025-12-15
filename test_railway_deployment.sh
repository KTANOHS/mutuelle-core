#!/bin/bash
# test_railway_deployment.sh

echo "🧪 Test du déploiement Railway..."

# Remplacez par votre URL Railway
RAILWAY_URL="https://votre-projet.railway.app"

# 1. Test de l'endpoint health
echo "1. Test de l'endpoint health..."
curl -s "$RAILWAY_URL/api/health/" | jq '.'

# 2. Test de l'admin (redirection attendue)
echo -e "\n2. Test de l'admin..."
curl -I "$RAILWAY_URL/admin/" | head -5

# 3. Test de l'API JWT
echo -e "\n3. Test de l'API JWT..."
echo "Tentative d'obtention d'un token..."
curl -s -X POST "$RAILWAY_URL/api/token/" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"votre-mot-de-passe"}' | jq '.'

# 4. Test des fichiers statiques
echo -e "\n4. Test des fichiers statiques..."
curl -I "$RAILWAY_URL/static/admin/css/base.css" | head -3

# 5. Informations système
echo -e "\n5. Informations système..."
echo "URL de l'application: $RAILWAY_URL"
echo "Pour accéder à l'interface Railway: https://railway.app"
echo "Pour voir les logs: railway logs"