#!/usr/bin/env python3
"""
CORRECTION RAPIDE DE LA SIDEBAR AGENT
"""

import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

BASE_DIR = Path(__file__).parent

def fix_sidebar_quick():
    """Correction rapide de la sidebar"""
    
    sidebar_path = BASE_DIR / 'templates' / 'includes' / 'sidebar.html'
    
    if not sidebar_path.exists():
        print("❌ sidebar.html non trouvé")
        return
    
    with open(sidebar_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si déjà présent
    if 'communication:messagerie_agent' in content:
        print("✅ Lien déjà présent dans sidebar")
        return
    
    # Lien à ajouter
    messaging_link = """
            <!-- Lien Messagerie Agent -->
            <li class="nav-item">
                <a class="nav-link" href="{% url 'communication:messagerie_agent' %}">
                    <i class="fas fa-envelope me-2"></i>
                    <span>Messagerie</span>
                    <span class="badge bg-warning rounded-pill ms-2">0</span>
                </a>
            </li>
"""
    
    # Ajouter après le premier élément de menu
    if '<li class="nav-item">' in content:
        first_nav = content.find('<li class="nav-item">')
        if first_nav != -1:
            # Trouver la fin du premier élément
            first_end = content.find('</li>', first_nav) + 5
            new_content = content[:first_end] + messaging_link + content[first_end:]
            
            with open(sidebar_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Lien messagerie ajouté à la sidebar")
            return
    
    # Si structure différente, ajouter avant fermeture
    if '</ul>' in content:
        new_content = content.replace('</ul>', messaging_link + '\n            </ul>')
        with open(sidebar_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ Lien messagerie ajouté (fin de liste)")

if __name__ == "__main__":
    fix_sidebar_quick()