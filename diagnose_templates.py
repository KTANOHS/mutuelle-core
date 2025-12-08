# diagnose_templates.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.template.loader import get_template
from django.template import TemplateDoesNotExist

def diagnose_templates():
    print("🔍 DIAGNOSTIC DES TEMPLATES")
    print("=" * 50)
    
    templates_to_check = [
        'medecin/base_medecin.html',
        'medecin/creer_ordonnance.html',
        'base.html'
    ]
    
    for template_name in templates_to_check:
        try:
            template = get_template(template_name)
            print(f"✅ {template_name} : TROUVÉ")
            print(f"   Chemin: {template.origin.name}")
        except TemplateDoesNotExist:
            print(f"❌ {template_name} : NON TROUVÉ")
    
    # Vérifier les dossiers de templates
    print("\n📁 DOSSERS DE TEMPLATES CONFIGURÉS:")
    from django.template.engine import Engine
    engine = Engine.get_default()
    for loader in engine.template_loaders:
        if hasattr(loader, 'get_dirs'):
            dirs = loader.get_dirs()
            for dir in dirs:
                print(f"   - {dir}")
    
    # Vérifier si base_medecin.html existe physiquement
    print("\n🔎 VÉRIFICATION PHYSIQUE:")
    import os
    template_paths = [
        'templates/medecin/base_medecin.html',
        'medecin/templates/medecin/base_medecin.html'
    ]
    
    for path in template_paths:
        if os.path.exists(path):
            print(f"✅ {path} : EXISTE")
            print(f"   Taille: {os.path.getsize(path)} octets")
        else:
            print(f"❌ {path} : N'EXISTE PAS")

if __name__ == "__main__":
    diagnose_templates()