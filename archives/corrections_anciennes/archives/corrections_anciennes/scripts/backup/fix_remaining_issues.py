# fix_remaining_issues.py
import os

def fix_remaining_templates():
    """Corrige les derniers templates vides"""
    empty_templates = {
        'core/home.html': """{% extends "core/base_core.html" %}
{% load static %}

{% block title %}Accueil - Mutuelle{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Bienvenue sur la Mutuelle Santé</h1>
    <p>Page d'accueil principale</p>
</div>
{% endblock %}
""",
        
        'core/default_dashboard.html': """{% extends "core/base_core.html" %}
{% load static %}

{% block title %}Tableau de Bord - Mutuelle{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Tableau de Bord Principal</h1>
    <p>Tableau de bord par défaut</p>
</div>
{% endblock %}
"""
    }
    
    print("🔧 CORRECTION DES DERNIERS TEMPLATES VIDES")
    print("=" * 45)
    
    fixed_count = 0
    for template_path, content in empty_templates.items():
        full_path = f'templates/{template_path}'
        if os.path.exists(full_path) and os.path.getsize(full_path) == 0:
            with open(full_path, 'w') as f:
                f.write(content)
            print(f"✅ Template vide complété: {template_path}")
            fixed_count += 1
        else:
            print(f"ℹ️  Template non vide ou non trouvé: {template_path}")
    
    print(f"📊 {fixed_count} templates corrigés")

if __name__ == "__main__":
    fix_remaining_templates()