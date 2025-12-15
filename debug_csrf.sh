#!/bin/bash
echo "🔍 Debug CSRF Railway..."

URL="https://web-production-555c.up.railway.app"

echo "1. Test HEAD pour voir les headers..."
curl -I "$URL/admin/login/"

echo -e "\n2. Test avec verbose pour voir toute la requête..."
curl -v -s "$URL/admin/login/" 2>&1 | grep -E "(CSRF|Cookie|Set-Cookie|Location)"

echo -e "\n3. Test de la configuration Django..."
curl -s "$URL/api/health/"
