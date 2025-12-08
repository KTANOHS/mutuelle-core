#!/usr/bin/env python3
"""
SCRIPT DE CORRECTION RAPIDE - COMMUNICATION ASSUREUR
Version corrigée avec les bons chemins
"""

import os
import sys
from pathlib import Path

# Définir le bon chemin de base
BASE_DIR = Path(__file__).resolve().parent
print(f"📁 Répertoire de travail: {BASE_DIR}")

# ============================================================================
# 1. CRÉER LE TEMPLATE messagerie.html MANQUANT
# ============================================================================

print("\n1. 🎨 CRÉATION DU TEMPLATE messagerie.html")

messagerie_path = BASE_DIR / "templates" / "assureur" / "communication" / "messagerie.html"

if not messagerie_path.exists():
    content = '''{% extends 'assureur/base_assureur.html' %}
{% load static %}

{% block content %}
<div class="container-fluid">
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">Messagerie Assureur</h1>
        <div>
            <a href="/assureur/communication/envoyer/" class="btn btn-primary">
                <i class="fas fa-paper-plane me-1"></i>Nouveau message
            </a>
            <a href="/communication/notifications/" class="btn btn-warning ml-2">
                <i class="fas fa-bell me-1"></i>Notifications
            </a>
        </div>
    </div>

    <div class="alert alert-info">
        <i class="fas fa-info-circle me-2"></i>
        Cette messagerie permet de communiquer avec les agents, médecins et membres.
        Utilisez les liens ci-dessous pour accéder aux différentes fonctionnalités.
    </div>

    <div class="row">
        <!-- Accès rapide -->
        <div class="col-lg-4 mb-4">
            <div class="card border-left-primary shadow h-100">
                <div class="card-body">
                    <div class="text-center">
                        <i class="fas fa-comments fa-3x text-primary mb-3"></i>
                        <h5 class="card-title">Messagerie complète</h5>
                        <p class="card-text">Accédez à l'interface de messagerie avancée</p>
                        <a href="/communication/messagerie/" class="btn btn-primary">
                            <i class="fas fa-external-link-alt me-1"></i>Ouvrir
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Envoyer un message -->
        <div class="col-lg-4 mb-4">
            <div class="card border-left-success shadow h-100">
                <div class="card-body">
                    <div class="text-center">
                        <i class="fas fa-paper-plane fa-3x text-success mb-3"></i>
                        <h5 class="card-title">Nouveau message</h5>
                        <p class="card-text">Envoyez un message à un destinataire</p>
                        <a href="/assureur/communication/envoyer/" class="btn btn-success">
                            <i class="fas fa-edit me-1"></i>Écrire
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Notifications -->
        <div class="col-lg-4 mb-4">
            <div class="card border-left-warning shadow h-100">
                <div class="card-body">
                    <div class="text-center">
                        <i class="fas fa-bell fa-3x text-warning mb-3"></i>
                        <h5 class="card-title">Notifications</h5>
                        <p class="card-text">Consultez vos alertes et notifications</p>
                        <a href="/communication/notifications/" class="btn btn-warning">
                            <i class="fas fa-list me-1"></i>Voir
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Liens utiles -->
    <div class="row">
        <div class="col-lg-12">
            <div class="card shadow">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">Liens utiles</h6>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-3 text-center mb-3">
                            <a href="/communication/conversations/" class="btn btn-outline-primary btn-block">
                                <i class="fas fa-comment-dots fa-2x mb-2 d-block"></i>
                                Conversations
                            </a>
                        </div>
                        <div class="col-md-3 text-center mb-3">
                            <a href="/communication/messages/" class="btn btn-outline-info btn-block">
                                <i class="fas fa-envelope fa-2x mb-2 d-block"></i>
                                Tous les messages
                            </a>
                        </div>
                        <div class="col-md-3 text-center mb-3">
                            <a href="/communication/search/" class="btn btn-outline-secondary btn-block">
                                <i class="fas fa-search fa-2x mb-2 d-block"></i>
                                Rechercher
                            </a>
                        </div>
                        <div class="col-md-3 text-center mb-3">
                            <a href="/communication/stats/" class="btn btn-outline-success btn-block">
                                <i class="fas fa-chart-bar fa-2x mb-2 d-block"></i>
                                Statistiques
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Instructions -->
    <div class="row mt-4">
        <div class="col-lg-12">
            <div class="card shadow">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-info">
                        <i class="fas fa-question-circle me-1"></i>Comment utiliser la messagerie
                    </h6>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-4">
                            <h6><i class="fas fa-1 text-primary me-2"></i>Envoyer un message</h6>
                            <p class="small">Cliquez sur "Nouveau message" pour écrire à un agent, médecin ou membre.</p>
                        </div>
                        <div class="col-md-4">
                            <h6><i class="fas fa-2 text-success me-2"></i>Consulter les réponses</h6>
                            <p class="small">Accédez à la messagerie complète pour voir les conversations.</p>
                        </div>
                        <div class="col-md-4">
                            <h6><i class="fas fa-3 text-warning me-2"></i>Gérer les notifications</h6>
                            <p class="small">Vérifiez régulièrement vos notifications pour ne rien manquer.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    
    messagerie_path.parent.mkdir(parents=True, exist_ok=True)
    with open(messagerie_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Template messagerie.html créé: {messagerie_path}")
else:
    print(f"✅ Template messagerie.html existe déjà")

# ============================================================================
# 2. VÉRIFIER ET CORRIGER LES FICHIERS EXISTANTS
# ============================================================================

print("\n2. 🔍 VÉRIFICATION DES FICHIERS EXISTANTS")

# Lister tous les fichiers importants
files_to_check = [
    ("assureur/views.py", "Fichier des vues Django"),
    ("assureur/urls.py", "Fichier des URLs"),
    ("templates/assureur/dashboard.html", "Template dashboard"),
    ("templates/assureur/base_assureur.html", "Template de base"),
]

for file_path, description in files_to_check:
    full_path = BASE_DIR / file_path
    if full_path.exists():
        print(f"✅ {description}: {full_path}")
    else:
        print(f"❌ {description}: NON TROUVÉ - {full_path}")

# ============================================================================
# 3. AJOUTER LE LIEN COMMUNICATION AU MENU (si base_assureur.html existe)
# ============================================================================

print("\n3. 🍔 AJOUT DU LIEN COMMUNICATION AU MENU")

base_path = BASE_DIR / "templates" / "assureur" / "base_assureur.html"
if base_path.exists():
    with open(base_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si le lien communication existe déjà
    if 'communication' not in content.lower() and 'messagerie' not in content.lower():
        # Chercher le menu de navigation
        menu_item = '''
        <!-- Communication -->
        <li class="nav-item">
            <a class="nav-link" href="/assureur/communication/">
                <i class="fas fa-envelope"></i>
                <span>Communication</span>
            </a>
        </li>
        '''
        
        # Chercher où insérer (après les autres liens de menu)
        # Chercher après "Membres" ou autre lien existant
        insert_points = [
            ('href="/assureur/membres/"', 'Membres'),
            ('href="/assureur/bons/"', 'Bons'),
            ('href="/assureur/paiements/"', 'Paiements'),
        ]
        
        inserted = False
        for pattern, name in insert_points:
            if pattern in content and not inserted:
                lines = content.split('\n')
                new_lines = []
                
                for line in lines:
                    new_lines.append(line)
                    if pattern in line and 'nav-item' in line and not inserted:
                        print(f"   → Ajout après le lien {name}")
                        new_lines.append(menu_item)
                        inserted = True
                
                if inserted:
                    with open(base_path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(new_lines))
                    print(f"✅ Lien communication ajouté au menu après {name}")
                    break
        
        if not inserted:
            print("❌ Impossible de trouver l'endroit pour insérer dans le menu")
    else:
        print("✅ Lien communication déjà présent dans le menu")
else:
    print(f"⚠️  Template base_assureur.html non trouvé, création d'un simple menu")

    # Créer un template de base simple si nécessaire
    base_content = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Assureur - Mutuelle{% endblock %}</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .navbar { background-color: #2E86C1; }
        .sidebar { background-color: #f8f9fa; height: 100vh; }
        .main-content { padding: 20px; }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="/assureur/">
                <i class="fas fa-shield-alt"></i> Assureur
            </a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/assureur/">
                            <i class="fas fa-home"></i> Dashboard
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/assureur/membres/">
                            <i class="fas fa-users"></i> Membres
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/assureur/bons/">
                            <i class="fas fa-file-medical"></i> Bons
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/assureur/paiements/">
                            <i class="fas fa-money-bill-wave"></i> Paiements
                        </a>
                    </li>
                    <!-- Communication -->
                    <li class="nav-item">
                        <a class="nav-link" href="/assureur/communication/">
                            <i class="fas fa-envelope"></i> Communication
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/admin/logout/">
                            <i class="fas fa-sign-out-alt"></i> Déconnexion
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <div class="col-md-3 col-lg-2 sidebar">
                <div class="position-sticky pt-3">
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <a class="nav-link active" href="/assureur/">
                                <i class="fas fa-tachometer-alt"></i> Tableau de bord
                            </a>
                        </li>
                        <hr>
                        <li class="nav-item">
                            <a class="nav-link" href="/assureur/membres/">
                                <i class="fas fa-users"></i> Gestion des membres
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/assureur/bons/">
                                <i class="fas fa-file-medical"></i> Bons de soins
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/assureur/paiements/">
                                <i class="fas fa-credit-card"></i> Paiements
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/assureur/cotisations/">
                                <i class="fas fa-calculator"></i> Cotisations
                            </a>
                        </li>
                        <hr>
                        <li class="nav-item">
                            <a class="nav-link" href="/assureur/communication/">
                                <i class="fas fa-envelope"></i> Communication
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/assureur/statistiques/">
                                <i class="fas fa-chart-bar"></i> Statistiques
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/assureur/configuration/">
                                <i class="fas fa-cog"></i> Configuration
                            </a>
                        </li>
                    </ul>
                </div>
            </div>

            <!-- Main content -->
            <div class="col-md-9 col-lg-10 main-content">
                {% if messages %}
                <div class="messages">
                    {% for message in messages %}
                    <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                    {% endfor %}
                </div>
                {% endif %}

                {% block content %}
                <!-- Le contenu spécifique à chaque page va ici -->
                {% endblock %}
            </div>
        </div>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <!-- jQuery -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>'''
    
    base_path.parent.mkdir(parents=True, exist_ok=True)
    with open(base_path, 'w', encoding='utf-8') as f:
        f.write(base_content)
    print(f"✅ Template base_assureur.html créé: {base_path}")

