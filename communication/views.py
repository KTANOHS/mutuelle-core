# communication/views.py - VERSION COMPLÈTEMENT CORRIGÉE ET OPTIMISÉE

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse, HttpResponse
from django.db.models import Q, Count, Max
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
import json
import os
import logging
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Message, PieceJointe, Notification, Conversation, MessageGroupe, GroupeCommunication
from .forms import MessageForm, MessageGroupeForm, UploadFileForm, GroupeCommunicationForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST  # CORRECTION: Import depuis django.views.decorators.http

# Configurer le logger
logger = logging.getLogger(__name__)

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def get_derniere_activite(user):
    """Récupère la date de la dernière activité de messagerie"""
    try:
        dernier_message_recu = Message.objects.filter(
            destinataire=user
        ).aggregate(Max('date_envoi'))['date_envoi__max']
        
        dernier_message_envoye = Message.objects.filter(
            expediteur=user
        ).aggregate(Max('date_envoi'))['date_envoi__max']
        
        dates = [d for d in [dernier_message_recu, dernier_message_envoye] if d is not None]
        return max(dates) if dates else None
    except Exception as e:
        logger.error(f"Erreur get_derniere_activite: {e}")
        return None

# =============================================================================
# VUE D'ACCUEIL DE LA COMMUNICATION
# =============================================================================

@login_required
def communication_home(request):
    """Page d'accueil de la communication - redirection vers la messagerie"""
    return redirect('messagerie')  # CORRECTION: Ajout de cette fonction manquante

# =============================================================================
# VUE PRINCIPALE DE MESSAGERIE - CORRIGÉE
# =============================================================================

@login_required
def messagerie(request):
    """Page principale de messagerie - VERSION COMPLÈTEMENT CORRIGÉE"""
    try:
        from django.db.models import Count, Q, Max
        from django.contrib.auth.models import User
        
        # Initialiser les variables par défaut
        conversations = []
        messages_recents = []
        all_users = User.objects.exclude(id=request.user.id).order_by('username')
        participants = []
        active_conversation = None
        active_messages = None
        active_conversation_participant_name = "Sélectionnez une conversation"
        
        try:
            # Récupérer les conversations avec annotations
            conversations = Conversation.objects.filter(
                participants=request.user
            ).annotate(
                nb_messages_non_lus=Count('messages', filter=Q(messages__est_lu=False) & ~Q(messages__expediteur=request.user)),
                derniere_activite=Max('messages__date_envoi'),
                total_messages=Count('messages')
            ).order_by('-derniere_activite')
            
            # Récupérer les messages récents
            messages_recents = Message.objects.filter(
                Q(expediteur=request.user) | Q(destinataire=request.user)
            ).select_related('expediteur', 'destinataire').order_by('-date_envoi')[:10]
            
            # Créer la liste des participants
            participants_ids = set()
            for conv in conversations:
                for user in conv.participants.all():
                    if user.id != request.user.id:
                        participants_ids.add(user.id)
            
            for msg in messages_recents:
                if msg.expediteur.id != request.user.id:
                    participants_ids.add(msg.expediteur.id)
                if msg.destinataire and msg.destinataire.id != request.user.id:
                    participants_ids.add(msg.destinataire.id)
            
            participants = User.objects.filter(id__in=participants_ids).order_by('username') if participants_ids else []
            
            # Déterminer la conversation active
            if conversations.exists():
                active_conversation = conversations.first()
                active_messages = active_conversation.messages.all().order_by('date_envoi')
                
                # Récupérer le nom du participant de la conversation active
                other_participants = active_conversation.participants.exclude(id=request.user.id)
                if other_participants.exists():
                    other_participant = other_participants.first()
                    active_conversation_participant_name = other_participant.get_full_name() or other_participant.username
        
        except (Conversation.DoesNotExist, Message.DoesNotExist):
            # Si les modèles n'existent pas, utiliser des listes vides
            pass
        
        # Compter les messages non lus
        messages_non_lus = 0
        try:
            messages_non_lus = Message.objects.filter(
                destinataire=request.user,
                est_lu=False
            ).count()
        except:
            pass
        
        context = {
            'conversations': conversations,
            'messages_recents': messages_recents,
            'all_users': all_users,
            'participants': participants,
            'active_conversation': active_conversation,
            'active_messages': active_messages,
            'active_conversation_participant_name': active_conversation_participant_name,
            'form': MessageForm(),
            'page_title': 'Messagerie',
            'total_conversations': len(conversations),
            'total_messages': len(messages_recents),
            'messages_non_lus': messages_non_lus,
            'unread_messages_count': messages_non_lus,
        }
        
        return render(request, 'communication/messagerie.html', context)
        
    except Exception as e:
        from django.contrib.auth.models import User
        
        context = {
            'conversations': [],
            'messages_recents': [],
            'all_users': User.objects.exclude(id=request.user.id).order_by('username'),
            'participants': [],
            'active_conversation': None,
            'active_messages': None,
            'active_conversation_participant_name': "Sélectionnez une conversation",
            'form': MessageForm(),
            'error': str(e),
            'page_title': 'Messagerie',
            'total_conversations': 0,
            'total_messages': 0,
            'messages_non_lus': 0,
            'unread_messages_count': 0,
        }
        return render(request, 'communication/messagerie.html', context)
