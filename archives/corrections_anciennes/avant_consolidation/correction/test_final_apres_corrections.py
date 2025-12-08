# test_final_apres_corrections.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_final_apres_corrections():
    from communication.forms import MessageForm
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    print("=== TEST FINAL APRÈS CORRECTIONS ===")
    
    # Trouver les utilisateurs
    expediteur = User.objects.filter(username='assureur_test').first()
    destinataire = User.objects.filter(username='koffitanoh').first()
    
    if not expediteur or not destinataire:
        print("❌ Utilisateurs de test non trouvés")
        return
    
    print(f"✅ Expéditeur: {expediteur.username}")
    print(f"✅ Destinataire: {destinataire.username}")
    
    # Test 1: Formulaire avec gestion de conversation
    print("\n1. TEST FORMULAIRE AVEC CONVERSATION:")
    test_data = {
        'destinataire': destinataire.id,
        'titre': 'Test final après corrections',
        'contenu': 'Ce message teste le formulaire complètement corrigé',
        'type_message': 'MESSAGE',
    }
    
    form = MessageForm(data=test_data, expediteur=expediteur)
    
    if form.is_valid():
        print("✅ Formulaire valide")
        try:
            message = form.save()
            print("✅ Message créé avec succès!")
            print(f"   - ID: {message.id}")
            print(f"   - Titre: {message.titre}")
            print(f"   - Conversation ID: {message.conversation.id}")
            print(f"   - De: {message.expediteur.username} → À: {message.destinataire.username}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ Formulaire invalide:")
        for field, errors in form.errors.items():
            print(f"   - {field}: {errors}")
    
    # Test 2: Vérification des statistiques
    print("\n2. STATISTIQUES FINALES:")
    from communication.models import Message, Conversation
    total_messages = Message.objects.count()
    total_conversations = Conversation.objects.count()
    
    print(f"   - Total messages: {total_messages}")
    print(f"   - Total conversations: {total_conversations}")
    print(f"   - Messages de l'assureur: {Message.objects.filter(expediteur=expediteur).count()}")
    print(f"   - Messages à l'assureur: {Message.objects.filter(destinataire=expediteur).count()}")

if __name__ == "__main__":
    test_final_apres_corrections()