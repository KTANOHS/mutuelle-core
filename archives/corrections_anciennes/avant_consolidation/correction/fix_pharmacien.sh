#!/bin/bash
# Script de correction rapide pour pharmacien/views.py

echo "=== CORRECTION DES PROBLÈMES IDENTIFIÉS ==="

# 1. Créer un fichier de correction pour views.py
cat > /tmp/fix_pharmacien_views.py << 'EOF'
import os
import sys
import django

# Trouver le bon chemin pour les settings
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_path)

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    django.setup()
except:
    # Essayer un autre nom de settings
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
        django.setup()
    except:
        print("Impossible de charger les settings Django")
        sys.exit(1)

# Maintenant, analysons la structure
print("=== STRUCTURE DES MODÈLES ===")

# Vérifier les modèles disponibles
try:
    from django.apps import apps
    
    # Afficher tous les modèles
    print("Modèles disponibles dans l'application:")
    for model in apps.get_models():
        print(f"  - {model._meta.app_label}.{model.__name__}")
        
except Exception as e:
    print(f"Erreur: {e}")

# Vérifier spécifiquement les modèles pharmacien
print("\n=== MODÈLES PHARMACIEN ===")
try:
    from pharmacien.models import *
    print("Modèles importés depuis pharmacien.models:")
    for attr in dir():
        if not attr.startswith('_') and attr[0].isupper():
            print(f"  - {attr}")
except Exception as e:
    print(f"Erreur: {e}")

# Vérifier OrdonnancePharmacien
print("\n=== ORDONNANCEPHARMACIEN ===")
try:
    from pharmacien.models import OrdonnancePharmacien
    print("Champs de OrdonnancePharmacien:")
    for field in OrdonnancePharmacien._meta.fields:
        print(f"  - {field.name} ({field.get_internal_type()})")
        
    # Vérifier les relations
    print("\nRelations de OrdonnancePharmacien:")
    for field in OrdonnancePharmacien._meta.get_fields():
        if field.is_relation:
            print(f"  - {field.name} -> {field.related_model.__name__ if field.related_model else 'None'}")
            
except Exception as e:
    print(f"Erreur: {e}")

print("\n=== SUGGESTION DE CODE POUR historique_validation ===")
EOF

python /tmp/fix_pharmacien_views.py

echo ""
echo "=== CRÉATION DES FICHIERS MANQUANTS ==="

# 2. Créer le fichier decorators.py manquant
cat > pharmacien/decorators.py << 'EOF'
"""
Décorateurs pour les vues pharmacien
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from core.utils import est_pharmacien

def pharmacien_required(view_func):
    """
    Décorateur qui vérifie que l'utilisateur est un pharmacien
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not est_pharmacien(request.user):
            messages.error(request, "Accès réservé aux pharmaciens.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
EOF

echo "✓ pharmacien/decorators.py créé"

# 3. Créer une version corrigée de la vue historique_validation
cat > /tmp/historique_corrige.py << 'EOF'
"""
Version corrigée de historique_validation
"""
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from pharmacien.decorators import pharmacien_required

# Importer gerer_erreurs depuis core.utils si disponible
try:
    from core.utils import gerer_erreurs
except ImportError:
    # Créer une version locale si non disponible
    def gerer_erreurs(view_func):
        from functools import wraps
        import logging
        logger = logging.getLogger(__name__)
        
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            try:
                return view_func(request, *args, **kwargs)
            except Exception as e:
                logger.error(f"Erreur dans {view_func.__name__}: {e}")
                messages.error(request, "Une erreur est survenue.")
                return redirect('pharmacien:dashboard')
        return _wrapped_view

logger = logging.getLogger(__name__)

@login_required
@pharmacien_required
@gerer_erreurs
def historique_validation(request):
    """Affiche l'historique des ordonnances validées par le pharmacien"""
    try:
        # Importer les modèles nécessaires
        from pharmacien.models import OrdonnancePharmacien
        from django.utils import timezone
        from datetime import timedelta
        
        # Récupérer l'historique des validations
        # Utiliser OrdonnancePharmacien qui a le champ date_validation
        validations_qs = OrdonnancePharmacien.objects.filter(
            pharmacien=request.user
        ).select_related(
            'ordonnance_medecin__patient',
            'ordonnance_medecin__medecin'
        ).order_by('-date_validation')
        
        # Adapter les données pour le template
        validations_list = []
        for validation in validations_qs:
            ordonnance = validation.ordonnance_medecin
            validations_list.append({
                'ordonnance': {
                    'id': ordonnance.id,
                    'ordonnance_medecin': {
                        'patient': ordonnance.patient,
                        'medecin': ordonnance.medecin,
                        'date_prescription': ordonnance.date_prescription,
                    }
                },
                'date_validation': validation.date_validation,
            })
        
        # Pagination
        paginator = Paginator(validations_list, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Statistiques
        stats = {
            'total': validations_qs.count(),
            'mois_courant': validations_qs.filter(
                date_validation__month=timezone.now().month,
                date_validation__year=timezone.now().year
            ).count(),
            'semaine_courante': validations_qs.filter(
                date_validation__gte=timezone.now() - timedelta(days=7)
            ).count(),
        }
        
        context = {
            'validations': page_obj,
            'stats': stats,
            'title': 'Historique des validations'
        }
        return render(request, 'pharmacien/historique.html', context)
        
    except Exception as e:
        logger.error(f"Erreur dans historique_validation : {e}")
        messages.error(request, "Erreur lors du chargement de l'historique.")
        return redirect('pharmacien:dashboard')

print("Code prêt à être copié dans pharmacien/views.py")
print("Remplacez la fonction historique_validation existante par celle-ci")
EOF

echo ""
echo "=== APPLICATIONS DES CORRECTIONS ==="

# 4. Afficher les corrections à appliquer
cat << 'EOF'

=== INSTRUCTIONS POUR CORRIGER ===

1. AJOUTER LES IMPORTS MANQUANTS dans pharmacien/views.py :

Au début du fichier, ajoutez:
-------------------------------
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from pharmacien.decorators import pharmacien_required

# Importer gerer_erreurs ou créer une version locale
try:
    from core.utils import gerer_erreurs
except ImportError:
    # Créer une version locale si non disponible
    def gerer_erreurs(view_func):
        from functools import wraps
        import logging
        logger = logging.getLogger(__name__)
        
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            try:
                return view_func(request, *args, **kwargs)
            except Exception as e:
                logger.error(f"Erreur dans {view_func.__name__}: {e}")
                messages.error(request, "Une erreur est survenue.")
                return redirect('pharmacien:dashboard')
        return _wrapped_view

logger = logging.getLogger(__name__)
-------------------------------

2. REMPLACER la fonction historique_validation par:

Copiez le code depuis /tmp/historique_corrige.py

3. VÉRIFIER que le fichier pharmacien/decorators.py existe

4. REDÉMARRER le serveur:
   python manage.py runserver

=== VÉRIFICATION RAPIDE ===

Pour vérifier que tout fonctionne:
1. python manage.py check
2. Accédez à: http://127.0.0.1:8000/pharmacien/historique/

EOF

# 5. Vérifier la structure actuelle de views.py
echo ""
echo "=== VÉRIFICATION DE LA VUE ACTUELLE ==="
if [ -f "pharmacien/views.py" ]; then
    echo "Lignes autour de historique_validation (ligne 280):"
    sed -n '270,290p' pharmacien/views.py
else
    echo "pharmacien/views.py non trouvé"
fi

echo ""
echo "=== CORRECTION TERMINÉE ==="
echo "Suivez les instructions ci-dessus pour appliquer les corrections."