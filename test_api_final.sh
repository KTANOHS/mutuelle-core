#!/bin/bash
echo "🧪 TEST FINAL DE L'API SUR RENDER"
echo "=================================="

BASE_URL="https://mutuelle-core-19.onrender.com"

echo "1. Test API Health:"
curl -s "$BASE_URL/api/health/"
echo -e "\n"

echo "2. Test API Root:"
curl -s "$BASE_URL/api/" | head -c 200
echo -e "\n...\n"

echo "3. Test JWT Token (admin):"
curl -X POST "$BASE_URL/api/token/" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Admin123!"}' \
  -w "\nStatus: %{http_code}\n"

echo -e "\n4. Test JWT Token (matrix):"
curl -X POST "$BASE_URL/api/token/" \
  -H "Content-Type: application/json" \
  -d '{"username":"matrix","password":"transport744"}' \
  -w "\nStatus: %{http_code}\n"

echo -e "\n=================================="
echo "✅ Tests terminés!"
