# analyze_template_blocks.py
import os
import re
from django.conf import settings

def analyze_template_blocks():
    """Analyse les blocs et composants réutilisables dans les templates"""
    
    templates_dir = os.path.join(settings.BASE_DIR, 'templates')
    
    print("🎨 ANALYSE DES BLOCS ET COMPOSANTS TEMPLATES")
    print("=" * 60)
    
    block_analysis = {}
    included_templates = set()
    
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, templates_dir)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Analyser les blocs
                blocks = re.findall(r'\{%\s*block\s+(\w+)\s*%\}', content)
                if blocks:
                    block_analysis[rel_path] = {
                        'blocks': blocks,
                        'includes': re.findall(r'\{%\s*include\s+[\'"]([^\'"]+)[\'"]\s*%\}', content),
                        'extends': re.findall(r'\{%\s*extends\s+[\'"]([^\'"]+)[\'"]\s*%\}', content)
                    }
                
                # Collecter les includes
                includes = re.findall(r'\{%\s*include\s+[\'"]([^\'"]+)[\'"]\s*%\}', content)
                included_templates.update(includes)
    
    # Afficher l'analyse des blocs
    print("\n📦 BLOCS PAR TEMPLATE:")
    for template, data in block_analysis.items():
        print(f"\n📄 {template}:")
        if data['blocks']:
            print(f"   🧱 Blocs: {', '.join(data['blocks'])}")
        if data['extends']:
            print(f"   🔗 Étend: {data['extends'][0]}")
        if data['includes']:
            print(f"   📎 Inclut: {', '.join(data['includes'])}")
    
    # Analyser la réutilisation
    print(f"\n🔄 TEMPLATES LES PLUS RÉUTILISÉS:")
    template_usage = {}
    for template, data in block_analysis.items():
        for included in data['includes']:
            template_usage[included] = template_usage.get(included, 0) + 1
    
    for template, count in sorted(template_usage.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   {template}: utilisé {count} fois")

def find_unused_templates():
    """Trouve les templates qui ne sont jamais inclus ou étendus"""
    
    templates_dir = os.path.join(settings.BASE_DIR, 'templates')
    all_templates = set()
    referenced_templates = set()
    
    # Collecter tous les templates
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                rel_path = os.path.relpath(os.path.join(root, file), templates_dir)
                all_templates.add(rel_path.replace('\\', '/'))
    
    # Collecter les templates référencés
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Trouver les extends et includes
                extends = re.findall(r'\{%\s*extends\s+[\'"]([^\'"]+)[\'"]\s*%\}', content)
                includes = re.findall(r'\{%\s*include\s+[\'"]([^\'"]+)[\'"]\s*%\}', content)
                
                referenced_templates.update(extends)
                referenced_templates.update(includes)
    
    # Templates non référencés
    unused_templates = all_templates - referenced_templates
    
    print(f"\n📊 STATISTIQUES DE RÉUTILISATION:")
    print(f"• Total templates: {len(all_templates)}")
    print(f"• Templates référencés: {len(referenced_templates)}")
    print(f"• Templates non référencés: {len(unused_templates)}")
    
    if unused_templates:
        print(f"\n📌 TEMPLATES POTENTIELLEMENT INUTILISÉS:")
        for template in sorted(unused_templates):
            print(f"   - {template}")

if __name__ == "__main__":
    analyze_template_blocks()
    find_unused_templates()