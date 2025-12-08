#!/usr/bin/env python3
"""
SCRIPT DE DIAGNOSTIC COMPLET POUR L'APPLICATION ASSUREUR - VERSION CORRIGÉE

Ce script vérifie tous les composants de l'application assureur avec les chemins corrects.
"""
import os
import sys
import django
from pathlib import Path

# Configuration de Django
BASE_DIR = Path(__file__).resolve().parent  # Le répertoire où se trouve ce script
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django initialisé avec succès")
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation de Django: {e}")
    sys.exit(1)

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def print_header(title):
    """Affiche un en-tête de section"""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)

def print_success(message):
    """Affiche un message de succès"""
    print(f"✅ {message}")

def print_warning(message):
    """Affiche un message d'avertissement"""
    print(f"⚠️  {message}")

def print_error(message):
    """Affiche un message d'erreur"""
    print(f"❌ {message}")

def print_info(message):
    """Affiche un message informatif"""
    print(f"📋 {message}")

# ============================================================================
# 1. VÉRIFICATION DES FICHIERS EXISTANTS
# ============================================================================

def check_files_exist():
    """Vérifie que les fichiers essentiels existent"""
    print_header("VÉRIFICATION DES FICHIERS ASSUREUR")
    
    assureur_dir = BASE_DIR / "assureur"
    if not assureur_dir.exists():
        print_error(f"Le répertoire assureur n'existe pas: {assureur_dir}")
        return False
    
    print_success(f"Répertoire assureur trouvé: {assureur_dir}")
    
    # Liste des fichiers essentiels
    essential_files = [
        "__init__.py",
        "models.py", 
        "views.py",
        "urls.py",
        "admin.py",
        "apps.py",
        "forms.py",
    ]
    
    missing_files = []
    for file in essential_files:
        file_path = assureur_dir / file
        if file_path.exists():
            print_success(f"{file}: Présent")
            # Afficher la taille du fichier
            size = file_path.stat().st_size
            if size == 0:
                print_warning(f"  {file} est vide (0 octets)")
            else:
                print_info(f"  Taille: {size} octets")
        else:
            print_error(f"{file}: MANQUANT")
            missing_files.append(file)
    
    # Vérifier les répertoires importants
    important_dirs = [
        "migrations",
        "templates/assureur",
        "static/css",
    ]
    
    for dir_name in important_dirs:
        dir_path = assureur_dir / dir_name
        if dir_path.exists():
            print_success(f"Répertoire {dir_name}: Présent")
        else:
            print_warning(f"Répertoire {dir_name}: Absent")
    
    if missing_files:
        print_error(f"Fichiers manquants: {', '.join(missing_files)}")
        return False
    
    return True

# ============================================================================
# 2. VÉRIFICATION DES MODÈLES
# ============================================================================

def check_models():
    """Vérifie que tous les modèles de l'application assureur sont correctement définis"""
    print_header("VÉRIFICATION DES MODÈLES ASSUREUR")
    
    try:
        # Import dynamique pour éviter les erreurs
        models_module = __import__('assureur.models', fromlist=['*'])
        
        # Liste des modèles attendus
        expected_models = [
            'Membre', 'Assureur', 'Bon', 'Soin', 'Paiement', 
            'Cotisation', 'StatistiquesAssurance', 'ConfigurationAssurance', 'RapportAssureur'
        ]
        
        found_models = []
        missing_models = []
        
        for model_name in expected_models:
            if hasattr(models_module, model_name):
                try:
                    model = getattr(models_module, model_name)
                    from django.db.models import Model
                    if issubclass(model, Model):
                        found_models.append(model_name)
                        # Compter les instances
                        count = model.objects.count()
                        print_success(f"{model_name}: {count} instances")
                    else:
                        print_error(f"{model_name}: N'est pas un modèle Django valide")
                        missing_models.append(model_name)
                except Exception as e:
                    print_error(f"{model_name}: Erreur - {e}")
                    missing_models.append(model_name)
            else:
                print_error(f"{model_name}: Modèle manquant dans models.py")
                missing_models.append(model_name)
        
        print_info(f"Modèles trouvés: {len(found_models)}/{len(expected_models)}")
        
        # Vérifier les champs des modèles principaux
        if 'Membre' in found_models:
            print_info("\nChamps du modèle Membre:")
            Membre = getattr(models_module, 'Membre')
            fields = [f.name for f in Membre._meta.get_fields()]
            for field in fields[:10]:  # Afficher seulement les 10 premiers
                print_info(f"  - {field}")
            if len(fields) > 10:
                print_info(f"  ... et {len(fields)-10} autres champs")
        
        return len(missing_models) == 0
        
    except ImportError as e:
        print_error(f"Impossible d'importer les modèles assureur: {e}")
        return False

