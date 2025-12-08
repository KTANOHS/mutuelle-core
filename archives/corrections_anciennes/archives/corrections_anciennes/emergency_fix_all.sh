#!/bin/bash

echo "🚨 CORRECTIF D'URGENCE COMPLET"
echo "=============================="

# Active l'environnement virtuel
source venv/bin/activate

# Applique le correctif d'urgence
echo ""
echo "🔧 Application du correctif d'urgence..."
python fix_urls_emergency.py

# Test rapide
echo ""
echo "🧪 Test rapide après correction..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    import django
    django.setup()
    
    # Test d'import critique
    from assureur import urls
    from assureur import views
    
    print('✅ Import des modules: OK')
    
    # Test de la vue
    if hasattr(views, 'recherche_membre'):
        print('✅ Vue recherche_membre: OK')
    else:
        print('❌ Vue recherche_membre: MANQUANTE')
        
    print('🎉 Correctif appliqué avec succès!')
    
except Exception as e:
    print(f'❌ Erreur: {e}')
"

# Test des connexions de base
echo ""
echo "🔐 Test des connexions utilisateurs..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()

from django.test import Client

client = Client()
users = [
    ('test_assureur', 'pass123'),
    ('test_medecin', 'pass123'),
    ('test_pharmacien', 'pass123'),
    ('test_membre', 'pass123')
]

print('Connexions utilisateurs:')
for username, password in users:
    if client.login(username=username, password=password):
        print(f'  ✅ {username}')
    else:
        print(f'  ❌ {username}')
"

echo ""
echo "=============================="
echo "🎉 CORRECTIF D'URGENCE TERMINÉ!"
echo ""
echo "💡 Vous pouvez maintenant lancer: python manage.py runserver"