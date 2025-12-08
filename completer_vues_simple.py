#!/usr/bin/env python
"""
VUES SIMPLIFIÉES POUR ASSUREUR
"""

import os

def creer_vues_simplifiees():
    """Crée des vues simplifiées pour les tests"""
    
    code_vues_simple = '''"""
VUES SIMPLIFIÉES POUR ASSUREUR - Version test
"""

from django.http import JsonResponse
from django.utils import timezone
from membres.models import Membre, Bon
from django.contrib.auth.decorators import login_required
import json

@login_required
def dashboard(request):
    """Tableau de bord simple"""
    return JsonResponse({
        'success': True,
        'message': 'Dashboard assureur - OK',
        'stats': {
            'membres': Membre.objects.count(),
            'bons': Bon.objects.count()
        }
    })

@login_required
def creer_bon(request, membre_id):
    """Création de bon - version simplifiée"""
    try:
        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Récupérer les données
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST.dict()
            
            # Trouver le membre
            membre = Membre.objects.get(numero_unique=membre_id)
            
            # Créer le bon
            bon = Bon.objects.create(
                numero_bon=f"BON_{membre_id}_{timezone.now().strftime('%H%M%S')}",
                membre=membre,
                type_soin=data.get('type_soin', 'Consultation'),
                montant_total=float(data.get('montant_total', 0)),
                statut='en_attente'
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Bon créé avec succès',
                'bon_id': bon.id,
                'numero_bon': bon.numero_bon
            })
            
        return JsonResponse({
            'success': False,
            'message': 'Méthode non autorisée'
        }, status=405)
        
    except Membre.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Membre non trouvé'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erreur: {str(e)}'
        }, status=500)

@login_required
def liste_bons(request):
    """Liste des bons simplifiée"""
    return JsonResponse({
        'success': True,
        'message': 'Liste des bons',
        'count': Bon.objects.count()
    })

@login_required
def recherche_membre(request):
    """Recherche simplifiée"""
    return JsonResponse({
        'success': True,
        'message': 'Recherche membres',
        'count': Membre.objects.count()
    })
'''

    chemin_views = os.path.join(os.path.dirname(__file__), 'assureur', 'views.py')
    
    # Sauvegarder l'ancienne version
    if os.path.exists(chemin_views):
        os.rename(chemin_views, chemin_views + '.backup_simple')
        print("✅ Ancienne vue sauvegardée")
    
    # Créer la nouvelle vue simplifiée
    with open(chemin_views, 'w') as f:
        f.write(code_vues_simple)
    
    print("✅ Vues simplifiées créées!")
    return True

if __name__ == "__main__":
    creer_vues_simplifiees()        