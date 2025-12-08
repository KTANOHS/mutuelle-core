#!/bin/bash

# Script: fix_membres_dashboard.sh
# Description: Corrige spécifiquement le problème du template membres/dashboard.html

echo "🔍 Analyse du problème TemplateDoesNotExist: membres/dashboard.html"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { echo -e "${BLUE}ℹ $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; }

# Vérification de la structure existante
info "Structure actuelle des templates membres:"
find membres/templates -name "*.html" | head -20

# Vérifier si le template dashboard existe déjà
if [ -f "membres/templates/membres/dashboard.html" ]; then
    success "Le template membres/dashboard.html existe déjà"
    echo "Emplacement: $(readlink -f membres/templates/membres/dashboard.html)"
    exit 0
fi

# Analyser les templates de dashboard existants
info "Templates de dashboard existants dans le projet:"
find . -name "*dashboard*.html" -type f | grep -v "__pycache__" | grep -v ".pyc"

# Vérifier la vue qui appelle le template
info "Analyse de la vue dashboard dans membres/views.py:"
if [ -f "membres/views.py" ]; then
    grep -A 10 -B 5 "dashboard.html" membres/views.py || echo "Template dashboard.html non trouvé dans la vue"
fi

# Solution 1: Créer le template manquant basé sur l'existant
echo ""
info "Création du template membres/dashboard.html..."

# Créer le dossier si nécessaire
mkdir -p "membres/templates/membres"

# Créer le template dashboard pour membres
cat > "membres/templates/membres/dashboard.html" << 'EOF'
{% extends 'base.html' %}
{% load static humanize %}

{% block title %}Tableau de Bord - Membres{% endblock %}

{% block content %}
<div class="container-fluid">
    <!-- En-tête -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="page-header bg-primary text-white p-4 rounded">
                <h1 class="h3 mb-0">
                    <i class="fas fa-tachometer-alt me-2"></i>
                    Tableau de Bord Membre
                </h1>
                <p class="mb-0 mt-2">Bienvenue, {{ user.get_full_name|default:user.username }}!</p>
            </div>
        </div>
    </div>

    <!-- Cartes de statistiques -->
    <div class="row mb-4">
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-primary shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                                Solde Actuel
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">
                                {{ solde_membre|default:0|intcomma }} FCFA
                            </div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-wallet fa-2x text-gray-300"></i>
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
                                Soins du Mois
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">
                                {{ nb_soins_mois|default:0 }}
                            </div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-stethoscope fa-2x text-gray-300"></i>
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
                                Dernier Paiement
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">
                                {% if dernier_paiement %}
                                    {{ dernier_paiement.montant|intcomma }} FCFA
                                {% else %}
                                    Aucun
                                {% endif %}
                            </div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-money-bill-wave fa-2x text-gray-300"></i>
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
                                Statut
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">
                                {{ statut_membre|default:"Actif" }}
                            </div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-user-check fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Actions rapides -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card shadow">
                <div class="card-header bg-white py-3">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-bolt me-2"></i>Actions Rapides
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-lg-2 col-md-4 col-sm-6 mb-3">
                            <a href="{% url 'mes_paiements' %}" class="btn btn-outline-primary btn-block w-100">
                                <i class="fas fa-credit-card me-2"></i>Mes Paiements
                            </a>
                        </div>
                        <div class="col-lg-2 col-md-4 col-sm-6 mb-3">
                            <a href="{% url 'mes_ordonnances' %}" class="btn btn-outline-success btn-block w-100">
                                <i class="fas fa-file-medical me-2"></i>Mes Ordonnances
                            </a>
                        </div>
                        <div class="col-lg-2 col-md-4 col-sm-6 mb-3">
                            <a href="{% url 'solde_remboursements' %}" class="btn btn-outline-info btn-block w-100">
                                <i class="fas fa-chart-line me-2"></i>Mon Solde
                            </a>
                        </div>
                        <div class="col-lg-2 col-md-4 col-sm-6 mb-3">
                            <a href="{% url 'profil' %}" class="btn btn-outline-warning btn-block w-100">
                                <i class="fas fa-user me-2"></i>Mon Profil
                            </a>
                        </div>
                        <div class="col-lg-2 col-md-4 col-sm-6 mb-3">
                            <a href="{% url 'liste_soins' %}" class="btn btn-outline-secondary btn-block w-100">
                                <i class="fas fa-history me-2"></i>Historique Soins
                            </a>
                        </div>
                        <div class="col-lg-2 col-md-4 col-sm-6 mb-3">
                            <a href="{% url 'support' %}" class="btn btn-outline-danger btn-block w-100">
                                <i class="fas fa-headset me-2"></i>Support
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Dernières activités -->
    <div class="row">
        <div class="col-lg-6 mb-4">
            <div class="card shadow">
                <div class="card-header bg-white py-3">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-history me-2"></i>Derniers Soins
                    </h5>
                </div>
                <div class="card-body">
                    {% if derniers_soins %}
                        <div class="list-group list-group-flush">
                            {% for soin in derniers_soins %}
                            <div class="list-group-item d-flex justify-content-between align-items-center">
                                <div>
                                    <h6 class="mb-1">{{ soin.type_soin }}</h6>
                                    <small class="text-muted">{{ soin.date_soin|date:"d/m/Y" }}</small>
                                </div>
                                <span class="badge bg-primary rounded-pill">{{ soin.montant|intcomma }} FCFA</span>
                            </div>
                            {% endfor %}
                        </div>
                    {% else %}
                        <p class="text-muted text-center">Aucun soin récent</p>
                    {% endif %}
                </div>
            </div>
        </div>

        <div class="col-lg-6 mb-4">
            <div class="card shadow">
                <div class="card-header bg-white py-3">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-bell me-2"></i>Notifications
                    </h5>
                </div>
                <div class="card-body">
                    {% if notifications %}
                        <div class="list-group list-group-flush">
                            {% for notif in notifications %}
                            <div class="list-group-item">
                                <div class="d-flex w-100 justify-content-between">
                                    <h6 class="mb-1">{{ notif.titre }}</h6>
                                    <small class="text-muted">{{ notif.date_creation|timesince }}</small>
                                </div>
                                <p class="mb-1">{{ notif.message }}</p>
                            </div>
                            {% endfor %}
                        </div>
                    {% else %}
                        <p class="text-muted text-center">Aucune notification</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
$(document).ready(function() {
    console.log('Dashboard membre chargé');
    
    // Actualiser les données toutes les 30 secondes
    setInterval(function() {
        $.ajax({
            url: '{% url "membres_dashboard_data" %}',
            success: function(data) {
                // Mettre à jour les cartes de statistiques
                if (data.solde_membre !== undefined) {
                    $('.card-border-left-primary .h5').text(data.solde_membre.toLocaleString() + ' FCFA');
                }
            }
        });
    }, 30000);
});
</script>
{% endblock %}
EOF

success "Template membres/dashboard.html créé avec succès"

# Vérification finale
echo ""
info "Vérification finale..."
python3 -c "
import os
import sys
import django
from django.conf import settings

sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.template.loader import get_template

try:
    template = get_template('membres/dashboard.html')
    print('✅ SUCCÈS: Template membres/dashboard.html chargé correctement')
    print('   Chemin:', template.origin.name)
except Exception as e:
    print('❌ ERREUR:', e)
"

# Test de rendu
echo ""
info "Test de rendu du template..."
python3 -c "
import os
import sys
import django
from django.contrib.auth.models import User

sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.template.loader import render_to_string

try:
    context = {
        'user': User(username='test_user', email='test@example.com'),
        'solde_membre': 15000,
        'nb_soins_mois': 3,
        'statut_membre': 'Actif',
        'derniers_soins': [
            {'type_soin': 'Consultation générale', 'date_soin': '2025-01-25', 'montant': 5000},
            {'type_soin': 'Analyse sanguine', 'date_soin': '2025-01-20', 'montant': 8000}
        ]
    }
    
    html = render_to_string('membres/dashboard.html', context)
    print('✅ SUCCÈS: Template rendu avec succès')
    print('   Taille HTML:', len(html), 'caractères')
except Exception as e:
    print('❌ ERREUR lors du rendu:', e)
"

echo ""
success "Correction terminée!"
info "Redémarrez le serveur: python manage.py runserver"
info "Testez l'URL: http://127.0.0.1:8000/membres/dashboard/"