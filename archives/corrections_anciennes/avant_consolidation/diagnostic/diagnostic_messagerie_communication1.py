# diagnostic_messagerie_communication.py
import os
import django
import sys

# Ajouter le chemin du projet
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

# Configuration Django AVANT tout import
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django configuré avec succès")
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def diagnostiquer_vue_messagerie():
    print("🔍 DIAGNOSTIC VUE MESSAGERIE (/communication/)")
    print("=" * 60)
    
    from communication.views import messagerie
    from django.contrib.auth.models import User
    from django.test import RequestFactory
    
    try:
        # Récupérer un utilisateur pharmacien pour tester
        pharmacien = User.objects.filter(username='test_pharmacien').first()
        if not pharmacien:
            print("❌ Utilisateur test_pharmacien non trouvé, création d'un utilisateur de test...")
            # Créer un utilisateur de test si nécessaire
            pharmacien = User.objects.create_user(
                username='test_pharmacien',
                password='test123',
                email='pharmacien@test.com'
            )
        
        # Créer une requête simulée
        factory = RequestFactory()
        request = factory.get('/communication/')
        request.user = pharmacien
        
        # Appeler la vue
        response = messagerie(request)
        
        print(f"✅ Vue messagerie exécutée avec succès")
        print(f"📊 Statut HTTP: {response.status_code}")
        
        # Vérifier le contexte
        if hasattr(response, 'context_data'):
            context = response.context_data
            print(f"📦 Données du contexte:")
            print(f"   - Conversations: {len(context.get('conversations', []))}")
            print(f"   - Formulaire présent: {'form' in context}")
            print(f"   - Erreur: {context.get('error', 'Aucune')}")
            
            # Afficher les détails des conversations
            conversations = context.get('conversations', [])
            if conversations:
                print(f"\n💬 DÉTAIL DES CONVERSATIONS:")
                for conv in conversations[:3]:  # Afficher les 3 premières
                    participants = list(conv.participants.all())
                    autre_participant = [p for p in participants if p != pharmacien]
                    print(f"   - Conversation {conv.id}: {len(autre_participant)} autre(s) participant(s)")
        else:
            print("❌ Aucun contexte de données")
            
    except Exception as e:
        print(f"❌ Erreur lors du diagnostic: {e}")
        import traceback
        traceback.print_exc()

def verifier_messages_utilisateur():
    """Vérifier les messages d'un utilisateur spécifique"""
    print("\n📨 VÉRIFICATION DES MESSAGES UTILISATEUR")
    print("=" * 60)
    
    try:
        from communication.models import Message, Conversation
        from django.contrib.auth.models import User
        
        # Test avec pharmacien
        pharmacien = User.objects.filter(username='test_pharmacien').first()
        if not pharmacien:
            print("❌ Utilisateur test_pharmacien non trouvé")
            return
        
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
            for msg in messages_recus.select_related('expediteur').order_by('-date_envoi')[:5]:
                print(f"   - '{msg.titre}' (de {msg.expediteur.username}) - {msg.date_envoi}")
        else:
            print("📭 Aucun message reçu")
            
        if messages_envoyes.exists():
            print("\n📤 DERNIERS MESSAGES ENVOYÉS:")
            for msg in messages_envoyes.select_related('destinataire').order_by('-date_envoi')[:3]:
                print(f"   - '{msg.titre}' (à {msg.destinataire.username}) - {msg.date_envoi}")
        else:
            print("📭 Aucun message envoyé")
                
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

def verifier_urls_fonctionnelles():
    """Vérifier quelles URLs de messagerie fonctionnent"""
    print("\n🌐 VÉRIFICATION DES URLs FONCTIONNELLES")
    print("=" * 60)
    
    try:
        from django.urls import reverse
        from django.contrib.auth.models import User
        
        pharmacien = User.objects.filter(username='test_pharmacien').first()
        if not pharmacien:
            print("❌ Utilisateur test_pharmacien non trouvé")
            return
        
        urls_a_tester = [
            'communication:messagerie',
            'communication:message_list', 
            'communication:envoyer_message',
            'communication:conversations',
            'communication:liste_messages',
        ]
        
        for url_name in urls_a_tester:
            try:
                url = reverse(url_name)
                print(f"✅ {url_name:30} → {url}")
            except Exception as e:
                print(f"❌ {url_name:30} → ERREUR: {e}")
                
    except Exception as e:
        print(f"❌ Erreur vérification URLs: {e}")

if __name__ == "__main__":
    diagnostiquer_vue_messagerie()
    verifier_messages_utilisateur()
    verifier_urls_fonctionnelles()
    
    print("\n🎯 RECOMMANDATIONS:")
    print("1. Utilisez http://127.0.0.1:8000/communication/messages/ pour voir les messages")
    print("2. Utilisez http://127.0.0.1:8000/communication/conversations/ pour les conversations")
    print("3. Vérifiez que l'utilisateur a des messages dans la base de données")