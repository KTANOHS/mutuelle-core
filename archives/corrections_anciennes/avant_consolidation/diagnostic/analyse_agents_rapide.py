#!/usr/bin/env python3
"""
Analyse rapide de l'application Agents
"""

import os
import sys
from pathlib import Path

def quick_agents_analysis():
    project_path = Path(__file__).resolve().parent
    agents_path = project_path / 'agents'
    
    print("🔍 ANALYSE RAPIDE - APPLICATION AGENTS")
    print("=" * 50)
    
    # Structure de base
    print("\n📁 STRUCTURE:")
    files = ['models.py', 'views.py', 'urls.py', 'admin.py', 'apps.py']
    for file in files:
        if (agents_path / file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
    
    # Templates
    print("\n🎨 TEMPLATES:")
    templates_path = project_path / 'templates' / 'agents'
    if templates_path.exists():
        templates = list(templates_path.glob('*.html'))
        print(f"  ✅ {len(templates)} templates trouvés")
        
        critical_templates = ['base_agent.html', 'dashboard.html']
        for template in critical_templates:
            if (templates_path / template).exists():
                print(f"    ✅ {template}")
            else:
                print(f"    ❌ {template}")
    else:
        print("  ❌ Dossier templates/agents introuvable")
    
    # URLs
    print("\n🔗 URLs:")
    main_urls = project_path / 'mutuelle_core' / 'urls.py'
    if main_urls.exists():
        with open(main_urls, 'r') as f:
            content = f.read()
        if 'agents.urls' in content:
            print("  ✅ Inclus dans URLs principales")
        else:
            print("  ❌ NON inclus dans URLs principales")
    
    # Settings
    print("\n⚙️  CONFIGURATION:")
    try:
        from django.conf import settings
        if 'agents' in settings.INSTALLED_APPS:
            print("  ✅ Dans INSTALLED_APPS")
        else:
            print("  ❌ Absent de INSTALLED_APPS")
    except:
        print("  ⚠️  Impossible de vérifier les settings")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    quick_agents_analysis()