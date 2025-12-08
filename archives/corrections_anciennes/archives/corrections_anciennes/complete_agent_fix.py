#!/usr/bin/env python3
"""
Correction complète des problèmes agent
"""

from pathlib import Path
import re

def complete_agent_fix():
    print("🎯 CORRECTION COMPLÈTE AGENT")
    print("=" * 50)
    
    # 1. Corriger les URLs cassées dans le dashboard
    print("\n1. 📝 Correction des URLs cassées...")
    emergency_fix_broken_urls()
    
    # 2. Corriger l'incohérence agents_notifications → notifications
    print("\n2. 🔄 Correction incohérence notifications...")
    fix_notifications_url()
    
    # 3. Vérifier la configuration
    print("\n3. 🔧 Vérification configuration...")
    check_configuration()

def fix_notifications_url():
    """Corriger l'URL agents_notifications → notifications"""
    agents_dir = Path("templates/agents")
    
    for template_file in agents_dir.rglob("*.html"):
        content = template_file.read_text()
        original_content = content
        
        # Remplacer l'ancien nom par le nouveau
        content = content.replace("agents:agents_notifications", "agents:notifications")
        
        if content != original_content:
            template_file.write_text(content)
            print(f"✅ {template_file.name}: agents_notifications → notifications")

def check_configuration():
    """Vérifier la configuration finale"""
    print("\n📋 CONFIGURATION FINALE:")
    
    # Vérifier urls.py
    urls_path = Path("agents/urls.py")
    if urls_path.exists():
        content = urls_path.read_text()
        required_urls = ['creer_bon_soin', 'liste_membres', 'notifications', 'verification_cotisation']
        
        for url_name in required_urls:
            if f"name='{url_name}'" in content or f'name="{url_name}"' in content:
                print(f"   ✅ {url_name}")
            else:
                print(f"   ❌ {url_name}")
    else:
        print("❌ agents/urls.py non trouvé")

if __name__ == "__main__":
    complete_agent_fix()