#!/bin/bash
echo "🧪 TEST FINAL APRÈS CORRECTIONS"
echo "================================"

BASE_URL="https://mutuelle-core-19.onrender.com"

echo "1. Test de santé principal:"
curl -s "$BASE_URL/health/" -w "Status: %{http_code}\n"

echo -e "\n2. Test API Health:"
curl -s "$BASE_URL/api/health/" -w "Status: %{http_code}\n"

echo -e "\n3. Test JWT Token (admin):"
curl -X POST "$BASE_URL/api/token/" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Admin123!"}' \
  -s -w "Status: %{http_code}\nContent-Type: %{content_type}\n" \
  | head -c 200
echo -e "\n"

echo -e "\n4. Test page d'accueil:"
curl -s "$BASE_URL/" -w "Status: %{http_code}\n" | grep -o "<title>.*</title>"

echo -e "\n================================"
echo "Si Status = 200, l'API fonctionne !"
echo "Si Status = 500, vérifiez les logs Render"
