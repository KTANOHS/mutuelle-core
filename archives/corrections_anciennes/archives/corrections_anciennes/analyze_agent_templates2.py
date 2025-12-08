#!/usr/bin/env python3
"""
Analyse complète de tous les templates agents
"""

from pathlib import Path
import hashlib

def analyze_all_agent_templates():
    agents_dir = Path("templates/agents")
    
    print("🔍 ANALYSE COMPLÈTE DES TEMPLATES AGENTS")
    print("=" * 60)
    
    if not agents_dir.exists():
        print("❌ Dossier agents non trouvé")
        return
    
    # Lister tous les fichiers templates
    template_files = list(agents_dir.rglob("*.html"))
    print(f"📁 {len(template_files)} templates trouvés dans agents/")
    
    for template_file in sorted(template_files):
        print(f"\n📄 {template_file.relative_to(agents_dir.parent)}")
        print("-" * 50)
        
        try:
            content = template_file.read_text(encoding='utf-8')
            size = len(content)
            lines = content.count('\n') + 1
            
            # Calculer un hash pour détecter les doublons
            content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
            
            print(f"   📏 Taille: {size} bytes, Lignes: {lines}")
            print(f"   🔑 Hash: {content_hash}")
            
            # Analyser le contenu
            if size < 100:
                print("   ⚠️  TRÈS COURT - potentiellement vide")
            elif 'dashboard' in template_file.name.lower():
                print("   🎯 TEMPLATE DASHBOARD")
            
            # Vérifier la structure de base
            if '{% extends' in content:
                extends = [line for line in content.split('\n') if '{% extends' in line][0].strip()
                print(f"   🔗 {extends}")
            
            if '{% block' in content:
                blocks = [line.split('block ')[1].split(' %')[0] for line in content.split('\n') if '{% block' in line and 'endblock' not in line]
                print(f"   🧱 Blocks: {', '.join(blocks[:3])}{'...' if len(blocks) > 3 else ''}")
            
            # Afficher les premières lignes
            first_lines = content.split('\n')[:3]
            print("   📝 Début:")
            for line in first_lines:
                if line.strip():
                    print(f"      {line[:80]}{'...' if len(line) > 80 else ''}")
            
        except Exception as e:
            print(f"   ❌ Erreur lecture: {e}")

def check_for_duplicate_dashboards():
    """Vérifier s'il y a plusieurs dashboards"""
    print(f"\n🔍 RECHERCHE DE DOUBLONS DASHBOARD")
    print("=" * 50)
    
    dashboard_files = list(Path("templates").rglob("*dashboard*.html"))
    agent_dashboards = [f for f in dashboard_files if 'agent' in str(f).lower()]
    
    print(f"📊 Dashboards trouvés: {len(dashboard_files)}")
    print(f"📊 Dashboards agent: {len(agent_dashboards)}")
    
    for dashboard in agent_dashboards:
        print(f"   📁 {dashboard.relative_to(Path('templates'))}")
        
        try:
            content = dashboard.read_text(encoding='utf-8')
            size = len(content)
            print(f"      📏 {size} bytes")
            
            # Vérifier s'il est utilisé
            if 'agents/' in str(dashboard):
                print(f"      ✅ Emplacement correct")
            else:
                print(f"      ⚠️  Emplacement suspect")
                
        except Exception as e:
            print(f"      ❌ {e}")

def verify_template_links():
    """Vérifier les liens entre templates"""
    print(f"\n🔗 VÉRIFICATION DES LIENS ENTRE TEMPLATES")
    print("=" * 50)
    
    agents_dir = Path("templates/agents")
    
    for template_file in agents_dir.rglob("*.html"):
        content = template_file.read_text(encoding='utf-8')
        
        # Vérifier les extends
        if '{% extends' in content:
            extends_line = [line for line in content.split('\n') if '{% extends' in line][0]
            extends_template = extends_line.split("'")[1] if "'" in extends_line else extends_line.split('"')[1]
            extends_path = Path("templates") / extends_template
            
            if extends_path.exists():
                print(f"✅ {template_file.name} → {extends_template}")
            else:
                print(f"❌ {template_file.name} → {extends_template} (MANQUANT)")
        
        # Vérifier les includes
        includes = [line for line in content.split('\n') if '{% include' in line]
        for include_line in includes:
            include_template = include_line.split("'")[1] if "'" in include_line else include_line.split('"')[1]
            include_path = Path("templates") / include_template
            
            if include_path.exists():
                print(f"   ✅ Include: {include_template}")
            else:
                print(f"   ❌ Include: {include_template} (MANQUANT)")

def check_current_dashboard_state():
    """Vérifier l'état actuel du dashboard"""
    print(f"\n🎯 ÉTAT ACTUEL DU DASHBOARD")
    print("=" * 50)
    
    dashboard_path = Path("templates/agents/dashboard.html")
    
    if dashboard_path.exists():
        content = dashboard_path.read_text(encoding='utf-8')
        print(f"✅ Dashboard existe: {dashboard_path}")
        print(f"📏 Taille: {len(content)} bytes")
        
        # Vérifier s'il s'agit de la version vérifiée
        if 'href="{% url \'agents:creer_bon_soin\' %}"' in content:
            print("🎯 C'est la VERSION VÉRIFIÉE")
        else:
            print("⚠️  Ce n'est PAS la version vérifiée")
            
        # Vérifier le contenu récent
        lines = content.split('\n')
        print("📝 5 premières lignes:")
        for i, line in enumerate(lines[:5]):
            if line.strip():
                print(f"   {i+1}: {line[:100]}{'...' if len(line) > 100 else ''}")
                
    else:
        print("❌ Dashboard n'existe pas")

if __name__ == "__main__":
    analyze_all_agent_templates()
    check_for_duplicate_dashboards()
    verify_template_links()
    check_current_dashboard_state()