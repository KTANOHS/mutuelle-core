# Dans assureur/utils.py ou en haut de views.py
from datetime import datetime

def normaliser_periode(periode_input):
    """
    Normalise la période au format 'YYYY-MM'
    Accepte: '2025-12', '01/12/2025', '12/2025', '12-2025'
    """
    if not periode_input:
        return datetime.now().strftime('%Y-%m')
    
    # Format YYYY-MM (input month)
    if '-' in periode_input and len(periode_input) == 7:
        try:
            # Valider que c'est une date valide
            datetime.strptime(periode_input, '%Y-%m')
            return periode_input
        except:
            pass
    
    # Format dd/mm/yyyy
    if '/' in periode_input:
        try:
            if len(periode_input.split('/')) == 3:
                date_obj = datetime.strptime(periode_input, '%d/%m/%Y')
                return date_obj.strftime('%Y-%m')
            elif len(periode_input.split('/')) == 2:
                # mm/yyyy
                date_obj = datetime.strptime(periode_input, '%m/%Y')
                return date_obj.strftime('%Y-%m')
        except:
            pass
    
    # Format mm-yyyy
    if '-' in periode_input and len(periode_input.split('-')) == 2:
        try:
            date_obj = datetime.strptime(periode_input, '%m-%Y')
            return date_obj.strftime('%Y-%m')
        except:
            pass
    
    # Si aucun format ne correspond, retourner le mois courant
    return datetime.now().strftime('%Y-%m')

# assureur/utils.py
from django.contrib.auth.decorators import user_passes_test
from .models import Assureur

def get_assureur_from_request(request):
    """Récupérer l'assureur associé à l'utilisateur connecté"""
    try:
        if hasattr(request.user, 'assureur'):
            return request.user.assureur
        elif hasattr(request.user, 'profile') and hasattr(request.user.profile, 'assureur'):
            return request.user.profile.assureur
        else:
            # Chercher l'assureur par relation
            assureur = Assureur.objects.filter(user=request.user).first()
            if assureur:
                return assureur
    except Exception:
        pass
    return None

def assureur_test(user):
    """Test pour le décorateur @assureur_required"""
    return get_assureur_from_request(user) is not None

assureur_required = user_passes_test(assureur_test, login_url='/login/')