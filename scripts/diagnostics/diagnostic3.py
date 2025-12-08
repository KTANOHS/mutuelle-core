#!/usr/bin/env python3
"""
DIAGNOSTIC COMPLET DE L'APPLICATION DJANGO
Version 2.0 - Vérifications approfondies
"""

import os
import sys
import django
import traceback
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ ERREUR Configuration Django: {e}")
    sys.exit(1)

# ============================================================================
# PARTIE 1: IMPORT DES MODULES
# ============================================================================

print("=" * 80)
print("DIAGNOSTIC DJANGO - VÉRIFICATIONS COMPLÈTES")
print("=" * 80)

def check_module(module_name, import_path=None):
    """Vérifie si un module peut être importé"""
    try:
        if import_path:
            module = __import__(import_path, fromlist=[module_name])
        else:
            module = __import__(module_name)
        print(f"✅ Module {module_name} importé avec succès")
        return module
    except ImportError as e:
        print(f"❌ Module {module_name} non trouvé: {e}")
        return None
    except Exception as e:
        print(f"⚠️  Erreur avec {module_name}: {e}")
        return None

# Liste des modules critiques
modules_to_check = [
    ('django', 'django'),
    ('assureur', 'assureur'),
    ('membres', 'membres'),
    ('agents', 'agents'),
    ('soins', 'soins'),
    ('medecin', 'medecin'),
]

for module_name, import_path in modules_to_check:
    check_module(module_name, import_path)

# ============================================================================
# PARTIE 2: VÉRIFICATION DES MODÈLES
# ============================================================================

print("\n" + "=" * 80)
print("VÉRIFICATION DES MODÈLES")
print("=" * 80)

from django.apps import apps

def check_model(model_name, app_label=None):
    """Vérifie si un modèle existe"""
    try:
        if app_label:
            model = apps.get_model(app_label, model_name)
        else:
            # Chercher dans toutes les apps
            model = None
            for app_config in apps.get_app_configs():
                try:
                    model = apps.get_model(app_config.label, model_name)
                    if model:
                        break
                except LookupError:
                    continue
            
        if model:
            print(f"✅ Modèle {model_name} trouvé dans {model._meta.app_label}")
            
            # Afficher les champs du modèle
            print(f"   Champs: {[f.name for f in model._meta.fields]}")
            return model
        else:
            print(f"❌ Modèle {model_name} non trouvé")
            return None
    except Exception as e:
        print(f"❌ Erreur modèle {model_name}: {e}")
        return None

# Modèles critiques
critical_models = [
    'Membre',
    'Paiement',
    'Soin',
    'Bon',
    'Cotisation',
    'Assureur',
    'ConfigurationAssurance',
]

for model_name in critical_models:
    check_model(model_name)

# ============================================================================
# PARTIE 3: VÉRIFICATION DES VUES ET FORMULAIRES
# ============================================================================

print("\n" + "=" * 80)
print("VÉRIFICATION DES VUES ET FORMULAIRES")
print("=" * 80)

def check_view_function(view_name, module_path):
    """Vérifie si une fonction de vue existe"""
    try:
        module = __import__(module_path, fromlist=[view_name])
        view_func = getattr(module, view_name, None)
        if view_func:
            print(f"✅ Vue {view_name} trouvée dans {module_path}")
            return view_func
        else:
            print(f"❌ Vue {view_name} non trouvée dans {module_path}")
            return None
    except Exception as e:
        print(f"❌ Erreur vue {view_name}: {e}")
        return None

# Vues critiques
critical_views = [
    ('creer_paiement', 'assureur.views'),
    ('get_soins_par_membre', 'assureur.views'),
    ('liste_paiements', 'assureur.views'),
    ('dashboard_assureur', 'assureur.views'),
]

for view_name, module_path in critical_views:
    check_view_function(view_name, module_path)

