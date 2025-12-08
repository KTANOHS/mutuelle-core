#!/bin/bash
# Script de diagnostic pour le projet Django - Pharmacien

echo "=================================================="
echo "DIAGNOSTIC DU PROJET DJANGO"
echo "Date: $(date)"
echo "Répertoire courant: $(pwd)"
echo "=================================================="

echo ""
echo "1. ENVIRONNEMENT VIRTUEL"
echo "--------------------------------------------------"
if [ -d "venv" ]; then
    echo "✓ Environnement virtuel trouvé"
    source venv/bin/activate
    echo "Environnement activé"
else
    echo "✗ Environnement virtuel non trouvé"
fi

echo ""
echo "2. VÉRIFICATION DES MODULES DJANGO"
echo "--------------------------------------------------"
python -c "
import sys
print('Python:', sys.version)
try:
    import django
    print('Django:', django.__version__)
    print('Chemin Django:', django.__path__[0])
except ImportError as e:
    print('✗ Django non installé:', e)
"

echo ""
echo "3. STRUCTURE DU PROJET"
echo "--------------------------------------------------"
echo "Arborescence:"
find . -type f -name "*.py" | grep -E "(models|views|urls)\.py$" | head -20

echo ""
echo "4. VÉRIFICATION DES MODÈLES PHARMACIEN"
echo "--------------------------------------------------"
python -c "
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
try:
    import django
    django.setup()
    
    # Vérifier les modèles pharmacien
    from django.apps import apps
    
    print('Applications installées:')
    for app in apps.get_app_configs():
        print(f'  - {app.name}')
    
    print('\nModèles dans pharmacien:')
    try:
        from pharmacien import models as pharmacien_models
        for attr in dir(pharmacien_models):
            if not attr.startswith('_') and attr[0].isupper():
                print(f'  - {attr}')
    except Exception as e:
        print(f'  Erreur: {e}')
        
    # Vérifier le modèle Ordonnance
    print('\nModèle Ordonnance:')
    try:
        from ordonnances.models import Ordonnance
        print('  ✓ Import réussi')
        print('  Champs disponibles:')
        for field in Ordonnance._meta.fields:
            print(f'    - {field.name} ({field.get_internal_type()})')
    except Exception as e:
        print(f'  ✗ Erreur: {e}')
        
except Exception as e:
    print(f'Erreur lors de l\'initialisation Django: {e}')
"

echo ""
echo "5. VÉRIFICATION DES MIGRATIONS"
echo "--------------------------------------------------"
python manage.py makemigrations --check --dry-run 2>/dev/null || echo "✗ Erreur lors de la vérification des migrations"

echo ""
echo "6. VÉRIFICATION DES ERREURS COURANTES"
echo "--------------------------------------------------"
echo "Vérification du problème date_validation..."

python -c "
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
try:
    import django
    django.setup()
    
    # Rechercher des modèles avec date_validation
    from django.apps import apps
    
    print('Recherche de champs date_validation dans les modèles:')
    models_with_date_validation = []
    for model in apps.get_models():
        for field in model._meta.fields:
            if 'date_validation' in field.name:
                models_with_date_validation.append(f'{model.__name__}.{field.name}')
    
    if models_with_date_validation:
        for item in models_with_date_validation:
            print(f'  ✓ {item}')
    else:
        print('  ✗ Aucun champ date_validation trouvé')
        
    # Vérifier le modèle GestionPharmacien
    print('\nVérification du modèle GestionPharmacien:')
    try:
        from pharmacien.models import GestionPharmacien
        print('  ✓ Modèle trouvé')
        print('  Champs disponibles:')
        for field in GestionPharmacien._meta.fields:
            print(f'    - {field.name} ({field.get_internal_type()})')
    except Exception as e:
        print(f'  ✗ Modèle non trouvé: {e}')
        
except Exception as e:
    print(f'Erreur: {e}')
"