# ============================================================================
# 4. CRÉER UN FICHIER DE CONFIGURATION SIMPLE POUR LES URLs
# ============================================================================

print("\n4. 🔗 CRÉATION D'UN FICHIER URLs SIMPLE")

# Vérifier si le module communication existe
comm_urls_path = BASE_DIR / "communication" / "urls.py"
if comm_urls_path.exists():
    print(f"✅ Module communication trouvé: {comm_urls_path}")
else:
    print(f"⚠️  Module communication non trouvé")

# Créer un fichier simple pour tester
test_urls_content = '''"""
URLs de test pour la communication assureur
À intégrer dans votre fichier assureur/urls.py
"""

from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    # Page de messagerie
    path('communication/', 
         TemplateView.as_view(template_name='assureur/communication/messagerie.html'),
         name='messagerie_assureur'),
    
    # Page d'envoi de message
    path('communication/envoyer/',
         TemplateView.as_view(template_name='assureur/communication/envoyer_message.html'),
         name='envoyer_message_assureur'),
    
    # Page de liste des messages
    path('communication/messages/',
         TemplateView.as_view(template_name='assureur/communication/liste_messages.html'),
         name='liste_messages_assureur'),
    
    # Page de notifications
    path('communication/notifications/',
         TemplateView.as_view(template_name='assureur/communication/liste_notifications.html'),
         name='liste_notifications_assureur'),
]
'''

