#!/usr/bin/env python3
"""
SCRIPT DE DIAGNOSTIC COMPLET POUR L'APPLICATION ASSUREUR

Ce script vérifie tous les composants de l'application assureur :
1. Models, Views, URLs, Admin, Forms, Templates
2. Vérifie la cohérence entre les vues et les URLs
3. Vérifie l'existence des templates nécessaires
4. Vérifie les permissions et décorateurs
"""

import os
import sys
import django
from pathlib import Path

# Configuration de Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation de Django: {e}")
    sys.exit(1)

# ============================================================================
# IMPORTATIONS APRÈS LA CONFIGURATION DJANGO
# ============================================================================

from django.apps import apps
from django.urls import URLPattern, URLResolver, get_resolver
from django.core.checks import run_checks
from django.db import connection
from django.db.models import Model
from django.contrib import admin
from django.contrib.auth.models import Group, Permission

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
# 1. VÉRIFICATION DES MODÈLES
# ============================================================================

def check_models():
    """Vérifie que tous les modèles de l'application assureur sont correctement définis"""
    print_header("VÉRIFICATION DES MODÈLES ASSUREUR")
    
    try:
        from assureur import models
        
        # Liste des modèles attendus
        expected_models = [
            'Membre', 'Assureur', 'Bon', 'Soin', 'Paiement', 
            'Cotisation', 'StatistiquesAssurance', 'ConfigurationAssurance', 'RapportAssureur'
        ]
        
        for model_name in expected_models:
            if hasattr(models, model_name):
                model = getattr(models, model_name)
                if issubclass(model, Model):
                    # Vérifier si le modèle est enregistré dans admin
                    try:
                        is_registered = admin.site.is_registered(model)
                        status = "ENREGISTRÉ" if is_registered else "NON ENREGISTRÉ"
                        print_success(f"{model_name}: {status} dans admin.py")
                        
                        # Compter les instances
                        count = model.objects.count()
                        print_info(f"   {count} instances en base de données")
                        
                    except Exception as e:
                        print_error(f"{model_name}: Erreur lors de la vérification - {e}")
                else:
                    print_error(f"{model_name}: N'est pas un modèle Django valide")
            else:
                print_error(f"{model_name}: Modèle manquant dans models.py")
        
        # Vérifier les relations entre modèles
        print_info("\nVérification des relations entre modèles...")
        
        # Exemple: vérifier la relation Membre -> Bon
        if hasattr(models, 'Membre') and hasattr(models, 'Bon'):
            try:
                membre_model = getattr(models, 'Membre')
                # Vérifier si le champ 'bon_set' existe (relation inverse)
                if hasattr(membre_model, 'bon_set'):
                    print_success("Relation Membre -> Bon: OK")
                else:
                    print_warning("Relation Membre -> Bon: Non détectée")
            except:
                pass
        
    except ImportError as e:
        print_error(f"Impossible d'importer les modèles assureur: {e}")
        return False
    
    return True

# ============================================================================
# 2. VÉRIFICATION DES VUES
# ============================================================================

def check_views():
    """Vérifie que toutes les vues sont définies et accessibles"""
    print_header("VÉRIFICATION DES VUES ASSUREUR")
    
    try:
        from assureur import views
        
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
        
        missing_views = []
        for view_name in expected_views:
            if hasattr(views, view_name):
                view_func = getattr(views, view_name)
                
                # Vérifier si c'est une fonction callable
                if callable(view_func):
                    print_success(f"{view_name}: OK")
                else:
                    print_error(f"{view_name}: N'est pas une fonction callable")
                    missing_views.append(view_name)
            else:
                print_error(f"{view_name}: VUE MANQUANTE")
                missing_views.append(view_name)
        
        if missing_views:
            print_warning(f"\nVues manquantes: {', '.join(missing_views)}")
            return False
        
        # Vérifier les décorateurs sur les vues principales
        print_info("\nVérification des décorateurs de sécurité...")
        
        # Vérifier une vue protégée
        import inspect
        from django.contrib.auth.decorators import login_required
        
        if hasattr(views, 'dashboard_assureur'):
            view_func = views.dashboard_assureur
            source = inspect.getsource(view_func)
            
            if '@login_required' in source:
                print_success("dashboard_assureur: Protégé par @login_required")
            else:
                print_warning("dashboard_assureur: NON protégé par @login_required")
            
            if '@user_passes_test' in source:
                print_success("dashboard_assureur: Protégé par @user_passes_test")
            else:
                print_warning("dashboard_assureur: NON protégé par @user_passes_test")
        
        return True
        
    except ImportError as e:
        print_error(f"Impossible d'importer les vues assureur: {e}")
        return False