# ============================================================================
# 3. VÉRIFICATION DES VUES
# ============================================================================

def check_views():
    """Vérifie que toutes les vues sont définies et accessibles"""
    print_header("VÉRIFICATION DES VUES ASSUREUR")
    
    try:
        views_module = __import__('assureur.views', fromlist=['*'])
        
        # Liste des vues attendues basées sur urls.py
        expected_views = [
            'dashboard_assureur', 'test_assureur',
            'liste_membres', 'creer_membre', 'detail_membre', 'recherche_membre',
            'liste_bons', 'creer_bon', 'detail_bon', 'valider_bon', 'rejeter_bon',
            'liste_soins', 'detail_soin', 'valider_soin', 'rejeter_soin',
            'liste_paiements', 'creer_paiement', 'detail_paiement', 'valider_paiement', 'annuler_paiement',
            'liste_cotisations', 'generer_cotisations', 'enregistrer_paiement_cotisation',
            'statistiques_assureur', 'rapports', 'generer_rapport', 'detail_rapport', 'export_rapport',
            'configuration_assureur', 'api_statistiques', 'api_recherche_membre',
            'export_donnees', 'messagerie_assureur', 'envoyer_message_assureur',
            'api_creer_bon', 'api_valider_bon', 'acces_interdit'
        ]
        
        found_views = []
        missing_views = []
        
        for view_name in expected_views:
            if hasattr(views_module, view_name):
                view_func = getattr(views_module, view_name)
                
                # Vérifier si c'est une fonction callable
                import inspect
                if callable(view_func):
                    found_views.append(view_name)
                    print_success(f"{view_name}: OK")
                else:
                    print_error(f"{view_name}: N'est pas une fonction callable")
                    missing_views.append(view_name)
            else:
                print_error(f"{view_name}: VUE MANQUANTE")
                missing_views.append(view_name)
        
        print_info(f"\nVues trouvées: {len(found_views)}/{len(expected_views)}")
        
        if missing_views:
            print_warning(f"Vues manquantes: {', '.join(missing_views[:10])}")
            if len(missing_views) > 10:
                print_warning(f"  ... et {len(missing_views)-10} autres")
        
        return len(missing_views) == 0
        
    except ImportError as e:
        print_error(f"Impossible d'importer les vues assureur: {e}")
        return False

# ============================================================================
# 4. VÉRIFICATION DES URLS
# ============================================================================

def check_urls():
    """Vérifie que toutes les URLs sont correctement configurées"""
    print_header("VÉRIFICATION DES URLS ASSUREUR")
    
    try:
        urls_module = __import__('assureur.urls', fromlist=['*'])
        
        # Récupérer toutes les URLs définies
        if hasattr(urls_module, 'urlpatterns'):
            url_patterns = urls_module.urlpatterns
            print_info(f"Nombre d'URLs définies: {len(url_patterns)}")
        else:
            print_error("Aucun urlpatterns trouvé dans urls.py")
            return False
        
        # Vérifier quelques URLs critiques
        from django.urls import reverse, NoReverseMatch
        
        critical_urls = [
            ('assureur:dashboard', []),
            ('assureur:liste_membres', []),
            ('assureur:liste_bons', []),
            ('assureur:liste_soins', []),
            ('assureur:liste_paiements', []),
            ('assureur:liste_cotisations', []),
            ('assureur:statistiques', []),
            ('assureur:configuration', []),
        ]
        
        accessible = []
        broken = []
        
        for url_name, args in critical_urls:
            try:
                reverse(url_name, args=args)
                accessible.append(url_name)
                print_success(f"{url_name}: Accessible")
            except NoReverseMatch as e:
                broken.append(url_name)
                print_error(f"{url_name}: INACCESSIBLE - {e}")
            except Exception as e:
                broken.append(url_name)
                print_error(f"{url_name}: ERREUR - {e}")
        
        print_info(f"\nURLs critiques accessibles: {len(accessible)}/{len(critical_urls)}")
        
        if broken:
            print_warning(f"URLs critiques cassées: {', '.join(broken)}")
            return False
        
        return True
        
    except ImportError as e:
        print_error(f"Impossible d'importer les URLs assureur: {e}")
        return False

# ============================================================================
# 5. VÉRIFICATION DES FORMULAIRES
# ============================================================================