echo ""
echo "7. VÉRIFICATION DES TEMPLATES"
echo "--------------------------------------------------"
echo "Templates pharmacien existants:"
ls -la templates/pharmacien/*.html 2>/dev/null | head -10

echo ""
echo "8. TEST DES IMPORTS CRITIQUES"
echo "--------------------------------------------------"
python -c "
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
try:
    import django
    django.setup()
    
    imports_a_tester = [
        'from core.utils import gerer_erreurs',
        'from django.contrib.auth.decorators import login_required',
        'from pharmacien.decorators import pharmacien_required',
        'from ordonnances.models import Ordonnance',
        'from django.shortcuts import render, redirect',
        'from django.contrib import messages',
    ]
    
    print('Test des imports:')
    for import_stmt in imports_a_tester:
        try:
            exec(import_stmt)
            print(f'  ✓ {import_stmt}')
        except Exception as e:
            print(f'  ✗ {import_stmt}')
            print(f'     Erreur: {e}')
            
except Exception as e:
    print(f'Erreur Django: {e}')
"

echo ""
echo "9. VÉRIFICATION DES VUES PHARMACIEN"
echo "--------------------------------------------------"
python -c "
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
try:
    import django
    django.setup()
    
    # Importer la vue problématique
    try:
        from pharmacien.views import historique_validation
        print('✓ Vue historique_validation importée')
        
        # Inspecter la vue
        import inspect
        source = inspect.getsource(historique_validation)
        lines = source.split('\n')
        print('Premières lignes de la vue:')
        for i, line in enumerate(lines[:15]):
            print(f'  {i+1}: {line}')
            
        # Vérifier les imports dans le module
        print('\nImports dans pharmacien/views.py:')
        import pharmacien.views
        for attr in dir(pharmacien.views):
            if not attr.startswith('_'):
                obj = getattr(pharmacien.views, attr)
                if hasattr(obj, '__module__'):
                    print(f'  - {attr} -> {obj.__module__}')
                    
    except Exception as e:
        print(f'✗ Erreur lors de l\'import de la vue: {e}')
        
except Exception as e:
    print(f'Erreur Django: {e}')
"

echo ""
echo "10. VÉRIFICATION DES URLS"
echo "--------------------------------------------------"
python -c "
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
try:
    import django
    django.setup()
    
    from django.urls import get_resolver, reverse, NoReverseMatch
    
    print('URLs pharmacien configurées:')
    try:
        from pharmacien.urls import urlpatterns
        for pattern in urlpatterns:
            print(f'  - {pattern.pattern} -> {pattern.name}')
    except Exception as e:
        print(f'  Erreur: {e}')
        
    print('\nTest des reverse URLs:')
    urls_a_tester = [
        'pharmacien:dashboard',
        'pharmacien:historique_validation',
        'pharmacien:detail_ordonnance',
    ]
    
    for url_name in urls_a_tester:
        try:
            url = reverse(url_name)
            print(f'  ✓ {url_name} -> {url}')
        except NoReverseMatch as e:
            print(f'  ✗ {url_name}: {e}')
            
except Exception as e:
    print(f'Erreur: {e}')
"

echo ""
echo "11. SCRIPT DE CORRECTION AUTOMATIQUE"
echo "--------------------------------------------------"
cat > /tmp/correction_historique.py << 'EOF'
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from pharmacien.models import GestionPharmacien
from ordonnances.models import Ordonnance

print("=== VÉRIFICATION DES DONNÉES ===")

# Compter les ordonnances validées
try:
    ordonnances_validees = Ordonnance.objects.filter(statut='validée').count()
    print(f"Ordonnances validées dans la base: {ordonnances_validees}")
except Exception as e:
    print(f"Erreur avec Ordonnance: {e}")

# Compter les GestionPharmacien
try:
    gestion_count = GestionPharmacien.objects.count()
    print(f"Entrées GestionPharmacien: {gestion_count}")
    
    if gestion_count > 0:
        sample = GestionPharmacien.objects.first()
        print(f"Exemple GestionPharmacien:")
        print(f"  - Pharmacien: {sample.pharmacien}")
        print(f"  - Ordonnance: {sample.ordonnance}")
        print(f"  - Date validation: {getattr(sample, 'date_validation', 'Non disponible')}")
        print(f"  - Autres attributs: {[attr for attr in dir(sample) if not attr.startswith('_')][:10]}")
except Exception as e:
    print(f"Erreur avec GestionPharmacien: {e}")

print("\n=== SUGGESTIONS DE CODE ===")
print("""
Option 1 (si GestionPharmacien existe):
    validations = GestionPharmacien.objects.filter(
        pharmacien=request.user
    ).select_related(
        'ordonnance__patient',
        'ordonnance__medecin'
    ).order_by('-date_validation')

Option 2 (fallback sur Ordonnance):
    historique = Ordonnance.objects.filter(
        gestion_pharmacien__pharmacien=request.user,
        statut='validée'
    ).select_related(
        'patient', 'medecin'
    ).order_by('-date_modification')
""")
EOF

python /tmp/correction_historique.py

echo ""
echo "12. VÉRIFICATION DE LA BASE DE DONNÉES"
echo "--------------------------------------------------"
python manage.py check

echo ""
echo "13. RÉCAPITULATIF DES CORRECTIONS NÉCESSAIRES"
echo "=================================================="
echo "Problèmes identifiés:"
echo "1. Le champ 'date_validation' n'existe pas dans le modèle Ordonnance"
echo "2. Utiliser 'date_modification' ou rechercher dans GestionPharmacien"
echo ""
echo "Solutions proposées:"
echo "1. Vérifier si le modèle GestionPharmacien existe avec date_validation"
echo "2. Si oui, l'utiliser pour l'historique"
echo "3. Sinon, utiliser Ordonnance.date_modification"
echo ""
echo "Code recommandé pour historique_validation:"
cat << 'EOF'
@login_required
@pharmacien_required
@gerer_erreurs
def historique_validation(request):
    try:
        # Essayer d'abord avec GestionPharmacien
        try:
            from pharmacien.models import GestionPharmacien
            validations = GestionPharmacien.objects.filter(
                pharmacien=request.user
            ).select_related(
                'ordonnance__patient',
                'ordonnance__medecin'
            ).order_by('-date_validation')
            
            # Adapter les données pour le template
            data_for_template = []
            for validation in validations:
                data_for_template.append({
                    'ordonnance': {
                        'id': validation.ordonnance.id,
                        'ordonnance_medecin': {
                            'patient': validation.ordonnance.patient,
                            'medecin': validation.ordonnance.medecin,
                            'date_prescription': validation.ordonnance.date_prescription,
                        }
                    },
                    'date_validation': validation.date_validation,
                })
            
        except ImportError:
            # Fallback sur Ordonnance
            from ordonnances.models import Ordonnance
            validations_qs = Ordonnance.objects.filter(
                gestion_pharmacien__pharmacien=request.user,
                statut='validée'
            ).select_related('patient', 'medecin')
            
            data_for_template = []
            for ordonnance in validations_qs:
                data_for_template.append({
                    'ordonnance': {
                        'id': ordonnance.id,
                        'ordonnance_medecin': {
                            'patient': ordonnance.patient,
                            'medecin': ordonnance.medecin,
                            'date_prescription': ordonnance.date_prescription,
                        }
                    },
                    'date_validation': ordonnance.date_modification,
                })
        
        # Pagination
        from django.core.paginator import Paginator
        paginator = Paginator(data_for_template, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {'validations': page_obj}
        return render(request, 'pharmacien/historique.html', context)
        
    except Exception as e:
        logger.error(f"Erreur historique: {e}")
        return redirect('pharmacien:dashboard')
EOF

echo ""
echo "=================================================="
echo "DIAGNOSTIC TERMINÉ"
echo "Pour appliquer la correction:"
echo "1. Copiez le code recommandé dans pharmacien/views.py"
echo "2. Vérifiez que le modèle GestionPharmacien existe"
echo "3. Redémarrez le serveur: python manage.py runserver"
echo "=================================================="