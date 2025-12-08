# diagnostic_contexte.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostiquer_contexte():
    print("🔍 DIAGNOSTIC DU CONTEXTE DE LA VUE MESSAGERIE")
    print("=" * 60)
    
    from communication.views import messagerie
    from django.test import RequestFactory
    from django.contrib.auth.models import User
    from django.template import Template, Context
    from django.template.loader import get_template
    
    try:
        # Récupérer l'utilisateur
        pharmacien = User.objects.get(username='test_pharmacien')
        
        # Créer une vraie requête (pas factory)
        from django.test import Client
        client = Client()
        client.force_login(pharmacien)
        
        # Faire une vraie requête HTTP
        response = client.get('/communication/')
        
        print(f"📊 Statut HTTP: {response.status_code}")
        print(f"📝 Content-Type: {response.get('Content-Type', 'Non défini')}")
        
        # Vérifier si c'est un TemplateResponse
        if hasattr(response, 'template_name'):
            print(f"✅ Template utilisé: {response.template_name}")
        
        # Vérifier le contexte
        if hasattr(response, 'context_data'):
            print(f"✅ Contexte disponible: {len(response.context_data)} éléments")
            for key, value in response.context_data.items():
                print(f"   - {key}: {type(value)}")
        else:
            print("❌ Aucun contexte_data (normal pour HttpResponse)")
        
        # Vérifier le contenu
        content = response.content.decode('utf-8')
        
        # Vérifier si les données sont dans le HTML
        checks = {
            'conversations dans HTML': 'conversation' in content.lower(),
            'messages dans HTML': 'message' in content.lower(),
            'test_agent dans HTML': 'test_agent' in content,
            'test_medecin dans HTML': 'test_medecin' in content
        }
        
        print("\n🔍 VÉRIFICATION DU CONTENU HTML:")
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"   {status} {check}: {'TROUVÉ' if result else 'NON TROUVÉ'}")
        
        # Afficher un extrait du HTML pour debug
        print(f"\n📄 EXTRAT DU HTML (premieres 1000 caracteres):")
        print(content[:1000] + "..." if len(content) > 1000 else content)
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

def verifier_template_rendu():
    """Vérifier comment le template est rendu"""
    print("\n🎨 VÉRIFICATION DU RENDU TEMPLATE")
    print("=" * 60)
    
    from django.template.loader import render_to_string
    from django.contrib.auth.models import User
    from communication.models import Conversation, Message
    from django.db.models import Q
    
    try:
        pharmacien = User.objects.get(username='test_pharmacien')
        
        # Récupérer les mêmes données que la vue
        conversations = Conversation.objects.filter(participants=pharmacien).annotate(
            nb_messages_non_lus=Count('messages', filter=Q(messages__est_lu=False) & ~Q(messages__expediteur=pharmacien)),
            derniere_activite=Max('messages__date_envoi'),
            total_messages=Count('messages')
        ).order_by('-derniere_activite')
        
        messages_recents = Message.objects.filter(
            Q(expediteur=pharmacien) | Q(destinataire=pharmacien)
        ).select_related('expediteur', 'destinataire').order_by('-date_envoi')[:10]
        
        context = {
            'conversations': conversations,
            'messages_recents': messages_recents,
            'form': MessageForm(),
            'page_title': 'Messagerie',
            'total_conversations': conversations.count(),
            'total_messages': Message.objects.filter(
                Q(expediteur=pharmacien) | Q(destinataire=pharmacien)
            ).count()
        }
        
        # Rendre le template manuellement
        html = render_to_string('communication/messagerie.html', context)
        
        print(f"✅ Template rendu avec succès")
        print(f"📏 Taille du HTML: {len(html)} caractères")
        
        # Vérifier si les données sont dans le HTML rendu
        if conversations:
            print(f"✅ Conversations trouvées dans le HTML rendu")
            # Vérifier si au moins une conversation est affichée
            for conv in conversations:
                if str(conv.id) in html:
                    print(f"   - Conversation {conv.id} trouvée dans le HTML")
        
    except Exception as e:
        print(f"❌ Erreur rendu template: {e}")

if __name__ == "__main__":
    from django.db.models import Q, Count, Max
    from communication.forms import MessageForm
    
    diagnostiquer_contexte()
    verifier_template_rendu()