# create_minimal_config_template.py
import os

def create_minimal_template():
    """Crée un template minimal pour résoudre l'erreur"""
    
    template_path = "assureur/templates/assureur/configuration.html"
    
    # Vérifier si le dossier existe
    os.makedirs(os.path.dirname(template_path), exist_ok=True)
    
    # Créer un template minimal
    template_content = """{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <h1>Configuration Assureur</h1>
    <div class="alert alert-info">
        <h4 class="alert-heading">En cours de développement</h4>
        <p>Cette page est en cours de développement. La fonctionnalité de configuration complète sera disponible prochainement.</p>
        <hr>
        <p class="mb-0">En attendant, vous pouvez utiliser l'interface d'administration Django pour configurer les paramètres.</p>
    </div>
    
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Actions disponibles</h5>
            <ul>
                <li><a href="/admin/" target="_blank">Accéder à l'administration Django</a></li>
                <li><a href="/assureur/communication/">Messagerie</a></li>
                <li><a href="/assureur/dashboard/">Tableau de bord</a></li>
            </ul>
        </div>
    </div>
</div>
{% endblock %}
"""
    
    # Écrire le fichier
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    print(f"✅ Template créé: {template_path}")
    print("📁 Dossier: assureur/templates/assureur/")
    print("📄 Fichier: configuration.html")

if __name__ == "__main__":
    create_minimal_template()