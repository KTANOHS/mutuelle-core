#!/bin/bash
echo "🔍 VÉRIFICATION DE L'APPLICATION EN COURS D'EXÉCUTION"
echo "===================================================="

# 1. Vérifier si l'application répond
echo "1. Test de l'application Railway..."
URL="https://web-production-555c.up.railway.app"
python3 -c "
import requests
import time

print('Test de connexion à l\'application...')
max_attempts = 5

for i in range(max_attempts):
    try:
        response = requests.get('$URL', timeout=10)
        print(f'Tentative {i+1}/{max_attempts}: HTTP {response.status_code}')
        
        if response.status_code == 200:
            print('✅ Application accessible et répond !')
            print(f'   Titre de la page: ', end='')
            
            # Chercher le titre
            import re
            title_match = re.search(r'<title>(.*?)</title>', response.text)
            if title_match:
                print(title_match.group(1))
            else:
                print('Non trouvé')
            break
        else:
            print(f'   ❌ Code inattendu: {response.status_code}')
            
    except requests.exceptions.RequestException as e:
        print(f'Tentative {i+1}/{max_attempts}: ❌ {e}')
    
    if i < max_attempts - 1:
        print('   ⏳ Attente 3 secondes...')
        time.sleep(3)
else:
    print('❌ Impossible de se connecter à l\'application après plusieurs tentatives')
"

# 2. Test du formulaire admin login
echo -e "\n2. Test du formulaire admin..."
python3 -c "
import requests
import re

url = '$URL/admin/login/'
try:
    print(f'Test de: {url}')
    response = requests.get(url, timeout=10)
    
    if response.status_code == 200:
        print(f'✅ Page admin accessible (HTTP {response.status_code})')
        
        # Vérifier CSRF
        if 'csrfmiddlewaretoken' in response.text:
            print('✅ Token CSRF présent dans le formulaire')
            
            # Extraire le token pour démonstration
            csrf_match = re.search(r'csrfmiddlewaretoken.*value=\"([^\"]+)\"', response.text)
            if csrf_match:
                print(f'   Token (tronqué): {csrf_match.group(1)[:20]}...')
            else:
                print('   ⚠️  Token présent mais non extractible')
        else:
            print('❌ Token CSRF absent - problème de configuration')
            
        # Vérifier DEBUG mode
        if 'DEBUG = True' in response.text:
            print('✅ Mode DEBUG activé (bon pour le développement)')
        else:
            print('⚠️  Mode DEBUG non détecté')
            
    else:
        print(f'❌ Page admin inaccessible (HTTP {response.status_code})')
        
except Exception as e:
    print(f'❌ Erreur: {e}')
"

# 3. Instructions pour créer un superutilisateur
echo -e "\n3. 📋 ÉTAPES SUIVANTES:"
echo "   Si l'application répond et le formulaire admin contient CSRF:"
echo ""
echo "   A. Créez un superutilisateur IMMÉDIATEMENT:"
echo "      Méthode Railway CLI (recommandée):"
echo "      railway run python manage.py createsuperuser"
echo ""
echo "   B. OU via l'interface Railway:"
echo "      1. Allez sur https://railway.app"
echo "      2. Sélectionnez votre projet"
echo "      3. Cliquez sur 'Console' ou 'Shell'"
echo "      4. Exécutez: python manage.py createsuperuser"
echo ""
echo "   C. Connectez-vous ensuite à:"
echo "      https://web-production-555c.up.railway.app/admin/"
