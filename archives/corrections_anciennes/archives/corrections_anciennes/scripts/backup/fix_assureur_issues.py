#!/usr/bin/env python
"""
CORRECTION AUTOMATIQUE DES PROBLÈMES ASSUREUR
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def fix_settings():
    """Corrige les ALLOWED_HOSTS dans settings.py"""
    print("🔧 Correction des ALLOWED_HOSTS...")
    
    settings_path = BASE_DIR / 'mutuelle_core' / 'settings.py'
    
    with open(settings_path, 'r') as f:
        content = f.read()
    
    # Ajouter testserver aux ALLOWED_HOSTS
    if 'testserver' not in content:
        content = content.replace(
            "ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')",
            "ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver').split(',')"
        )
    
    with open(settings_path, 'w') as f:
        f.write(content)
    
    print("✅ ALLOWED_HOSTS corrigés")

def fix_assureur_urls():
    """Corrige les URLs manquantes dans assureur/urls.py"""
    print("🔧 Correction des URLs assureur...")
    
    urls_path = BASE_DIR / 'assureur' / 'urls.py'
    
    corrected_urls = '''from django.urls import path
from . import views

app_name = 'assureur'

urlpatterns = [
    # Tableau de bord
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Gestion des membres
    path('membres/recherche/', views.recherche_membre, name='recherche_membre'),
    path('membres/<str:numero_membre>/', views.detail_membre, name='detail_membre'),
    path('membres/creer/', views.creer_membre, name='creer_membre'),
    
    # Gestion des bons
    path('bons/', views.liste_bons, name='liste_bons'),
    path('bons/creer/<str:numero_membre>/', views.creer_bon, name='creer_bon'),
    path('bons/valider/<int:bon_id>/', views.valider_bon, name='valider_bon'),
    
    # Rapports et exports
    path('rapports/statistiques/', views.rapport_statistiques, name='rapport_statistiques'),
    path('export/bons/', views.export_bons, name='export_bons'),
    path('export/membres/', views.export_membres, name='export_membres'),
    
    # API temps réel
    path('api/statistiques/', views.statistiques_temps_reel, name='statistiques_temps_reel'),
]'''
    
    with open(urls_path, 'w') as f:
        f.write(corrected_urls)
    
    print("✅ URLs assureur corrigées")

def create_missing_template():
    """Crée le template manquant"""
    print("📁 Création du template rapport_statistiques.html...")
    
    template_dir = BASE_DIR / 'templates' / 'assureur'
    template_dir.mkdir(parents=True, exist_ok=True)
    
    template_content = '''{% extends 'base.html' %}
{% load humanize %}

{% block title %}Rapports Statistiques - Assureur{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1><i class="fas fa-chart-bar"></i> Rapports Statistiques</h1>
        <div class="btn-group">
            <a href="{% url 'assureur:dashboard' %}" class="btn btn-outline-primary">
                <i class="fas fa-arrow-left"></i> Dashboard
            </a>
            <a href="{% url 'assureur:export_membres' %}" class="btn btn-success">
                <i class="fas fa-file-csv"></i> Export CSV
            </a>
        </div>
    </div>

    <div class="row">
        <div class="col-md-4 mb-4">
            <div class="card shadow-sm">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0"><i class="fas fa-users"></i> Statistiques Membres</h5>
                </div>
                <div class="card-body">
                    <p>Rapport détaillé des membres par statut, catégorie, et période.</p>
                    <a href="#" class="btn btn-outline-primary w-100">Générer le rapport</a>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-4">
            <div class="card shadow-sm">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0"><i class="fas fa-file-medical"></i> Statistiques Bons</h5>
                </div>
                <div class="card-body">
                    <p>Analyse des bons par type, statut, et période mensuelle.</p>
                    <a href="#" class="btn btn-outline-success w-100">Générer le rapport</a>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-4">
            <div class="card shadow-sm">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0"><i class="fas fa-money-bill-wave"></i> Statistiques Financières</h5>
                </div>
                <div class="card-body">
                    <p>Rapport des recettes, paiements et indicateurs financiers.</p>
                    <a href="#" class="btn btn-outline-info w-100">Générer le rapport</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    
    template_path = template_dir / 'rapport_statistiques.html'
    template_path.write_text(template_content)
    print("✅ Template rapport_statistiques.html créé")

def check_models():
    """Vérifie et corrige les modèles"""
    print("🗄️  Vérification des modèles...")
    
    models_path = BASE_DIR / 'membres' / 'models.py'
    
    if models_path.exists():
        with open(models_path, 'r') as f:
            content = f.read()
        
        if 'class Bon' not in content:
            print("⚠️  Modèle Bon manquant - à ajouter manuellement")
        else:
            print("✅ Modèle Bon présent")
    else:
        print("❌ Fichier models.py non trouvé")

if __name__ == "__main__":
    print("🔄 CORRECTION DES PROBLÈMES ASSUREUR")
    print("=" * 50)
    
    fix_settings()
    fix_assureur_urls()
    create_missing_template()
    check_models()
    
    print("\n🎉 CORRECTIONS APPLIQUÉES !")
    print("📋 Prochaines étapes :")
    print("   1. Vérifiez manuellement le modèle Bon dans membres/models.py")
    print("   2. Exécutez les migrations : python manage.py makemigrations")
    print("   3. Appliquez les migrations : python manage.py migrate")
    print("   4. Testez à nouveau : python final_check_assureur.py")