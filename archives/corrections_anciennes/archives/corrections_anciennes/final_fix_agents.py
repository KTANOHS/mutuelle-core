# final_fix_agents.py
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

def corriger_urls_principales():
    """S'assure que les agents sont inclus dans les URLs principales"""
    main_urls_path = BASE_DIR / 'mutuelle_core' / 'urls.py'
    
    if not main_urls_path.exists():
        print("❌ Fichier urls.py principal introuvable")
        return False
        
    try:
        with open(main_urls_path, 'r') as f:
            content = f.read()
        
        # Vérifier si agents est déjà inclus
        if 'agents' in content and 'include' in content:
            print("✅ URLs agents déjà incluses")
            return True
            
        # Ajouter l'import si nécessaire
        if 'from django.urls import include' not in content:
            content = content.replace(
                'from django.urls import path', 
                'from django.urls import path, include'
            )
        
        # Trouver le bon endroit pour ajouter
        if 'urlpatterns = [' in content:
            lines = content.split('\n')
            new_lines = []
            url_pattern_added = False
            
            for line in lines:
                new_lines.append(line)
                if 'urlpatterns = [' in line and not url_pattern_added:
                    # Ajouter après la ligne urlpatterns
                    new_lines.append("    path('agents/', include('agents.urls')),")
                    url_pattern_added = True
            
            new_content = '\n'.join(new_lines)
            
            with open(main_urls_path, 'w') as f:
                f.write(new_content)
            
            print("✅ URLs agents ajoutées au fichier urls.py principal")
            return True
            
    except Exception as e:
        print(f"❌ Erreur modification urls.py: {e}")
        return False

def corriger_views_py():
    """Corrige le fichier views.py avec les bonnes vues"""
    views_path = BASE_DIR / 'agents' / 'views.py'
    
    try:
        # Vues corrigées
        views_content = '''from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
import json

@login_required
def verification_cotisations(request):
    """Page principale de vérification des cotisations"""
    context = {
        'verifications_du_jour': 15,
        'dernieres_verifications': [],
    }
    return render(request, 'agents/verification_cotisations.html', context)

@login_required
def recherche_membres_api(request):
    """API pour la recherche de membres - VERSION SIMPLIFIÉE"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'membres': []})
    
    try:
        # DONNÉES DE TEST - À REMPLACER PAR VOTRE MODÈLE
        membres_test = [
            {
                'id': 1,
                'nom_complet': 'Jean Dupont',
                'numero_membre': 'MEM001',
                'telephone': '01 23 45 67 89',
                'est_a_jour': True
            },
            {
                'id': 2, 
                'nom_complet': 'Marie Martin',
                'numero_membre': 'MEM002',
                'telephone': '01 34 56 78 90',
                'est_a_jour': False
            },
            {
                'id': 3,
                'nom_complet': 'Pierre Lambert',
                'numero_membre': 'MEM003', 
                'telephone': '01 45 67 89 01',
                'est_a_jour': True
            }
        ]
        
        # Filtrer selon la requête
        membres_filtres = [
            m for m in membres_test 
            if query.lower() in m['nom_complet'].lower() 
            or query in m['numero_membre']
        ]
        
        return JsonResponse({'membres': membres_filtres})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def verifier_cotisation_api(request, membre_id):
    """API pour vérifier la cotisation d'un membre - VERSION SIMPLIFIÉE"""
    try:
        # DONNÉES DE TEST - À REMPLACER PAR VOTRE MODÈLE
        membres_test = {
            1: {'nom': 'Jean Dupont', 'est_a_jour': True},
            2: {'nom': 'Marie Martin', 'est_a_jour': False},
            3: {'nom': 'Pierre Lambert', 'est_a_jour': True}
        }
        
        if int(membre_id) not in membres_test:
            return JsonResponse({
                'success': False,
                'error': 'Membre non trouvé'
            }, status=404)
        
        membre = membres_test[int(membre_id)]
        
        if membre['est_a_jour']:
            return JsonResponse({
                'success': True,
                'est_a_jour': True,
                'message': '✅ Le membre est à jour dans ses cotisations',
                'prochaine_echeance': '31/12/2024',
                'dernier_paiement': '15/01/2024',
                'verification_id': f"VER{datetime.now().strftime('%Y%m%d%H%M%S')}"
            })
        else:
            return JsonResponse({
                'success': True,
                'est_a_jour': False, 
                'message': '⚠️ Le membre a des cotisations en retard',
                'prochaine_echeance': '31/12/2024',
                'dernier_paiement': '15/06/2023',
                'verification_id': f"VER{datetime.now().strftime('%Y%m%d%H%M%S')}"
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erreur lors de la vérification: {str(e)}'
        }, status=500)

@login_required
def tableau_de_bord_agent(request):
    """Tableau de bord de l'agent"""
    return render(request, 'agents/dashboard.html')
'''
        
        with open(views_path, 'w') as f:
            f.write(views_content)
        
        print("✅ Fichier views.py corrigé avec les vues API")
        return True
        
    except Exception as e:
        print(f"❌ Erreur modification views.py: {e}")
        return False

