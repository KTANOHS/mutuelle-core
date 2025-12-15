#!/bin/bash
echo "🔐 TEST FINAL AVEC VOS IDENTIFIANTS"
echo "==================================="

python3 -c "
import requests
import re

url = 'https://web-production-555c.up.railway.app/admin/login/'
session = requests.Session()

print('1. Préparation de la requête...')
response = session.get(url)

# Extraire CSRF
csrf_match = re.search(r'csrfmiddlewaretoken.*value=\"([^\"]+)\"', response.text)
if not csrf_match:
    print('❌ CSRF non trouvé')
    exit(1)

csrf = csrf_match.group(1)
print(f'2. CSRF token: {csrf[:20]}...')

# Vos identifiants
credentials = [
    {'user': 'matrix', 'pass': 'transport744'},
    {'user': 'admin', 'pass': 'admin'},
    {'user': 'root', 'pass': 'root'},
]

print('\\n3. Test des identifiants...')
print('=' * 40)

for cred in credentials:
    print(f'\\n🔑 Test: {cred[\"user\"]}')
    
    data = {
        'csrfmiddlewaretoken': csrf,
        'username': cred['user'],
        'password': cred['pass'],
        'next': '/admin/'
    }
    
    headers = {
        'Referer': url,
        'Origin': 'https://web-production-555c.up.railway.app'
    }
    
    resp = session.post(url, data=data, headers=headers, allow_redirects=False)
    
    if resp.status_code == 302:
        print(f'   ✅ SUCCÈS ! Redirection détectée')
        print(f'   👤 Utilisateur: {cred[\"user\"]}')
        print(f'   🔐 Mot de passe: {cred[\"pass\"]}')
        print(f'   🌐 Connecté avec succès !')
        break
    elif resp.status_code == 200:
        if 'Please enter the correct username' in resp.text:
            print(f'   ❌ Identifiants incorrects')
        else:
            print(f'   ⚠️  Réponse 200 (vérifiez manuellement)')
    else:
        print(f'   ❌ Échec (HTTP {resp.status_code})')

print('\\n' + '=' * 40)
print('📋 Résumé:')
print('Si aucun succès, vous devez créer un superutilisateur:')
print('1. En local: python manage.py createsuperuser')
print('2. Ou sur Railway: railway run python manage.py createsuperuser')
print('\\n🌐 Votre URL admin: https://web-production-555c.up.railway.app/admin/')
"

echo -e "\n✅ Test terminé"