# =============================================================================
# API ENVOYER MESSAGE - VERSION CORRIGÉE (ACCEPTE JSON ET FORM-DATA)
# =============================================================================

@csrf_exempt
@require_POST
@login_required
def envoyer_message_api(request):
    """Envoyer un nouveau message - Version corrigée (JSON & Form-Data)"""
    logger.debug("=== API DEBUG ===")
    logger.debug(f"User: {request.user}")
    logger.debug(f"Method: {request.method}")
    logger.debug(f"Content-Type: {request.content_type}")
    
    # Initialisation
    post_data = {}
    files = request.FILES
    
    # Traitement selon le Content-Type
    if request.content_type == 'application/json':
        try:
            # Traitement JSON
            raw_data = request.body.decode('utf-8')
            logger.debug(f"Raw JSON: {raw_data}")
            json_data = json.loads(raw_data)
            logger.debug(f"Parsed JSON: {json_data}")
            
            # Conversion en format formulaire
            post_data = {
                'destinataire': json_data.get('destinataire_id') or json_data.get('destinataire'),
                'contenu': json_data.get('contenu') or json_data.get('message') or '',
                'titre': json_data.get('titre') or 'Message via API',
                'type_message': json_data.get('type_message', 'MESSAGE')
            }
            
            # Nettoyage
            post_data = {k: v for k, v in post_data.items() if v is not None}
            
        except json.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}")
            return JsonResponse({
                'success': False, 
                'error': f'JSON invalide: {str(e)}'
            }, status=400)
        except Exception as e:
            logger.error(f"Erreur traitement JSON: {e}")
            return JsonResponse({
                'success': False, 
                'error': f'Erreur traitement: {str(e)}'
            }, status=400)
    else:
        # Traitement Form-Data standard
        post_data = request.POST.dict()
        files = request.FILES
    
    logger.debug(f"Post data: {post_data}")
    logger.debug(f"Files: {files}")
    
    # Validation des données obligatoires
    if not post_data.get('destinataire'):
        return JsonResponse({
            'success': False, 
            'error': 'destinataire/destinataire_id est requis'
        }, status=400)
    
    if not post_data.get('contenu'):
        return JsonResponse({
            'success': False, 
            'error': 'contenu/message est requis'
        }, status=400)
    
    try:
        # Création du formulaire
        form = MessageForm(post_data, files)
        
        if not form.is_valid():
            errors = {}
            for field, field_errors in form.errors.items():
                errors[field] = [str(error) for error in field_errors]
            
            logger.error(f"Form errors: {errors}")
            return JsonResponse({
                'success': False, 
                'errors': errors,
                'debug_info': {
                    'content_type': request.content_type,
                    'user': str(request.user),
                    'has_files': bool(files)
                }
            }, status=400)
        
        # Sauvegarde du message
        message = form.save(commit=False)
        message.expediteur = request.user
        
        # Validation du destinataire
        destinataire = form.cleaned_data['destinataire']
        
        # Empêcher l'auto-message
        if destinataire == request.user:
            return JsonResponse({
                'success': False, 
                'error': 'Vous ne pouvez pas vous envoyer un message à vous-même'
            }, status=400)
        
        # Gestion de la conversation
        conversation = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=destinataire
        ).distinct().first()
        
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, destinataire)
        
        message.conversation = conversation
        message.save()
        
        # Gestion des pièces jointes
        if 'pieces_jointes' in files:
            for fichier in files.getlist('pieces_jointes'):
                PieceJointe.objects.create(
                    message=message,
                    fichier=fichier,
                    nom_original=fichier.name,
                    taille=fichier.size
                )
        
        # Mise à jour de la conversation
        conversation.date_modification = timezone.now()
        conversation.save()
        
        # Notification au destinataire
        Notification.objects.create(
            user=destinataire,
            titre=f"Nouveau message de {request.user.get_full_name() or request.user.username}",
            message=message.titre or message.contenu[:100],
            type_notification='MESSAGE'
        )
        
        # Préparation de la réponse
        response_data = {
            'success': True, 
            'message_id': message.id,
            'conversation_id': conversation.id,
            'message': 'Message envoyé avec succès',
            'destinataire': {
                'id': destinataire.id,
                'username': destinataire.username,
                'full_name': destinataire.get_full_name()
            },
            'date': timezone.now().isoformat(),
            'timestamp': int(timezone.now().timestamp())
        }
        
        # Ajout de la date de création si disponible
        if hasattr(message, 'date'):
            response_data['date_creation'] = message.date.isoformat()
        elif hasattr(message, 'date_envoi'):
            response_data['date_creation'] = message.date_envoi.isoformat()
        elif hasattr(message, 'created_at'):
            response_data['date_creation'] = message.created_at.isoformat()
        
        logger.debug(f"API success: {response_data}")
        return JsonResponse(response_data)
        
    except Exception as e:
        logger.error(f"Erreur serveur envoyer_message_api: {e}", exc_info=True)
        return JsonResponse({
            'success': False, 
            'error': f'Erreur serveur: {str(e)}',
            'debug_info': {
                'content_type': request.content_type,
                'user': str(request.user)
            }
        }, status=500)

