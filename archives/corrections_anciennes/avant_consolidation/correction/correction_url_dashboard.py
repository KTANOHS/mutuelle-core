#!/usr/bin/env python3
"""
Correction de l'URL dans le template dashboard.html
"""

from pathlib import Path

def fix_dashboard_url():
    template_file = Path('templates/agents/dashboard.html')
    
    print("🔧 Correction de l'URL dans dashboard.html...")
    
    if template_file.exists():
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Corriger l'URL (ajouter le 's' manquant)
        if "{% url 'agents:verification_cotisation' %}" in content:
            content = content.replace(
                "{% url 'agents:verification_cotisation' %}", 
                "{% url 'agents:verification_cotisations' %}"
            )
            
            with open(template_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ URL corrigée: verification_cotisation → verification_cotisations")
        else:
            print("✅ URL déjà correcte")
            
    else:
        print("❌ Fichier templates/agents/dashboard.html introuvable")

if __name__ == "__main__":
    fix_dashboard_url()