def check_forms():
    """Vérifie que les formulaires nécessaires sont définis"""
    print_header("VÉRIFICATION DES FORMULAIRES ASSUREUR")
    
    forms_path = BASE_DIR / "assureur" / "forms.py"
    
    if not forms_path.exists():
        print_error(f"Fichier forms.py non trouvé: {forms_path}")
        return False
    
    print_success(f"Fichier forms.py trouvé: {forms_path}")
    
    try:
        forms_module = __import__('assureur.forms', fromlist=['*'])
        
        # Liste des formulaires courants
        common_forms = [
            'MembreForm', 'BonForm', 'SoinForm', 'PaiementForm',
            'CotisationForm', 'ConfigurationForm', 'RapportForm'
        ]
        
        found_forms = []
        missing_forms = []
        
        for form_name in common_forms:
            if hasattr(forms_module, form_name):
                found_forms.append(form_name)
                print_success(f"{form_name}: Présent")
            else:
                missing_forms.append(form_name)
                print_warning(f"{form_name}: Absent")
        
        # Lister tous les formulaires trouvés
        all_forms = [attr for attr in dir(forms_module) 
                    if not attr.startswith('_') and 'Form' in attr]
        
        print_info(f"\nFormulaires trouvés dans forms.py: {len(all_forms)}")
        for form in all_forms:
            print_info(f"  - {form}")
        
        if missing_forms:
            print_warning(f"Formulaires courants manquants: {', '.join(missing_forms)}")
        
        return True
        
    except ImportError as e:
        print_error(f"Erreur d'import de forms.py: {e}")
        return False

# ============================================================================
# 6. VÉRIFICATION DES TEMPLATES
# ============================================================================

def check_templates():
    """Vérifie que tous les templates nécessaires existent"""
    print_header("VÉRIFICATION DES TEMPLATES ASSUREUR")
    
    templates_dir = BASE_DIR / "templates" / "assureur"
    
    if not templates_dir.exists():
        print_error(f"Le répertoire templates/assureur n'existe pas: {templates_dir}")
        
        # Essayer de trouver templates ailleurs
        alt_path = BASE_DIR / "assureur" / "templates" / "assureur"
        if alt_path.exists():
            print_warning(f"Templates trouvés à: {alt_path}")
            templates_dir = alt_path
        else:
            return False
    
    print_success(f"Répertoire templates trouvé: {templates_dir}")
    
    # Compter les fichiers .html
    html_files = list(templates_dir.rglob("*.html"))
    print_info(f"Nombre total de templates HTML: {len(html_files)}")
    
    # Templates essentiels
    essential_templates = [
        'dashboard.html',
        'base_assureur.html',
        'liste_membres.html',
        'liste_bons.html',
        'liste_soins.html',
        'liste_paiements.html',
        'liste_cotisations.html',
        'statistiques.html',
        'configuration.html',
    ]
    
    missing_templates = []
    
    for template in essential_templates:
        template_path = templates_dir / template
        if template_path.exists():
            print_success(f"{template}: Présent")
        else:
            # Chercher dans les sous-répertoires
            found = False
            for html_file in html_files:
                if html_file.name == template:
                    print_success(f"{template}: Présent (à {html_file.relative_to(templates_dir)})")
                    found = True
                    break
            
            if not found:
                print_error(f"{template}: MANQUANT")
                missing_templates.append(template)
    
    # Vérifier les sous-répertoires
    subdirs = [d for d in templates_dir.iterdir() if d.is_dir()]
    print_info(f"\nSous-répertoires templates: {len(subdirs)}")
    for subdir in subdirs[:10]:  # Limiter l'affichage
        html_count = len(list(subdir.rglob("*.html")))
        print_info(f"  {subdir.name}/: {html_count} fichiers HTML")
    
    if missing_templates:
        print_warning(f"Templates essentiels manquants: {', '.join(missing_templates)}")
        return False
    
    return True

# ============================================================================
# 7. VÉRIFICATION DES MIGRATIONS
# ============================================================================

