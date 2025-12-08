# diagnostic_messagerie_communication.py
import os
import django
from django.test import RequestFactory
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostiquer_vue_messagerie():
    print("🔍 DIAGNOSTIC VUE MESSAGERIE (/communication/)")
    print("=" * 60)
    
    from communication.views import messagerie
    from django.contrib.auth.models import User
    
    # Créer une requête simulée
    factory = RequestFactory()
    
    try:
        # Récupérer un utilisateur pharmacien pour tester
        pharmacien = User.objects.get(username='test_pharmacien')
        
        # Créer une requête simulée
        request = factory.get('/communication/')
        request.user = pharmacien
        
        # Appeler la vue
        response = messagerie(request)
        
        print(f"✅ Vue messagerie exécutée avec succès")
        print(f"📊 Statut HTTP: {response.status_code}")
        print(f"📝 Template utilisé: {response.template_name}")
        
        # Vérifier le contexte
        if hasattr(response, 'context_data'):
            context = response.context_data
            print(f"📦 Données du contexte:")
            print(f"   - Conversations: {len(context.get('conversations', []))}")
            print(f"   - Formulaire présent: {'form' in context}")
            print(f"   - Erreur: {context.get('error', 'Aucune')}")
        else:
            print("❌ Aucun contexte de données")
            
    except User.DoesNotExist:
        print("❌ Utilisateur test_pharmacien non trouvé")
    except Exception as e:
        print(f"❌ Erreur lors du diagnostic: {e}")

def verifier_messages_utilisateur():
    """Vérifier les messages d'un utilisateur spécifique"""
    print("\n📨 VÉRIFICATION DES MESSAGES UTILISATEUR")
    print("=" * 60)
    
    try:
        from communication.models import Message, Conversation
        from django.contrib.auth.models import User
        
        # Test avec pharmacien
        pharmacien = User.objects.get(username='test_pharmacien')
        
        # Messages reçus
        messages_recus = Message.objects.filter(destinataire=pharmacien)
        messages_envoyes = Message.objects.filter(expediteur=pharmacien)
        
        print(f"👤 Utilisateur: {pharmacien.username} ({pharmacien.get_full_name()})")
        print(f"📥 Messages reçus: {messages_recus.count()}")
        print(f"📤 Messages envoyés: {messages_envoyes.count()}")
        
        # Conversations
        conversations = Conversation.objects.filter(participants=pharmacien)
        print(f"💬 Conversations: {conversations.count()}")
        
        # Détail des messages
        if messages_recus.exists():
            print("\n📋 DERNIERS MESSAGES REÇUS:")
            for msg in messages_recus.order_by('-date_envoi')[:5]:
                print(f"   - {msg.titre} (de {msg.expediteur}) - {msg.date_envoi}")
                
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    diagnostiquer_vue_messagerie()
    verifier_messages_utilisateur()