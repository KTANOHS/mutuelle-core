# views.py - À ajouter à vos vues Django
import os
import sys
import subprocess
import platform
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
import json

def is_superuser(user):
    return user.is_superuser

class RenderDiagnosticView(View):
    """
    Vue de diagnostic pour Render.com
    Accessible uniquement aux superutilisateurs en production
    """
    
    @method_decorator(user_passes_test(is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request):
        diagnostic_data = self.run_diagnostics()
        return JsonResponse(diagnostic_data)
    
    def run_diagnostics(self):
        """Exécute les diagnostics système"""
        data = {
            "status": "running",
            "timestamp": datetime.now().isoformat(),
            "environment": self.get_environment_info(),
            "django": self.get_django_info(),
            "database": self.get_database_info(),
            "filesystem": self.get_filesystem_info(),
            "services": self.get_services_info(),
            "issues": [],
            "recommendations": []
        }
        
        # Vérifications automatiques
        self.check_migrations(data)
        self.check_static_files(data)
        self.check_environment_vars(data)
        
        data["status"] = "complete"
        return data
    
    def get_environment_info(self):
        """Informations sur l'environnement"""
        return {
            "python_version": sys.version,
            "platform": platform.platform(),
            "current_directory": os.getcwd(),
            "is_render": os.environ.get('RENDER') is not None,
            "render_service_id": os.environ.get('RENDER_SERVICE_ID'),
            "render_instance_id": os.environ.get('RENDER_INSTANCE_ID'),
        }
    
    def get_django_info(self):
        """Informations Django"""
        return {
            "version": settings.VERSION if hasattr(settings, 'VERSION') else "N/A",
            "debug": settings.DEBUG,
            "allowed_hosts": settings.ALLOWED_HOSTS,
            "installed_apps_count": len(settings.INSTALLED_APPS),
            "middleware_count": len(settings.MIDDLEWARE),
            "database_engine": settings.DATABASES['default']['ENGINE'],
            "static_root": settings.STATIC_ROOT,
            "secret_key_set": bool(settings.SECRET_KEY and settings.SECRET_KEY != 'django-insecure-'),
        }
    
    def get_database_info(self):
        """Informations sur la base de données"""
        try:
            from django.db import connection
            
            with connection.cursor() as cursor:
                # Tables Django essentielles
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' 
                    AND name IN ('django_migrations', 'django_session', 'auth_user', 'django_content_type')
                """)
                essential_tables = [row[0] for row in cursor.fetchall()]
                
                # Nombre de migrations appliquées
                cursor.execute("SELECT COUNT(*) FROM django_migrations")
                migrations_count = cursor.fetchone()[0]
                
                # Nombre d'utilisateurs
                cursor.execute("SELECT COUNT(*) FROM auth_user")
                users_count = cursor.fetchone()[0]
                
            return {
                "essential_tables_found": essential_tables,
                "essential_tables_missing": [t for t in ['django_migrations', 'django_session', 'auth_user', 'django_content_type'] 
                                           if t not in essential_tables],
                "migrations_applied": migrations_count,
                "users_count": users_count,
                "connection_ok": True,
            }
        except Exception as e:
            return {
                "connection_ok": False,
                "error": str(e),
            }
    
    def get_filesystem_info(self):
        """Informations sur le système de fichiers"""
        paths_to_check = [
            ("static_root", settings.STATIC_ROOT),
            ("base_dir", settings.BASE_DIR),
            ("current_dir", os.getcwd()),
        ]
        
        info = {}
        for name, path in paths_to_check:
            if path:
                try:
                    if os.path.exists(path):
                        if os.path.isdir(path):
                            # Compter les fichiers
                            count = sum(len(files) for _, _, files in os.walk(path))
                            info[name] = {
                                "exists": True,
                                "is_directory": True,
                                "file_count": count,
                                "path": path,
                            }
                        else:
                            info[name] = {
                                "exists": True,
                                "is_directory": False,
                                "path": path,
                            }
                    else:
                        info[name] = {
                            "exists": False,
                            "path": path,
                        }
                except Exception as e:
                    info[name] = {
                        "error": str(e),
                        "path": path,
                    }
        
        return info
    
    def get_services_info(self):
        """Informations sur les services"""
        return {
            "web_concurrency": os.environ.get('WEB_CONCURRENCY', '1'),
            "port": os.environ.get('PORT', '10000'),
            "disable_collectstatic": os.environ.get('DISABLE_COLLECTSTATIC', '0'),
            "python_version_env": os.environ.get('PYTHON_VERSION', 'N/A'),
        }
    
    def check_migrations(self, data):
        """Vérifie l'état des migrations"""
        try:
            result = subprocess.run(
                ['python', 'manage.py', 'showmigrations', '--list'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                pending = [line for line in lines if '[ ]' in line]
                
                if pending:
                    data["issues"].append(f"{len(pending)} migration(s) en attente")
                    data["recommendations"].append("Exécuter: python manage.py migrate")
            else:
                data["issues"].append("Impossible de vérifier les migrations")
                
        except subprocess.TimeoutExpired:
            data["issues"].append("Timeout lors de la vérification des migrations")
        except Exception as e:
            data["issues"].append(f"Erreur vérification migrations: {str(e)}")
    
    def check_static_files(self, data):
        """Vérifie les fichiers statiques"""
        static_root = settings.STATIC_ROOT
        
        if static_root and os.path.exists(static_root):
            # Vérifier les fichiers critiques
            critical_files = [
                os.path.join(static_root, "mutuelle_core", "images", "logo.jpg"),
                os.path.join(static_root, "js", "messagerie-integration.js"),
                os.path.join(static_root, "img", "favicon.ico"),
            ]
            
            missing_files = []
            for file_path in critical_files:
                if not os.path.exists(file_path):
                    missing_files.append(os.path.relpath(file_path, static_root))
            
            if missing_files:
                data["issues"].append(f"Fichiers statiques manquants: {', '.join(missing_files)}")
                data["recommendations"].append("Exécuter: python manage.py collectstatic")
        else:
            data["issues"].append("Répertoire STATIC_ROOT non configuré ou inexistant")
    
    def check_environment_vars(self, data):
        """Vérifie les variables d'environnement critiques"""
        critical_vars = {
            'SECRET_KEY': 'Clé secrète Django',
            'ALLOWED_HOSTS': 'Hosts autorisés',
            'DATABASE_URL': 'URL de base de données',
        }
        
        for var, description in critical_vars.items():
            if var not in os.environ and not hasattr(settings, var):
                data["issues"].append(f"Variable d'environnement manquante: {var} ({description})")