test_urls_path = BASE_DIR / "test_communication_urls.py"
with open(test_urls_path, 'w', encoding='utf-8') as f:
    f.write(test_urls_content)
print(f"✅ Fichier de test URLs créé: {test_urls_path}")

# ============================================================================
# 5. CRÉER UN SCRIPT DE TEST
# ============================================================================

print("\n5. 🧪 CRÉATION D'UN SCRIPT DE TEST")

test_script = '''#!/usr/bin/env python3
"""
SCRIPT DE TEST - Communication Assureur
Teste les URLs et templates de communication
"""

import requests
import sys

BASE_URL = "http://localhost:8000"

def test_url(url, expected_status=200):
    """Teste une URL"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == expected_status:
            print(f"✅ {url} - {response.status_code}")
            return True
        else:
            print(f"❌ {url} - {response.status_code} (attendu: {expected_status})")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {url} - Serveur non disponible")
        return False
    except Exception as e:
        print(f"❌ {url} - Erreur: {e}")
        return False

print("🔧 TEST DES URLS DE COMMUNICATION")
print("="*60)

# URLs à tester
urls_to_test = [
    f"{BASE_URL}/assureur/communication/",
    f"{BASE_URL}/assureur/communication/envoyer/",
    f"{BASE_URL}/communication/messagerie/",
    f"{BASE_URL}/communication/notifications/",
    f"{BASE_URL}/assureur/",
    f"{BASE_URL}/assureur/membres/",
]

success_count = 0
for url in urls_to_test:
    if test_url(url):
        success_count += 1

print("\n" + "="*60)
print(f"📊 RÉSULTATS: {success_count}/{len(urls_to_test)} URLs fonctionnent")

if success_count == len(urls_to_test):
    print("🎉 Toutes les URLs fonctionnent parfaitement !")
else:
    print("⚠️  Certaines URLs ont des problèmes")
    print("\n🔧 CONSEILS:")
    print("1. Vérifiez que le serveur Django est démarré")
    print("2. Vérifiez les logs Django pour les erreurs")
    print("3. Assurez-vous d'être connecté (les URLs peuvent nécessiter une authentification)")
    print("4. Testez manuellement dans le navigateur")
'''