# =============================================================================
# SCRIPT DE TEST API SIMPLIFIÉ
# =============================================================================

def create_test_api_script():
    """Crée un script de test API simple"""
    test_script = '''#!/usr/bin/env python3
# test_api_simple.py - Test simplifié de l'API
import requests
import json
import sys

def test_api():
    base_url = "http://127.0.0.1:8000"
    
    # Test 1: JSON
    print("\\n🔍 Test 1: Envoi JSON")
    url = f"{base_url}/communication/envoyer-message-api/"
    data = {
        "destinataire_id": 1,
        "contenu": "Test message via JSON API",
        "titre": "Test API"
    }
    
    try:
        response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Succès: {response.json()}")
        else:
            print(f"   ❌ Erreur: {response.text[:200]}")
    except Exception as e:
        print(f"   💥 Exception: {str(e)}")
    
    # Test 2: Form-Data
    print("\\n🔍 Test 2: Envoi Form-Data")
    data_form = {
        "destinataire": 1,
        "contenu": "Test message via Form-Data",
        "titre": "Test Form"
    }
    
    try:
        response = requests.post(url, data=data_form)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Succès: {response.json()}")
        else:
            print(f"   ❌ Erreur: {response.text[:200]}")
    except Exception as e:
        print(f"   💥 Exception: {str(e)}")

if __name__ == "__main__":
    test_api()
'''
    
    with open('test_api_simple.py', 'w') as f:
        f.write(test_script)
    
    print("✅ Script de test créé: test_api_simple.py")
    print("   Pour l'exécuter: python test_api_simple.py")

# =============================================================================
# AUTRES VUES IMPORTANTES (CORRIGÉES)
# =============================================================================

@login_required
def conversations(request):
    """Liste des conversations - OPTIMISÉE"""
    try:
        conversations_list = Conversation.objects.filter(participants=request.user).annotate(
            nb_messages=Count('messages'),
            messages_non_lus=Count('messages', filter=Q(messages__est_lu=False) & ~Q(messages__expediteur=request.user))
        ).order_by('-date_modification')
        
        context = {
            'conversations': conversations_list,
            'page_title': 'Conversations',
            'total_conversations': conversations_list.count()
        }
        return render(request, 'communication/conversations.html', context)
        
    except Exception as e:
        logger.error(f"Erreur conversations: {e}")
        context = {
            'conversations': [],
            'page_title': 'Conversations',
            'error': f"Aucune conversation trouvée : {str(e)}",
            'total_conversations': 0
        }
        return render(request, 'communication/conversations.html', context)

@login_required
def liste_messages(request):
    """Vue pour lister les messages - OPTIMISÉE"""
    try:
        messages_recus = Message.objects.filter(destinataire=request.user).select_related('expediteur').order_by('-date_envoi')
        messages_envoyes = Message.objects.filter(expediteur=request.user).select_related('destinataire').order_by('-date_envoi')
        
        # Marquer les messages comme lus
        messages_recus.filter(est_lu=False).update(est_lu=True, date_lecture=timezone.now())
        
        return render(request, 'communication/liste_messages.html', {
            'messages_recus': messages_recus,
            'messages_envoyes': messages_envoyes,
            'page_title': 'Mes Messages'
        })
    except Exception as e:
        logger.error(f"Erreur liste_messages: {e}")
        context = {
            'messages_recus': [],
            'messages_envoyes': [],
            'page_title': 'Mes Messages',
            'error': str(e)
        }
        return render(request, 'communication/liste_messages.html', context)

@login_required
def envoyer_message(request):
    """Vue pour envoyer un message - OPTIMISÉE"""
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                message = form.save(commit=False)
                message.expediteur = request.user
                
                # Gestion de la conversation
                destinataire = form.cleaned_data['destinataire']
                conversation = Conversation.objects.filter(
                    participants=request.user
                ).filter(
                    participants=destinataire
                ).first()
                
                if not conversation:
                    conversation = Conversation.objects.create()
                    conversation.participants.add(request.user, destinataire)
                
                message.conversation = conversation
                message.save()
                
                # Gestion des pièces jointes
                fichiers = request.FILES.getlist('pieces_jointes')
                for fichier in fichiers:
                    PieceJointe.objects.create(
                        message=message,
                        fichier=fichier,
                        nom_original=fichier.name,
                        taille=fichier.size
                    )
                
                messages.success(request, "Message envoyé avec succès!")
                return redirect('communication:liste_messages')
                
            except Exception as e:
                logger.error(f"Erreur envoi message: {e}")
                messages.error(request, f"Erreur lors de l'envoi: {str(e)}")
    else:
        form = MessageForm()
    
    return render(request, 'communication/envoyer_message.html', {
        'form': form,
        'page_title': 'Envoyer un message'
    })

# =============================================================================
# VUES MESSAGERIE MULTI-ACTEURS (SIMPLIFIÉES)
# =============================================================================

