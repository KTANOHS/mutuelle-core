#!/usr/bin/env python
"""
VÉRIFICATION RAPIDE DES CORRECTIONS
"""

from pathlib import Path

def check_fixes():
    project_path = Path(__file__).parent
    
    print("🔍 VÉRIFICATION RAPIDE DES CORRECTIONS")
    print("=" * 40)
    
    # Vérifier home.html
    home_path = project_path / 'templates/home.html'
    if home_path.exists():
        with open(home_path, 'r') as f:
            content = f.read()
        
        if '{% load static' in content:
            print("✅ home.html: {% load static %} présent")
        else:
            print("❌ home.html: {% load static %} manquant")
        
        if 'href="{% static \'css/style.css\' %}"' in content:
            print("✅ home.html: Fichier static corrigé")
        elif 'href="/static/css/style.css"' in content:
            print("❌ home.html: Fichier static toujours en dur")
        else:
            print("⚠️  home.html: Fichier CSS non trouvé")
    
    # Vérifier assureur templates
    files_to_check = [
        ('templates/assureur/liste_membres.html', 'assureur:detail_membre'),
        ('templates/assureur/detail_membre.html', 'assureur:creer_bon')
    ]
    
    for file_path, url_pattern in files_to_check:
        full_path = project_path / file_path
        if full_path.exists():
            with open(full_path, 'r') as f:
                content = f.read()
            
            if f"{url_pattern}\\" in content:
                print(f"❌ {file_path}: Backslash présent dans l'URL")
            else:
                print(f"✅ {file_path}: URL corrigée")

if __name__ == '__main__':
    check_fixes()