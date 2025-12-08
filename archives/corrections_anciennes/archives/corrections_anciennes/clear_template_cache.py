import os
import shutil
from django.core.management import execute_from_command_line

def clear_template_cache():
    print("🧹 NETTOYAGE COMPLET DU CACHE TEMPLATES")
    
    # 1. Vider le cache Django
    os.system('python manage.py clear_cache')
    
    # 2. Supprimer le cache templates
    cache_dirs = [
        'templates/__pycache__',
        'agents/templatetags/__pycache__',
    ]
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
            print(f"✅ Supprimé: {cache_dir}")
    
    # 3. Redémarrer
    print("🔄 Redémarrage du serveur...")
    os.system('python manage.py runserver --noreload')

if __name__ == '__main__':
    clear_template_cache()