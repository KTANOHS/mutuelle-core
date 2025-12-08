#!/usr/bin/env python3
"""
Reconstruction complète des templates agents
"""

from pathlib import Path
import shutil
from datetime import datetime
from django.utils import timezone

def backup_current_templates():
    """Sauvegarder les templates actuels"""
    agents_dir = Path("templates/agents")
    backup_dir = Path(f"templates_backup_agents_{timezone.now().strftime('%Y%m%d_%H%M%S')}")
    
    if agents_dir.exists():
        shutil.copytree(agents_dir, backup_dir / "agents")
        print(f"📦 Backup créé: {backup_dir}")
    else:
        print("❌ Dossier agents non trouvé pour backup")

def create_clean_agent_structure():
    """Créer une structure propre pour les agents"""
    agents_dir = Path("templates/agents")
    
    # Supprimer et recréer le dossier
    if agents_dir.exists():
        shutil.rmtree(agents_dir)
    agents_dir.mkdir(parents=True)
    (agents_dir / "partials").mkdir()
    
    print("🧹 Structure agents nettoyée et recréée")

def create_base_agent_template():
    """Créer le template de base agent"""
    base_content = """{% extends "base.html" %}
{% load static %}

{% block title %}Espace Agent - Mutuelle{% endblock %}

{% block extra_css %}
<style>
.agent-sidebar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}
.agent-sidebar .nav-link {
    color: rgba(255,255,255,0.8);
    padding: 12px 20px;
    margin: 4px 0;
    border-radius: 8px;
    transition: all 0.3s ease;
}
.agent-sidebar .nav-link:hover {
    background: rgba(255,255,255,0.1);
    color: white;
    transform: translateX(5px);
}
</style>
{% endblock %}

{% block sidebar %}
<nav class="agent-sidebar">
    <div class="sidebar-header p-3">
        <h5 class="text-white mb-0">Espace Agent</h5>
        <small class="text-white-50">{% firstof user.get_full_name user.username %}</small>
    </div>
    
    <ul class="nav flex-column">
        <li class="nav-item">
            <a class="nav-link {% if request.resolver_match.url_name == 'dashboard' %}active{% endif %}" 
               href="{% url 'agents:dashboard' %}">
                📊 Tableau de Bord
            </a>
        </li>
        <li class="nav-item">
            <a class="nav-link {% if 'membres' in request.resolver_match.url_name %}active{% endif %}" 
               href="{% url 'agents:liste_membres' %}">
                👥 Gestion Membres
            </a>
        </li>
        <li class="nav-item">
            <a class="nav-link {% if 'creer_bon_soin' in request.resolver_match.url_name %}active{% endif %}" 
               href="{% url 'agents:creer_bon_soin' %}">
                📝 Bons de Soin
            </a>
        </li>
        <li class="nav-item">
            <a class="nav-link {% if 'verification_cotisation' in request.resolver_match.url_name %}active{% endif %}" 
               href="{% url 'agents:verification_cotisation' %}">
                ✅ Vérification Cotisations
            </a>
        </li>
        <li class="nav-item">
            <a class="nav-link {% if 'notifications' in request.resolver_match.url_name %}active{% endif %}" 
               href="{% url 'agents:notifications' %}">
                🔔 Notifications
            </a>
        </li>
    </ul>
</nav>
{% endblock %}

{% block content %}
<div class="container-fluid py-4">
    {% block agent_content %}
    {% endblock %}
</div>
{% endblock %}
"""
    
    base_path = Path("templates/agents/base_agent.html")
    base_path.write_text(base_content)
    print("✅ base_agent.html créé")

def create_simple_dashboard():
    """Créer un dashboard simple et propre"""
    dashboard_content = """{% extends "agents/base_agent.html" %}
{% load static %}

{% block title %}Tableau de Bord Agent{% endblock %}

{% block agent_content %}
<div class="container-fluid">
    <div class="alert alert-info">
        <h4>🔄 DASHBOARD RECONSTRUIT</h4>
        <p>Ce dashboard a été complètement reconstruit le {% now "Y-m-d à H:i:s" %}</p>
    </div>

    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">Tableau de Bord Agent</h1>
    </div>

    <div class="row">
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-success shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                                Statut</div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">Actif</div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-check-circle fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-12">
            <div class="card shadow mb-4">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">Navigation</h6>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <a href="{% url 'agents:creer_bon_soin' %}" class="btn btn-primary btn-block">
                                📝 Créer Bon de Soin
                            </a>
                        </div>
                        <div class="col-md-6 mb-3">
                            <a href="{% url 'agents:liste_membres' %}" class="btn btn-info btn-block">
                                👥 Liste Membres
                            </a>
                        </div>
                        <div class="col-md-6 mb-3">
                            <a href="{% url 'agents:verification_cotisation' %}" class="btn btn-warning btn-block">
                                ✅ Vérification Cotisations
                            </a>
                        </div>
                        <div class="col-md-6 mb-3">
                            <a href="{% url 'agents:notifications' %}" class="btn btn-secondary btn-block">
                                🔔 Notifications
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
    
    dashboard_path = Path("templates/agents/dashboard.html")
    dashboard_path.write_text(dashboard_content)
    print("✅ dashboard.html créé")

def create_other_templates():
    """Créer les autres templates de base"""
    templates = {
        'creer_bon_soin.html': """{% extends "agents/base_agent.html" %}
{% block title %}Créer Bon de Soin{% endblock %}
{% block agent_content %}
<div class="container-fluid">
    <h1>Créer Bon de Soin</h1>
    <p>Formulaire de création de bon de soin</p>
</div>
{% endblock %}""",

        'liste_membres.html': """{% extends "agents/base_agent.html" %}
{% block title %}Liste des Membres{% endblock %}
{% block agent_content %}
<div class="container-fluid">
    <h1>Liste des Membres</h1>
    <p>Gestion des membres assignés</p>
</div>
{% endblock %}""",

        'notifications.html': """{% extends "agents/base_agent.html" %}
{% block title %}Notifications{% endblock %}
{% block agent_content %}
<div class="container-fluid">
    <h1>Notifications</h1>
    <p>Gestion des notifications</p>
</div>
{% endblock %}""",

        'verification_cotisation.html': """{% extends "agents/base_agent.html" %}
{% block title %}Vérification Cotisations{% endblock %}
{% block agent_content %}
<div class="container-fluid">
    <h1>Vérification des Cotisations</h1>
    <p>Interface de vérification</p>
</div>
{% endblock %}"""
    }
    
    for filename, content in templates.items():
        path = Path("templates/agents") / filename
        path.write_text(content)
        print(f"✅ {filename} créé")

if __name__ == "__main__":
    print("🔨 RECONSTRUCTION COMPLÈTE DES TEMPLATES AGENTS")
    print("=" * 60)
    
    backup_current_templates()
    create_clean_agent_structure()
    create_base_agent_template()
    create_simple_dashboard()
    create_other_templates()
    
    print(f"\n🎉 RECONSTRUCTION TERMINÉE!")
    print("📋 Prochaines étapes:")
    print("   1. Videz le cache du navigateur")
    print("   2. Redémarrez le serveur Django")
    print("   3. Testez: http://127.0.0.1:8000/agents/")