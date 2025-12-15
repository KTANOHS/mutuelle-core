#!/bin/bash
echo "🧪 Test de l'API sur Render..."
echo "================================="

# Variables
BASE_URL="https://mutuelle-core-19.onrender.com"
USERS=("admin" "matrix")
PASSWORDS=("Admin123!" "transport744")

# Test Health Check
echo -e "\n1. Testing Health Check:"
curl -s -o /dev/null -w "Status: %{http_code}\n" "$BASE_URL/api/health/"

# Test API Root
echo -e "\n2. Testing API Root:"
curl -s "$BASE_URL/api/" | head -c 200
echo -e "\n..."

# Test JWT for each user
for i in "${!USERS[@]}"; do
    USER="${USERS[$i]}"
    PASS="${PASSWORDS[$i]}"
    
    echo -e "\n3. Testing JWT Token for $USER:"
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/token/" \
        -H "Content-Type: application/json" \
        -d "{\"username\":\"$USER\",\"password\":\"$PASS\"}")
    
    STATUS=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n -1)
    
    echo "   HTTP Status: $STATUS"
    
    if [ "$STATUS" = "200" ]; then
        echo "   ✅ Success! Token obtenu"
        TOKEN=$(echo "$BODY" | grep -o '"access":"[^"]*"' | cut -d'"' -f4)
        echo "   Token: ${TOKEN:0:50}..."
        
        # Test avec le token
        echo -e "\n4. Testing authenticated endpoint with token:"
        curl -s -H "Authorization: Bearer $TOKEN" \
            "$BASE_URL/api/statistiques/" | head -c 100
        echo -e "\n..."
    elif [ "$STATUS" = "401" ]; then
        echo "   ❌ Authentication failed"
        echo "   Response: $BODY"
    else
        echo "   ⚠️  Unexpected status: $STATUS"
        echo "   Response: $BODY"
    fi
done

echo -e "\n================================="
echo "Tests terminés!"
