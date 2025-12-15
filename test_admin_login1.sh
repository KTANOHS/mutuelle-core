cat > test_admin_login.sh << 'EOF'
#!/bin/bash
echo -e "🔐 TEST DE CONNEXION ADMIN COMPLET\n"

URL="https://web-production-555c.up.railway.app"
LOGIN_URL="$URL/admin/login/"

# 1. Récupérer le token CSRF
echo "1. Récupération du token CSRF..."
HTML_CONTENT=$(curl -s "$LOGIN_URL")
CSRF_TOKEN=$(echo "$HTML_CONTENT" | grep -o 'name="csrfmiddlewaretoken"[^>]*value="[^"]*"' | sed 's/.*value="\([^"]*\)".*/\1/')

if [ -z "$CSRF_TOKEN" ]; then
    echo "❌ Échec de récupération du token CSRF"
    exit 1
fi

echo "✅ Token CSRF obtenu: ${CSRF_TOKEN:0:20}..."

# 2. Demander les identifiants
echo -e "\n2. Identifiants de connexion"
echo "================================"
read -p "Nom d'utilisateur admin: " ADMIN_USER
read -sp "Mot de passe: " ADMIN_PASS
echo ""

# 3. Tentative de connexion
echo -e "\n3. Tentative de connexion..."
RESPONSE=$(curl -s -X POST \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Referer: $LOGIN_URL" \
    --data-urlencode "csrfmiddlewaretoken=$CSRF_TOKEN" \
    --data-urlencode "username=$ADMIN_USER" \
    --data-urlencode "password=$ADMIN_PASS" \
    -c admin_cookies.txt \
    -w "%{http_code}" \
    -o response.html \
    "$LOGIN_URL")

echo "Code HTTP de réponse: $RESPONSE"

# 4. Analyser la réponse
echo -e "\n4. Analyse de la réponse..."

if [ "$RESPONSE" = "302" ] || [ "$RESPONSE" = "200" ]; then
    # Vérifier si la connexion a réussi
    if grep -q "sessionid" admin_cookies.txt; then
        echo "✅ Session créée (cookie sessionid présent)"
        
        # Vérifier la redirection
        REDIRECT_URL=$(grep -i "location:" response.html 2>/dev/null || echo "")
        if [ -n "$REDIRECT_URL" ]; then
            echo "🔀 Redirection détectée: $REDIRECT_URL"
        fi
        
        # Tester l'accès à l'admin
        echo -e "\n5. Test d'accès à l'interface admin..."
        ADMIN_RESPONSE=$(curl -s -b admin_cookies.txt "$URL/admin/" | head -100)
        
        if echo "$ADMIN_RESPONSE" | grep -q "Site administration\|Tableau de bord"; then
            echo "🎉 SUCCÈS : Vous êtes connecté à l'interface admin !"
        else
            echo "⚠️  Connecté mais interface admin non accessible"
            echo "Extrait réponse:"
            echo "$ADMIN_RESPONSE" | grep -i "title\|h1" | head -5
        fi
    else
        echo "❌ Échec : Aucun cookie de session créé"
        
        # Afficher les erreurs possibles
        echo "Contenu de la page d'erreur:"
        grep -i "error\|invalid\|incorrect" response.html | head -5
    fi
else
    echo "❌ Échec : Code HTTP inattendu"
fi

# 5. Nettoyage
rm -f response.html admin_cookies.txt

echo -e "\n✅ Test terminé"
EOF

chmod +x test_admin_login1.sh
./test_admin_login1.sh