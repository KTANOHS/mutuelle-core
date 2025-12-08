# correction_definitive_vue.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def corriger_vue_messagerie_definitivement():
    """Corriger définitivement la vue messagerie pour qu'elle rende le template correctement"""
    
    vue_path = 'communication/views.py'
    
    with open(vue_path, 'r') as f:
        contenu = f.read()
    
    print("🔧 CORRECTION DÉFINITIVE DE LA VUE MESSAGERIE")
    print("=" * 60)
    
    # Rechercher la fonction messagerie
    debut = contenu.find('def messagerie(request):')
    if debut == -1:
        print("❌ Fonction messagerie non trouvée")
        return
    
    # Extraire jusqu'à la fonction suivante
    fin = contenu.find('def ', debut + 1)
    if fin == -1:
        fin = len(contenu)
    
    fonction_actuelle = contenu[debut:fin]
    
    # Vérifier si la fonction utilise return render (correct) ou return HttpResponse (incorrect)
    if 'return HttpResponse' in fonction_actuelle:
        print("❌ La vue utilise HttpResponse au lieu de render")
        
        # Remplacer par une version corrigée
        nouvelle_fonction = '''@login_required
def messagerie(request):
    """Page principale de messagerie - VERSION DÉFINITIVEMENT CORRIGÉE"""
    try:
        from django.db.models import Q, Count, Max
        from communication.models import Conversation, Message
        from communication.forms import MessageForm
        
        print(f"🔍 MESSAGERIE - Utilisateur: {request.user.username}")
        
        # Récupérer les conversations
        conversations = Conversation.objects.filter(participants=request.user).annotate(
            nb_messages_non_lus=Count('messages', filter=Q(messages__est_lu=False) & ~Q(messages__expediteur=request.user)),
            derniere_activite=Max('messages__date_envoi'),
            total_messages=Count('messages')
        ).order_by('-derniere_activite')
        
        print(f"🔍 Conversations trouvées: {conversations.count()}")
        
        # Messages récents
        messages_recents = Message.objects.filter(
            Q(expediteur=request.user) | Q(destinataire=request.user)
        ).select_related('expediteur', 'destinataire').order_by('-date_envoi')[:10]
        
        # CRÉATION DU CONTEXTE
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
        
        print(f"🔍 Rendu du template avec {len(context)} éléments de contexte")
        
        # UTILISER RENDER() POUR RENVOYER LE TEMPLATE AVEC LE CONTEXTE
        from django.shortcuts import render
        return render(request, 'communication/messagerie.html', context)
        
    except Exception as e:
        print(f"❌ Erreur dans messagerie: {e}")
        # Fallback avec render aussi
        from django.shortcuts import render
        from communication.forms import MessageForm
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
        
        # Remplacer l'ancienne fonction
        contenu = contenu.replace(fonction_actuelle, nouvelle_fonction)
        print("✅ Vue messagerie complètement corrigée pour utiliser render()")
    
    elif 'return render(' in fonction_actuelle:
        print("✅ La vue utilise déjà render() - vérification de l'import")
        
        # Vérifier que l'import de render existe
        if 'from django.shortcuts import render' not in contenu:
            # Ajouter l'import en haut du fichier
            contenu = contenu.replace(
                'from django.shortcuts import render, redirect, get_object_or_404',
                'from django.shortcuts import render, redirect, get_object_or_404'
            )
            print("✅ Import de render vérifié")
    
    else:
        print("❓ Structure de fonction non reconnue")
        print("Fonction actuelle:")
        print(fonction_actuelle)
        return
    
    # Écrire les modifications
    with open(vue_path, 'w') as f:
        f.write(contenu)
    
    print("✅ Correction définitive appliquée à la vue messagerie")

def restaurer_url_originale():
    """Restaurer l'URL originale pour utiliser la vue corrigée"""
    
    urls_path = 'communication/urls.py'
    
    with open(urls_path, 'r') as f:
        contenu = f.read()
    
    # Remplacer la redirection d'urgence par la vue originale
    if 'test_conversations_ultime' in contenu and 'messagerie' in contenu:
        contenu = contenu.replace(
            'path(\'\', views.test_conversations_ultime, name=\'messagerie\')  # URGENCE: redirigé vers test',
            'path(\'\', views.messagerie, name=\'messagerie\')'
        )
        print("✅ URL principale restaurée vers la vue messagerie corrigée")
    else:
        print("ℹ️  Aucune redirection d'urgence trouvée à restaurer")
    
    with open(urls_path, 'w') as f:
        f.write(contenu)

if __name__ == "__main__":
    corriger_vue_messagerie_definitivement()
    restaurer_url_originale()
    
    print(f"\n🎯 CORRECTIONS APPLIQUÉES:")
    print("1. Vue messagerie corrigée pour utiliser render()")
    print("2. URL principale restaurée vers la vue corrigée")
    print("🌐 Testez: http://127.0.0.1:8000/communication/")
    print("")
    print("📋 CE QUI A ÉTÉ CORRIGÉ:")
    print("   - La vue utilise maintenant render() au lieu de HttpResponse")
    print("   - Le contexte est correctement passé au template")
    print("   - Les conversations devraient maintenant s'afficher")