#!/bin/bash
# DIAGNOSTIC RAPIDE PHARMACIEN

echo "=== DIAGNOSTIC RAPIDE PHARMACIEN ==="
echo "Exécuté le: $(date)"
echo ""

# Vérifications rapides
check() {
    echo -n "Vérification de $1... "
    if $2; then
        echo "✓ OK"
    else
        echo "✗ ÉCHEC"
    fi
}

# 1. Environnement
check "Environnement virtuel" "[ -n \"$VIRTUAL_ENV\" ]"

# 2. Django
check "Django installé" "python -c 'import django' 2>/dev/null"

# 3. Application pharmacien
check "Application pharmacien" "python -c 'import pharmacien' 2>/dev/null"

# 4. Modèle OrdonnancePharmacien
check "Modèle OrdonnancePharmacien" "python -c 'from pharmacien.models import OrdonnancePharmacien' 2>/dev/null"

# 5. Vue historique_validation
check "Vue historique_validation" "python -c 'from pharmacien.views import historique_validation' 2>/dev/null"

# 6. Template historique
check "Template historique" "[ -f \"templates/pharmacien/historique_validation.html\" ]"

# 7. URLs
check "URLs pharmacien" "[ -f \"pharmacien/urls.py\" ]"

# 8. Décorateurs
check "Décorateur pharmacien_required" "[ -f \"pharmacien/decorators.py\" ]"

# Test rapide de la vue
echo ""
echo "=== TEST DE LA VUE historique_validation ==="
python << 'PYTHON_TEST'
import os
import sys
import django

sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    # Importer la vue
    from pharmacien.views import historique_validation
    print("✓ Vue importée avec succès")
    
    # Vérifier les décorateurs
    import inspect
    source = inspect.getsource(historique_validation)
    
    checks = [
        ('@login_required', 'Décorateur login_required'),
        ('@pharmacien_required', 'Décorateur pharmacien_required'),
        ('@gerer_erreurs', 'Décorateur gerer_erreurs'),
        ('OrdonnancePharmacien', 'Utilise le bon modèle'),
        ('date_validation', 'Utilise date_validation'),
        ('.order_by(', 'Trie les résultats'),
    ]
    
    for text, description in checks:
        if text in source:
            print(f"✓ {description}")
        else:
            print(f"✗ {description} - NON TROUVÉ")
            
except Exception as e:
    print(f"✗ Erreur: {e}")
PYTHON_TEST

# Vérification finale
echo ""
echo "=== VÉRIFICATION FINALE ==="
echo "Pour un test complet, exécutez:"
echo "  python manage.py runserver"
echo "  Puis accédez à: http://127.0.0.1:8000/pharmacien/historique/"
echo ""
echo "Si des erreurs persistent, vérifiez:"
echo "1. Les logs du serveur Django"
echo "2. La console JavaScript du navigateur"
echo "3. Les permissions de la base de données"