@login_required
def messagerie_pharmacien(request):
    """Vue messagerie spécifique pour les pharmaciens - OPTIMISÉE"""
    try:
        conversations_list = Conversation.objects.filter(participants=request.user).annotate(
            nb_messages_non_lus=Count('messages', filter=Q(messages__est_lu=False) & ~Q(messages__expediteur=request.user)),
            derniere_activite=Max('messages__date_envoi'),
            total_messages=Count('messages')
        ).order_by('-derniere_activite')
        
        from datetime import timedelta
        derniers_7_jours = timezone.now() - timedelta(days=7)
        
        messages_recents = Message.objects.filter(
            Q(expediteur=request.user) | Q(destinataire=request.user),
            date_envoi__gte=derniers_7_jours
        ).select_related('expediteur', 'destinataire').order_by('-date_envoi')[:15]
        
        messages_urgents = Message.objects.filter(
            destinataire=request.user,
            type_message__in=['URGENT', 'ORDONNANCE', 'PHARMACIE'],
            est_lu=False
        ).order_by('-date_envoi')
        
        context = {
            'conversations': conversations_list,
            'messages_recents': messages_recents,
            'messages_urgents': messages_urgents,
            'form': MessageForm(),
            'page_title': 'Messagerie Pharmacien',
            'total_conversations': conversations_list.count(),
            'user_type': 'pharmacien'
        }
        
        return render(request, 'communication/messagerie_pharmacien.html', context)
        
    except Exception as e:
        logger.error(f"Erreur messagerie_pharmacien: {e}")
        context = {
            'conversations': [],
            'messages_recents': [],
            'messages_urgents': [],
            'form': MessageForm(),
            'error': str(e),
            'page_title': 'Messagerie Pharmacien',
            'user_type': 'pharmacien'
        }
        return render(request, 'communication/messagerie_pharmacien.html', context)

# =============================================================================
# EXÉCUTION DES CORRECTIONS
# =============================================================================

# Créer le script de test
create_test_api_script()

print("""
🎯 CORRECTIONS APPLIQUÉES :

✅ API envoyer_message_api corrigée pour accepter :
   - JSON (Content-Type: application/json)
   - Form-Data (Content-Type: multipart/form-data)

✅ Logging amélioré pour le débogage
✅ Gestion d'erreurs robuste
✅ Validation des données améliorée
✅ Script de test automatique créé

📋 POUR TESTER :

1. Redémarrez le serveur :
   python manage.py runserver

2. Testez l'API avec :
   python test_api_simple.py

🔧 EN CAS D'ERREUR 400 :
   - Vérifiez que le destinataire existe (ID valide)
   - Vérifiez que le contenu n'est pas vide
   - Vérifiez les logs Django pour plus de détails
""")

# =============================================================================
# GARDEZ LE RESTE DU CODE EXISTANT (SANS MODIFICATION)
# =============================================================================

@login_required
def detail_conversation(request, conversation_id):
    """Détail d'une conversation - CORRIGÉE"""
    try:
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        messages_conversation = conversation.messages.all().order_by('date_envoi')
        
        # Marquer les messages comme lus
        messages_non_lus = messages_conversation.filter(est_lu=False, destinataire=request.user)
        for message in messages_non_lus:
            message.marquer_comme_lu()
        
        return render(request, 'communication/detail_conversation.html', {
            'conversation': conversation,
            'messages': messages_conversation
        })
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement de la conversation: {str(e)}")
        return redirect('communication:conversations')

@login_required
def detail_message(request, message_id):
    """Vue pour afficher le détail d'un message - CORRIGÉE"""
    try:
        message = get_object_or_404(
            Message.objects.select_related('expediteur', 'destinataire', 'conversation'),
            id=message_id
        )
        
        # Vérifier que l'utilisateur a le droit de voir ce message
        if message.expediteur != request.user and message.destinataire != request.user:
            messages.error(request, "Vous n'avez pas accès à ce message.")
            # CORRECTION : Redirection vers la bonne URL
            return redirect('communication:liste_messages')
        
        # Marquer comme lu si l'utilisateur est le destinataire
        if message.destinataire == request.user and not message.est_lu:
            message.marquer_comme_lu()
        
        return render(request, 'communication/detail_message.html', {
            'message': message,
            'page_title': f'Message: {message.titre}'
        })
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement du message: {str(e)}")
        # CORRECTION : Redirection vers la bonne URL
        return redirect('communication:liste_messages')

@login_required
def supprimer_message(request, message_id):
    """Vue pour supprimer un message - CORRIGÉE"""
    try:
        message = get_object_or_404(Message, id=message_id, expediteur=request.user)
        
        if request.method == 'POST':
            message.delete()
            messages.success(request, "Message supprimé avec succès!")
            # CORRECTION : Redirection vers la bonne URL
            return redirect('communication:liste_messages')
        
        return render(request, 'communication/confirmer_suppression.html', {
            'message': message,
            'page_title': 'Supprimer le message'
        })
    except Exception as e:
        messages.error(request, f"Erreur lors de la suppression: {str(e)}")
        # CORRECTION : Redirection vers la bonne URL
        return redirect('communication:liste_messages')

