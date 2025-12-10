#!/usr/bin/env bash
# test_api.sh - Test des APIs Django

API_URL="${1:-http://localhost:8000}"

echo "🧪 Test des APIs sur $API_URL"
echo "=============================="

# Fonction de test
test_endpoint() {
    local endpoint=$1
    local method=${2:-GET}
    local expected=${3:-200}
    
    echo -n "Testing $method $endpoint... "
    
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X "$method" "$API_URL$endpoint")
    
    if [ "$STATUS" -eq "$expected" ] || [ "$STATUS" -eq "302" ]; then
        echo "✅ $STATUS"
        return 0
    else
        echo "❌ $STATUS (attendu: $expected)"
        return 1
    fi
}

# Tests
test_endpoint "/"
test_endpoint "/admin/"  # Redirection vers login
test_endpoint "/api/"
test_endpoint "/health/" "GET" "200"

# Test d'API avec authentification (si token disponible)
if [ -n "${API_TOKEN:-}" ]; then
    test_endpoint "/api/membres/" "GET" "200"
    test_endpoint "/api/assureurs/" "GET" "200"
fi

echo "=============================="
echo "Tests terminés!"