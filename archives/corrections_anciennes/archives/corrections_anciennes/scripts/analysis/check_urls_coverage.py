#!/usr/bin/env python3
"""
Vérifie la couverture des URLs et les vues manquantes
"""

import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.urls import get_resolver

class URLCoverageChecker:
    """Vérifie la couverture des URLs"""
    
    def check_urls_coverage(self):
        """Vérifie toutes les URLs enregistrées"""
        print("🔗 VÉRIFICATION DE LA COUVERTURE DES URLs")
        print("=" * 50)
        
        resolver = get_resolver()
        all_urls = self.get_all_urls(resolver)
        
        print(f"📊 URLs totales dans le projet: {len(all_urls)}")
        
        # Vérifier les apps spécifiques de votre projet
        apps_to_check = ['assureur', 'medecin', 'pharmacien', 'membres', 'paiements', 'soins', 'api', 'core']
        
        for app_name in apps_to_check:
            app_urls = [url for url in all_urls if app_name in url['pattern'] or app_name == url['app_name']]
            print(f"\n📱 {app_name.upper()}: {len(app_urls)} URLs")
            
            for url in app_urls[:3]:  # Afficher 3 URLs par app
                print(f"   🔗 {url['pattern']} → {url['view_name']}")
            
            if len(app_urls) > 3:
                print(f"   ... et {len(app_urls) - 3} autres")
    
    def get_all_urls(self, resolver, namespace='', prefix=''):
        """Récupère toutes les URLs"""
        url_patterns = []
        
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'url_patterns'):
                # Sous-URLs
                new_namespace = pattern.namespace or namespace
                new_prefix = f"{prefix}{pattern.pattern.regex.pattern}"
                url_patterns.extend(self.get_all_urls(pattern, new_namespace, new_prefix))
            else:
                url_info = {
                    'pattern': f"{prefix}{pattern.pattern.regex.pattern}",
                    'view_name': pattern.callback.__name__ if hasattr(pattern.callback, '__name__') else str(pattern.callback),
                    'app_name': namespace.split(':')[0] if ':' in namespace else 'core',
                }
                url_patterns.append(url_info)
        
        return url_patterns

def main():
    """Fonction principale"""
    checker = URLCoverageChecker()
    checker.check_urls_coverage()

if __name__ == "__main__":
    main()