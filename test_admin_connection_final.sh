#!/bin/bash
echo "🔐 TEST DE CONNEXION ADMIN FINAL"
echo "================================="

URL="https://web-production-555c.up.railway.app"
LOGIN_URL="$URL/admin/login/"

# Script Python pour tester la connexion
python3 -c "
import requests
import re
from urllib.parse import urljoin

print('🚀 Test de connexion à l\\'admin Django')
print('=' * 50)

# Créer une session
session = requests.Session()

# 1. Obtenir la page de login
print('1. Obtention de la page de login...')
response = session.get('$LOGIN_URL')
print(f'   Status: {response.status_code}')

if response.status_code != 200:
    print('❌ Impossible d\\'accéder à la page de login')
    exit(1)

# 2. Extraire le token CSRF
csrf_match = re.search(r'csrfmiddlewaretoken.*value=\"([^\"]+)\"', response.text)
if not csrf_match:
    print('❌ Aucun token CSRF trouvé')
    print('   Extrait HTML:')
    print(response.text[:200])
    exit(1)

csrf_token = csrf_match.group(1)
print(f'2. Token CSRF extrait: {csrf_token[:20]}...')

# 3. Demander les identifiants
print('\\n3. Entrez vos identifiants admin:')
print('   (Les identifiants que vous avez créés avec createsuperuser)')
username = input('   Nom d\\'utilisateur: ')
password = input('   Mot de passe: ')

# 4. Préparer la requête POST
data = {
    'csrfmiddlewaretoken': csrf_token,
    'username': username,
    'password': password,
    'next': '/admin/'
}

headers = {
    'Referer': '$LOGIN_URL',
    'Origin': '$URL',
}

print('\\n4. Tentative de connexion...')
login_response = session.post('$LOGIN_URL', data=data, headers=headers, allow_redirects=False)

print(f'   Status: {login_response.status_code}')
print(f'   Redirection: {login_response.headers.get(\"Location\", \"Aucune\")}')

# 5. Analyser la réponse
if login_response.status_code == 302:
    redirect_url = login_response.headers.get('Location')
    if redirect_url.startswith('/'):
        redirect_url = '$URL' + redirect_url
    
    print('\\n✅ REDIRECTION DÉTECTÉE !')
    print(f'5. Suivi vers: {redirect_url}')
    
    # Suivre la redirection
    admin_response = session.get(redirect_url)
    
    if 'Site administration' in admin_response.text or 'Django administration' in admin_response.text:
        print('🎉 SUCCÈS COMPLET ! Vous êtes connecté à l\\'admin Django.')
        print('\\n📋 Informations:')
        print(f'   - URL admin: {redirect_url}')
        print(f'   - Session active: Oui')
        
        # Extraire le titre
        title_match = re.search(r'<title>(.*?)</title>', admin_response.text)
        if title_match:
            print(f'   - Titre: {title_match.group(1)}')
            
    else:
        print('⚠️  Connecté mais page différente')
        # Vérifier si c'est la page d'admin
        if 'admin' in redirect_url:
            print('   Probablement connecté à l\\'admin')
            
elif login_response.status_code == 200:
    print('\\n⚠️  Page retournée sans redirection')
    
    # Chercher les messages d'erreur
    if 'Please enter the correct username' in login_response.text:
        print('❌ Identifiants incorrects')
        print('   Vérifiez votre nom d\\'utilisateur et mot de passe')
    else:
        print('   Page reçue (vérifiez manuellement):')
        print('   https://web-production-555c.up.railway.app/admin/login/')
        
elif login_response.status_code == 403:
    print('\\n❌ ERREUR 403 FORBIDDEN')
    
    # Analyser l'erreur
    if 'CSRF' in login_response.text:
        print('   Problème CSRF détecté')
        
        # Vérifier la raison spécifique
        reason_match = re.search(r'<pre>(.*?)</pre>', login_response.text, re.DOTALL)
        if reason_match:
            reason = reason_match.group(1).strip()
            print(f'   Raison: {reason}')
            
            if 'Origin checking failed' in reason:
                print('   Solution: Vérifiez CSRF_TRUSTED_ORIGINS dans settings.py')
            elif 'CSRF cookie not set' in reason:
                print('   Solution: Vérifiez les cookies dans votre navigateur')
    else:
        print('   Erreur 403 non liée à CSRF')
        
else:
    print(f'\\n⚠️  Code HTTP inattendu: {login_response.status_code}')

print('\\n✅ Test terminé')
"

# Instructions supplémentaires
echo -e "\n📋 Si la connexion échoue:"
echo "1. Vérifiez que vous avez créé un superutilisateur:"
echo "   python manage.py createsuperuser"
echo "2. Si vous n'avez pas encore de superutilisateur, créez-en un localement"
echo "3. Poussez la base de données ou recréez l'utilisateur sur Railway"
