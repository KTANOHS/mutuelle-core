# analyze_urls_templates_mapping.py
import os
import django
from django.conf import settings
from django.urls import get_resolver
import inspect

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyze_url_template_mapping():
    """Analyse détaillée du mapping entre URLs et templates"""
    
    print("🔗 MAPPING COMPLET URLs → TEMPLATES")
    print("=" * 80)
    
    url_resolver = get_resolver()
    url_mappings = []
    
    def collect_urls(patterns, namespace='', prefix=''):
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):
                # Namespace ou include
                new_namespace = pattern.namespace or namespace
                new_prefix = prefix + str(pattern.pattern)
                collect_urls(pattern.url_patterns, new_namespace, new_prefix)
            else:
                # URL simple
                full_path = prefix + str(pattern.pattern)
                view = pattern.callback
                
                # Extraire les informations de la view
                view_info = extract_view_info(view, full_path)
                url_mappings.append(view_info)
    
    def extract_view_info(view, url_path):
        """Extrait les informations d'une view"""
        info = {
            'url': url_path,
            'view_name': getattr(view, '__name__', str(view)),
            'template': 'Non spécifié',
            'view_type': 'Fonction' if hasattr(view, '__name__') else 'Classe',
            'module': inspect.getmodule(view).__name__ if inspect.getmodule(view) else 'Inconnu'
        }
        
        # Essayer d'extraire le template
        if hasattr(view, 'view_class'):
            # View basée sur une classe
            view_class = view.view_class
            if hasattr(view_class, 'template_name'):
                info['template'] = view_class.template_name
            elif hasattr(view_class, 'get_template_names'):
                try:
                    # Créer une instance pour appeler get_template_names
                    instance = view_class()
                    templates = instance.get_template_names()
                    info['template'] = templates[0] if templates else 'Dynamique'
                except:
                    info['template'] = 'Dynamique (erreur)'
        elif hasattr(view, 'template_name'):
            info['template'] = view.template_name
        
        return info
    
    collect_urls(url_resolver.url_patterns)
    
    # Afficher les résultats par application
    apps_mapping = {}
    for mapping in url_mappings:
        module_parts = mapping['module'].split('.')
        app_name = module_parts[0] if module_parts else 'core'
        
        if app_name not in apps_mapping:
            apps_mapping[app_name] = []
        apps_mapping[app_name].append(mapping)
    
    # Afficher par application
    for app_name, mappings in apps_mapping.items():
        print(f"\n📱 APPLICATION: {app_name.upper()}")
        print("-" * 60)
        
        for mapping in mappings:
            print(f"🌐 URL: {mapping['url']}")
            print(f"   👁️  View: {mapping['view_name']} ({mapping['view_type']})")
            print(f"   📄 Template: {mapping['template']}")
            print(f"   📦 Module: {mapping['module']}")
            print()

def check_template_existence():
    """Vérifie l'existence des templates référencés"""
    
    print("\n🔍 VÉRIFICATION DE L'EXISTENCE DES TEMPLATES")
    print("=" * 60)
    
    templates_dir = os.path.join(settings.BASE_DIR, 'templates')
    all_templates = []
    
    # Lister tous les templates existants
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                rel_path = os.path.relpath(os.path.join(root, file), templates_dir)
                all_templates.append(rel_path.replace('\\', '/'))
    
    # Analyser les URLs pour trouver les templates référencés
    url_resolver = get_resolver()
    referenced_templates = set()
    
    def find_templates_in_views(patterns):
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):
                find_templates_in_views(pattern.url_patterns)
            else:
                view = pattern.callback
                template_name = extract_template_name(view)
                if template_name and template_name != 'Non spécifié':
                    referenced_templates.add(template_name)
    
    def extract_template_name(view):
        if hasattr(view, 'view_class'):
            view_class = view.view_class
            if hasattr(view_class, 'template_name'):
                return view_class.template_name
        elif hasattr(view, 'template_name'):
            return view.template_name
        return None
    
    find_templates_in_views(url_resolver.url_patterns)
    
    # Vérifier l'existence
    missing_templates = []
    for template in referenced_templates:
        if template not in all_templates:
            missing_templates.append(template)
        else:
            print(f"✅ {template}")
    
    if missing_templates:
        print(f"\n❌ TEMPLATES MANQUANTS:")
        for template in missing_templates:
            print(f"   - {template}")

if __name__ == "__main__":
    analyze_url_template_mapping()
    check_template_existence()