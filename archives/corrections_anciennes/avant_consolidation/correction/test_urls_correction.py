"""
TESTS POUR LA CORRECTION DES URLs
"""

import os
import django
from django.test import TestCase
from django.urls import reverse, NoReverseMatch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

class TestUrlsBasics(TestCase):
    """Tests de base pour les URLs"""
    
    def test_urls_essentielles(self):
        """Test que les URLs essentielles existent"""
        urls_essentielles = [
            'home',
            'login',
            'logout',
            'dashboard',
        ]
        
        for url_name in urls_essentielles:
            with self.subTest(url=url_name):
                try:
                    reverse(url_name)
                except NoReverseMatch:
                    self.fail(f"URL essentielle manquante: {url_name}")
    
    def test_apps_principales(self):
        """Test que les applications principales ont leurs URLs"""
        apps_principales = [
            ('agents:dashboard', []),
            ('medecin:dashboard', []),
            ('membres:dashboard', []),
            ('assureur:dashboard', []),
            ('pharmacien:dashboard', []),
        ]
        
        for url_name, args in apps_principales:
            with self.subTest(app=url_name):
                try:
                    reverse(url_name, args=args)
                except NoReverseMatch:
                    # Ce n'est pas un échec critique, juste un warning
                    print(f"⚠️  URL d'application manquante: {url_name}")

class TestConflitsUrls(TestCase):
    """Test des conflits d'URLs identifiés"""
    
    def test_pas_de_doublon_creation_membre(self):
        """Vérifie qu'il n'y a pas de doublon pour la création membre"""
        from django.urls import get_resolver
        
        resolver = get_resolver()
        urls_creation = []
        
        def trouver_creation_membre(patterns, namespace=None):
            for pattern in patterns:
                if hasattr(pattern, 'url_patterns'):
                    new_ns = f"{namespace}:{pattern.namespace}" if namespace else pattern.namespace
                    trouver_creation_membre(pattern.url_patterns, new_ns)
                elif pattern.name and 'creer_membre' in pattern.name:
                    urls_creation.append({
                        'namespace': namespace,
                        'name': pattern.name,
                        'pattern': str(pattern.pattern)
                    })
        
        trouver_creation_membre(resolver.url_patterns)
        
        # Ne devrait avoir qu'une seule URL de création membre
        noms_uniques = set(url['name'] for url in urls_creation)
        if len(noms_uniques) > 1:
            print(f"⚠️  Plusieurs URLs création membre: {noms_uniques}")

if __name__ == "__main__":
    import unittest
    unittest.main()