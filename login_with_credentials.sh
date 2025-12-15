#!/bin/bash
# Remplacez ces valeurs par vos identifiants réels
ADMIN_USER="matrix"  # Changez ceci
ADMIN_PASS="transport744"  # Changez ceci

echo "🔐 Tentative de connexion avec: $ADMIN_USER"

URL="https://web-production-555c.up.railway.app"
LOGIN_URL="$URL/admin/login/"

# Récupérer CSRF
CSRF_TOKEN=$(curl -s "$LOGIN_URL" | grep -o 'name="csrfmiddlewaretoken"[^>]*value="[^"]*"' | sed 's/.*value="\([^"]*\)".*/\1/')

if [ -z "$CSRF_TOKEN" ]; then
    echo "❌ Impossible de récupérer CSRF"
    exit 1
fi

echo "Token CSRF: ${CSRF_TOKEN:0:10}..."

# Connexion
echo "Connexion en cours..."
RESPONSE=$(curl -s -X POST \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Referer: $LOGIN_URL" \
    --data-urlencode "csrfmiddlewaretoken=$CSRF_TOKEN" \
    --data-urlencode "username=$ADMIN_USER" \
    --data-urlencode "password=$ADMIN_PASS" \
    -c cookies.txt \
    -w "\n%{http_code}\n%{redirect_url}" \
    "$LOGIN_URL")

HTTP_CODE=$(echo "$RESPONSE" | tail -2 | head -1)
REDIRECT=$(echo "$RESPONSE" | tail -1)

echo -e "\nRésultat:"
echo "Code HTTP: $HTTP_CODE"
echo "Redirection: $REDIRECT"

# Vérifier le cookie
if grep -q "sessionid" cookies.txt; then
    echo "✅ SUCCÈS : Session admin créée !"
    
    # Tester l'accès
    echo -e "\nTest d'accès à /admin/"
    curl -s -b cookies.txt "$URL/admin/" | grep -o "<title>[^<]*</title>" || echo "Pas de titre trouvé"
else
    echo "❌ ÉCHEC : Mauvais identifiants ou problème de configuration"
    
    # Afficher la réponse pour déboguer
    echo -e "\nDébogage (premières 10 lignes):"
    echo "$RESPONSE" | head -10
fi

rm -f cookies.txt
