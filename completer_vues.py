#!/usr/bin/env python
"""
COMPLÉTION DES VUES ASSUREUR - VERSION CORRIGÉE
"""

import os

def completer_vues_assureur():
    """Complète la vue avec toutes les fonctions nécessaires - Version corrigée"""
    
    code_vues_complete = '''"""
VUES COMPLÈTES POUR ASSUREUR
"""

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from membres.models import Membre, Bon
from paiements.models import Paiement
from django.contrib.auth.decorators import login_required
import json

@login_required
def dashboard(request):
    """
    Tableau de bord de l'assureur
    """
    # Pour les tests, retourner une réponse simple
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Dashboard assureur',
            'stats': {
                'membres_total': Membre.objects.count(),
                'bons_total': Bon.objects.count(),
                'bons_en_attente': Bon.objects.filter(statut='en_attente').count()
            }
        })
    else:
        # Retourner une page HTML simple pour les tests
        html_content = """
        <html>
            <body>
                <h1>Tableau de bord Assureur</h1>
                <p>Bienvenue dans l'interface assureur</p>
                <ul>
                    <li><a href="/assureur/bons/">Liste des bons</a></li>
                    <li><a href="/assureur/recherche/">Recherche membres</a></li>
                </ul>
            </body>
        </html>
        """
        return HttpResponse(html_content)

@login_required
def creer_bon(request, membre_id):
    """
    Création d'un bon de soin
    """
    try:
        # Vérifier si c'est une requête AJAX POST
        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            # Vérifier que l'utilisateur est un assureur (staff)
            if not request.user.is_staff:
                return JsonResponse({
                    'success': False,
                    'message': 'Accès non autorisé. Réservé aux assureurs.'
                }, status=403)
            
            # Gérer les données JSON ou form data
            if request.content_type == 'application/json':
                try:
                    data = json.loads(request.body)
                except json.JSONDecodeError:
                    return JsonResponse({
                        'success': False,
                        'message': 'Données JSON invalides'
                    }, status=400)
            else:
                data = request.POST.dict()
            
            # Récupérer le membre
            try:
                membre = Membre.objects.get(numero_unique=membre_id)
            except Membre.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': f'Membre {membre_id} non trouvé'
                }, status=404)
            
            # Validation des données requises
            type_soin = data.get('type_soin')
            if not type_soin:
                return JsonResponse({
                    'success': False,
                    'message': 'Le type de soin est requis'
                }, status=400)
            
            # Créer le bon
            numero_bon = f"BON_{membre.numero_unique}_{timezone.now().strftime('%Y%m%d_%H%M%S')}"
            
            bon = Bon.objects.create(
                numero_bon=numero_bon,
                membre=membre,
                type_soin=type_soin,
                description=data.get('description', ''),
                lieu_soins=data.get('lieu_soins', 'Centre Médical'),
                date_soins=data.get('date_soins', timezone.now().date()),
                medecin_traitant=data.get('medecin_traitant', ''),
                numero_ordonnance=data.get('numero_ordonnance', ''),
                montant_total=float(data.get('montant_total', 0)),
                taux_remboursement=float(data.get('taux_remboursement', 70)),
                montant_rembourse=0,
                frais_dossier=0,
                statut='en_attente',
                date_creation=timezone.now(),
                date_emission=timezone.now().date()
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Bon créé avec succès',
                'bon_id': bon.id,
                'numero_bon': bon.numero_bon,
                'membre': f"{membre.nom} {membre.prenom}",
                'statut': bon.statut,
                'type_soin': bon.type_soin,
                'montant_total': str(bon.montant_total)
            })
            
        else:
            # Méthode non autorisée
            return JsonResponse({
                'success': False,
                'message': 'Méthode non autorisée. Utilisez POST avec en-tête XMLHttpRequest.'
            }, status=405)
            
    except Exception as e:
        # Erreur générale
        return JsonResponse({
            'success': False,
            'message': f'Erreur lors de la création du bon: {str(e)}'
        }, status=500)

@login_required
def liste_bons(request):
    """
    Liste des bons
    """
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Version AJAX
        bons = Bon.objects.select_related('membre').order_by('-date_creation')[:10]
        bons_data = []
        
        for bon in bons:
            bons_data.append({
                'id': bon.id,
                'numero_bon': bon.numero_bon,
                'membre': f"{bon.membre.nom} {bon.membre.prenom}",
                'type_soin': bon.type_soin,
                'montant_total': str(bon.montant_total),
                'statut': bon.statut,
                'date_creation': bon.date_creation.strftime('%Y-%m-%d %H:%M')
            })
        
        return JsonResponse({
            'success': True,
            'message': 'Liste des bons',
            'bons': bons_data,
            'total': Bon.objects.count()
        })
    else:
        # Version HTML
        html_content = """
        <html>
            <body>
                <h1>Liste des bons</h1>
                <p>Interface de gestion des bons de soin</p>
                <div id="bons-list">
                    <!-- Les bons seront chargés ici en AJAX -->
                </div>
                <script>
                    // Chargement AJAX des bons
                    fetch('/assureur/bons/', {
                        headers: { 'X-Requested-With': 'XMLHttpRequest' }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            const list = document.getElementById('bons-list');
                            data.bons.forEach(bon => {
                                const div = document.createElement('div');
                                div.innerHTML = `
                                    <h3>${bon.numero_bon}</h3>
                                    <p>Membre: ${bon.membre} | Type: ${bon.type_soin}</p>
                                    <p>Montant: ${bon.montant_total} | Statut: ${bon.statut}</p>
                                `;
                                list.appendChild(div);
                            });
                        }
                    });
                </script>
            </body>
        </html>
        """
        return HttpResponse(html_content)

@login_required
def recherche_membre(request):
    """
    Recherche de membres
    """
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Version AJAX
        query = request.GET.get('q', '')
        if query:
            membres = Membre.objects.filter(
                nom__icontains=query
            ) | Membre.objects.filter(
                prenom__icontains=query
            ) | Membre.objects.filter(
                numero_unique__icontains=query
            )
            membres = membres[:10]
        else:
            membres = Membre.objects.all()[:10]
        
        membres_data = []
        for membre in membres:
            membres_data.append({
                'id': membre.id,
                'numero_unique': membre.numero_unique,
                'nom_complet': f"{membre.nom} {membre.prenom}",
                'email': membre.email,
                'telephone': membre.telephone,
                'statut': membre.statut
            })
        
        return JsonResponse({
            'success': True,
            'message': 'Résultats de recherche',
            'membres': membres_data,
            'query': query,
            'total': len(membres_data)
        })
    else:
        # Version HTML
        html_content = """
        <html>
            <body>
                <h1>Recherche de membres</h1>
                <form id="search-form">
                    <input type="text" name="q" placeholder="Nom, prénom ou numéro..." />
                    <button type="submit">Rechercher</button>
                </form>
                <div id="results">
                    <!-- Résultats de recherche -->
                </div>
                <script>
                    document.getElementById('search-form').addEventListener('submit', function(e) {
                        e.preventDefault();
                        const query = document.querySelector('input[name="q"]').value;
                        
                        fetch(`/assureur/recherche/?q=${encodeURIComponent(query)}`, {
                            headers: { 'X-Requested-With': 'XMLHttpRequest' }
                        })
                        .then(response => response.json())
                        .then(data => {
                            const results = document.getElementById('results');
                            results.innerHTML = '';
                            
                            if (data.success) {
                                data.membres.forEach(membre => {
                                    const div = document.createElement('div');
                                    div.innerHTML = `
                                        <h3>${membre.nom_complet}</h3>
                                        <p>Numéro: ${membre.numero_unique} | Tél: ${membre.telephone}</p>
                                        <p>Email: ${membre.email} | Statut: ${membre.statut}</p>
                                        <a href="/assureur/bons/creer/${membre.numero_unique}/">Créer un bon</a>
                                    `;
                                    results.appendChild(div);
                                });
                            }
                        });
                    });
                </script>
            </body>
        </html>
        """
        return HttpResponse(html_content)
'''

    chemin_views = os.path.join(os.path.dirname(__file__), 'assureur', 'views.py')
    
    # Sauvegarder l'ancienne version
    if os.path.exists(chemin_views):
        os.rename(chemin_views, chemin_views + '.backup_complete')
        print("✅ Ancienne vue sauvegardée")
    
    # Créer la nouvelle vue complète
    with open(chemin_views, 'w') as f:
        f.write(code_vues_complete)
    
    print("✅ Vues complètes créées!")
    return True

if __name__ == "__main__":
    completer_vues_assureur()