#!/usr/bin/env python3
"""
SCRIPT DE VÉRIFICATION DE COHÉRENCE URLs
"""

import os
import re

def verifier_coherence_urls():
    """Vérifie la cohérence entre urls.py et les templates"""
    
    print("🔍 VÉRIFICATION DE COHÉRENCE URLs")
    print("=" * 50)
    
    # 1. Lire agents/urls.py
    with open('agents/urls.py', 'r') as f:
        urls_content = f.read()
    
    # Extraire tous les noms d'URLs
    url_pattern = r"name='([^']+)'"
    url_names = re.findall(url_pattern, urls_content)
    
    print("📋 Noms d'URLs dans agents/urls.py:")
    for name in url_names:
        print(f"   - {name}")
    
    # 2. Vérifier le template base_agent.html
    with open('templates/agents/base_agent.html', 'r') as f:
        template_content = f.read()
    
    # Extraire toutes les références d'URL dans le template
    template_urls = re.findall(r"{% url 'agents:([^']+)' %}", template_content)
    
    print("\n📋 Références d'URL dans base_agent.html:")
    for url_ref in template_urls:
        status = "✅" if url_ref in url_names else "❌"
        print(f"   {status} agents:{url_ref}")
    
    # 3. Vérifier les incohérences
    print("\n🔍 INCOHÉRENCES DÉTECTÉES:")
    incoherences = []
    for url_ref in template_urls:
        if url_ref not in url_names:
            incoherences.append(url_ref)
    
    if incoherences:
        for inc in incoherences:
            print(f"   ❌ '{inc}' utilisé dans le template mais non trouvé dans urls.py")
    else:
        print("   ✅ Aucune incohérence détectée")
    
    return len(incoherences) == 0

if __name__ == "__main__":
    if verifier_coherence_urls():
        print("\n🎯 TOUT EST COHÉRENT - Redémarrez le serveur")
    else:
        print("\n🚨 CORRIGEZ LES INCOHÉRENCES AVANT DE CONTINUER")