# ============================================================================
# 3. VÉRIFICATION DES URLS
# ============================================================================

def check_urls():
    """Vérifie que toutes les URLs sont correctement configurées"""
    print_header("VÉRIFICATION DES URLS ASSUREUR")
    
    try:
        from assureur import urls as assureur_urls
        from django.urls import reverse, NoReverseMatch
        
        # Récupérer toutes les URLs définies
        url_patterns = assureur_urls.urlpatterns
        
        print_info(f"Nombre d'URLs définies: {len(url_patterns)}")
        
        # Liste des URLs attendues avec leurs noms
        expected_urls = [
            ('assureur:dashboard', []),
            ('assureur:test', []),
            ('assureur:liste_membres', []),
            ('assureur:creer_membre', []),
            ('assureur:detail_membre', [1]),
            ('assureur:recherche_membre', []),
            ('assureur:liste_bons', []),
            ('assureur:creer_bon', []),
            ('assureur:detail_bon', [1]),
            ('assureur:valider_bon', [1]),
            ('assureur:rejeter_bon', [1]),
            ('assureur:liste_soins', []),
            ('assureur:detail_soin', [1]),
            ('assureur:valider_soin', [1]),
            ('assureur:rejeter_soin', [1]),
            ('assureur:liste_paiements', []),
            ('assureur:creer_paiement', []),
            ('assureur:detail_paiement', [1]),
            ('assureur:valider_paiement', [1]),
            ('assureur:annuler_paiement', [1]),
            ('assureur:liste_cotisations', []),
            ('assureur:generer_cotisations', []),
            ('assureur:enregistrer_paiement_cotisation', [1]),
            ('assureur:statistiques', []),
            ('assureur:rapports', []),
            ('assureur:generer_rapport', []),
            ('assureur:detail_rapport', [1]),
            ('assureur:export_rapport', [1]),
            ('assureur:configuration', []),
            ('assureur:api_get_stats', []),
            ('assureur:api_recherche_membre', []),
            ('assureur:export_donnees', ['membres']),
            ('assureur:messagerie_assureur', []),
            ('assureur:envoyer_message_assureur', []),
            ('assureur:api_creer_bon', [1]),
            ('assureur:api_valider_bon', [1]),
        ]
        
        accessible_urls = []
        broken_urls = []
        
        for url_name, args in expected_urls:
            try:
                reverse(url_name, args=args)
                accessible_urls.append(url_name)
                print_success(f"{url_name}: Accessible")
            except NoReverseMatch as e:
                broken_urls.append(url_name)
                print_error(f"{url_name}: INACCESSIBLE - {e}")
            except Exception as e:
                broken_urls.append(url_name)
                print_error(f"{url_name}: ERREUR - {e}")
        
        print_info(f"\nURLs accessibles: {len(accessible_urls)}/{len(expected_urls)}")
        if broken_urls:
            print_warning(f"URLs cassées: {', '.join(broken_urls)}")
            return False
        
        return True
        
    except ImportError as e:
        print_error(f"Impossible d'importer les URLs assureur: {e}")
        return False

# ============================================================================
# 4. VÉRIFICATION DE L'ADMIN
# ============================================================================

def check_admin():
    """Vérifie la configuration admin.py"""
    print_header("VÉRIFICATION DE L'ADMIN ASSUREUR")
    
    try:
        from assureur import admin as assureur_admin
        
        # Vérifier si admin.py existe et est importable
        print_success("admin.py: Fichier importé avec succès")
        
        # Vérifier les modèles enregistrés
        registered_models = admin.site._registry.keys()
        
        # Liste des modèles qui devraient être enregistrés
        expected_admin_models = [
            'Membre', 'Assureur', 'Bon', 'Soin', 'Paiement', 
            'Cotisation', 'StatistiquesAssurance', 'ConfigurationAssurance', 'RapportAssureur'
        ]
        
        from assureur import models
        missing_admin = []
        
        for model_name in expected_admin_models:
            if hasattr(models, model_name):
                model = getattr(models, model_name)
                if model in registered_models:
                    print_success(f"{model_name}: Enregistré dans l'admin")
                else:
                    print_warning(f"{model_name}: NON enregistré dans l'admin")
                    missing_admin.append(model_name)
            else:
                print_error(f"{model_name}: Modèle non trouvé pour vérification admin")
        
        if missing_admin:
            print_warning(f"Modèles non enregistrés dans admin: {', '.join(missing_admin)}")
        
        # Vérifier les customisations admin
        if hasattr(assureur_admin, 'MembreAdmin'):
            print_success("MembreAdmin: Class personnalisée présente")
        else:
            print_warning("MembreAdmin: Class personnalisée absente")
        
        return len(missing_admin) == 0
        
    except ImportError as e:
        print_error(f"Impossible d'importer admin.py: {e}")
        return False

