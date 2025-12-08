# assureur/diagnostic.py
import os
import django
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.template.loader import get_template

def find_dashboard_template():
    """Trouve quel template est utilisé pour le dashboard assureur"""
    try:
        # Essayer de trouver le template
        template = get_template('assureur/dashboard.html')
        print(f"✅ Template trouvé: {template.origin.name}")
        print(f"📁 Chemin complet: {template.origin.loadname}")
        return True
    except Exception as e:
        print(f"❌ Template non trouvé: {e}")
        return False

def list_assureur_templates():
    """Lister tous les templates de l'app assureur"""
    template_dirs = settings.TEMPLATES[0]['DIRS']
    print("📂 Dossiers de templates configurés:")
    for dir in template_dirs:
        print(f"  - {dir}")
    
    # Chercher dans les apps installed
    from django.apps import apps
    assureur_config = apps.get_app_config('assureur')
    if assureur_config:
        print(f"📦 App assureur trouvée: {assureur_config.path}")
        templates_path = os.path.join(assureur_config.path, 'templates')
        if os.path.exists(templates_path):
            print(f"📁 Templates de l'app: {templates_path}")

if __name__ == "__main__":
    print("🔍 Diagnostic du dashboard assureur...")
    list_assureur_templates()
    find_dashboard_template()