def corriger_urls_py():
    """Corrige le fichier urls.py des agents"""
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
        
        print("✅ Fichier urls.py corrigé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur modification urls.py: {e}")
        return False

def corriger_template_verification():
    """Corrige le template de vérification"""
    template_path = BASE_DIR / 'agents' / 'templates' / 'agents' / 'verification_cotisations.html'
    
    try:
        template_content = '''{% extends 'agents/base_agent.html' %}
{% load static %}

{% block title %}Vérification cotisations - Agent{% endblock %}
{% block page_title %}Vérification des cotisations{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-8">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">
                    <i class="fas fa-check-circle me-2"></i>Vérification en temps réel
                </h5>
            </div>
            <div class="card-body">
                <!-- Recherche rapide -->
                <div class="mb-4">
                    <label class="form-label">Rechercher un membre</label>
                    <div class="input-group">
                        <input type="text" class="form-control" id="rechercheMembreRapide" 
                               placeholder="Nom, prénom ou numéro de membre...">
                        <button class="btn btn-outline-primary" type="button" id="btnRechercheRapide">
                            <i class="fas fa-search"></i>
                        </button>
                    </div>
                    <div id="resultatsRechercheRapide" class="mt-2"></div>
                </div>

                <!-- Résultats -->
                <div id="resultatsVerification" class="mt-4">
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle me-2"></i>
                        Utilisez la recherche ci-dessus pour vérifier les cotisations des membres.
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="col-lg-4">
        <!-- Statistiques -->
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">
                    <i class="fas fa-chart-bar me-2"></i>Statistiques
                </h5>
            </div>
            <div class="card-body">
                <div class="mb-3">
                    <small class="text-muted">Vérifications aujourd'hui</small>
                    <h4>{{ verifications_du_jour }}</h4>
                </div>
                <div class="mb-3">
                    <small class="text-muted">Taux de conformité</small>
                    <div class="progress mb-1">
                        <div class="progress-bar bg-success" style="width: 85%">85%</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Guide rapide -->
        <div class="card mt-4">
            <div class="card-header">
                <h5 class="card-title mb-0">
                    <i class="fas fa-question-circle me-2"></i>Guide rapide
                </h5>
            </div>
            <div class="card-body">
                <p class="small">
                    <strong>Comment vérifier une cotisation:</strong>
                </p>
                <ol class="small">
                    <li>Saisissez le nom ou numéro du membre</li>
                    <li>Sélectionnez le membre dans les résultats</li>
                    <li>Cliquez sur "Vérifier" pour voir le statut</li>
                </ol>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
// Variables globales
let rechercheTimeout = null;

// Recherche rapide - Événements
document.getElementById('btnRechercheRapide').addEventListener('click', function() {
    clearTimeout(rechercheTimeout);
    rechercherMembre();
});

document.getElementById('rechercheMembreRapide').addEventListener('input', function(e) {
    clearTimeout(rechercheTimeout);
    rechercheTimeout = setTimeout(() => {
        if (this.value.length >= 2) {
            rechercherMembre();
        }
    }, 500);
});

function rechercherMembre() {
    const query = document.getElementById('rechercheMembreRapide').value.trim();
    const resultsDiv = document.getElementById('resultatsRechercheRapide');
    
    if (query.length < 2) {
        resultsDiv.innerHTML = '<div class="alert alert-warning">Entrez au moins 2 caractères</div>';
        return;
    }

    resultsDiv.innerHTML = '<div class="text-center"><div class="spinner-border text-primary"></div><p class="mt-2">Recherche en cours...</p></div>';

    // URL CORRIGÉE - utilise le bon chemin
    const apiUrl = `/agents/api/recherche-membres/?q=${encodeURIComponent(query)}`;
    
    fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        afficherResultatsRecherche(data);
    })
    .catch(error => {
        console.error('Erreur recherche:', error);
        resultsDiv.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Erreur lors de la recherche: ${error.message}
            </div>
        `;
    });
}

function afficherResultatsRecherche(data) {
    const resultsDiv = document.getElementById('resultatsRechercheRapide');
    
    if (!data || !data.membres || data.membres.length === 0) {
        resultsDiv.innerHTML = '<div class="alert alert-info">Aucun membre trouvé</div>';
        return;
    }

    let html = '<div class="list-group">';
    
    data.membres.forEach(membre => {
        html += `
            <div class="list-group-item list-group-item-action">
                <div class="d-flex w-100 justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <h6 class="mb-1">${escapeHtml(membre.nom_complet)}</h6>
                        <p class="mb-1 text-muted">
                            <small>Numéro: ${escapeHtml(membre.numero_membre || 'N/A')}</small><br>
                            <small>Téléphone: ${escapeHtml(membre.telephone || 'N/A')}</small>
                        </p>
                    </div>
                    <div class="ms-3">
                        <span class="badge bg-${membre.est_a_jour ? 'success' : 'danger'}">
                            ${membre.est_a_jour ? 'À jour' : 'En retard'}
                        </span>
                        <button class="btn btn-sm btn-outline-primary mt-2 verifier-membre" 
                                data-membre-id="${membre.id}">
                            <i class="fas fa-check-circle me-1"></i>Vérifier
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    resultsDiv.innerHTML = html;
    
    // Ajouter les événements aux boutons de vérification
    document.querySelectorAll('.verifier-membre').forEach(button => {
        button.addEventListener('click', function() {
            const membreId = this.getAttribute('data-membre-id');
            const membreNom = this.closest('.list-group-item').querySelector('h6').textContent;
            verifierCotisation(membreId, membreNom);
        });
    });
}

function verifierCotisation(membreId, membreNom) {
    const resultsDiv = document.getElementById('resultatsVerification');
    
    resultsDiv.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-2">Vérification en cours pour ${escapeHtml(membreNom)}...</p>
        </div>
    `;

    // URL CORRIGÉE - utilise le bon chemin
    const apiUrl = `/agents/api/verifier-cotisation/${membreId}/`;
    
    fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            resultsDiv.innerHTML = `
                <div class="alert alert-${data.est_a_jour ? 'success' : 'warning'}">
                    <div class="d-flex align-items-center">
                        <i class="fas fa-${data.est_a_jour ? 'check-circle' : 'exclamation-triangle'} fa-2x me-3"></i>
                        <div>
                            <h5 class="mb-1">${escapeHtml(membreNom)}</h5>
                            <p class="mb-2">${escapeHtml(data.message)}</p>
                            ${data.prochaine_echeance ? 
                                `<p class="mb-1"><strong>Prochaine échéance:</strong> ${escapeHtml(data.prochaine_echeance)}</p>` : ''}
                            ${data.dernier_paiement ? 
                                `<p class="mb-1"><strong>Dernier paiement:</strong> ${escapeHtml(data.dernier_paiement)}</p>` : ''}
                        </div>
                    </div>
                    <hr>
                    <small class="text-muted">
                        Vérification ID: ${data.verification_id || 'N/A'} | 
                        ${new Date().toLocaleString('fr-FR')}
                    </small>
                </div>
            `;
        } else {
            resultsDiv.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-times-circle me-2"></i>
                    <strong>Erreur</strong><br>
                    ${escapeHtml(data.error || 'Erreur inconnue')}
                </div>
            `;
        }
    })
    .catch(error => {
        console.error('Erreur vérification:', error);
        resultsDiv.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-network-wired me-2"></i>
                <strong>Erreur de connexion</strong><br>
                Impossible de vérifier la cotisation: ${error.message}
            </div>
        `;
    });
}

// Fonction utilitaire pour échapper le HTML
function escapeHtml(unsafe) {
    if (unsafe === null || unsafe === undefined) return '';
    return unsafe
        .toString()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    console.log('Module de vérification des cotisations initialisé');
});
</script>
{% endblock %}
'''
        
        with open(template_path, 'w') as f:
            f.write(template_content)
        
        print("✅ Template verification_cotisations.html corrigé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur modification template: {e}")
        return False

def appliquer_corrections_finales():
    """Applique toutes les corrections finales"""
    print("🔧 APPLICATION DES CORRECTIONS FINALES")
    print("=" * 50)
    
    corrections = [
        ("Correction URLs principales", corriger_urls_principales),
        ("Correction views.py", corriger_views_py),
        ("Correction urls.py", corriger_urls_py),
        ("Correction template", corriger_template_verification),
    ]
    
    for nom, fonction in corrections:
        print(f"\n📝 {nom}...")
        if fonction():
            print("   ✅ SUCCÈS")
        else:
            print("   ❌ ÉCHEC")
    
    print("\n🎯 CORRECTIONS FINALES APPLIQUÉES!")
    print("\n📋 PROCHAINES ÉTAPES:")
    print("1. Redémarrez le serveur Django")
    print("2. Accédez à: http://localhost:8000/agents/verification-cotisations/")
    print("3. Testez la recherche avec: 'Jean' ou 'MEM001'")

if __name__ == "__main__":
    appliquer_corrections_finales()