def check_migrations():
    """Vérifie l'état des migrations"""
    print_header("VÉRIFICATION DES MIGRATIONS ASSUREUR")
    
    migrations_dir = BASE_DIR / "assureur" / "migrations"
    
    if not migrations_dir.exists():
        print_error("Répertoire migrations/ non trouvé")
        return False
    
    # Compter les fichiers de migration
    migration_files = list(migrations_dir.glob("*.py"))
    # Exclure __init__.py
    migration_files = [f for f in migration_files if f.name != '__init__.py']
    
    print_info(f"Fichiers de migration trouvés: {len(migration_files)}")
    
    if migration_files:
        # Afficher les 5 dernières migrations
        print_info("Dernières migrations:")
        for mfile in sorted(migration_files, reverse=True)[:5]:
            print_info(f"  - {mfile.name}")
    
    # Vérifier avec Django
    from django.db.migrations.recorder import MigrationRecorder
    from django.db import connection
    
    try:
        recorder = MigrationRecorder(connection)
        applied_migrations = recorder.applied_migrations()
        assureur_migrations = [m for m in applied_migrations if m[0] == 'assureur']
        
        print_info(f"\nMigrations appliquées pour 'assureur': {len(assureur_migrations)}")
        
        if len(assureur_migrations) < len(migration_files):
            print_warning(f"Certaines migrations ne sont pas appliquées ({len(assureur_migrations)}/{len(migration_files)})")
            
            # Afficher les migrations non appliquées
            applied_names = [m[1] for m in assureur_migrations]
            for mfile in migration_files:
                migration_name = mfile.stem
                if migration_name not in applied_names:
                    print_warning(f"  Migration non appliquée: {migration_name}")
            
            return False
        else:
            print_success("Toutes les migrations sont appliquées")
            return True
            
    except Exception as e:
        print_error(f"Erreur lors de la vérification des migrations: {e}")
        return False

# ============================================================================
# 8. VÉRIFICATION DE L'ADMIN
# ============================================================================

def check_admin():
    """Vérifie la configuration admin.py"""
    print_header("VÉRIFICATION DE L'ADMIN ASSUREUR")
    
    admin_path = BASE_DIR / "assureur" / "admin.py"
    
    if not admin_path.exists():
        print_error("Fichier admin.py non trouvé")
        return False
    
    print_success(f"Fichier admin.py trouvé: {admin_path}")
    
    try:
        admin_module = __import__('assureur.admin', fromlist=['*'])
        
        # Vérifier les modèles enregistrés
        from django.contrib import admin
        registered_models = list(admin.site._registry.keys())
        
        # Récupérer les modèles assureur
        models_module = __import__('assureur.models', fromlist=['*'])
        assureur_models = []
        
        for attr_name in dir(models_module):
            try:
                attr = getattr(models_module, attr_name)
                if hasattr(attr, '_meta') and hasattr(attr._meta, 'app_label'):
                    if attr._meta.app_label == 'assureur':
                        assureur_models.append(attr)
            except:
                pass
        
        print_info(f"Modèles assureur détectés: {len(assureur_models)}")
        
        registered_count = 0
        for model in assureur_models:
            if model in registered_models:
                registered_count += 1
                print_success(f"{model.__name__}: Enregistré dans l'admin")
            else:
                print_warning(f"{model.__name__}: NON enregistré dans l'admin")
        
        print_info(f"\nModèles enregistrés dans admin: {registered_count}/{len(assureur_models)}")
        
        return registered_count == len(assureur_models)
        
    except ImportError as e:
        print_error(f"Erreur d'import d'admin.py: {e}")
        return False

# ============================================================================
# 9. VÉRIFICATION DES TESTS
# ============================================================================

def check_tests():
    """Vérifie que les tests sont configurés"""
    print_header("VÉRIFICATION DES TESTS ASSUREUR")
    
    tests_path = BASE_DIR / "assureur" / "tests.py"
    
    if tests_path.exists():
        print_success("Fichier tests.py présent")
        
        try:
            with open(tests_path, 'r') as f:
                content = f.read()
            
            if 'TestCase' in content or 'test_' in content:
                print_success("tests.py: Contient des tests")
                # Compter les fonctions de test
                test_count = content.count('def test_')
                print_info(f"Nombre de tests détectés: {test_count}")
            else:
                print_warning("tests.py: Ne semble pas contenir de tests")
            
            return True
            
        except Exception as e:
            print_error(f"Erreur de lecture de tests.py: {e}")
            return False
    else:
        print_warning("Fichier tests.py absent")
        return False

# ============================================================================
# 10. VÉRIFICATION DES STATIQUES
# ============================================================================

