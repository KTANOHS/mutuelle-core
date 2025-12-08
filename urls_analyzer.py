#!/usr/bin/env python
"""
ANALYSE SPÉCIFIQUE DES URLs AGENTS
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

from django.urls import get_resolver, reverse, NoReverseMatch
from agents import urls as agents_urls

def analyze_urls():
    print("🔗 ANALYSE DÉTAILLÉE DES URLs AGENTS")
    print("=" * 50)
    
    resolver = get_resolver(agents_urls)
    
    print("📋 Liste complète des URLs:")
    print("-" * 30)
    
    url_count = 0
    for pattern in resolver.url_patterns:
        if hasattr(pattern, 'pattern'):
            url_name = getattr(pattern, 'name', 'Sans nom')
            url_pattern = str(pattern.pattern)
            print(f"📍 {url_name:30} -> {url_pattern}")
            url_count += 1
            
    print(f"\n📊 Total: {url_count} URLs définies")
    
    # Tester le reverse des URLs principales
    print("\n🧪 TEST DES URLs PRINCIPALES:")
    print("-" * 30)
    
    test_urls = [
        'agents:dashboard',
        'agents:verification_cotisations', 
        'agents:creer_bon_soin',
        'agents:recherche_membres_api',
        'agents:verifier_cotisation_api',
    ]
    
    for url_name in test_urls:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name:35} -> {url}")
        except NoReverseMatch:
            print(f"❌ {url_name:35} -> NON TROUVÉE")

if __name__ == '__main__':
    analyze_urls()