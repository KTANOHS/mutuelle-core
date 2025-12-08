# mettre_a_jour_vue_messagerie.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def mettre_a_jour_vue_messagerie():
    """Mettre à jour la vue messagerie avec la version corrigée"""
    
    fichier = 'communication/views.py'
    
    with open(fichier, 'r') as f:
        contenu = f.read()
    
    # Ancienne version (celle actuelle)
    ancienne_version = '''def messagerie(request):
    """Page principale de messagerie - CORRIGÉE"""
    try:
        conversations = Conversation.objects.filter(participants=request.user).annotate(
            nb_messages_non_lus=Count('messages', filter=Q(messages__est_lu=False) & ~Q(messages__expediteur=request.user)),
            derniere_activite=Max('messages__date_envoi')
        ).order_by('-derniere_activite')
        
        context = {
            'conversations': conversations,
            'form': MessageForm()
        }
        return render(request, 'communication/messagerie.html', context)
    except Exception as e:
        # Fallback en cas d'erreur
        context = {
            'conversations': [],
            'form': MessageForm(),
            'error': str(e)
        }
        return render(request, 'communication/messagerie.html', context)'''
    
    # Nouvelle version améliorée
    nouvelle_version = '''def messagerie(request):
    """Page principale de messagerie - VERSION AMÉLIORÉE"""
    try:
        # Récupérer les conversations avec annotations
        conversations = Conversation.objects.filter(participants=request.user).annotate(
            nb_messages_non_lus=Count('messages', filter=Q(messages__est_lu=False) & ~Q(messages__expediteur=request.user)),
            derniere_activite=Max('messages__date_envoi'),
            total_messages=Count('messages')
        ).order_by('-derniere_activite')
        
        # Récupérer les messages récents pour affichage
        messages_recents = Message.objects.filter(
            Q(expediteur=request.user) | Q(destinataire=request.user)
        ).select_related('expediteur', 'destinataire').order_by('-date_envoi')[:10]
        
        context = {
            'conversations': conversations,
            'messages_recents': messages_recents,
            'form': MessageForm(),
            'page_title': 'Messagerie',
            'total_conversations': conversations.count(),
            'total_messages': Message.objects.filter(
                Q(expediteur=request.user) | Q(destinataire=request.user)
            ).count()
        }
        return render(request, 'communication/messagerie.html', context)
        
    except Exception as e:
        # Fallback en cas d'erreur
        context = {
            'conversations': [],
            'messages_recents': [],
            'form': MessageForm(),
            'error': str(e),
            'page_title': 'Messagerie',
            'total_conversations': 0,
            'total_messages': 0
        }
        return render(request, 'communication/messagerie.html', context)'''
    
    if ancienne_version in contenu:
        contenu = contenu.replace(ancienne_version, nouvelle_version)
        with open(fichier, 'w') as f:
            f.write(contenu)
        print("✅ Vue messagerie mise à jour avec succès !")
    else:
        print("ℹ️  La vue messagerie a une structure différente")

if __name__ == "__main__":
    mettre_a_jour_vue_messagerie()