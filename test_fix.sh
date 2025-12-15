#!/bin/bash
# test_fix.sh

echo "🧪 Test après correction..."

# Test 1: Le fichier existe-t-il ?
echo "1. Vérification des fichiers..."
ls -la agents/affichage_unifie.py agents/views.py

# Test 2: Y a-t-il encore des imports problématiques ?
echo -e "\n2. Vérification des imports problématiques..."
if grep -q "from affichage_unifie import" agents/views.py; then
    echo "❌ Il reste des imports problématiques:"
    grep -n "from affichage_unifie import" agents/views.py
else
    echo "✅ Aucun import problématique trouvé"
fi

# Test 3: Syntaxe Python valide ?
echo -e "\n3. Vérification syntaxique..."
python3 -m py_compile agents/views.py && echo "✅ Syntaxe Python valide"

# Test 4: Test simple sans Django
echo -e "\n4. Test d'import simple..."
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    # Import de base sans déclencher Django
    import agents
    print('✅ Module agents importable')
    
    # Vérification du contenu
    import inspect
    if hasattr(agents, 'views'):
        print('✅ Module views présent')
        views_content = dir(agents.views)
        print(f'   Fonctions disponibles: {[f for f in views_content if not f.startswith(\"_\")]}')
    else:
        print('⚠️  Module views manquant')
        
except Exception as e:
    print(f'❌ Erreur: {e}')
    import traceback
    traceback.print_exc()
"

echo -e "\n✅ Test terminé !"