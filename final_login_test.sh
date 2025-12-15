#!/bin/bash
echo -e "\n🎯 TEST FINAL DE CONNEXION ADMIN"

echo "1. Vérification de l'application..."
curl -s -I https://web-production-555c.up.railway.app | head -1

echo -e "\n2. Test du formulaire de login..."

# Méthode compatible macOS (sans -P)
HTML_CONTENT=$(curl -s https://web-production-555c.up.railway.app/admin/login/)

# Essayez plusieurs méthodes d'extraction CSRF
CSRF_TOKEN=$(echo "$HTML_CONTENT" | grep -o 'name="csrfmiddlewaretoken"[^>]*value="[^"]*"' | sed 's/.*value="\([^"]*\)".*/\1/')

if [ -z "$CSRF_TOKEN" ]; then
    # Méthode alternative
    CSRF_TOKEN=$(echo "$HTML_CONTENT" | grep -o 'csrfmiddlewaretoken.*value="[^"]*"' | sed 's/.*value="\([^"]*\)".*/\1/')
fi

if [ -z "$CSRF_TOKEN" ]; then
    # Dernière tentative
    CSRF_TOKEN=$(echo "$HTML_CONTENT" | grep csrfmiddlewaretoken | sed -n 's/.*value="\([^"]*\)".*/\1/p')
fi

if [ -n "$CSRF_TOKEN" ]; then
    echo "✅ Token CSRF extrait avec succès"
    echo "Token (tronqué): ${CSRF_TOKEN:0:20}..."
    
    # Afficher plus d'informations de débogage
    echo -e "\n📋 Information de débogage :"
    echo "Page accessible : Oui (HTTP 200)"
    echo "Formulaires détectés :"
    echo "$HTML_CONTENT" | grep -c "<form" | xargs echo "Nombre de formulaires :"
    echo "$HTML_CONTENT" | grep -i "csrf" | head -2
    
    # Test de connexion (optionnel - enlevez les commentaires si nécessaire)
    # echo -e "\n3. Tentative de connexion..."
    # RESPONSE=$(curl -s -X POST \
    #     -H "Content-Type: application/x-www-form-urlencoded" \
    #     -H "Referer: https://web-production-555c.up.railway.app/admin/login/" \
    #     --data-urlencode "csrfmiddlewaretoken=$CSRF_TOKEN" \
    #     --data-urlencode "username=votre_admin" \
    #     --data-urlencode "password=votre_mot_de_passe" \
    #     -c cookies.txt \
    #     https://web-production-555c.up.railway.app/admin/login/)
    # 
    # if echo "$RESPONSE" | grep -q "dashboard\|admin\|Bienvenue\|302 Found"; then
    #     echo "✅ Connexion réussie !"
    # else
    #     echo "❌ Échec de connexion"
    #     echo "Réponse (premières 200 chars): ${RESPONSE:0:200}"
    # fi
else
    echo "❌ Impossible d'extraire le token CSRF"
    echo -e "\n🔍 Analyse de la page :"
    
    # Vérifier si la page contient un formulaire
    if echo "$HTML_CONTENT" | grep -q "<form"; then
        echo "✅ Formulaires détectés dans la page"
        echo "Nombre de formulaires : $(echo "$HTML_CONTENT" | grep -c "<form")"
        
        # Afficher les formulaires
        echo -e "\n📄 Extrait du formulaire de login :"
        echo "$HTML_CONTENT" | grep -A 10 -B 2 "login\|auth\|admin" | head -30
    else
        echo "❌ Aucun formulaire détecté"
        echo "La page pourrait rediriger ou être différente"
    fi
    
    echo -e "\n🎯 Actions recommandées :"
    echo "1. Visitez https://web-production-555c.up.railway.app/admin/login/ manuellement"
    echo "2. Vérifiez 'Inspecter l'élément' pour voir le formulaire"
    echo "3. Assurez-vous que DEBUG=True dans Railway Variables"
    echo "4. Vérifiez que Django sert bien le template d'admin"
fi

echo -e "\n✅ Test terminé"
