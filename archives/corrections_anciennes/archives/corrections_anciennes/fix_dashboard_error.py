# fix_dashboard_error.py
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def corriger_urls_py():
    """Corrige le fichier urls.py avec les bons noms"""
    urls_path = BASE_DIR / 'agents' / 'urls.py'
    
    try:
        urls_content = '''from django.urls import path
from . import views

app_name = 'agents'

urlpatterns = [
    # Pages principales
    path('verification-cotisations/', views.verification_cotisations, name='verification_cotisations'),
    path('tableau-de-bord/', views.tableau_de_bord_agent, name='tableau_de_bord'),
    
    # API endpoints
    path('api/recherche-membres/', views.recherche_membres_api, name='recherche_membres_api'),
    path('api/verifier-cotisation/<int:membre_id>/', views.verifier_cotisation_api, name='verifier_cotisation_api'),
]
'''
        with open(urls_path, 'w') as f:
            f.write(urls_content)
        
        print("✅ Fichier urls.py corrigé avec les bons noms d'URL")
        return True
        
    except Exception as e:
        print(f"❌ Erreur modification urls.py: {e}")
        return False

def corriger_base_template():
    """Corrige le template base_agent.html"""
    template_path = BASE_DIR / 'templates' / 'agents' / 'base_agent.html'
    
    try:
        template_content = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Agents - Mutuelle{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <style>
        .sidebar {
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .sidebar .nav-link {
            color: #fff;
            margin: 5px 0;
            border-radius: 5px;
        }
        .sidebar .nav-link:hover, .sidebar .nav-link.active {
            background: rgba(255, 255, 255, 0.1);
        }
        .main-content {
            background-color: #f8f9fa;
        }
    </style>
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <div class="col-md-3 col-lg-2 sidebar p-0">
                <div class="p-3">
                    <div class="text-center mb-4">
                        <h4 class="text-white mb-1">
                            {% if request.user.get_full_name %}
                                {{ request.user.get_full_name }}
                            {% else %}
                                {{ request.user.username }}
                            {% endif %}
                        </h4>
                        <small class="text-light">Agent</small>
                    </div>
                    
                    <ul class="nav flex-column">
                        <!-- ✅ CORRIGÉ : Utilisation du bon nom d'URL -->
                        <li class="nav-item">
                            <a class="nav-link {% if request.resolver_match.url_name == 'tableau_de_bord' %}active{% endif %}" 
                               href="{% url 'agents:tableau_de_bord' %}">
                                <i class="fas fa-tachometer-alt me-2"></i>Tableau de bord
                            </a>
                        </li>
                        
                        <li class="nav-item">
                            <a class="nav-link {% if request.resolver_match.url_name == 'verification_cotisations' %}active{% endif %}" 
                               href="{% url 'agents:verification_cotisations' %}">
                                <i class="fas fa-check-circle me-2"></i>Vérification cotisations
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
            
            <!-- Main content -->
            <div class="col-md-9 col-lg-10 main-content">
                <!-- Header -->
                <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom">
                    <div class="container-fluid">
                        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" 
                                data-bs-target="#navbarSupportedContent">
                            <span class="navbar-toggler-icon"></span>
                        </button>
                        
                        <div class="collapse navbar-collapse" id="navbarSupportedContent">
                            <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                                <li class="nav-item dropdown">
                                    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" 
                                       role="button" data-bs-toggle="dropdown">
                                        <i class="fas fa-user-circle me-1"></i>
                                        {{ request.user.username }}
                                    </a>
                                    <ul class="dropdown-menu dropdown-menu-end">
                                        <li><a class="dropdown-item" href="#">
                                            <i class="fas fa-cog me-2"></i>Paramètres
                                        </a></li>
                                        <li><hr class="dropdown-divider"></li>
                                        <li>
                                            <a class="dropdown-item text-danger" href="{% url 'logout' %}">
                                                <i class="fas fa-sign-out-alt me-2"></i>Déconnexion
                                            </a>
                                        </li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                    </div>
                </nav>
                
                <!-- Page content -->
                <main class="p-4">
                    <!-- Page title -->
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h2 class="h4 mb-0">
                            <i class="fas fa-{% block page_icon %}home{% endblock %} me-2"></i>
                            {% block page_title %}Tableau de bord{% endblock %}
                        </h2>
                    </div>
                    
                    <!-- Messages -->
                    {% if messages %}
                    <div class="messages mb-4">
                        {% for message in messages %}
                        <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                        {% endfor %}
                    </div>
                    {% endif %}
                    
                    <!-- Main content block -->
                    {% block content %}
                    <div class="row">
                        <div class="col-12">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">Bienvenue, agent !</h5>
                                    <p class="card-text">Utilisez le menu de gauche pour naviguer.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endblock %}
                </main>
            </div>
        </div>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>'''
        
        with open(template_path, 'w') as f:
            f.write(template_content)
        
        print("✅ Template base_agent.html corrigé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur modification template: {e}")
        return False

def corriger_views_py():
    """S'assure que les vues existent"""
    views_path = BASE_DIR / 'agents' / 'views.py'
    
    try:
        # Vérifier si la vue existe déjà
        with open(views_path, 'r') as f:
            content = f.read()
        
        if 'tableau_de_bord_agent' not in content:
            # Ajouter la vue manquante
            views_content = '''
@login_required
def tableau_de_bord_agent(request):
    """Tableau de bord de l'agent"""
    # Statistiques simples pour le moment
    stats = {
        'verifications_jour': 15,
        'membres_a_jour': 120,
        'membres_retard': 8,
    }
    
    context = {
        'stats': stats,
    }
    return render(request, 'agents/dashboard.html', context)
'''
            with open(views_path, 'a') as f:
                f.write(views_content)
            print("✅ Vue tableau_de_bord_agent ajoutée")
        else:
            print("✅ Vue tableau_de_bord_agent existe déjà")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur vérification views.py: {e}")
        return False

def creer_template_dashboard():
    """Crée le template dashboard.html"""
    template_path = BASE_DIR / 'templates' / 'agents' / 'dashboard.html'
    
    try:
        dashboard_content = '''{% extends 'agents/base_agent.html' %}
{% load static %}

{% block title %}Tableau de bord - Agent{% endblock %}
{% block page_icon %}tachometer-alt{% endblock %}
{% block page_title %}Tableau de bord{% endblock %}

{% block content %}
<div class="row">
    <!-- Statistiques -->
    <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-primary shadow h-100 py-2">
            <div class="card-body">
                <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                        <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                            Vérifications aujourd'hui
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.verifications_jour }}</div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-check-circle fa-2x text-gray-300"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-success shadow h-100 py-2">
            <div class="card-body">
                <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                        <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                            Membres à jour
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.membres_a_jour }}</div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-user-check fa-2x text-gray-300"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-warning shadow h-100 py-2">
            <div class="card-body">
                <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                        <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                            En retard
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.membres_retard }}</div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-exclamation-triangle fa-2x text-gray-300"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-info shadow h-100 py-2">
            <div class="card-body">
                <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                        <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                            Taux conformité
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">94%</div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-percent fa-2x text-gray-300"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-lg-8">
        <div class="card shadow mb-4">
            <div class="card-header py-3">
                <h6 class="m-0 font-weight-bold text-primary">Actions rapides</h6>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <a href="{% url 'agents:verification_cotisations' %}" class="btn btn-primary btn-block">
                            <i class="fas fa-check-circle me-2"></i>Vérifier cotisations
                        </a>
                    </div>
                    <div class="col-md-6 mb-3">
                        <button class="btn btn-outline-primary btn-block" disabled>
                            <i class="fas fa-search me-2"></i>Rechercher membre
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-lg-4">
        <div class="card shadow mb-4">
            <div class="card-header py-3">
                <h6 class="m-0 font-weight-bold text-primary">Guide rapide</h6>
            </div>
            <div class="card-body">
                <p class="small">
                    <strong>Fonctionnalités disponibles:</strong>
                </p>
                <ul class="small">
                    <li>Vérification des cotisations</li>
                    <li>Recherche de membres</li>
                    <li>Consultation des statuts</li>
                </ul>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''
        
        with open(template_path, 'w') as f:
            f.write(dashboard_content)
        
        print("✅ Template dashboard.html créé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur création dashboard: {e}")
        return False

def appliquer_corrections():
    """Applique toutes les corrections"""
    print("🔧 CORRECTION DE L'ERREUR NoReverseMatch")
    print("=" * 50)
    
    corrections = [
        ("Correction urls.py", corriger_urls_py),
        ("Correction base template", corriger_base_template),
        ("Vérification views.py", corriger_views_py),
        ("Création template dashboard", creer_template_dashboard),
    ]
    
    for nom, fonction in corrections:
        print(f"\n📝 {nom}...")
        if fonction():
            print("   ✅ SUCCÈS")
        else:
            print("   ❌ ÉCHEC")
    
    print("\n🎯 CORRECTIONS APPLIQUÉES!")
    print("\n📋 PROCHAINES ÉTAPES:")
    print("1. Redémarrez le serveur: python manage.py runserver")
    print("2. Accédez à: http://localhost:8000/agents/verification-cotisations/")
    print("3. Testez la navigation entre les pages")

if __name__ == "__main__":
    appliquer_corrections()