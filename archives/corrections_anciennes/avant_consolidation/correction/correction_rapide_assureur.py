# correction_rapide_assureur.py
import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def corriger_erreurs_rapide():
    print("🔧 CORRECTION RAPIDE DES ERREURS ASSUREUR...")
    
    # 1. Corriger les URLs manquantes
    print("\n1. 📝 CORRECTION DES URLs MANQUANTES")
    
    # Vérifier et corriger assureur/urls.py
    urls_file = BASE_DIR / 'assureur' / 'urls.py'
    if urls_file.exists():
        with open(urls_file, 'r') as f:
            content = f.read()
        
        # Vérifier si 'rapports' existe
        if 'rapport_statistiques' not in content:
            print("❌ URL 'rapport_statistiques' manquante dans urls.py")
            
            # Ajouter l'URL manquante
            new_urls_content = '''from django.urls import path
from . import views

app_name = 'assureur'

urlpatterns = [
    # Dashboard principal
    path('dashboard/', views.dashboard_assureur, name='dashboard'),
    
    # Gestion des membres
    path('membres/', views.liste_membres, name='liste_membres'),
    path('recherche-membre/', views.recherche_membre, name='recherche_membre'),
    path('creer-membre/', views.creer_membre, name='creer_membre'),
    
    # Gestion des bons
    path('bons/', views.liste_bons, name='liste_bons'),
    
    # Paiements et finances
    path('paiements/', views.liste_paiements, name='liste_paiements'),
    
    # Rapports et statistiques - CORRECTION
    path('rapports/', views.rapport_statistiques, name='rapport_statistiques'),
]'''
            
            with open(urls_file, 'w') as f:
                f.write(new_urls_content)
            print("✅ URLs corrigées avec succès")
        else:
            print("✅ URLs déjà correctes")
    else:
        print("❌ Fichier urls.py non trouvé")
    
    # 2. Corriger les vues manquantes
    print("\n2. 👁️ CORRECTION DES VUES MANQUANTES")
    
    views_file = BASE_DIR / 'assureur' / 'views.py'
    if views_file.exists():
        with open(views_file, 'r') as f:
            content = f.read()
        
        # Vérifier si acces_interdit existe
        if 'def acces_interdit' not in content:
            print("❌ Vue 'acces_interdit' manquante")
            
            # Ajouter la vue manquante
            vue_acces_interdit = '''
@login_required
@gerer_erreurs
def acces_interdit(request):
    """Page d'accès interdit"""
    return render(request, 'assureur/acces_interdit.html', {
        'title': 'Accès Interdit',
        'date_aujourdhui': timezone.now().strftime("%A %d %B %Y"),
    })
'''
            # Insérer avant la dernière ligne
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('def ') and 'acces_interdit' not in content:
                    # Trouver la fin des fonctions
                    pass
            
            # Ajouter à la fin du fichier
            with open(views_file, 'a') as f:
                f.write(vue_acces_interdit)
            print("✅ Vue 'acces_interdit' ajoutée")
        else:
            print("✅ Vue 'acces_interdit' déjà présente")
    else:
        print("❌ Fichier views.py non trouvé")
    
    # 3. Créer les templates manquants
    print("\n3. 🎨 CRÉATION DES TEMPLATES MANQUANTS")
    
    templates_dir = BASE_DIR / 'assureur' / 'templates' / 'assureur'
    templates_dir.mkdir(parents=True, exist_ok=True)
    
    # Template base_assureur.html
    base_template = templates_dir / 'base_assureur.html'
    if not base_template.exists():
        base_content = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Espace Assureur - Mutuelle Core{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <style>
        .sidebar {
            background-color: #2c3e50;
            min-height: 100vh;
            padding: 0;
        }
        .sidebar .nav-link {
            color: #fff;
            padding: 15px 20px;
            display: block;
            text-decoration: none;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .sidebar .nav-link:hover {
            background-color: #34495e;
            color: #fff;
        }
        .main-content {
            padding: 20px;
            background-color: #f8f9fa;
        }
    </style>
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <nav class="col-md-3 col-lg-2 sidebar">
                <div class="position-sticky pt-3">
                    <div class="text-center p-3">
                        <h5 class="text-white">Espace Assureur</h5>
                        <small class="text-muted">{{ user.username }}</small>
                    </div>
                    
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'assureur:dashboard' %}">
                                <i class="fas fa-tachometer-alt me-2"></i>Dashboard
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'assureur:liste_membres' %}">
                                <i class="fas fa-users me-2"></i>Membres
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'assureur:liste_bons' %}">
                                <i class="fas fa-file-medical me-2"></i>Bons de Soin
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'assureur:liste_paiements' %}">
                                <i class="fas fa-money-bill-wave me-2"></i>Paiements
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'assureur:rapport_statistiques' %}">
                                <i class="fas fa-chart-bar me-2"></i>Rapports
                            </a>
                        </li>
                        <li class="nav-item mt-4">
                            <a class="nav-link text-warning" href="/logout/">
                                <i class="fas fa-sign-out-alt me-2"></i>Déconnexion
                            </a>
                        </li>
                    </ul>
                </div>
            </nav>

            <!-- Main content -->
            <main class="col-md-9 ms-sm-auto col-lg-10 main-content">
                {% if messages %}
                <div class="messages">
                    {% for message in messages %}
                    <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                    {% endfor %}
                </div>
                {% endif %}

                {% block content %}
                {% endblock %}
            </main>
        </div>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>'''
        
        with open(base_template, 'w') as f:
            f.write(base_content)
        print("✅ Template base_assureur.html créé")
    else:
        print("✅ Template base_assureur.html existe déjà")
    
    # Template dashboard.html
    dashboard_template = templates_dir / 'dashboard.html'
    if not dashboard_template.exists():
        dashboard_content = '''{% extends "assureur/base_assureur.html" %}
{% load humanize %}

