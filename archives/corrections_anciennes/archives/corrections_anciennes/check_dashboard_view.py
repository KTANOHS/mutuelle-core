#!/usr/bin/env python3
# check_dashboard_view.py

import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    # Analyser la vue dashboard
    views_path = BASE_DIR / 'membres' / 'views.py'
    
    if views_path.exists():
        print("🔍 Analyse de la vue dashboard dans membres/views.py")
        print("=" * 50)
        
        with open(views_path, 'r') as f:
            content = f.read()
            
        # Chercher la fonction dashboard
        import re
        
        # Pattern pour trouver la fonction dashboard
        dashboard_pattern = r'def dashboard\(request\):.*?return render\(request,\s*[\'"]([^\'"]+)[\'"]'
        match = re.search(dashboard_pattern, content, re.DOTALL)
        
        if match:
            template_name = match.group(1)
            print(f"✅ Template utilisé dans la vue: {template_name}")
            
            # Vérifier si le template existe
            from django.template.loader import get_template
            try:
                template = get_template(template_name)
                print(f"✅ Template trouvé: {template.origin.name}")
            except Exception as e:
                print(f"❌ Template non trouvé: {e}")
        else:
            print("❌ Fonction dashboard non trouvée dans membres/views.py")
            
        # Vérifier les URLs
        print("\n🔗 Vérification des URLs:")
        from django.urls import get_resolver
        try:
            resolver = get_resolver()
            url_patterns = []
            
            def collect_urls(patterns, namespace=None):
                for pattern in patterns:
                    if hasattr(pattern, 'pattern'):
                        if hasattr(pattern, 'url_patterns'):
                            # C'est un include
                            new_namespace = pattern.namespace if hasattr(pattern, 'namespace') else namespace
                            collect_urls(pattern.url_patterns, new_namespace)
                        else:
                            # C'est un pattern simple
                            url_patterns.append({
                                'pattern': str(pattern.pattern),
                                'name': pattern.name,
                                'namespace': namespace
                            })
            
            collect_urls(resolver.url_patterns)
            
            # Filtrer les URLs dashboard
            dashboard_urls = [url for url in url_patterns if 'dashboard' in str(url['pattern']).lower() or 
                             (url['name'] and 'dashboard' in url['name'].lower())]
            
            for url in dashboard_urls:
                print(f"   📍 {url['namespace'] + ':' if url['namespace'] else ''}{url['name'] or 'unnamed'} -> {url['pattern']}")
                
        except Exception as e:
            print(f"   Erreur lors de l'analyse des URLs: {e}")
            
except Exception as e:
    print(f"Erreur: {e}")