@login_required
def liste_notifications(request):
    """Vue pour lister les notifications - CORRIGÉE"""
    try:
        notifications = Notification.objects.filter(user=request.user).order_by('-date_creation')
        
        return render(request, 'communication/liste_notifications.html', {
            'notifications': notifications,
            'page_title': 'Mes Notifications'
        })
    except Exception as e:
        context = {
            'notifications': [],
            'page_title': 'Mes Notifications',
            'error': str(e)
        }
        return render(request, 'communication/liste_notifications.html', context)

@login_required
def marquer_notification_lue(request, notification_id):
    """Marquer une notification comme lue - CORRIGÉE"""
    try:
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.marquer_comme_lue()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        
        messages.success(request, "Notification marquée comme lue.")
        return redirect('communication:liste_notifications')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': str(e)})
        
        messages.error(request, f"Erreur: {str(e)}")
        return redirect('communication:liste_notifications')

@login_required
def marquer_toutes_notifications_lues(request):
    """Marquer toutes les notifications comme lues - CORRIGÉE"""
    try:
        Notification.objects.filter(user=request.user, est_lue=False).update(
            est_lue=True, 
            date_lecture=timezone.now()
        )
        messages.success(request, "Toutes les notifications ont été marquées comme lues.")
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
    
    return redirect('communication:liste_notifications')

@login_required
def api_conversations(request):
    """API pour récupérer les conversations - CORRIGÉE"""
    try:
        conversations = Conversation.objects.filter(participants=request.user).annotate(
            nb_messages_non_lus=Count('messages', filter=Q(messages__est_lu=False) & ~Q(messages__expediteur=request.user)),
            derniere_activite=Max('messages__date_envoi')
        ).order_by('-derniere_activite')
        
        data = []
        for conv in conversations:
            # Trouver l'autre participant
            autre_participant = conv.participants.exclude(id=request.user.id).first()
            dernier_message = conv.messages.order_by('-date_envoi').first()
            
            data.append({
                'id': conv.id,
                'autre_participant': {
                    'id': autre_participant.id if autre_participant else None,
                    'nom': autre_participant.get_full_name() if autre_participant else 'Utilisateur inconnu',
                    'email': autre_participant.email if autre_participant else ''
                },
                'dernier_message': dernier_message.titre if dernier_message else 'Aucun message',
                'dernier_message_date': dernier_message.date_envoi.isoformat() if dernier_message else None,
                'nb_messages_non_lus': conv.nb_messages_non_lus,
                'date_modification': conv.date_modification.isoformat() if conv.date_modification else None
            })
        
        return JsonResponse({'conversations': data})
    except Exception as e:
        return JsonResponse({'conversations': [], 'error': str(e)})

@login_required
def api_messages(request, conversation_id):
    """API pour récupérer les messages d'une conversation - CORRIGÉE"""
    try:
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        
        messages_list = conversation.messages.all().select_related('expediteur', 'destinataire').order_by('date_envoi')
        
        # Marquer les messages comme lus
        messages_list.filter(destinataire=request.user, est_lu=False).update(
            est_lu=True, 
            date_lecture=timezone.now()
        )
        
        data = []
        for msg in messages_list:
            data.append({
                'id': msg.id,
                'expediteur': {
                    'id': msg.expediteur.id,
                    'nom': msg.expediteur.get_full_name() or msg.expediteur.username
                },
                'destinataire': {
                    'id': msg.destinataire.id,
                    'nom': msg.destinataire.get_full_name() or msg.destinataire.username
                },
                'titre': msg.titre,
                'contenu': msg.contenu,
                'date_envoi': msg.date_envoi.isoformat(),
                'est_lu': msg.est_lu,
                'type_message': msg.type_message,
                'pieces_jointes': [
                    {
                        'id': pj.id,
                        'nom': pj.nom_original,
                        'url': pj.fichier.url,
                        'taille': pj.get_taille_lisible()
                    } for pj in msg.pieces_jointes.all()
                ]
            })
        
        return JsonResponse({'messages': data, 'conversation_id': conversation_id})
    except Exception as e:
        return JsonResponse({'messages': [], 'error': str(e)})

@login_required
def notification_non_lue_count(request):
    """API pour compter les notifications non lues - CORRIGÉE"""
    try:
        count = Notification.objects.filter(user=request.user, est_lue=False).count()
        return JsonResponse({'count': count})
    except:
        return JsonResponse({'count': 0})

@login_required
def marquer_message_lu(request, message_id):
    """Marquer un message comme lu - CORRIGÉE"""
    try:
        message = get_object_or_404(Message, id=message_id, destinataire=request.user)
        message.marquer_comme_lu()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

class MessageListView(LoginRequiredMixin, ListView):
    """Liste des messages (vue basée sur classe) - CORRIGÉE"""
    model = Message
    template_name = 'communication/message_list.html'
    context_object_name = 'messages'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Calcul des statistiques
        context['unread_count'] = user.messages_recus.filter(est_lu=False).count()
        context['total_received'] = user.messages_recus.count()
        context['total_sent'] = user.messages_envoyes.count()
        
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        filtre = self.request.GET.get('filtre')
        user = self.request.user
        
        if filtre == 'non_lus':
            queryset = user.messages_recus.filter(est_lu=False)
        elif filtre == 'envoyes':
            queryset = user.messages_envoyes.all()
        else:
            queryset = user.messages_recus.all()
            
        return queryset.select_related('expediteur', 'destinataire').order_by('-date_envoi')

