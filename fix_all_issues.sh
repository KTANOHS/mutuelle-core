#!/bin/bash
# Correction de tous les problèmes identifiés

echo "🔧 CORRECTION DES PROBLÈMES IDENTIFIÉS"
echo "======================================"

# 1. Installer psycopg2-binary
echo "📦 Installation de psycopg2-binary..."
pip install psycopg2-binary

# 2. Vérifier et corriger ALLOWED_HOSTS
echo "🌐 Correction de ALLOWED_HOSTS..."
python -c "
import re

# Lire le fichier settings.py
with open('mutuelle_core/settings.py', 'r') as f:
    content = f.read()

# Vérifier si ALLOWED_HOSTS contient .onrender.com
if '.onrender.com' not in content:
    print('⚠️  .onrender.com non trouvé dans ALLOWED_HOSTS')
    
    # Ajouter une configuration conditionnelle si nécessaire
    if 'RENDER = os.environ.get' not in content:
        # Trouver la ligne ALLOWED_HOSTS et la remplacer
        import re
        pattern = r'ALLOWED_HOSTS\s*=\s*\[[^\]]*\]'
        
        new_content = '''
# Détecter si on est sur Render
RENDER = os.environ.get('RENDER') == 'true'

if RENDER:
    # Mode production sur Render
    ALLOWED_HOSTS = [
        '.onrender.com',
        'mutuelle-core-18.onrender.com',
        'mutuelle-core-17.onrender.com',
        'mutuelle-core.onrender.com',
    ]
else:
    # Mode développement local
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        '[::1]',
        '0.0.0.0',
        '*',  # Pour le développement seulement
    ]
'''
        
        # Remplacer l'ancienne configuration
        if re.search(pattern, content):
            content = re.sub(pattern, new_content, content)
            print('✅ Configuration ALLOWED_HOSTS mise à jour')
        else:
            # Ajouter après les imports
            import_section = 'import os'
            if import_section in content:
                content = content.replace(import_section, import_section + new_content)
                print('✅ Configuration ALLOWED_HOSTS ajoutée')
            else:
                print('❌ Impossible de mettre à jour ALLOWED_HOSTS')
    
    # Écrire le fichier modifié
    with open('mutuelle_core/settings.py', 'w') as f:
        f.write(content)
else:
    print('✅ ALLOWED_HOSTS contient déjà .onrender.com')
"

# 3. Appliquer les migrations
echo "🔄 Application des migrations..."
python manage.py migrate

# 4. Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# 5. Créer un superutilisateur
echo "👤 Création d'un superutilisateur de test..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()
from django.contrib.auth import get_user_model

User = get_user_model()
username = 'admin'
email = 'admin@mutuelle.com'
password = 'Admin123!'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'✅ Superutilisateur créé: {username} / {password}')
else:
    print(f'✅ Superutilisateur existe déjà: {username}')
"

# 6. Tester les URLs
echo "🔗 Test des URLs..."
python test_urls.py

# 7. Exécuter le diagnostic final
echo "📊 Diagnostic final..."
python run_diagnostic.py

echo ""
echo "✅ CORRECTIONS TERMINÉES!"
echo ""
echo "📝 Prochaines étapes:"
echo "1. Testez l'application: python manage.py runserver"
echo "2. Visitez: http://localhost:8000"
echo "3. Connectez-vous avec: admin / Admin123!"
echo "4. Poussez les modifications: git add . && git commit -m 'Corrections' && git push"
echo "5. Render déploiera automatiquement"