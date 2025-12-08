
# =============================================================================
# VUE API SIMPLE POUR LES MESSAGES
# =============================================================================

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
import json

@require_GET
@login_required
def api_conversation_messages_simple(request, conversation_id):
    """API simple pour récupérer les messages d'une conversation"""
    try:
        from communication.models import Conversation, Message
        
        # Récupérer la conversation (vérifier que l'utilisateur est participant)
        conversation = get_object_or_404(
            Conversation.objects.filter(participants=request.user),
            id=conversation_id
        )
        
        # Récupérer les messages
        messages = Message.objects.filter(
            conversation=conversation
        ).select_related('expediteur', 'destinataire').order_by('date_envoi')
        
        # Construire la réponse JSON
        data = []
        for msg in messages:
            data.append({
                'id': msg.id,
                'titre': msg.titre,
                'contenu': msg.contenu,
                'expediteur': {
                    'id': msg.expediteur.id,
                    'username': msg.expediteur.username,
                    'email': msg.expediteur.email,
                },
                'destinataire': {
                    'id': msg.destinataire.id,
                    'username': msg.destinataire.username,
                    'email': msg.destinataire.email,
                },
                'date_envoi': msg.date_envoi.isoformat() if msg.date_envoi else None,
                'est_lu': msg.est_lu,
                'type_message': msg.type_message,
            })
        
        return JsonResponse({
            'success': True,
            'conversation_id': conversation_id,
            'total_messages': len(data),
            'messages': data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'conversation_id': conversation_id
        }, status=500)

@csrf_exempt
@require_POST
def api_send_message(request):
    """API pour envoyer un message (sans authentification pour test)"""
    try:
        from communication.models import Conversation, Message
        from django.contrib.auth.models import User
        
        # Parser les données JSON
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({
                'success': False,
                'error': 'Données JSON invalides'
            }, status=400)
        
        # Récupérer les paramètres
        expediteur_id = data.get('expediteur_id')
        destinataire_id = data.get('destinataire_id')
        contenu = data.get('contenu', '').strip()
        titre = data.get('titre', 'Message via API')
        
        # Validation
        if not all([expediteur_id, destinataire_id, contenu]):
            return JsonResponse({
                'success': False,
                'error': 'Paramètres manquants: expediteur_id, destinataire_id et contenu sont requis'
            }, status=400)
        
        # Récupérer les utilisateurs
        expediteur = User.objects.get(id=expediteur_id)
        destinataire = User.objects.get(id=destinataire_id)
        
        # Trouver ou créer la conversation
        conversation = Conversation.objects.filter(
            participants=expediteur
        ).filter(
            participants=destinataire
        ).first()
        
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(expediteur, destinataire)
        
        # Créer le message
        message = Message.objects.create(
            expediteur=expediteur,
            destinataire=destinataire,
            conversation=conversation,
            titre=titre,
            contenu=contenu,
            type_message=data.get('type_message', 'NORMAL')
        )
        
        return JsonResponse({
            'success': True,
            'message_id': message.id,
            'conversation_id': conversation.id,
            'created_at': message.date_envoi.isoformat() if message.date_envoi else None
        })
        
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Utilisateur non trouvé'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

# =============================================================================
# VUE API PUBLIQUE (sans authentification)
# =============================================================================

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404
import json

@csrf_exempt
@require_GET
def api_public_conversation_messages(request, conversation_id):
    """API publique pour récupérer les messages d'une conversation - sans authentification"""
    try:
        from communication.models import Conversation, Message
        
        # Récupérer la conversation
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        # Récupérer les messages
        messages = Message.objects.filter(
            conversation=conversation
        ).select_related('expediteur', 'destinataire').order_by('id')
        
        # Formater les données
        data = []
        for msg in messages:
            data.append({
                'id': msg.id,
                'titre': msg.titre,
                'contenu': msg.contenu,
                'expediteur': {
                    'id': msg.expediteur.id,
                    'username': msg.expediteur.username,
                    'email': msg.expediteur.email,
                } if msg.expediteur else None,
                'destinataire': {
                    'id': msg.destinataire.id,
                    'username': msg.destinataire.username,
                    'email': msg.destinataire.email,
                } if msg.destinataire else None,
                'date_envoi': msg.date_envoi.isoformat() if msg.date_envoi else None,
                'est_lu': msg.est_lu,
                'type_message': msg.type_message,
            })
        
        return JsonResponse({
            'success': True,
            'conversation_id': conversation_id,
            'total_messages': len(data),
            'messages': data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'conversation_id': conversation_id
        }, status=500)

@csrf_exempt
@require_GET
def api_public_test(request):
    """Endpoint de test public"""
    return JsonResponse({
        'status': 'API publique fonctionnelle',
        'timestamp': 'test',
        'instructions': 'Utilisez /api/public/conversations/5/messages/ pour les messages'
    })

# =============================================================================
# VUE API PUBLIQUE (sans authentification)
# =============================================================================

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404
import json

@csrf_exempt
@require_GET
def api_public_conversation_messages(request, conversation_id):
    """API publique pour récupérer les messages d'une conversation - sans authentification"""
    try:
        from communication.models import Conversation, Message
        
        # Récupérer la conversation
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        # Récupérer les messages
        messages = Message.objects.filter(
            conversation=conversation
        ).select_related('expediteur', 'destinataire').order_by('id')
        
        # Formater les données
        data = []
        for msg in messages:
            data.append({
                'id': msg.id,
                'titre': msg.titre,
                'contenu': msg.contenu,
                'expediteur': {
                    'id': msg.expediteur.id,
                    'username': msg.expediteur.username,
                    'email': msg.expediteur.email,
                } if msg.expediteur else None,
                'destinataire': {
                    'id': msg.destinataire.id,
                    'username': msg.destinataire.username,
                    'email': msg.destinataire.email,
                } if msg.destinataire else None,
                'date_envoi': msg.date_envoi.isoformat() if msg.date_envoi else None,
                'est_lu': msg.est_lu,
                'type_message': msg.type_message,
            })
        
        return JsonResponse({
            'success': True,
            'conversation_id': conversation_id,
            'total_messages': len(data),
            'messages': data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'conversation_id': conversation_id
        }, status=500)

@csrf_exempt
@require_GET
def api_public_test(request):
    """Endpoint de test public"""
    return JsonResponse({
        'status': 'API publique fonctionnelle',
        'timestamp': 'test',
        'instructions': 'Utilisez /api/public/conversations/5/messages/ pour les messages'
    })