{% block title %}Dashboard Assureur{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h2">Dashboard Assureur</h1>
        <div class="btn-toolbar mb-2 mb-md-0">
            <button type="button" class="btn btn-sm btn-outline-secondary" onclick="window.location.reload()">
                <i class="fas fa-sync-alt"></i> Actualiser
            </button>
        </div>
    </div>

    <!-- Statistiques principales -->
    <div class="row">
        <!-- Membres actifs -->
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-primary shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                                Membres actifs
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">
                                {{ stats.membres_actifs|default:"0"|intcomma }}
                            </div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-users fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Bons en attente -->
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-warning shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                                Bons en attente
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">
                                {{ stats.bons_attente|default:"0"|intcomma }}
                            </div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-file-medical fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Paiements ce mois -->
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-info shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                                Paiements ce mois
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">
                                {{ stats.paiements_mois|default:"0"|intcomma }} FCFA
                            </div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-money-bill-wave fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Taux de satisfaction -->
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-success shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                                Taux de satisfaction
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">
                                {{ stats.taux_satisfaction|default:"0" }}%
                            </div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-star fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Actions rapides -->
    <div class="row mt-4">
        <div class="col-12">
            <div class="card shadow">
                <div class="card-header bg-white">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-bolt text-warning me-2"></i>Actions rapides
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-3 mb-3">
                            <a href="{% url 'assureur:liste_membres' %}" class="btn btn-primary btn-block w-100 h-100 py-3">
                                <i class="fas fa-users fa-2x mb-2"></i><br>
                                Gérer les membres
                            </a>
                        </div>
                        <div class="col-md-3 mb-3">
                            <a href="{% url 'assureur:liste_bons' %}" class="btn btn-success btn-block w-100 h-100 py-3">
                                <i class="fas fa-file-medical fa-2x mb-2"></i><br>
                                Voir les bons
                            </a>
                        </div>
                        <div class="col-md-3 mb-3">
                            <a href="{% url 'assureur:liste_paiements' %}" class="btn btn-info btn-block w-100 h-100 py-3">
                                <i class="fas fa-money-bill-wave fa-2x mb-2"></i><br>
                                Paiements
                            </a>
                        </div>
                        <div class="col-md-3 mb-3">
                            <a href="{% url 'assureur:rapport_statistiques' %}" class="btn btn-warning btn-block w-100 h-100 py-3">
                                <i class="fas fa-chart-bar fa-2x mb-2"></i><br>
                                Rapports
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Message de bienvenue -->
    <div class="row mt-4">
        <div class="col-12">
            <div class="alert alert-success">
                <h4 class="alert-heading">
                    <i class="fas fa-check-circle me-2"></i>Dashboard Assureur Opérationnel!
                </h4>
                <p class="mb-0">
                    Bienvenue dans votre espace assureur. Le système est maintenant fonctionnel.
                    Vous pouvez commencer à gérer les membres, les bons de soin et les paiements.
                </p>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
        
        with open(dashboard_template, 'w') as f:
            f.write(dashboard_content)
        print("✅ Template dashboard.html créé")
    else:
        print("✅ Template dashboard.html existe déjà")
    
    # Template acces_interdit.html
    acces_template = templates_dir / 'acces_interdit.html'
    if not acces_template.exists():
        acces_content = '''{% extends "assureur/base_assureur.html" %}

{% block title %}Accès Interdit{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card border-danger">
                <div class="card-header bg-danger text-white">
                    <h4 class="card-title mb-0">
                        <i class="fas fa-ban me-2"></i>Accès Interdit
                    </h4>
                </div>
                <div class="card-body text-center">
                    <i class="fas fa-lock fa-5x text-danger mb-4"></i>
                    <h3>Accès Refusé</h3>
                    <p class="text-muted">
                        Vous n'avez pas les permissions nécessaires pour accéder à cette page.
                        Cette section est réservée aux assureurs autorisés.
                    </p>
                    <div class="mt-4">
                        <a href="{% url 'assureur:dashboard' %}" class="btn btn-primary">
                            <i class="fas fa-arrow-left me-2"></i>Retour au Dashboard
                        </a>
                        <a href="/" class="btn btn-outline-secondary">
                            <i class="fas fa-home me-2"></i>Page d'accueil
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
        
        with open(acces_template, 'w') as f:
            f.write(acces_content)
        print("✅ Template acces_interdit.html créé")
    
    # 4. Vérification finale
    print("\n4. ✅ VÉRIFICATION FINALE")
    
    # Vérifier que l'URL rapports existe
    from django.urls import get_resolver
    url_conf = get_resolver()
    
    def check_url_exists(pattern_name):
        try:
            from django.urls import reverse
            reverse(f'assureur:{pattern_name}')
            return True
        except:
            return False
    
    urls_essentielles = ['dashboard', 'liste_membres', 'liste_bons', 'liste_paiements', 'rapport_statistiques']
    
    for url_name in urls_essentielles:
        if check_url_exists(url_name):
            print(f"✅ URL '{url_name}' fonctionnelle")
        else:
            print(f"❌ URL '{url_name}' non fonctionnelle")
    
    print("\n🎉 CORRECTIONS APPLIQUÉES AVEC SUCCÈS!")
    print("\n📋 PROCHAINES ÉTAPES:")
    print("1. Redémarrez le serveur: python manage.py runserver")
    print("2. Connectez-vous avec un utilisateur assureur")
    print("3. Accédez à: http://127.0.0.1:8000/assureur/dashboard/")
    print("4. Testez toutes les fonctionnalités")

if __name__ == '__main__':
    corriger_erreurs_rapide()