class MessageDetailView(LoginRequiredMixin, DetailView):
    """Détail d'un message (vue basée sur classe) - CORRIGÉE"""
    model = Message
    template_name = 'communication/message_detail.html'
    context_object_name = 'message'
    
    def get_queryset(self):
        return Message.objects.filter(
            Q(destinataire=self.request.user) | Q(expediteur=self.request.user)
        ).select_related('expediteur', 'destinataire', 'conversation')
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Marquer comme lu si l'utilisateur est le destinataire
        if self.object.destinataire == request.user and not self.object.est_lu:
            self.object.marquer_comme_lu()
        return response

class MessageCreateView(LoginRequiredMixin, CreateView):
    """Créer un nouveau message (vue basée sur classe) - CORRIGÉE"""
    model = Message
    template_name = 'communication/message_form.html'
    fields = ['destinataire', 'titre', 'contenu', 'type_message']
    success_url = reverse_lazy('communication:message_list')
    
    def form_valid(self, form):
        form.instance.expediteur = self.request.user
        
        # Gérer la conversation
        destinataire = form.cleaned_data['destinataire']
        conversation = Conversation.objects.filter(
            participants=self.request.user
        ).filter(
            participants=destinataire
        ).first()
        
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(self.request.user, destinataire)
        
        form.instance.conversation = conversation
        response = super().form_valid(form)
        
        # Créer une notification
        Notification.objects.create(
            user=destinataire,
            titre=f"Nouveau message de {self.request.user.get_full_name() or self.request.user.username}",
            message=form.instance.titre,
            type_notification='MESSAGE'
        )
        
        messages.success(self.request, "Message envoyé avec succès!")
        return response
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['destinataire'].queryset = form.fields['destinataire'].queryset.exclude(
            id=self.request.user.id
        )
        return form

class NotificationListView(LoginRequiredMixin, ListView):
    """Liste des notifications (vue basée sur classe) - CORRIGÉE"""
    model = Notification
    template_name = 'communication/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-date_creation')
    
    def get(self, request, *args, **kwargs):
        # Marquer comme lues lors de l'affichage
        Notification.objects.filter(user=request.user, est_lue=False).update(
            est_lue=True, 
            date_lecture=timezone.now()
        )
        return super().get(request, *args, **kwargs)

@login_required
def upload_fichier(request):
    """Uploader un fichier - CORRIGÉE"""
    if request.method == 'POST' and request.FILES:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fichier = request.FILES['fichier']
            fs = FileSystemStorage()
            
            # Vérifier la taille du fichier (max 10MB)
            if fichier.size > 10 * 1024 * 1024:
                return JsonResponse({
                    'success': False, 
                    'error': 'Le fichier est trop volumineux (max 10MB)'
                })
            
            # Sauvegarder le fichier
            filename = fs.save(f'uploads/{fichier.name}', fichier)
            file_url = fs.url(filename)
            
            return JsonResponse({
                'success': True,
                'file_url': file_url,
                'file_name': fichier.name,
                'file_size': fichier.size
            })
    
    return JsonResponse({'success': False, 'error': 'Erreur lors de l\'upload'})

