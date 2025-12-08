# corriger_vue_messagerie.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def corriger_vue_messagerie():
    """Corriger la vue messagerie dans communication/views.py"""
    
    fichier = 'communication/views.py'
    
    with open(fichier, 'r') as f:
        contenu = f.read()
    
    # Vérifier si la vue messagerie existe déjà avec le bon contexte
    if "return render(request, 'communication/messagerie.html', context)" in contenu:
        print("✅ La vue messagerie semble déjà correcte")
        return
    
    # Trouver la fonction messagerie et la remplacer
    ancienne_vue = '''
@login_required
def messagerie(request):
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
        return render(request, 'communication/messagerie.html', context)
'''

    nouvelle_vue = '''
@login_required
def messagerie(request):
    """Page principale de messagerie - VERSION CORRIGÉE"""
    try:
        # Récupérer les conversations de l'utilisateur
        conversations = Conversation.objects.filter(participants=request.user).annotate(
            nb_messages_non_lus=Count('messages', filter=Q(messages__est_lu=False) & ~Q(messages__expediteur=request.user)),
            derniere_activite=Max('messages__date_envoi')
        ).order_by('-derniere_activite')
        
        # Récupérer aussi les messages récents pour affichage
        messages_recents = Message.objects.filter(
            Q(expediteur=request.user) | Q(destinataire=request.user)
        ).select_related('expediteur', 'destinataire').order_by('-date_envoi')[:10]
        
        context = {
            'conversations': conversations,
            'messages_recents': messages_recents,
            'form': MessageForm(),
            'page_title': 'Messagerie'
        }
        return render(request, 'communication/messagerie.html', context)
        
    except Exception as e:
        # Fallback en cas d'erreur
        context = {
            'conversations': [],
            'messages_recents': [],
            'form': MessageForm(),
            'error': str(e),
            'page_title': 'Messagerie'
        }
        return render(request, 'communication/messagerie.html', context)
'''
    
    # Remplacer l'ancienne vue par la nouvelle
    if ancienne_vue in contenu:
        contenu = contenu.replace(ancienne_vue, nouvelle_vue)
        with open(fichier, 'w') as f:
            f.write(contenu)
        print("✅ Vue messagerie corrigée avec succès !")
    else:
        print("ℹ️  La vue messagerie a une structure différente, vérification manuelle nécessaire")

if __name__ == "__main__":
    corriger_vue_messagerie()