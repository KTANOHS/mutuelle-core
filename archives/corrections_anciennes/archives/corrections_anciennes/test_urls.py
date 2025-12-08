#!/usr/bin/env python3
"""
SCRIPT DE VÉRIFICATION DES URLS
Teste l'accessibilité des endpoints
"""

import os
import django
from django.test import Client
from django.urls import reverse, resolve
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

class URLTester:
    def __init__(self):
        self.client = Client()
        self.results = []
    
    def test_url(self, url_name, args=None, kwargs=None):
        """Teste une URL spécifique"""
        try:
            url = reverse(url_name, args=args, kwargs=kwargs)
            response = self.client.get(url)
            
            result = {
                'url_name': url_name,
                'url': url,
                'status_code': response.status_code,
                'working': 200 <= response.status_code < 400
            }
            
            self.results.append(result)
            
            status_icon = "✅" if result['working'] else "❌"
            print(f"{status_icon} {url_name:30} -> {url:40} [{response.status_code}]")
            
        except Exception as e:
            print(f"❌ {url_name:30} -> ERREUR: {e}")
            self.results.append({
                'url_name': url_name,
                'error': str(e),
                'working': False
            })
    
    def test_core_urls(self):
        """Teste les URLs principales"""
        print("=" * 60)
        print("🌐 TEST DES URLS PRINCIPALES")
        print("=" * 60)
        
        # URLs de base
        base_urls = [
            'admin:index',
            'login',
            'logout',
        ]
        
        for url_name in base_urls:
            self.test_url(url_name)
        
        # URLs des applications (à adapter selon vos apps)
        app_urls = [
            'membres:dashboard',
            'agents:dashboard', 
            'api:root',
        ]
        
        for url_name in app_urls:
            self.test_url(url_name)
    
    def generate_report(self):
        """Génère un rapport des tests"""
        working_urls = [r for r in self.results if r.get('working')]
        broken_urls = [r for r in self.results if not r.get('working')]
        
        print(f"\n📊 RAPPORT URLS:")
        print(f"   ✅ URLs fonctionnelles: {len(working_urls)}")
        print(f"   ❌ URLs défaillantes: {len(broken_urls)}")
        
        if broken_urls:
            print(f"\n🚨 URLS À CORRIGER:")
            for result in broken_urls:
                print(f"   • {result['url_name']}: {result.get('error', 'Status code erreur')}")

def test_urls():
    """Teste toutes les URLs"""
    tester = URLTester()
    tester.test_core_urls()
    tester.generate_report()

if __name__ == "__main__":
    test_urls()