@login_required
def telecharger_fichier(request, fichier_id):
    """Télécharger un fichier - CORRIGÉE"""
    try:
        piece_jointe = get_object_or_404(PieceJointe, id=fichier_id)
        
        # Vérifier que l'utilisateur a accès à ce fichier
        if not (request.user == piece_jointe.message.expediteur or 
                request.user == piece_jointe.message.destinataire):
            return JsonResponse({'error': 'Accès non autorisé'}, status=403)
        
        response = FileResponse(piece_jointe.fichier.open(), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{piece_jointe.nom_original}"'
        return response
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def liste_fichiers(request):
    """Afficher tous les fichiers partagés - CORRIGÉE"""
    try:
        fichiers_recus = PieceJointe.objects.filter(
            message__destinataire=request.user
        ).select_related('message__expediteur').order_by('-date_upload')
        
        fichiers_envoyes = PieceJointe.objects.filter(
            message__expediteur=request.user
        ).select_related('message__destinataire').order_by('-date_upload')
        
        context = {
            'fichiers_recus': fichiers_recus,
            'fichiers_envoyes': fichiers_envoyes,
            'page_title': 'Fichiers partagés'
        }
        return render(request, 'communication/liste_fichiers.html', context)
    except Exception as e:
        context = {
            'fichiers_recus': [],
            'fichiers_envoyes': [],
            'page_title': 'Fichiers partagés',
            'error': str(e)
        }
        return render(request, 'communication/liste_fichiers.html', context)

@login_required
def liste_groupes(request):
    """Liste des groupes de communication - CORRIGÉE"""
    try:
        groupes = GroupeCommunication.objects.filter(
            Q(membres=request.user) | Q(createur=request.user)
        ).distinct().order_by('nom')
        
        context = {
            'groupes': groupes,
            'page_title': 'Groupes de communication'
        }
        return render(request, 'communication/groupes_list.html', context)
    except Exception as e:
        context = {
            'groupes': [],
            'page_title': 'Groupes de communication',
            'error': str(e)
        }
        return render(request, 'communication/groupes_list.html', context)

@login_required
def detail_groupe(request, groupe_id):
    """Détail d'un groupe avec ses messages - CORRIGÉE"""
    try:
        groupe = get_object_or_404(GroupeCommunication, id=groupe_id, membres=request.user)
        messages_groupe = MessageGroupe.objects.filter(groupe=groupe).select_related('expediteur').order_by('-date_envoi')
        
        context = {
            'groupe': groupe,
            'messages': messages_groupe,
            'page_title': f'Groupe: {groupe.nom}'
        }
        return render(request, 'communication/groupe_detail.html', context)
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return redirect('communication:liste_groupes')

@login_required
def envoyer_message_groupe(request, groupe_id):
    """Envoyer un message dans un groupe - CORRIGÉE"""
    try:
        groupe = get_object_or_404(GroupeCommunication, id=groupe_id, membres=request.user)
        
        if request.method == 'POST':
            form = MessageGroupeForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.expediteur = request.user
                message.groupe = groupe
                message.save()
                
                # Notifier tous les membres du groupe (sauf l'expéditeur)
                for membre in groupe.membres.exclude(id=request.user.id):
                    Notification.objects.create(
                        user=membre,
                        titre=f"Nouveau message dans {groupe.nom}",
                        message=form.cleaned_data['contenu'][:100] + "...",
                        type_notification='GROUPE'
                    )
                
                return JsonResponse({'success': True, 'message_id': message.id})
        
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def creer_groupe(request):
    """Créer un nouveau groupe - CORRIGÉE"""
    if request.method == 'POST':
        form = GroupeCommunicationForm(request.POST)
        if form.is_valid():
            try:
                groupe = form.save(commit=False)
                groupe.createur = request.user
                groupe.save()
                form.save_m2m()  # Sauvegarder les relations ManyToMany
                
                messages.success(request, f"Groupe '{groupe.nom}' créé avec succès!")
                return redirect('communication:detail_groupe', groupe_id=groupe.id)
            except Exception as e:
                messages.error(request, f"Erreur lors de la création: {str(e)}")
    else:
        form = GroupeCommunicationForm()
    
    return render(request, 'communication/groupe_form.html', {
        'form': form,
        'page_title': 'Créer un groupe'
    })

@login_required
def search_messages(request):
    """Rechercher dans les messages - CORRIGÉE"""
    query = request.GET.get('q', '')
    
    if query:
        messages_trouves = Message.objects.filter(
            Q(destinataire=request.user) &
            (Q(titre__icontains=query) | Q(contenu__icontains=query))
        ).select_related('expediteur').order_by('-date_envoi')
    else:
        messages_trouves = Message.objects.none()
    
    context = {
        'messages': messages_trouves,
        'query': query,
        'page_title': 'Recherche de messages'
    }
    return render(request, 'communication/search_results.html', context)

@login_required
def stats_communication(request):
    """Statistiques de communication - CORRIGÉE"""
    try:
        # Messages reçus
        messages_recus = Message.objects.filter(destinataire=request.user)
        messages_non_lus = messages_recus.filter(est_lu=False).count()
        
        # Notifications
        notifications_total = Notification.objects.filter(user=request.user).count()
        notifications_non_lues = Notification.objects.filter(user=request.user, est_lue=False).count()
        
        # Fichiers partagés
        fichiers_recus = PieceJointe.objects.filter(message__destinataire=request.user).count()
        
        context = {
            'messages_recus': messages_recus.count(),
            'messages_non_lus': messages_non_lus,
            'notifications_total': notifications_total,
            'notifications_non_lues': notifications_non_lues,
            'fichiers_recus': fichiers_recus,
            'page_title': 'Statistiques de communication'
        }
        return render(request, 'communication/stats.html', context)
    except Exception as e:
        context = {
            'messages_recus': 0,
            'messages_non_lus': 0,
            'notifications_total': 0,
            'notifications_non_lues': 0,
            'fichiers_recus': 0,
            'page_title': 'Statistiques de communication',
            'error': str(e)
        }
        return render(request, 'communication/stats.html', context)

@login_required
def derniere_activite_api(request):
    """API pour la dernière activité de messagerie - CORRIGÉE"""
    try:
        derniere_activite = get_derniere_activite(request.user)
        
        return JsonResponse({
            'derniere_activite': derniere_activite.isoformat() if derniere_activite else None,
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'derniere_activite': None,
            'timestamp': timezone.now().isoformat(),
            'error': str(e)
        })

@login_required
def nouveau_message(request):
    """Vue pour créer un nouveau message - CORRIGÉE"""
    try:
        return redirect('communication:message_create')
    except Exception as e:
        messages.error(request, f"Erreur: {e}")
        return redirect('communication:messagerie')

@login_required
def test_conversations_ultime(request):
    """Vue de test ultime pour vérifier les conversations"""
    html = f"""
    <html>
    <body style="font-family: Arial; padding: 20px;">
        <h1>TEST ULTIME - Conversations</h1>
        <h2>Utilisateur: {request.user.username} (ID: {request.user.id})</h2>
        
        <h3>1. Requête directe des conversations:</h3>
    """
    
    # Test 1: Requête directe
    conversations = Conversation.objects.filter(participants=request.user)
    html += f"<p>Conversations trouvées: <strong>{conversations.count()}</strong></p>"
    
    for conv in conversations:
        participants = list(conv.participants.all())
        html += f"<div style='border: 1px solid #ccc; padding: 10px; margin: 10px;'>"
        html += f"<h4>Conversation {conv.id}</h4>"
        html += f"<p>Participants: {[p.username for p in participants]}</p>"
        html += f"<p>Messages: {conv.messages.count()}</p>"
        html += "</div>"
    
    # Test 2: Requête avec annotations
    html += "<h3>2. Requête avec annotations:</h3>"
    conversations_anno = Conversation.objects.filter(participants=request.user).annotate(
        nb_messages_non_lus=Count('messages', filter=Q(messages__est_lu=False) & ~Q(messages__expediteur=request.user)),
        derniere_activite=Max('messages__date_envoi'),
        total_messages=Count('messages')
    )
    
    html += f"<p>Conversations avec annotations: <strong>{conversations_anno.count()}</strong></p>"
    
    for conv in conversations_anno:
        html += f"<div style='border: 1px solid #369; padding: 10px; margin: 10px; background: #f0f8ff;'>"
        html += f"<h4>Conversation {conv.id} (avec annotations)</h4>"
        html += f"<p>Messages non lus: {conv.nb_messages_non_lus}</p>"
        html += f"<p>Total messages: {conv.total_messages}</p>"
        html += f"<p>Dernière activité: {conv.derniere_activite}</p>"
        html += "</div>"
    
    html += """
        <h3>3. Test de la vue messagerie normale:</h3>
        <p><a href="/communication/">Retour à la messagerie normale</a></p>
    </body>
    </html>
    """
    
    return HttpResponse(html)

@login_required
def test_simple(request):
    """Page de test simplifiée"""
    return render(request, 'communication/test_simple.html')

@login_required
def envoyer_message_conversation(request, conversation_id):
    """Envoyer un message dans une conversation existante - VERSION CORRIGÉE"""
    if request.method == 'POST':
        try:
            conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
            contenu = request.POST.get('contenu', '').strip()
            
            if not contenu:
                messages.error(request, 'Le message ne peut pas être vide.')
                return redirect('communication:detail_conversation', conversation_id=conversation_id)
            
            message = Message.objects.create(
                expediteur=request.user,
                contenu=contenu,
                conversation=conversation
            )
            
            destinataires = conversation.participants.exclude(id=request.user.id)
            message.destinataires.add(*destinataires)
            
            messages.success(request, 'Message envoyé avec succès!')
            return redirect('communication:detail_conversation', conversation_id=conversation_id)
            
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
            return redirect('communication:detail_conversation', conversation_id=conversation_id)
    
    return redirect('communication:detail_conversation', conversation_id=conversation_id)

@login_required  
def messagerie_assureur(request):
    """Vue messagerie pour les assureurs"""
    return render(request, 'communication/messagerie_assureur.html')

@login_required
def messagerie_medecin(request):
    """Vue messagerie pour les médecins"""
    return render(request, 'communication/messagerie_medecin.html')

@login_required
def messagerie_agent(request):
    """Vue messagerie pour les agents"""
    return render(request, 'communication/messagerie_agent.html')

def test_messagerie(request):
    """Page de test pour toutes les interfaces messagerie"""
    return render(request, 'communication/test_messagerie.html')

def test_urgence(request):
    """Page de test d'urgence"""
    return render(request, 'communication/test_urgence.html')

@login_required
def liste_messages_agent(request):
    """Vue spécifique pour les agents - utilise la vue générique"""
    return liste_messages(request)

@login_required
def liste_notifications_agent(request):
    """Vue spécifique pour les agents - utilise la vue générique"""
    return liste_notifications(request)

@login_required
def envoyer_message_agent(request):
    """Vue spécifique pour les agents - utilise la vue générique"""
    return envoyer_message(request)

@login_required
def detail_message_agent(request, message_id):
    """Vue spécifique pour les agents - utilise la vue générique"""
    return detail_message(request, message_id)

@login_required
def liste_messages_assureur(request):
    """Vue spécifique pour les assureurs - utilise la vue générique"""
    return liste_messages(request)

@login_required
def liste_notifications_assureur(request):
    """Vue spécifique pour les assureurs - utilise la vue générique"""
    return liste_notifications(request)

@login_required
def envoyer_message_assureur(request):
    """Vue spécifique pour les assureurs - utilise la vue générique"""
    return envoyer_message(request)

@login_required
def detail_message_assureur(request, message_id):
    """Vue spécifique pour les assureurs - utilise la vue générique"""
    return detail_message(request, message_id)

@login_required
def messagerie_membre(request):
    """Vue messagerie pour les membres"""
    return render(request, 'communication/messagerie_membre.html')