#!/bin/bash
echo "🧪 TEST SIMPLE DE CONNEXION GLORIA1"
echo "=================================="

# Test 1: Avec point d'exclamation
echo "Test 1: Avec 'Pharmacien123!'"
python manage.py shell -c "
from django.contrib.auth import authenticate
user = authenticate(username='GLORIA1', password='Pharmacien123!')
if user:
    print('✅ SUCCÈS avec Pharmacien123!')
    print(f'   User: {user.username}')
else:
    print('❌ ÉCHEC avec Pharmacien123!')
"

echo ""
echo "Test 2: Sans point d'exclamation"
python manage.py shell -c "
from django.contrib.auth import authenticate
user = authenticate(username='GLORIA1', password='Pharmacien123')
if user:
    print('✅ SUCCÈS avec Pharmacien123')
    print(f'   User: {user.username}')
else:
    print('❌ ÉCHEC avec Pharmacien123')
"

echo ""
echo "Test 3: Vérification directe"
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='GLORIA1')
print(f'User: {user.username}')
print(f'Password hash: {user.password[:50]}...')
print(f'is_active: {user.is_active}')

# Test tous les mots de passe possibles
passwords = ['Pharmacien123!', 'Pharmacien123', 'GLORIA1', '']
for pwd in passwords:
    if user.check_password(pwd):
        print(f'✅ Mot de passe trouvé: \"{pwd}\"')
        break
else:
    print('❌ Aucun mot de passe ne correspond')
"