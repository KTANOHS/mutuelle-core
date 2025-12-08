#!/usr/bin/env python3
"""
Inspection détaillée du contenu du dashboard
"""

from pathlib import Path

def inspect_dashboard_content():
    dashboard_path = Path("templates/agents/dashboard.html")
    
    if not dashboard_path.exists():
        print("❌ Dashboard non trouvé")
        return
    
    content = dashboard_path.read_text()
    lines = content.split('\n')
    
    print("🔍 INSPECTION DÉTAILLÉE DU DASHBOARD")
    print("=" * 50)
    
    # Trouver toutes les lignes avec des href
    href_lines = []
    for i, line in enumerate(lines, 1):
        if 'href=' in line:
            href_lines.append((i, line.strip()))
    
    print(f"📋 Lignes avec href trouvées: {len(href_lines)}")
    
    # Afficher les lignes problématiques
    problematic = []
    for line_num, line_content in href_lines:
        if '{% url' in line_content and '%}"' not in line_content:
            problematic.append((line_num, line_content))
    
    if problematic:
        print(f"\n🚨 LIGNES PROBLÉMATIQUES:")
        for line_num, line_content in problematic:
            print(f"\n📍 Ligne {line_num}:")
            print(f"   {line_content}")
            
            # Analyser ce qui ne va pas
            if '"{% url' in line_content and line_content.count('"') == 1:
                print("   ❌ PROBLÈME: Guillemet de fermeture manquant")
            elif '{% url' in line_content and '%}' not in line_content:
                print("   ❌ PROBLÈME: Balise Django non fermée")
            else:
                print("   ❌ PROBLÈME: Format inconnu")
    
    return problematic

def show_specific_examples():
    """Montrer des exemples spécifiques de correction"""
    print(f"\n🎯 EXEMPLES DE CORRECTIONS:")
    print("=" * 40)
    
    examples = {
        "MAUVAIS": '''<a href="{% url 'agents:creer_bon_soin' %}''',
        "BON": '''<a href="{% url 'agents:creer_bon_soin' %}">''',
        "MAUVAIS": '''href="{% url 'agents:liste_membres' %}''',
        "BON": '''href="{% url 'agents:liste_membres' %}"''',
    }
    
    for i, (bad, good) in enumerate(examples.items(), 1):
        if i % 2 == 1:
            print(f"❌ {bad}")
        else:
            print(f"✅ {good}")
            print()

if __name__ == "__main__":
    problematic_lines = inspect_dashboard_content()
    show_specific_examples()
    
    if problematic_lines:
        print(f"\n🚨 ACTION REQUISE:")
        print(f"   {len(problematic_lines)} lignes nécessitent une correction manuelle")