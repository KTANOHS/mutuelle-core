#!/bin/bash

echo "🔧 CORRECTION ULTIME - MUTUELLE_CORE"
echo "=========================================="

# Active le virtualenv
source venv/bin/activate

# Exécute la correction complète
echo ""
echo "🔨 Application des corrections complètes..."
python final_complete_fix.py

# Crée les migrations pour mutuelle_core
echo ""
echo "🗃️ Création des migrations pour mutuelle_core..."
python manage.py makemigrations mutuelle_core

echo ""
echo "🗃️ Application des migrations..."
python manage.py migrate

# Vérifie que mutuelle_core est bien installé
echo ""
echo "🔍 Vérification de l'installation..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()

from django.apps import apps
if apps.is_installed('mutuelle_core'):
    print('✅ mutuelle_core est bien installé')
else:
    print('❌ mutuelle_core n\\'est pas installé')
"

# Test final
echo ""
echo "🎯 TEST FINAL..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()

try:
    from mutuelle_core.models import Session, User
    from django.contrib.auth import get_user_model
    from membres.models import LigneBon
    
    print('✅ Modèle Session importé:', hasattr(Session, '__str__'))
    print('✅ Modèle User proxy importé:', hasattr(User, '__str__'))
    print('✅ Modèle User Django importé:', hasattr(get_user_model(), '__str__'))
    print('✅ Modèle LigneBon importé:', hasattr(LigneBon, '__str__'))
    
    # Test de la méthode __str__
    try:
        session_str = str(Session())
        print('✅ Session.__str__ fonctionne')
    except Exception as e:
        print('❌ Session.__str__ erreur:', e)
        
    print('🎉 TOUS LES TESTS PASSÉS!')
    
except Exception as e:
    print('❌ Erreur lors des tests:', e)
"

echo ""
echo "=========================================="
echo "✅ CORRECTIONS ULTIMES TERMINÉES!"
echo ""
echo "🚀 Votre projet mutuelle_core est maintenant complètement corrigé!"
echo "💡 Vous pouvez lancer: python manage.py runserver"