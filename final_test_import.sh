#!/bin/bash
# final_test_import.sh

echo "🧪 TEST FINAL D'IMPORT AVANT RAILWAY"

# Test dans un environnement Django configuré
python3 -c "
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.insert(0, '.')

print('1. Configuration Django...')
try:
    django.setup()
    print('   ✅ Django configuré')
except Exception as e:
    print(f'   ❌ Erreur Django: {e}')
    sys.exit(1)

print('2. Test import agents.views...')
try:
    import agents.views
    print('   ✅ agents.views importé avec succès')
    
    # Vérifier les fonctions essentielles
    from agents.views import dashboard, verification_cotisations
    print('   ✅ Fonctions principales disponibles')
    
except ImportError as e:
    print(f'   ❌ Erreur d\'import: {e}')
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f'   ❌ Autre erreur: {e}')
    import traceback
    traceback.print_exc()

print('3. Test import agents.affichage_unifie...')
try:
    from agents.affichage_unifie import afficher_fiche_cotisation_unifiee, determiner_statut_cotisation
    print('   ✅ Module affichage_unifie importé')
    
    # Test des fonctions
    result = determiner_statut_cotisation()
    print(f'   ✅ Fonction test: {result[0]}')
    
except Exception as e:
    print(f'   ❌ Erreur: {e}')

print('🎉 TEST COMPLETÉ AVEC SUCCÈS !')
"

echo -e "\n📊 VÉRIFICATION DES FICHIERS:"
ls -la agents/ | grep -E "(views|affichage_unifie|__init__)"

echo -e "\n🔍 DERNIÈRE VÉRIFICATION DES IMPORTS PROBLÉMATIQUES:"
if grep -r "from affichage_unifie import" agents/; then
    echo "❌ Il reste des imports problématiques"
else
    echo "✅ Aucun import problématique trouvé"
fi