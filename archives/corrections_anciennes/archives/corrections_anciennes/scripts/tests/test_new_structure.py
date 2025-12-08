#!/usr/bin/env python3
"""
Script de test de la nouvelle structure de templates
"""

import os
from django.conf import settings
from django.template import Template, Context
from django.template.loader import get_template

def test_template_inheritance():
    """Teste l'héritage des templates"""
    print("🧪 TEST DE LA STRUCTURE DES TEMPLATES")
    print("=" * 50)
    
    test_cases = [
        {
            'name': 'Page d\'accueil',
            'template': 'home.html',
            'expected_base': 'base_home.html'
        },
        {
            'name': 'Application assureur', 
            'template': 'apps/assureur/base_assureur.html',
            'expected_base': 'base.html'
        }
    ]
    
    for test in test_cases:
        template_path = os.path.join('templates', test['template'])
        
        if os.path.exists(template_path):
            print(f"✅ {test['name']}: {test['template']} existe")
            
            # Vérifier le contenu basique
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if '{% extends' in content:
                print(f"   ✅ Contient une extension")
            else:
                print(f"   ⚠️  Ne contient pas d'extension")
                
        else:
            print(f"❌ {test['name']}: {test['template']} manquant")

def generate_usage_examples():
    """Génère des exemples d'utilisation"""
    print("\n📚 EXEMPLES D'UTILISATION")
    print("=" * 50)
    
    examples = {
        'Nouvelle page d\'accueil': """{% extends "base_home.html" %}

{% block title %}Accueil - Mon Application{% endblock %}

{% block content %}
<div class="container">
    <h1>Bienvenue</h1>
    <p>Contenu de la page d'accueil...</p>
</div>
{% endblock %}""",
        
        'Nouvelle application': """{% extends "base_app.html" %}

{% block title %}Assureur - Tableau de bord{% endblock %}

{% block content %}
<div class="app-container">
    <h1>Tableau de bord Assureur</h1>
    <!-- Contenu spécifique à l'application -->
</div>
{% endblock %}

{% block extra_js %}
<script>
// JavaScript spécifique à l'application
</script>
{% endblock %}"""
    }
    
    for title, code in examples.items():
        print(f"\n{title}:")
        print("-" * 30)
        print(code)

if __name__ == "__main__":
    test_template_inheritance()
    generate_usage_examples()