# Vérification des formulaires
print("\n🔍 VÉRIFICATION DES FORMULAIRES:")
try:
    from assureur import forms
    form_classes = [name for name in dir(forms) if name.endswith('Form')]
    print(f"   Formulaires trouvés: {form_classes}")
    
    if 'PaiementForm' in form_classes:
        print(f"✅ Formulaire PaiementForm trouvé")
        # Afficher les champs du formulaire
        form = forms.PaiementForm()
        print(f"   Champs du formulaire: {list(form.fields.keys())}")
    else:
        print(f"❌ Formulaire PaiementForm non trouvé")
        
except Exception as e:
    print(f"❌ Erreur formulaires: {e}")

# ============================================================================
# PARTIE 4: VÉRIFICATION DES URLS
# ============================================================================

print("\n" + "=" * 80)
print("VÉRIFICATION DES URLS")
print("=" * 80)

from django.urls import get_resolver

def check_url_patterns():
    """Vérifie les patterns d'URL"""
    try:
        resolver = get_resolver()
        urls = []
        
        def collect_urls(patterns, prefix=''):
            for pattern in patterns:
                if hasattr(pattern, 'pattern'):
                    if hasattr(pattern, 'name') and pattern.name:
                        urls.append(f"{prefix}/{pattern.pattern} -> {pattern.name}")
                    else:
                        urls.append(f"{prefix}/{pattern.pattern}")
                    
                    # Vérifier les sous-patterns
                    if hasattr(pattern, 'url_patterns'):
                        collect_urls(pattern.url_patterns, f"{prefix}/{pattern.pattern}")
        
        collect_urls(resolver.url_patterns)
        
        print("📋 URLs DISPONIBLES:")
        urls_assureur = [u for u in urls if 'assureur' in u]
        
        for url in urls_assureur[:20]:  # Afficher les 20 premières
            print(f"   {url}")
        
        # Vérifier les URLs critiques
        critical_urls = [
            'assureur/paiements/creer/',
            'assureur/api/soins-par-membre/',
            'assureur/paiements/',
        ]
        
        print("\n🔍 VÉRIFICATION URLs CRITIQUES:")
        for critical_url in critical_urls:
            found = any(critical_url in u for u in urls)
            if found:
                print(f"✅ URL {critical_url} trouvée")
            else:
                print(f"❌ URL {critical_url} NON trouvée")
                
    except Exception as e:
        print(f"❌ Erreur URLs: {e}")

check_url_patterns()

# ============================================================================
# PARTIE 5: VÉRIFICATION DES TEMPLATES
# ============================================================================

print("\n" + "=" * 80)
print("VÉRIFICATION DES TEMPLATES")
print("=" * 80)

def check_template_exists(template_path):
    """Vérifie si un template existe"""
    try:
        from django.template.loader import get_template
        template = get_template(template_path)
        print(f"✅ Template {template_path} trouvé")
        return True
    except Exception as e:
        print(f"❌ Template {template_path} NON trouvé: {e}")
        return False

# Templates critiques
critical_templates = [
    'assureur/creer_paiement.html',
    'assureur/base_assureur.html',
    'assureur/liste_paiements.html',
    'assureur/dashboard.html',
]

for template in critical_templates:
    check_template_exists(template)

# ============================================================================
# PARTIE 6: VÉRIFICATION DES DONNÉES
# ============================================================================

print("\n" + "=" * 80)
print("VÉRIFICATION DES DONNÉES")
print("=" * 80)

try:
    # Compter les membres
    from agents.models import Membre
    total_membres = Membre.objects.count()
    print(f"👥 Membres dans la base: {total_membres}")
    
    if total_membres > 0:
        # Afficher les 5 premiers membres
        print("   Exemples de membres:")
        for m in Membre.objects.all()[:5]:
            print(f"   - {m.id}: {m.prenom} {m.nom} ({m.numero_unique})")
    
    # Compter les soins
    try:
        from assureur.models import Soin
        total_soins = Soin.objects.count()
        print(f"🏥 Soins dans la base: {total_soins}")
    except:
        print("⚠️  Modèle Soin non disponible ou vide")
    
    # Compter les paiements
    try:
        from assureur.models import Paiement
        total_paiements = Paiement.objects.count()
        print(f"💰 Paiements dans la base: {total_paiements}")
    except:
        print("⚠️  Modèle Paiement non disponible ou vide")
        
