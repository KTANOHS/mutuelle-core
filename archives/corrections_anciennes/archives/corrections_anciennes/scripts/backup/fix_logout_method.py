#!/usr/bin/env python
"""
CORRECTION DE LA MÉTHODE DE DÉCONNEXION
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def fix_base_template():
    """Corrige le template base.html pour utiliser POST"""
    print("🔧 Correction du template base.html...")
    
    base_path = BASE_DIR / 'templates' / 'base.html'
    
    if base_path.exists():
        content = base_path.read_text()
        
        # Remplacer le lien GET par un formulaire POST
        old_logout = '<a href="{% url \\'logout\\' %}" style="color: white;">Déconnexion</a>'
        new_logout = '''<form method="post" action="{% url 'logout' %}" style="display: inline;">
    {% csrf_token %}
    <button type="submit" style="background: none; border: none; color: white; cursor: pointer; text-decoration: underline;">
        Déconnexion
    </button>
</form>'''
        
        if old_logout in content:
            content = content.replace(old_logout, new_logout)
            base_path.write_text(content)
            print("✅ Template base.html corrigé (POST method)")
        else:
            print("ℹ️  Lien de déconnexion déjà corrigé ou format différent")
    else:
        print("❌ base.html non trouvé")

def create_alternative_logout():
    """Crée une page de déconnexion qui redirige vers POST"""
    print("📁 Création d'une page de déconnexion intermédiaire...")
    
    content = """<!DOCTYPE html>
<html>
<head>
    <title>Déconnexion</title>
    <script>
        function logout() {
            // Créer un formulaire invisible et le soumettre
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '{% url "logout" %}';
            
            const csrf = document.createElement('input');
            csrf.name = 'csrfmiddlewaretoken';
            csrf.value = '{{ csrf_token }}';
            form.appendChild(csrf);
            
            document.body.appendChild(form);
            form.submit();
        }
        
        // Déconnexion automatique au chargement
        window.onload = logout;
    </script>
</head>
<body>
    <p>Déconnexion en cours...</p>
</body>
</html>"""
    
    alt_path = BASE_DIR / 'templates' / 'registration' / 'logout_redirect.html'
    alt_path.write_text(content)
    print("✅ Page de redirection créée")

if __name__ == "__main__":
    fix_base_template()
    create_alternative_logout()
    print("🎉 Corrections appliquées ! Redémarrez le serveur.")