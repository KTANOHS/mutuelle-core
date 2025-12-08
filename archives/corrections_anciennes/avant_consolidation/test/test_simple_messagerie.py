# test_simple_messagerie.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_simple():
    from django.contrib.auth.models import User
    from communication.models import Message
    
    print("🔍 TEST SIMPLE MESSAGERIE")
    print("=" * 40)
    
    # Compter les messages pour test_pharmacien
    try:
        pharmacien = User.objects.get(username='test_pharmacien')
        messages_recus = Message.objects.filter(destinataire=pharmacien).count()
        messages_envoyes = Message.objects.filter(expediteur=pharmacien).count()
        
        print(f"👤 Utilisateur: test_pharmacien")
        print(f"📥 Messages reçus: {messages_recus}")
        print(f"📤 Messages envoyés: {messages_envoyes}")
        print(f"📊 Total messages: {messages_recus + messages_envoyes}")
        
        if messages_recus + messages_envoyes == 0:
            print("\n💡 ASTUCE: Aucun message trouvé. Créez des messages de test.")
            print("   Allez sur: http://127.0.0.1:8000/agents/envoyer-message/")
            print("   Envoyez un message à test_pharmacien")
            
    except User.DoesNotExist:
        print("❌ Utilisateur test_pharmacien non trouvé")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_simple()