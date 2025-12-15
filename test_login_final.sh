#!/bin/bash
echo "🔐 TEST FINAL DE CONNEXION CSRF"

URL="https://web-production-555c.up.railway.app"
echo "Test de: $URL"

# Test 1: Vérifier que le site répond
echo -e "\n1. Test de disponibilité..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
echo "   Code HTTP: $STATUS"

# Test 2: Obtenir page admin
echo -e "\n2. Test page admin login..."
ADMIN_PAGE=$(curl -s "$URL/admin/login/")
CSRF_TOKEN=$(echo "$ADMIN_PAGE" | grep -o 'csrfmiddlewaretoken[^>]*value="[^"]*"' | sed 's/.*value="\([^"]*\)".*/\1/')

if [ -n "$CSRF_TOKEN" ]; then
    echo "   ✅ CSRF token trouvé: ${CSRF_TOKEN:0:20}..."
    
    # Test 3: Tentative de connexion
    echo -e "\n3. Test de connexion CSRF..."
    
    read -p "   Username admin: " USERNAME
    read -sp "   Password: " PASSWORD
    echo ""
    
    # Requête POST
    RESPONSE=$(curl -s -X POST "$URL/admin/login/" \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Referer: $URL/admin/login/" \
      --data-urlencode "csrfmiddlewaretoken=$CSRF_TOKEN" \
      --data-urlencode "username=$USERNAME" \
      --data-urlencode "password=$PASSWORD" \
      -c cookies.txt \
      -w "HTTP: %{http_code}")
    
    echo "   $RESPONSE"
    
    # Vérifier résultat
    if echo "$RESPONSE" | grep -q "HTTP: 302"; then
        echo "   🎉 SUCCÈS! Redirection détectée (connexion réussie)"
        
        # Test admin
        ADMIN_TEST=$(curl -s -b cookies.txt "$URL/admin/")
        if echo "$ADMIN_TEST" | grep -q "Site administration"; then
            echo "   ✅ Interface admin accessible!"
        fi
    else
        echo "   ❌ Échec de connexion"
    fi
    
    rm -f cookies.txt
else
    echo "   ❌ Aucun token CSRF trouvé"
    echo "   Page reçue (premières 200 chars):"
    echo "$ADMIN_PAGE" | head -c 200
fi

echo -e "\n✅ Test terminé"
