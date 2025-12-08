#!/usr/bin/env python3
"""
Diagnostic des URLs dans le dashboard agent
"""

from pathlib import Path
import re

def diagnose_dashboard_urls():
    dashboard_path = Path("templates/agents/dashboard.html")
    
    if not dashboard_path.exists():
        print("❌ Fichier dashboard.html introuvable")
        return
    
    content = dashboard_path.read_text()
    
    print("🔍 ANALYSE DES URLS DANS LE DASHBOARD AGENT")
    print("=" * 50)
    
    # Trouver toutes les URLs
    urls = re.findall(r'\{%\s*url\s+[\'"]([^\'"]+)[\'"]\s*%\}', content)
    
    print(f"\n📋 URLs trouvées ({len(urls)}):")
    for url in urls:
        print(f"   🔗 {url}")
    
    # Vérifier les URLs problématiques
    print(f"\n⚠️  URLs à vérifier:")
    for url in urls:
        if ':' not in url and not url.startswith('#'):
            print(f"   ❌ {url} - Manque peut-être le namespace")
    
    # Vérifier les liens href
    href_links = re.findall(r'href=[\'"]([^\'"]*)[\'"]', content)
    print(f"\n🔗 Liens href trouvés ({len(href_links)}):")
    for link in href_links[:10]:  # Afficher les 10 premiers
        if link and not link.startswith(('http', '#', 'javascript')):
            print(f"   📎 {link}")

if __name__ == "__main__":
    diagnose_dashboard_urls()