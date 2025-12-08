# inscription/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
import json

def inscription_membre(request):
    """Page d'inscription par téléphone - Version simplifiée sans formulaire"""
    # Si l'utilisateur est déjà connecté, le rediriger
    if request.user.is_authenticated:
        messages.info(request, "Vous êtes déjà connecté.")
        return redirect('home')
    
    # Préparer le message de succès si présent
    success_message = None
    
    context = {
        'title': 'Inscription - Devenir Membre',
    }
    
    # Enregistrer une vue statistique (optionnel)
    try:
        request.session['inscription_page_viewed'] = datetime.now().isoformat()
    except:
        pass
    
    return render(request, 'inscription/inscription.html', context)

def demande_rappel(request):
    """Traitement AJAX pour les demandes de rappel"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            
            # Valider les données
            nom = data.get('nom', '').strip()
            prenom = data.get('prenom', '').strip()
            telephone = data.get('telephone', '').strip()
            email = data.get('email', '').strip()
            creneau = data.get('creneau', '')
            message = data.get('message', '').strip()
            
            # Validation simple
            if not nom or not prenom or not telephone:
                return JsonResponse({
                    'success': False,
                    'message': 'Veuillez remplir les champs obligatoires.'
                })
            
            # Préparer les données pour l'email
            creneau_text = {
                '9-12': '9h-12h',
                '12-14': '12h-14h',
                '14-16': '14h-16h',
                '16-18': '16h-18h',
            }.get(creneau, 'Non spécifié')
            
            # Sauvegarder en session (optionnel)
            request.session['last_demande_rappel'] = {
                'nom': nom,
                'prenom': prenom,
                'telephone': telephone,
                'email': email,
                'creneau': creneau,
                'date': datetime.now().strftime('%d/%m/%Y %H:%M')
            }
            
            # Envoyer l'email (en production)
            if not settings.DEBUG:
                try:
                    email_body = f"""
                    Nouvelle demande de rappel pour inscription:
                    
                    Nom: {nom} {prenom}
                    Téléphone: {telephone}
                    Email: {email if email else 'Non fourni'}
                    Créneau horaire préféré: {creneau_text}
                    Message: {message if message else 'Aucun message'}
                    
                    Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}
                    IP: {request.META.get('REMOTE_ADDR', 'Inconnue')}
                    """
                    
                    send_mail(
                        subject=f"🔔 Demande de rappel - {nom} {prenom}",
                        message=email_body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[getattr(settings, 'ADMIN_EMAIL', 'contact@santedirect.fr')],
                        fail_silently=True,
                    )
                except Exception as e:
                    print(f"Erreur d'envoi d'email: {e}")
            
            return JsonResponse({
                'success': True,
                'message': f'Merci {prenom} ! Nous vous rappellerons au {telephone} dans le créneau {creneau_text}.'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Format de données invalide.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Une erreur est survenue: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Méthode non autorisée.'
    })

def inscription_success(request):
    """Page de succès après inscription téléphonique (optionnel)"""
    # Cette page pourrait afficher les informations sur le processus d'inscription
    context = {
        'title': 'Inscription par téléphone',
        'telephone': '07 98 91 09 12',
        'horaires': 'Lundi au vendredi, 9h-18h'
    }
    return render(request, 'inscription/success_info.html', context)