except Exception as e:
    print(f"❌ Erreur données: {e}")

# ============================================================================
# PARTIE 7: TEST DE L'API SOINS PAR MEMBRE
# ============================================================================

print("\n" + "=" * 80)
print("TEST DE L'API SOINS PAR MEMBRE")
print("=" * 80)

def test_api_soins_par_membre():
    """Test l'API get_soins_par_membre"""
    try:
        # Import de la vue
        from assureur.views import get_soins_par_membre
        from django.test import RequestFactory
        
        # Créer une requête factice
        factory = RequestFactory()
        request = factory.get('/api/soins-par-membre/1/')
        
        # Tester avec différents IDs de membre
        print("🧪 Test de l'API avec différents IDs:")
        
        from agents.models import Membre
        
        # Tester avec le premier membre
        if Membre.objects.exists():
            membre = Membre.objects.first()
            print(f"   Test avec membre ID {membre.id}: {membre.prenom} {membre.nom}")
            
            # Appeler la vue
            response = get_soins_par_membre(request, membre_id=membre.id)
            print(f"   Réponse API: {response.status_code}")
            
            # Afficher les données
            if hasattr(response, 'content'):
                import json
                try:
                    data = json.loads(response.content)
                    print(f"   Données retournées: {len(data)} éléments")
                    for item in data[:3]:  # Afficher les 3 premiers
                        print(f"     - {item}")
                except:
                    print(f"   Contenu: {response.content}")
        else:
            print("   Aucun membre trouvé pour le test")
            
    except Exception as e:
        print(f"❌ Erreur test API: {e}")
        import traceback
        traceback.print_exc()

test_api_soins_par_membre()

# ============================================================================
# PARTIE 8: VÉRIFICATION DES DÉCORATEURS
# ============================================================================

print("\n" + "=" * 80)
print("VÉRIFICATION DES DÉCORATEURS")
print("=" * 80)

def check_decorators():
    """Vérifie les décorateurs"""
    try:
        from assureur.decorators import assureur_required
        print(f"✅ Décorateur assureur_required trouvé")
        
        # Tester avec un utilisateur fictif
        from django.contrib.auth.models import User
        test_user = User(username='test_user')
        
        result = assureur_required(test_user)
        print(f"   Test décorateur: {result} (attendu: False pour utilisateur normal)")
        
    except Exception as e:
        print(f"❌ Erreur décorateurs: {e}")

check_decorators()

# ============================================================================
# PARTIE 9: VÉRIFICATION DU FORMULAIRE PAIEMENT
# ============================================================================

print("\n" + "=" * 80)
print("TEST DU FORMULAIRE PAIEMENT")
print("=" * 80)

def test_paiement_form():
    """Teste le formulaire de paiement"""
    try:
        from assureur.forms import PaiementForm
        
        # Créer un formulaire vide
        form = PaiementForm()
        print(f"✅ Formulaire PaiementForm instancié")
        
        # Afficher les champs
        print(f"   Nombre de champs: {len(form.fields)}")
        
        # Vérifier les champs requis
        required_fields = []
        for field_name, field in form.fields.items():
            if field.required:
                required_fields.append(field_name)
        
        print(f"   Champs requis: {required_fields}")
        
        # Tester avec des données de test
        test_data = {
            'membre': 1 if Membre.objects.exists() else None,
            'montant': 5000,
            'mode_paiement': 'especes',
            'date_paiement': '2023-12-04 15:00:00',
        }
        
        form_with_data = PaiementForm(data=test_data)
        print(f"   Formulaire valide: {form_with_data.is_valid()}")
        
        if not form_with_data.is_valid():
            print(f"   Erreurs: {form_with_data.errors}")
            
    except Exception as e:
        print(f"❌ Erreur formulaire: {e}")
        import traceback
        traceback.print_exc()

test_paiement_form()