# ============================================================================
# 5. VÉRIFICATION DES FORMULAIRES
# ============================================================================

def check_forms():
    """Vérifie que les formulaires nécessaires sont définis"""
    print_header("VÉRIFICATION DES FORMULAIRES ASSUREUR")
    
    try:
        from assureur import forms
        
        # Liste des formulaires attendus
        expected_forms = [
            'MembreForm', 'BonForm', 'SoinForm', 'PaiementForm',
            'CotisationForm', 'ConfigurationForm', 'RapportForm'
        ]
        
        missing_forms = []
        
        for form_name in expected_forms:
            if hasattr(forms, form_name):
                form_class = getattr(forms, form_name)
                print_success(f"{form_name}: Présent")
            else:
                print_warning(f"{form_name}: ABSENT")
                missing_forms.append(form_name)
        
        if missing_forms:
            print_warning(f"Formulaires manquants: {', '.join(missing_forms)}")
        
        # Vérifier forms.py n'est pas vide
        with open(BASE_DIR / 'assureur' / 'forms.py', 'r') as f:
            content = f.read()
            if len(content.strip()) > 0:
                print_success("forms.py: Fichier non vide")
            else:
                print_error("forms.py: Fichier vide ou presque")
        
        return len(missing_forms) == 0
        
    except ImportError as e:
        print_error(f"Impossible d'importer forms.py: {e}")
        return False

# ============================================================================
# 6. VÉRIFICATION DES TEMPLATES
# ============================================================================

def check_templates():
    """Vérifie que tous les templates nécessaires existent"""
    print_header("VÉRIFICATION DES TEMPLATES ASSUREUR")
    
    templates_dir = BASE_DIR / 'templates' / 'assureur'
    
    if not templates_dir.exists():
        print_error(f"Le répertoire templates/assureur n'existe pas: {templates_dir}")
        return False
    
    print_success(f"Répertoire templates trouvé: {templates_dir}")
    
    # Liste des templates attendus basés sur les vues
    expected_templates = [
        'dashboard.html',
        'liste_membres.html',
        'creer_membre.html',
        'detail_membre.html',
        'recherche_membre.html',
        'liste_bons.html',
        'creer_bon.html',
        'detail_bon.html',
        'liste_soins.html',
        'detail_soin.html',
        'liste_paiements.html',
        'creer_paiement.html',
        'detail_paiement.html',
        'liste_cotisations.html',
        'generer_cotisations.html',
        'statistiques.html',
        'rapports.html',
        'generer_rapport.html',
        'detail_rapport.html',
        'configuration.html',
        'acces_interdit.html',
        'base_assureur.html',
    ]
    
    missing_templates = []
    
    for template in expected_templates:
        template_path = templates_dir / template
        if template_path.exists():
            print_success(f"{template}: Présent")
        else:
            print_error(f"{template}: MANQUANT à {template_path}")
            missing_templates.append(template)
    
    # Vérifier les sous-répertoires
    subdirs = ['communication', 'cotisations', 'partials', 'rapports']
    for subdir in subdirs:
        subdir_path = templates_dir / subdir
        if subdir_path.exists():
            print_success(f"Répertoire {subdir}/: Présent")
            # Lister quelques fichiers dans les sous-répertoires
            try:
                files = list(subdir_path.glob('*.html'))
                if files:
                    print_info(f"  Fichiers trouvés: {len(files)}")
            except:
                pass
        else:
            print_warning(f"Répertoire {subdir}/: Absent")
    
    if missing_templates:
        print_warning(f"Templates manquants: {', '.join(missing_templates)}")
        return False
    
    return True

# ============================================================================
# 7. VÉRIFICATION DES MIGRATIONS
# ============================================================================