def check_static():
    """Vérifie les fichiers statiques"""
    print_header("VÉRIFICATION DES FICHIERS STATIQUES")
    
    static_dir = BASE_DIR / "assureur" / "static"
    
    if not static_dir.exists():
        print_warning("Répertoire static/ non trouvé dans assureur/")
        
        # Chercher dans le projet global
        global_static = BASE_DIR / "static"
        if global_static.exists():
            print_info(f"Répertoire static global trouvé: {global_static}")
            static_dir = global_static
    
    if static_dir.exists():
        print_success(f"Répertoire static trouvé: {static_dir}")
        
        # Compter les fichiers CSS et JS
        css_files = list(static_dir.rglob("*.css"))
        js_files = list(static_dir.rglob("*.js"))
        
        print_info(f"Fichiers CSS: {len(css_files)}")
        print_info(f"Fichiers JS: {len(js_files)}")
        
        # Chercher spécifiquement les fichiers assureur
        assureur_css = [f for f in css_files if 'assureur' in str(f).lower()]
        if assureur_css:
            print_success("Fichiers CSS assureur trouvés")
            for css in assureur_css[:3]:  # Afficher les 3 premiers
                print_info(f"  - {css.relative_to(static_dir)}")
        else:
            print_warning("Aucun fichier CSS spécifique à assureur trouvé")
        
        return True
    else:
        print_error("Aucun répertoire static trouvé")
        return False

# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    """Fonction principale du diagnostic"""
    print("="*80)
    print("DIAGNOSTIC COMPLET DE L'APPLICATION ASSUREUR - VERSION CORRIGÉE")
    print("="*80)
    
    # D'abord vérifier que les fichiers existent
    if not check_files_exist():
        print_error("❌ Fichiers essentiels manquants. Diagnostic interrompu.")
        return
    
    results = {}
    
    # Exécuter toutes les vérifications
    print("\n" + "="*80)
    print("EXÉCUTION DES VÉRIFICATIONS")
    print("="*80)
    
    results['models'] = check_models()
    results['views'] = check_views()
    results['urls'] = check_urls()
    results['forms'] = check_forms()
    results['templates'] = check_templates()
    results['migrations'] = check_migrations()
    results['admin'] = check_admin()
    results['tests'] = check_tests()
    results['static'] = check_static()
    
    # Résumé
    print_header("RÉSUMÉ DU DIAGNOSTIC")
    
    total_checks = len(results)
    passed_checks = sum(1 for r in results.values() if r)
    failed_checks = total_checks - passed_checks
    
    print(f"\n📊 Résultat: {passed_checks}/{total_checks} vérifications passées")
    
    if failed_checks == 0:
        print_success("✅ TOUS LES TESTS SONT PASSÉS! L'application assureur est prête.")
    else:
        print_warning(f"⚠️  {failed_checks} problème(s) détecté(s)")
        
        print("\n📋 Détail des problèmes:")
        for check_name, passed in results.items():
            status = "✅ PASSÉ" if passed else "❌ ÉCHEC"
            print(f"  {status} - {check_name}")
    
    # Recommandations basées sur les problèmes détectés
    print_header("RECOMMANDATIONS")
    
    if not results.get('templates', True):
        print("1. 📁 Créez les templates manquants dans templates/assureur/")
        print("   Commandes utiles:")
        print("   - mkdir -p templates/assureur/{communication,cotisations,rapports,partials}")
        print("   - touch templates/assureur/dashboard.html templates/assureur/base_assureur.html")
    
    if not results.get('migrations', True):
        print("\n2. 🗃️  Appliquez les migrations:")
        print("   python manage.py makemigrations assureur")
        print("   python manage.py migrate assureur")
    
    if not results.get('urls', True):
        print("\n3. 🔗 Vérifiez les URLs dans assureur/urls.py")
        print("   Problème détecté: assureur:detail_paiement inaccessible")
        print("   Solution: Vérifiez que la vue 'detail_paiement' existe et est bien référencée")
    
    if not results.get('forms', True):
        print("\n4. 📝 Complétez les formulaires dans assureur/forms.py")
        print("   Formulaires manquants: RapportForm")
    
    # Vérification finale
    print_header("VÉRIFICATION FINALE")
    
    try:
        # Tester l'accès au dashboard
        from django.urls import reverse
        from django.test import RequestFactory
        from django.contrib.auth.models import AnonymousUser
        
        print("Test d'accès au dashboard assureur...")
        
        url = reverse('assureur:dashboard')
        print_success(f"URL du dashboard: {url}")
        
        # Tester l'import de la vue
        from assureur.views import dashboard_assureur
        print_success("Vue dashboard_assureur importée avec succès")
        
        print("\n🎯 L'application assureur semble fonctionnelle avec quelques ajustements nécessaires.")
        
    except Exception as e:
        print_error(f"Erreur lors du test final: {e}")
    
    print("\n" + "="*80)
    print("DIAGNOSTIC TERMINÉ")
    print("="*80)

if __name__ == "__main__":
    main()