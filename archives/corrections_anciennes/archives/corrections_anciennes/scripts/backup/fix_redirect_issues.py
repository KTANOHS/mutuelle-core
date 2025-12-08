#!/usr/bin/env python
"""
SCRIPT DE CORRECTION AUTOMATIQUE DES PROBLÈMES IDENTIFIÉS
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def fix_settings():
    """Corrige les paramètres problématiques dans settings.py"""
    print("🔧 Correction des paramètres settings.py...")
    
    settings_path = BASE_DIR / 'mutuelle_core' / 'settings.py'
    
    with open(settings_path, 'r') as f:
        content = f.read()
    
    # Remplacer les paramètres problématiques
    content = content.replace(
        "LOGOUT_REDIRECT_URL = '/accounts/login/'", 
        "LOGOUT_REDIRECT_URL = 'home'"
    )
    
    content = content.replace(
        "LOGIN_REDIRECT_URL = '/dashboard/'", 
        "LOGIN_REDIRECT_URL = 'dashboard'"
    )
    
    # Ajouter la configuration développement
    dev_config = """
# Configuration développement
if DEBUG:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax'"""
    
    if 'if DEBUG:' not in content:
        # Trouver où ajouter la configuration
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'LOGOUT_REDIRECT_URL' in line:
                lines.insert(i + 1, dev_config)
                break
        content = '\n'.join(lines)
    
    with open(settings_path, 'w') as f:
        f.write(content)
    
    print("✅ Paramètres settings.py corrigés")

def create_missing_templates():
    """Crée les templates manquants"""
    print("📁 Création des templates manquants...")
    
    templates_dir = BASE_DIR / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    # Template logout.html
    logout_template = templates_dir / 'registration' / 'logout.html'
    logout_template.parent.mkdir(parents=True, exist_ok=True)
    
    logout_template.write_text("""{% extends 'base.html' %}

{% block title %}Déconnexion - Mutuelle{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h4 class="mb-0">Déconnexion réussie</h4>
                </div>
                <div class="card-body text-center">
                    <p>Vous avez été déconnecté avec succès.</p>
                    <a href="{% url 'home' %}" class="btn btn-primary">Retour à l'accueil</a>
                    <a href="{% url 'login' %}" class="btn btn-secondary">Se reconnecter</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}""")
    
    # Template dashboard.html
    dashboard_template = templates_dir / 'dashboard.html'
    dashboard_template.write_text("""{% extends 'base.html' %}

{% block title %}Tableau de Bord - Mutuelle{% endblock %}

{% block content %}
<div class="container mt-4">
    <h2>Tableau de Bord</h2>
    <div class="row">
        <div class="col-md-12">
            <div class="alert alert-success">
                Bienvenue, {{ user.username }} ! Vous êtes connecté.
            </div>
            <div class="card">
                <div class="card-body">
                    <a href="{% url 'logout' %}" class="btn btn-danger">Déconnexion</a>
                    <a href="{% url 'home' %}" class="btn btn-secondary">Accueil</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}""")
    
    print("✅ Templates manquants créés")

if __name__ == "__main__":
    print("🔄 Début de la correction automatique...")
    fix_settings()
    create_missing_templates()
    print("🎉 Correction terminée ! Redémarrez le serveur.")