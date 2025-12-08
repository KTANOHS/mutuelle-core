#!/usr/bin/env python
"""
CORRECTION SPÉCIFIQUE DU LIEN DE DÉCONNEXION DANS BASE.HTML
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def fix_base_html_logout():
    """Corrige spécifiquement le lien de déconnexion dans base.html"""
    print("🔧 Correction du lien de déconnexion dans base.html...")
    
    base_path = BASE_DIR / 'templates' / 'base.html'
    
    if not base_path.exists():
        print("❌ templates/base.html non trouvé")
        print("📁 Recherche dans d'autres emplacements...")
        
        # Chercher base.html dans d'autres dossiers
        for root, dirs, files in os.walk(BASE_DIR):
            if 'base.html' in files:
                base_path = Path(root) / 'base.html'
                print(f"✅ base.html trouvé dans: {base_path}")
                break
        else:
            print("❌ base.html introuvable")
            return
    
    # Lire le contenu
    with open(base_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("📋 Recherche du lien de déconnexion...")
    
    # Pattern à rechercher (lien GET problématique)
    problematic_patterns = [
        '<a href="{% url \'logout\' %}"',
        '<a href="{% url "logout" %}"',
        "href=\"{% url 'logout' %}\""
    ]
    
    for pattern in problematic_patterns:
        if pattern in content:
            print(f"✅ Pattern trouvé: {pattern}")
            
            # Trouver la ligne complète contenant le pattern
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if pattern in line:
                    print(f"📝 Ligne {i+1}: {line.strip()}")
                    
                    # Remplacer par le formulaire POST
                    new_line = '''    <form method="post" action="{% url 'logout' %}" style="display: inline;">
        {% csrf_token %}
        <button type="submit" style="background: none; border: none; color: white; cursor: pointer; text-decoration: underline;">
            Déconnexion
        </button>
    </form>'''
                    
                    lines[i] = new_line
                    content = '\n'.join(lines)
                    
                    # Sauvegarder
                    with open(base_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print("✅ Lien de déconnexion corrigé (GET → POST)")
                    return
    
    print("ℹ️  Aucun lien de déconnexion GET trouvé")
    print("💡 Le problème peut être ailleurs...")

def check_current_logout_config():
    """Vérifie la configuration actuelle"""
    print("\n🔍 Vérification de la configuration...")
    
    base_path = BASE_DIR / 'templates' / 'base.html'
    if base_path.exists():
        with open(base_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'method="post"' in content and 'logout' in content:
            print("✅ Formulaire POST détecté pour la déconnexion")
        elif 'href' in content and 'logout' in content:
            print("❌ Lien GET détecté pour la déconnexion")
        else:
            print("ℹ️  Aucune référence à la déconnexion trouvée")
            
        # Afficher les lignes autour de "Déconnexion"
        if 'Déconnexion' in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'Déconnexion' in line:
                    print(f"📄 Ligne {i+1}: {line.strip()}")

if __name__ == "__main__":
    fix_base_html_logout()
    check_current_logout_config()
    print("\n🎉 Correction terminée ! Redémarrez le serveur.")