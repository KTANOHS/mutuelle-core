#!/usr/bin/env python3
"""
Correction complète des problèmes agent - VERSION CORRIGÉE
"""

from pathlib import Path
import re

def emergency_fix_broken_urls():
    """CORRECTION URGENTE des URLs cassées dans le dashboard"""
    dashboard_path = Path("templates/agents/dashboard.html")
    
    if not dashboard_path.exists():
        print("❌ Dashboard non trouvé")
        return
    
    content = dashboard_path.read_text()
    original_content = content
    
    print("🚨 CORRECTION URGENTE DES URLS CASSÉES")
    print("=" * 50)
    
    # PROBLÈME: Les URLs Django dans les href sont mal fermées
    # Trouver toutes les occurrences problématiques
    broken_patterns = re.findall(r'href=[\'"]\{%\s*url\s+[^\'"]*', content)
    print(f"🚨 URLs cassées détectées: {len(broken_patterns)}")
    
    if broken_patterns:
        for pattern in broken_patterns[:3]:  # Montrer les 3 premiers
            print(f"   ❌ Exemple: {pattern}...")
    
    # CORRECTION: Remplacer les URLs cassées par les bonnes
    corrections = {
        # Pattern cassé → Correction
        r'href="\{% url \'agents:creer_bon_soin\' %\}': 'href="{% url \'agents:creer_bon_soin\' %}"',
        r'href="\{% url \'agents:liste_membres\' %\}': 'href="{% url \'agents:liste_membres\' %}"',
        r'href="\{% url \'agents:historique_bons\' %\}': 'href="{% url \'agents:historique_bons\' %}"',
        r'href="\{% url \'agents:agents_notifications\' %\}': 'href="{% url \'agents:notifications\' %}"',
        r'href="\{% url \'agents:verification_cotisation\' %\}': 'href="{% url \'agents:verification_cotisation\' %}"',
    }
    
    total_fixes = 0
    for broken, fixed in corrections.items():
        before = content.count(broken)
        content = content.replace(broken, fixed)
        after = content.count(broken)
        fixes = before - after
        total_fixes += fixes
        if fixes > 0:
            print(f"✅ Fixé: {broken} → {fixed}")
    
    # Vérification finale
    remaining_broken = re.findall(r'href="\{%\s*url\s+[^\'"]*', content)
    if remaining_broken:
        print(f"⚠️  Il reste {len(remaining_broken)} URLs mal formatées")
        # Correction générique pour les restants
        content = re.sub(
            r'href="\{%\s*url\s+([^\'"]*)', 
            r'href="{% url \1', 
            content
        )
        print("✅ Correction générique appliquée")
    
    if content != original_content:
        # Sauvegarde
        backup_path = dashboard_path.with_suffix('.html.broken_urls_backup')
        dashboard_path.rename(backup_path)
        
        # Écrire la version corrigée
        dashboard_path.write_text(content)
        print(f"\n🎯 RÉSULTAT:")
        print(f"✅ Dashboard corrigé avec succès!")
        print(f"📦 Backup sauvegardé: {backup_path}")
        print(f"🔧 {total_fixes} corrections appliquées")
        
        # Vérifier le résultat
        verify_fix()
    else:
        print("ℹ️  Aucune correction nécessaire")

def verify_fix():
    """Vérifier que la correction a fonctionné"""
    print(f"\n🔍 VÉRIFICATION POST-CORRECTION")
    print("=" * 40)
    
    dashboard_path = Path("templates/agents/dashboard.html")
    content = dashboard_path.read_text()
    
    # Compter les URLs bien formatées
    good_urls = re.findall(r'href="\{%\s*url\s+[\'"][^\'"]+[\'"]\s*%\}"', content)
    bad_urls = re.findall(r'href="\{%\s*url\s+[^\'"]*', content)
    
    print(f"✅ URLs bien formatées: {len(good_urls)}")
    print(f"❌ URLs mal formatées: {len(bad_urls)}")
    
    if bad_urls:
        print(f"🚨 Problèmes restants:")
        for bad in bad_urls[:2]:
            print(f"   {bad}...")

def fix_notifications_url():
    """Corriger l'URL agents_notifications → notifications"""
    agents_dir = Path("templates/agents")
    
    corrections_made = 0
    for template_file in agents_dir.rglob("*.html"):
        content = template_file.read_text()
        original_content = content
        
        # Remplacer l'ancien nom par le nouveau
        content = content.replace("agents:agents_notifications", "agents:notifications")
        
        if content != original_content:
            template_file.write_text(content)
            corrections_made += 1
            print(f"✅ {template_file.name}: agents_notifications → notifications")
    
    if corrections_made == 0:
        print("ℹ️  Aucune correction notifications nécessaire")

def check_configuration():
    """Vérifier la configuration finale"""
    print("\n📋 CONFIGURATION FINALE:")
    
    # Vérifier urls.py
    urls_path = Path("agents/urls.py")
    if urls_path.exists():
        content = urls_path.read_text()
        required_urls = ['creer_bon_soin', 'liste_membres', 'notifications', 'verification_cotisation']
        
        print("   URLs requises dans agents/urls.py:")
        for url_name in required_urls:
            if f"name='{url_name}'" in content or f'name="{url_name}"' in content:
                print(f"      ✅ {url_name}")
            else:
                print(f"      ❌ {url_name} - MANQUANT")
    else:
        print("❌ agents/urls.py non trouvé")
    
    # Vérifier views.py
    views_path = Path("agents/views.py")
    if views_path.exists():
        content = views_path.read_text()
        required_views = ['dashboard_agent', 'liste_membres', 'agents_notifications', 'verification_cotisation']
        
        print("\n   Vues requises dans agents/views.py:")
        for view_name in required_views:
            if f"def {view_name}" in content or f"class {view_name}" in content:
                print(f"      ✅ {view_name}")
            else:
                print(f"      ❌ {view_name} - MANQUANT")
    else:
        print("❌ agents/views.py non trouvé")

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
    
    print("\n🎉 CORRECTION TERMINÉE!")

if __name__ == "__main__":
    complete_agent_fix()