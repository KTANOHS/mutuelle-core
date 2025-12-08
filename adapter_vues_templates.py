#!/usr/bin/env python
"""
ADAPTATION DES VUES POUR UTILISER LES TEMPLATES EXISTANTS - VERSION CORRIGÉE
"""

import os

def adapter_vues_templates():
    """Adapte les vues pour utiliser les templates HTML existants"""
    
    # Trouver le bon chemin
    current_dir = os.path.dirname(os.path.abspath(__file__))
    chemin_views = os.path.join(current_dir, 'assureur', 'views.py')
    
    print(f"📁 Chemin views.py: {chemin_views}")
    
    if not os.path.exists(chemin_views):
        print("❌ Fichier views.py non trouvé")
        print("🔍 Recherche dans le projet...")
        
        # Chercher le fichier
        for root, dirs, files in os.walk(current_dir):
            if 'views.py' in files and 'assureur' in root:
                chemin_views = os.path.join(root, 'views.py')
                print(f"✅ Views.py trouvé: {chemin_views}")
                break
        else:
            print("❌ Impossible de trouver views.py")
            return False
    
    code_vues_avec_templates = '''"""
VUES ASSUREUR - Version avec templates HTML
"""

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db import IntegrityError
from membres.models import Membre, Bon
from django.contrib.auth.decorators import login_required
import json
import random

@login_required
def dashboard(request):
    """
    Tableau de bord de l'assureur - Version HTML
    """
    # Statistiques pour le template
    stats = {
        'membres_total': Membre.objects.count(),
        'bons_total': Bon.objects.count(),
        'bons_en_attente': Bon.objects.filter(statut='en_attente').count(),
        'bons_valides': Bon.objects.filter(statut='valide').count(),
        'bons_refuses': Bon.objects.filter(statut='refuse').count(),
    }
    
    # Derniers bons créés
    derniers_bons = Bon.objects.select_related('membre').order_by('-date_creation')[:5]
    
    context = {
        'stats': stats,
        'derniers_bons': derniers_bons,
        'page_title': 'Tableau de bord Assureur'
    }
    
    return render(request, 'assureur/dashboard.html', context)

@login_required  
def creer_bon(request, membre_id):
    """
    Création de bon - Support HTML et AJAX
    """
    # Récupérer le membre
    membre = get_object_or_404(Membre, numero_unique=membre_id)
    
    # Méthode GET : Afficher le formulaire
    if request.method == 'GET':
        context = {
            'membre': membre,
            'types_soin': [
                'Consultation générale',
                'Pharmacie',
                'Analyse médicale', 
                'Hospitalisation',
                'Radiologie',
                'Soins dentaires',
                'Optique',
                'Soins spécialisés'
            ],
            'page_title': f'Créer un bon pour {membre.nom} {membre.prenom}'
        }
        return render(request, 'assureur/creer_bon.html', context)
    
    # Méthode POST : Créer le bon
    elif request.method == 'POST':
        try:
            # Récupérer les données
            if request.content_type == 'application/json':
                try:
                    data = json.loads(request.body)
                except json.JSONDecodeError:
                    data = {}
            else:
                data = request.POST.dict()
            
            # Validation des données
            type_soin = data.get('type_soin', '').strip()
            if not type_soin:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'Le type de soin est requis'
                    }, status=400)
                else:
                    # Rediriger vers le formulaire avec erreur
                    context = {
                        'membre': membre,
                        'types_soin': ['Consultation générale', 'Pharmacie', 'Analyse médicale', 'Hospitalisation', 'Radiologie'],
                        'error': 'Le type de soin est requis',
                        'form_data': data
                    }
                    return render(request, 'assureur/creer_bon.html', context)
            
            # Convertir le montant
            try:
                montant_total = float(data.get('montant_total', 0))
            except (ValueError, TypeError):
                montant_total = 0
            
            # Génération de numéro de bon unique
            max_attempts = 5
            for attempt in range(max_attempts):
                timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
                random_suffix = f"_{random.randint(1000, 9999)}" if attempt > 0 else ""
                numero_bon = f"BON_{membre_id}_{timestamp}{random_suffix}"
                
                if not Bon.objects.filter(numero_bon=numero_bon).exists():
                    break
            else:
                error_msg = 'Impossible de générer un numéro de bon unique'
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': error_msg}, status=500)
                else:
                    context = {'membre': membre, 'error': error_msg, 'form_data': data}
                    return render(request, 'assureur/creer_bon.html', context)
            
            # Préparer les données du bon
            bon_data = {
                'numero_bon': numero_bon,
                'membre': membre,
                'type_soin': type_soin,
                'montant_total': montant_total,
                'statut': 'en_attente'
            }
            
            # Champs optionnels
            optional_fields = [
                'description', 'lieu_soins', 'medecin_traitant', 
                'numero_ordonnance', 'taux_remboursement', 'diagnostic'
            ]
            
            for field in optional_fields:
                if field in data:
                    if field == 'taux_remboursement':
                        try:
                            bon_data[field] = float(data[field])
                        except (ValueError, TypeError):
                            bon_data[field] = 70.0
                    else:
                        bon_data[field] = data[field]
            
            # Valeurs par défaut
            if 'taux_remboursement' not in bon_data:
                bon_data['taux_remboursement'] = 70.0
            if 'lieu_soins' not in bon_data:
                bon_data['lieu_soins'] = 'Centre Médical'
            
            # Créer le bon
            try:
                bon = Bon.objects.create(**bon_data)
            except IntegrityError as e:
                if 'numero_bon' in str(e):
                    # Réessayer avec un autre numéro
                    numero_bon = f"BON_{membre_id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(10000, 99999)}"
                    bon_data['numero_bon'] = numero_bon
                    bon = Bon.objects.create(**bon_data)
                else:
                    raise e
            
            # Réponse selon le type de requête
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Bon créé avec succès',
                    'bon_id': bon.id,
                    'numero_bon': bon.numero_bon,
                    'membre': f"{membre.nom} {membre.prenom}",
                    'type_soin': bon.type_soin,
                    'montant_total': float(bon.montant_total),
                    'statut': bon.statut
                })
            else:
                # Redirection vers la liste des bons ou confirmation
                context = {
                    'success': True,
                    'bon': bon,
                    'membre': membre,
                    'message': f'Bon {bon.numero_bon} créé avec succès pour {membre.nom} {membre.prenom}'
                }
                return render(request, 'assureur/creer_bon.html', context)
                
        except Exception as e:
            print(f"❌ Erreur création bon: {e}")
            error_msg = f'Erreur serveur: {str(e)}'
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': error_msg}, status=500)
            else:
                context = {'membre': membre, 'error': error_msg, 'form_data': data}
                return render(request, 'assureur/creer_bon.html', context)
    
    else:
        return JsonResponse({
            'success': False,
            'message': 'Méthode non autorisée'
        }, status=405)

@login_required
def liste_bons(request):
    """
    Liste des bons - Version HTML
    """
    # Filtres
    statut_filter = request.GET.get('statut', '')
    type_soin_filter = request.GET.get('type_soin', '')
    search_query = request.GET.get('q', '')
    
    bons = Bon.objects.select_related('membre').order_by('-date_creation')
    
    # Appliquer les filtres
    if statut_filter:
        bons = bons.filter(statut=statut_filter)
    if type_soin_filter:
        bons = bons.filter(type_soin__icontains=type_soin_filter)
    if search_query:
        bons = bons.filter(
            numero_bon__icontains=search_query
        ) | bons.filter(
            membre__nom__icontains=search_query
        ) | bons.filter(
            membre__prenom__icontains=search_query
        )
    
    # Pagination simple
    page = int(request.GET.get('page', 1))
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    
    total_bons = bons.count()
    bons_page = bons[start:end]
    
    context = {
        'bons': bons_page,
        'total_bons': total_bons,
        'page': page,
        'per_page': per_page,
        'has_previous': page > 1,
        'has_next': end < total_bons,
        'statut_filter': statut_filter,
        'type_soin_filter': type_soin_filter,
        'search_query': search_query,
        'statuts_choices': ['en_attente', 'valide', 'refuse', 'utilise'],
        'page_title': 'Liste des Bons'
    }
    
    return render(request, 'assureur/liste_bons.html', context)

@login_required
def recherche_membre(request):
    """
    Recherche de membres - Version HTML
    """
    query = request.GET.get('q', '')
    membres = Membre.objects.all()
    
    if query:
        membres = membres.filter(
            nom__icontains=query
        ) | membres.filter(
            prenom__icontains=query
        ) | membres.filter(
            numero_unique__icontains=query
        ) | membres.filter(
            email__icontains=query
        )
    
    membres = membres.order_by('nom', 'prenom')
    
    context = {
        'membres': membres,
        'query': query,
        'total_trouves': membres.count(),
        'page_title': 'Recherche de Membres'
    }
    
    return render(request, 'assureur/recherche_membre.html', context)
'''

    # Sauvegarder l'ancienne version
    if os.path.exists(chemin_views):
        backup_path = chemin_views + '.backup_template'
        os.rename(chemin_views, backup_path)
        print(f"✅ Ancienne vue sauvegardée: {backup_path}")
    
    # Créer la nouvelle vue avec templates
    with open(chemin_views, 'w') as f:
        f.write(code_vues_avec_templates)
    
    print("✅ Vues adaptées pour utiliser les templates HTML!")
    print("\n🎯 URLs à tester:")
    print("   http://127.0.0.1:8000/assureur/")
    print("   http://127.0.0.1:8000/assureur/bons/")
    print("   http://127.0.0.1:8000/assureur/recherche/")
    print("   http://127.0.0.1:8000/assureur/bons/creer/MEM001/")
    
    return True

if __name__ == "__main__":
    adapter_vues_templates()