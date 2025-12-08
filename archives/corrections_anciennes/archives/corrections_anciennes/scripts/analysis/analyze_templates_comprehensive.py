# analyze_templates_comprehensive.py
import os
import django
from django.conf import settings
from django.template.loader import get_template
from django.urls import get_resolver
import re

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyze_templates_structure():
    """Analyse complète de la structure des templates"""
    
    templates_dir = os.path.join(settings.BASE_DIR, 'templates')
    print("🔍 ANALYSE DES TEMPLATES")
    print("=" * 60)
    
    # Statistiques générales
    template_count = 0
    template_extensions = {}
    template_sizes = {}
    
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith(('.html', '.htm', '.txt')):
                template_count += 1
                ext = os.path.splitext(file)[1]
                template_extensions[ext] = template_extensions.get(ext, 0) + 1
                
                file_path = os.path.join(root, file)
                size = os.path.getsize(file_path)
                template_sizes[file] = size
                
                # Afficher le chemin relatif
                rel_path = os.path.relpath(file_path, templates_dir)
                print(f"📄 {rel_path} ({size} bytes)")
    
    print(f"\n📊 STATISTIQUES TEMPLATES:")
    print(f"• Total templates: {template_count}")
    print(f"• Répartition extensions: {template_extensions}")
    
    # Templates les plus volumineux
    if template_sizes:
        largest = sorted(template_sizes.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"• Templates les plus volumineux:")
        for name, size in largest:
            print(f"  - {name}: {size} bytes")

def analyze_template_content():
    """Analyse le contenu des templates"""
    
    templates_dir = os.path.join(settings.BASE_DIR, 'templates')
    template_patterns = {
        'extends': r'\{%\s*extends\s+[\'"]([^\'"]+)[\'"]\s*%\}',
        'include': r'\{%\s*include\s+[\'"]([^\'"]+)[\'"]\s*%\}',
        'url_tags': r'\{%\s*url\s+[\'"]([^\'"]+)[\'"]\s*%\}',
        'static_tags': r'\{%\s*static\s+[\'"]([^\'"]+)[\'"]\s*%\}',
        'for_loops': r'\{%\s*for\s+.*?%\}',
        'if_conditions': r'\{%\s*if\s+.*?%\}',
    }
    
    print(f"\n🔧 ANALYSE DU CONTENU DES TEMPLATES")
    print("=" * 60)
    
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, templates_dir)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                print(f"\n📋 {rel_path}:")
                
                for pattern_name, pattern in template_patterns.items():
                    matches = re.findall(pattern, content)
                    if matches:
                        print(f"  • {pattern_name}: {len(matches)} occurrences")
                        if pattern_name in ['extends', 'include'] and matches:
                            print(f"    → {matches}")

def map_urls_to_templates():
    """Mappe les URLs vers leurs templates"""
    
    print(f"\n🌐 MAPPING URLs → TEMPLATES")
    print("=" * 60)
    
    urlconf = get_resolver()
    
    def extract_urls(url_patterns, prefix=''):
        for pattern in url_patterns:
            if hasattr(pattern, 'url_patterns'):
                # Pattern include
                new_prefix = prefix + str(pattern.pattern)
                extract_urls(pattern.url_patterns, new_prefix)
            else:
                # Pattern simple
                full_path = prefix + str(pattern.pattern)
                view = pattern.callback
                
                # Essayer d'extraire le nom du template
                template_name = "Non spécifié"
                if hasattr(view, 'view_class'):
                    # View basée sur une classe
                    view_class = view.view_class
                    if hasattr(view_class, 'template_name'):
                        template_name = view_class.template_name
                elif hasattr(view, 'template_name'):
                    # View fonction avec template_name
                    template_name = view.template_name
                
                print(f"🔗 {full_path}")
                print(f"   👁️  View: {view.__name__ if hasattr(view, '__name__') else view}")
                print(f"   📄 Template: {template_name}")
                print()

    extract_urls(urlconf.url_patterns)

def check_template_inheritance():
    """Vérifie la hiérarchie d'héritage des templates"""
    
    print(f"\n🏗️  HIÉRARCHIE DES TEMPLATES")
    print("=" * 60)
    
    templates_dir = os.path.join(settings.BASE_DIR, 'templates')
    inheritance_chain = {}
    
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, templates_dir)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                extends_match = re.search(r'\{%\s*extends\s+[\'"]([^\'"]+)[\'"]\s*%\}', content)
                if extends_match:
                    parent_template = extends_match.group(1)
                    inheritance_chain[rel_path] = parent_template
    
    # Afficher les chaînes d'héritage
    for child, parent in inheritance_chain.items():
        print(f"📄 {child} → extends → {parent}")

if __name__ == "__main__":
    analyze_templates_structure()
    analyze_template_content()
    map_urls_to_templates()
    check_template_inheritance()