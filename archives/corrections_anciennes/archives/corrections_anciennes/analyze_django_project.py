import os
import ast
import inspect
from pathlib import Path
import django
from django.conf import settings

# Configuration Django minimale pour l'analyse
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()


class DjangoProjectAnalyzer:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.analysis_results = {
            'apps': {},
            'models': {},
            'views': {},
            'urls': {},
            'templates': {},
            'static_files': {},
            'settings': {},
            'potential_issues': []
        }

    def analyze_project_structure(self):
        """Analyse la structure générale du projet"""
        print("🔍 Analyse de la structure du projet...")

        structure = {
            'apps': [],
            'requirements': [],
            'migrations': {},
            'templates_count': 0,
            'static_folders': []
        }

        # Lister les applications
        for item in self.project_root.iterdir():
            if item.is_dir() and not item.name.startswith(('.', '__')):
                if (item / 'models.py').exists() or (item / 'views.py').exists():
                    structure['apps'].append(item.name)

                    # Compter les migrations
                    migrations_dir = item / 'migrations'
                    if migrations_dir.exists():
                        migration_files = [
                            f for f in migrations_dir.glob('*.py')
                            if not f.name.startswith('__')
                        ]
                        structure['migrations'][item.name] = len(migration_files)

        # Chercher requirements.txt
        requirements_file = self.project_root / 'requirements.txt'
        if requirements_file.exists():
            with open(requirements_file, 'r') as f:
                structure['requirements'] = [line.strip() for line in f if line.strip()]

        # Compter les templates
        templates_dir = self.project_root / 'templates'
        if templates_dir.exists():
            structure['templates_count'] = len(list(templates_dir.rglob('*.html')))

        # Lister les dossiers static
        static_dir = self.project_root / 'static'
        if static_dir.exists():
            structure['static_folders'] = [f.name for f in static_dir.iterdir() if f.is_dir()]

        self.analysis_results['structure'] = structure
        return structure

    def analyze_models(self):
        """Analyse tous les modèles Django"""
        print("🔍 Analyse des modèles...")

        from django.apps import apps

        models_info = {}
        for app_config in apps.get_app_configs():
            app_models = {}
            for model in app_config.get_models():
                model_info = {
                    'name': model.__name__,
                    'app_label': model._meta.app_label,
                    'fields': [],
                    'relationships': [],
                    'meta': {}
                }

                # Champs du modèle
                for field in model._meta.get_fields():
                    field_info = {
                        'name': field.name,
                        'type': field.get_internal_type(),
                        'blank': getattr(field, 'blank', False),
                        'null': getattr(field, 'null', False),
                        'unique': getattr(field, 'unique', False),
                    }

                    # Relations
                    if field.is_relation:
                        if hasattr(field, 'related_model') and field.related_model:
                            field_info['related_model'] = field.related_model.__name__
                            model_info['relationships'].append({
                                'field': field.name,
                                'type': field.get_internal_type(),
                                'related_model': field.related_model.__name__
                            })

                    model_info['fields'].append(field_info)

                # Métadonnées
                if model._meta.verbose_name:
                    model_info['meta']['verbose_name'] = str(model._meta.verbose_name)
                if model._meta.ordering:
                    model_info['meta']['ordering'] = list(model._meta.ordering)

                app_models[model.__name__] = model_info

            if app_models:
                models_info[app_config.label] = app_models

        self.analysis_results['models'] = models_info
        return models_info

    def analyze_views(self):
        """Analyse les vues et leurs méthodes"""
        print("🔍 Analyse des vues...")

        views_info = {}

        for app_name in settings.INSTALLED_APPS:
            if not app_name.startswith('django.'):
                try:
                    views_module = __import__(f'{app_name}.views', fromlist=[''])

                    app_views = {}
                    for name, obj in inspect.getmembers(views_module):
                        if (inspect.isclass(obj) and
                                (issubclass(obj, django.views.generic.View) or hasattr(obj, 'as_view'))):

                            view_info = {
                                'type': 'Class Based View',
                                'methods': [],
                                'decorators': []
                            }

                            for method in ['get', 'post', 'put', 'patch', 'delete']:
                                if hasattr(obj, method):
                                    view_info['methods'].append(method.upper())

                            app_views[name] = view_info

                        elif callable(obj) and not name.startswith('_'):
                            view_info = {
                                'type': 'Function Based View',
                                'decorators': []
                            }
                            app_views[name] = view_info

                    if app_views:
                        views_info[app_name] = app_views

                except ImportError:
                    continue
                except Exception as e:
                    print(f"⚠️ Erreur analyse vues {app_name}: {e}")

        self.analysis_results['views'] = views_info
        return views_info

    def analyze_urls(self):
        """Analyse les configurations d'URLs"""
        print("🔍 Analyse des URLs...")

        from django.urls import get_resolver

        urls_info = {
            'patterns': [],
            'total_routes': 0,
            'app_namespaces': []
        }

        resolver = get_resolver()

        def extract_patterns(patterns, prefix='', depth=0):
            for pattern in patterns:
                pattern_info = {
                    'pattern': str(pattern.pattern),
                    'full_pattern': prefix + str(pattern.pattern),
                    'depth': depth
                }

                if hasattr(pattern, 'callback'):
                    if hasattr(pattern.callback, '__name__'):
                        pattern_info['view'] = pattern.callback.__name__
                    if hasattr(pattern.callback, '__module__'):
                        pattern_info['module'] = pattern.callback.__module__

                if hasattr(pattern, 'name') and pattern.name:
                    pattern_info['name'] = pattern.name

                if hasattr(pattern, 'namespace') and pattern.namespace:
                    pattern_info['namespace'] = pattern.namespace
                    urls_info['app_namespaces'].append(pattern.namespace)

                urls_info['patterns'].append(pattern_info)
                urls_info['total_routes'] += 1

                if hasattr(pattern, 'url_patterns'):
                    extract_patterns(pattern.url_patterns,
                                     prefix + str(pattern.pattern), depth + 1)

        extract_patterns(resolver.url_patterns)
        self.analysis_results['urls'] = urls_info
        return urls_info

    def analyze_settings(self):
        """Analyse la configuration Django"""
        print("🔍 Analyse des settings...")

        settings_info = {
            'installed_apps_count': len(settings.INSTALLED_APPS),
            'installed_apps': list(settings.INSTALLED_APPS),
            'middleware_count': len(settings.MIDDLEWARE),
            'middleware': list(settings.MIDDLEWARE),
            'database': settings.DATABASES['default']['ENGINE'],
            'debug': settings.DEBUG,
            'allowed_hosts': list(settings.ALLOWED_HOSTS),
            'static_config': {
                'static_url': settings.STATIC_URL,
                'static_dirs': getattr(settings, 'STATICFILES_DIRS', []),
                'static_root': getattr(settings, 'STATIC_ROOT', '')
            },
            'auth_config': {
                'login_redirect': getattr(settings, 'LOGIN_REDIRECT_URL', ''),
                'login_url': getattr(settings, 'LOGIN_URL', ''),
                'logout_redirect': getattr(settings, 'LOGOUT_REDIRECT_URL', '')
            }
        }

        self.analysis_results['settings'] = settings_info
        return settings_info

    def check_potential_issues(self):
        """Détecte les problèmes potentiels"""
        print("🔍 Recherche de problèmes potentiels...")

        issues = []

        if not settings.DEBUG:
            if not getattr(settings, 'SECRET_KEY', '').startswith('django-insecure'):
                issues.append("❌ SECRET_KEY semble sécurisée")
            else:
                issues.append("⚠️  SECRET_KEY non sécurisée en production!")

            if not settings.ALLOWED_HOSTS:
                issues.append("⚠️  ALLOWED_HOSTS est vide en production!")

        if not getattr(settings, 'LOGIN_REDIRECT_URL', ''):
            issues.append("⚠️  LOGIN_REDIRECT_URL non configuré")

        critical_apps = ['django.contrib.auth', 'django.contrib.sessions']
        for app in critical_apps:
            if app not in settings.INSTALLED_APPS:
                issues.append(f"⚠️  App critique manquante: {app}")

        critical_middleware = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware'
        ]
        for middleware in critical_middleware:
            if middleware not in settings.MIDDLEWARE:
                issues.append(f"⚠️  Middleware critique manquant: {middleware}")

        self.analysis_results['potential_issues'] = issues
        return issues

    def generate_report(self):
        """Génère un rapport complet"""
        print("\n" + "=" * 60)
        print("📊 RAPPORT D'ANALYSE DU PROJET DJANGO")
        print("=" * 60)

        structure = self.analysis_results.get('structure', {})
        print(f"\n🏗️  STRUCTURE:")
        print(f"  • Applications: {len(structure.get('apps', []))}")
        print(f"  • Templates: {structure.get('templates_count', 0)}")
        print(f"  • Dependencies: {len(structure.get('requirements', []))}")

        models = self.analysis_results.get('models', {})
        total_models = sum(len(app_models) for app_models in models.values())
        print(f"\n🗃️  MODÈLES:")
        print(f"  • Total modèles: {total_models}")
        for app, app_models in models.items():
            print(f"  • {app}: {len(app_models)} modèles")

        views = self.analysis_results.get('views', {})
        total_views = sum(len(app_views) for app_views in views.values())
        print(f"\n👁️  VUES:")
        print(f"  • Total vues: {total_views}")

        urls = self.analysis_results.get('urls', {})
        print(f"\n🔗 URLs:")
        print(f"  • Total routes: {urls.get('total_routes', 0)}")
        print(f"  • Namespaces: {len(urls.get('app_namespaces', []))}")

        settings_info = self.analysis_results.get('settings', {})
        print(f"\n⚙️  CONFIGURATION:")
        print(f"  • Apps installées: {settings_info.get('installed_apps_count', 0)}")
        print(f"  • Middlewares: {settings_info.get('middleware_count', 0)}")
        print(f"  • Base de données: {settings_info.get('database', '')}")
        print(f"  • Mode debug: {settings_info.get('debug', '')}")

        issues = self.analysis_results.get('potential_issues', [])
        print(f"\n🚨 PROBLÈMES POTENTIELS: {len(issues)}")
        for issue in issues:
            print(f"  • {issue}")

        print("\n" + "=" * 60)
        print("✅ Analyse terminée!")

    def run_analysis(self):
        """Exécute l'analyse complète"""
        print("🚀 Démarrage de l'analyse du projet Django...")

        try:
            self.analyze_project_structure()
            self.analyze_models()
            self.analyze_views()
            self.analyze_urls()
            self.analyze_settings()
            self.check_potential_issues()
            self.generate_report()

            return self.analysis_results

        except Exception as e:
            print(f"❌ Erreur lors de l'analyse: {e}")
            return None


def main():
    """Fonction principale"""
    project_root = input("Entrez le chemin du projet Django (ou laissez vide pour le répertoire actuel): ").strip()

    if not project_root:
        project_root = os.getcwd()

    if not os.path.exists(os.path.join(project_root, 'manage.py')):
        print("❌ Ceci ne semble pas être un projet Django (manage.py introuvable)")
        return

    analyzer = DjangoProjectAnalyzer(project_root)
    results = analyzer.run_analysis()

    if results:
        import json
        with open('django_analysis_report.json', 'w', encoding='utf-8') as f:
            # ✅ Correction ici — conversion automatique des objets non JSON
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        print("📄 Rapport sauvegardé dans: django_analysis_report.json")


if __name__ == "__main__":
    main()