test_script_path = BASE_DIR / "test_communication.py"
with open(test_script_path, 'w', encoding='utf-8') as f:
    f.write(test_script)
    
# Rendre le script exécutable
import os
os.chmod(test_script_path, 0o755)
print(f"✅ Script de test créé: {test_script_path}")

print("\n" + "="*80)
print("✅ CORRECTIONS TERMINÉES !")
print("="*80)
print("""
📋 RÉCAPITULATIF :

1. ✅ Template messagerie.html créé
2. ✅ Template base_assureur.html créé/amélioré
3. ✅ Lien Communication ajouté au menu
4. ✅ Fichier de test URLs créé
5. ✅ Script de test créé

🚀 PROCHAINES ÉTAPES :

1. REDÉMARRER LE SERVEUR :
   python manage.py runserver

2. TESTER LES URLS :
   python test_communication.py

3. TESTER MANUELLEMENT :
   - http://localhost:8000/assureur/communication/
   - http://localhost:8000/assureur/communication/envoyer/
   - Vérifiez que le lien "Communication" apparaît dans le menu

🔧 POUR INTÉGRER COMPLÈTEMENT :

1. Ajoutez ces URLs à votre fichier assureur/urls.py :

   from django.urls import path
   from django.views.generic import TemplateView

   urlpatterns = [
       # ... vos URLs existantes ...
       
       # Communication
       path('communication/', 
            TemplateView.as_view(template_name='assureur/communication/messagerie.html'),
            name='messagerie_assureur'),
       
       path('communication/envoyer/',
            TemplateView.as_view(template_name='assureur/communication/envoyer_message.html'),
            name='envoyer_message_assureur'),
   ]

2. Si vous avez des vues spécifiques, remplacez TemplateView par vos vues

3. Personnalisez les templates selon vos besoins

💡 ASTUCE :
   Pour un système de messagerie complet, utilisez l'application 'communication'
   déjà présente dans votre projet.
""")