#!/bin/bash
echo "🧪 Test CSRF après correction..."

URL="https://web-production-555c.up.railway.app"

echo "1. Test de l'endpoint santé..."
curl -s "$URL/api/health/" | head -5

echo -e "\n2. Tentative de récupération du token CSRF..."
curl -s -c cookies.txt "$URL/admin/login/" | grep -o "csrfmiddlewaretoken.*value" | head -1

echo -e "\n3. Test de connexion admin..."
echo "   Ouvrez: $URL/admin/"
echo "   Username: matrix"
echo "   Password: transport744"

echo -e "\n✅ Si le formulaire de login s'affiche sans erreur CSRF, c'est bon !"