def check_migrations():
    """Vérifie l'état des migrations"""
    print_header("VÉRIFICATION DES MIGRATIONS ASSUREUR")
    
    migrations_dir = BASE_DIR / 'assureur' / 'migrations'
    
    if not migrations_dir.exists():
        print_error("Répertoire migrations/ non trouvé")
        return False
    
    # Compter les fichiers de migration
    migration_files = list(migrations_dir.glob('*.py'))
    # Exclure __init__.py
    migration_files = [f for f in migration_files if f.name != '__init__.py']
    
    print_info(f"Fichiers de migration trouvés: {len(migration_files)}")
    
    # Vérifier si les migrations ont été appliquées
    from django.db.migrations.recorder import MigrationRecorder
    recorder = MigrationRecorder(connection)
    
    try:
        applied_migrations = recorder.applied_migrations()
        assureur_migrations = [m for m in applied_migrations if m[0] == 'assureur']
        
        print_info(f"Migrations appliquées pour 'assureur': {len(assureur_migrations)}")
        
        if len(assureur_migrations) < len(migration_files):
            print_warning("Certaines migrations ne sont pas appliquées")
            return False
        else:
            print_success("Toutes les migrations sont appliquées")
            return True
            
    except Exception as e:
        print_error(f"Erreur lors de la vérification des migrations: {e}")
        return False

# ============================================================================
# 8. VÉRIFICATION DES PERMISSIONS
# ============================================================================

def check_permissions():
    """Vérifie les permissions et groupes"""
    print_header("VÉRIFICATION DES PERMISSIONS ASSUREUR")
    
    # Vérifier si le groupe 'assureur' existe
    try:
        assureur_group, created = Group.objects.get_or_create(name='assureur')
        
        if created:
            print_warning("Groupe 'assureur': Créé (n'existait pas)")
        else:
            print_success("Groupe 'assureur': Existe")
        
        # Vérifier les permissions associées au groupe
        permissions_count = assureur_group.permissions.count()
        print_info(f"Permissions associées au groupe 'assureur': {permissions_count}")
        
        if permissions_count == 0:
            print_warning("Le groupe 'assureur' n'a aucune permission assignée")
        
        # Vérifier les permissions pour les modèles assureur
        from django.contrib.contenttypes.models import ContentType
        from assureur import models
        
        model_permissions = {}
        for model_name in ['Membre', 'Bon', 'Soin', 'Paiement', 'Cotisation']:
            if hasattr(models, model_name):
                model = getattr(models, model_name)
                content_type = ContentType.objects.get_for_model(model)
                perms = Permission.objects.filter(content_type=content_type)
                model_permissions[model_name] = perms.count()
        
        print_info("Permissions disponibles par modèle:")
        for model, count in model_permissions.items():
            print_info(f"  {model}: {count} permissions")
        
        return True
        
    except Exception as e:
        print_error(f"Erreur lors de la vérification des permissions: {e}")
        return False

# ============================================================================
# 9. VÉRIFICATION DE LA BASE DE DONNÉES
# ============================================================================

def check_database():
    """Vérifie la connexion à la base de données et les tables"""
    print_header("VÉRIFICATION DE LA BASE DE DONNÉES")
    
    try:
        # Test de connexion
        connection.ensure_connection()
        print_success("Connexion à la base de données: OK")
        
        # Vérifier les tables
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_name LIKE 'assureur_%'
            """)
            tables = cursor.fetchall()
            
        assureur_tables = [t[0] for t in tables]
        print_info(f"Tables assureur trouvées: {len(assureur_tables)}")
        
        if assureur_tables:
            print_info("Liste des tables:")
            for table in assureur_tables:
                print_info(f"  - {table}")
            
            # Vérifier les données dans les tables principales
            from assureur.models import Membre, Bon, Cotisation
            
            stats = {
                'Membre': Membre.objects.count(),
                'Bon': Bon.objects.count(),
                'Cotisation': Cotisation.objects.count(),
            }
            
            print_info("\nStatistiques des données:")
            for model, count in stats.items():
                print_info(f"  {model}: {count} enregistrements")
            
            return True
        else:
            print_error("Aucune table assureur trouvée dans la base")
            return False
            
    except Exception as e:
        print_error(f"Erreur de base de données: {e}")
        return False

# ============================================================================
# 10. VÉRIFICATION DES SIGNALS
# ============================================================================

def check_signals():
    """Vérifie que les signaux sont configurés"""
    print_header("VÉRIFICATION DES SIGNALS ASSUREUR")
    
    signals_file = BASE_DIR / 'assureur' / 'signals.py'
    
    if signals_file.exists():
        print_success("signals.py: Fichier présent")
        
        try:
            from assureur import signals
            print_success("signals.py: Importé avec succès")
            
            # Vérifier les signaux courants
            if hasattr(signals, 'creer_profil_assureur'):
                print_success("Signal 'creer_profil_assureur': Présent")
            else:
                print_warning("Signal 'creer_profil_assureur': Absent")
            
            return True
            
        except ImportError as e:
            print_error(f"Erreur d'import de signals.py: {e}")
            return False
    else:
        print_warning("signals.py: Fichier absent")
        return False

# ============================================================================
# 11. VÉRIFICATION DES TESTS
# ============================================================================

def check_tests():
    """Vérifie que les tests sont configurés"""
    print_header("VÉRIFICATION DES TESTS ASSUREUR")
    
    tests_file = BASE_DIR / 'assureur' / 'tests.py'
    
    if tests_file.exists():
        print_success("tests.py: Fichier présent")
        
        try:
            with open(tests_file, 'r') as f:
                content = f.read()
                
            if 'TestCase' in content or 'test_' in content:
                print_success("tests.py: Contient des tests")
            else:
                print_warning("tests.py: Ne semble pas contenir de tests")
            
            return True
            
        except Exception as e:
            print_error(f"Erreur de lecture de tests.py: {e}")
            return False
    else:
        print_warning("tests.py: Fichier absent")
        return False

# ============================================================================
# 12. VÉRIFICATION GLOBALE DE L'APPLICATION
# ============================================================================

def check_app_config():
    """Vérifie la configuration de l'application"""
    print_header("VÉRIFICATION DE LA CONFIGURATION DE L'APPLICATION")
    
    try:
        from assureur.apps import AssureurConfig
        
        app_config = AssureurConfig
        
        print_success(f"Nom de l'application: {app_config.name}")
        print_success(f"Nom verbose: {app_config.verbose_name}")
        
        # Vérifier si l'application est dans INSTALLED_APPS
        from django.conf import settings
        
        if 'assureur' in settings.INSTALLED_APPS:
            print_success("'assureur' est dans INSTALLED_APPS")
        else:
            print_error("'assureur' n'est PAS dans INSTALLED_APPS")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Erreur de configuration: {e}")
        return False

# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    """Fonction principale du diagnostic"""
    print("="*80)
    print("DIAGNOSTIC COMPLET DE L'APPLICATION ASSUREUR")
    print("="*80)
    
    results = {}
    
    # Exécuter toutes les vérifications
    results['models'] = check_models()
    results['views'] = check_views()
    results['urls'] = check_urls()
    results['admin'] = check_admin()
    results['forms'] = check_forms()
    results['templates'] = check_templates()
    results['migrations'] = check_migrations()
    results['permissions'] = check_permissions()
    results['database'] = check_database()
    results['signals'] = check_signals()
    results['tests'] = check_tests()
    results['app_config'] = check_app_config()
    
    # Résumé
    print_header("RÉSUMÉ DU DIAGNOSTIC")
    
    total_checks = len(results)
    passed_checks = sum(1 for r in results.values() if r)
    failed_checks = total_checks - passed_checks
    
    print(f"\n{passed_checks}/{total_checks} vérifications passées")
    
    if failed_checks == 0:
        print_success("✅ TOUS LES TESTS SONT PASSÉS! L'application assureur est prête.")
    else:
        print_warning(f"⚠️  {failed_checks} problème(s) détecté(s)")
        
        print("\nProblèmes détectés:")
        for check_name, passed in results.items():
            if not passed:
                print_error(f"  - {check_name}")
    
    # Recommandations
    print_header("RECOMMANDATIONS")
    
    if not results['templates']:
        print("1. Créez les templates manquants dans templates/assureur/")
        print("   Templates de base nécessaires: base_assureur.html, dashboard.html, etc.")
    
    if not results['migrations']:
        print("2. Appliquez les migrations: python manage.py migrate assureur")
    
    if not results['permissions']:
        print("3. Configurez les permissions pour le groupe 'assureur'")
        print("   python manage.py assign_assureur_permissions")
    
    if not results['forms']:
        print("4. Complétez les formulaires dans forms.py")
    
    # Vérification finale de santé
    print_header("VÉRIFICATION FINALE DE SANTÉ")
    
    try:
        # Exécuter les checks système Django
        django_checks = run_checks()
        
        if django_checks:
            print_warning(f"Django a détecté {len(django_checks)} problème(s)")
            for check in django_checks[:5]:  # Limiter l'affichage
                print_warning(f"  - {check}")
        else:
            print_success("✅ Aucun problème détecté par les checks Django")
            
    except Exception as e:
        print_error(f"Erreur lors des checks Django: {e}")
    
    print("\n" + "="*80)
    print("DIAGNOSTIC TERMINÉ")
    print("="*80)

if __name__ == "__main__":
    main()