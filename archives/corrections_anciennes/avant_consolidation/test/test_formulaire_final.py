# test_formulaire_final.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_formulaire_final():
    from communication.forms import MessageForm
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    print("=== TEST FORMULAIRE FINAL ===")
    
    # Trouver les utilisateurs
    expediteur = User.objects.filter(username='assureur_test').first()
    destinataire = User.objects.filter(username='koffitanoh').first()
    
    if not expediteur or not destinataire:
        print("❌ Utilisateurs de test non trouvés")
        return
    
    print(f"✅ Expéditeur: {expediteur.username}")
    print(f"✅ Destinataire: {destinataire.username}")
    
    # Données de test
    test_data = {
        'destinataire': destinataire.id,
        'titre': 'Test formulaire corrigé',
        'contenu': 'Ce message teste le formulaire avec gestion automatique de la conversation',
        'type_message': 'MESSAGE',
    }
    
    # Tester le formulaire avec l'expéditeur
    form = MessageForm(data=test_data, expediteur=expediteur)
    
    print(f"Formulaire valide: {form.is_valid()}")
    
    if not form.is_valid():
        print("❌ Erreurs de validation:")
        for field, errors in form.errors.items():
            print(f"   - {field}: {errors}")
    else:
        print("✅ Formulaire valide!")
        
        # Sauvegarder le message
        try:
            message = form.save()
            print("✅ Message créé avec succès!")
            print(f"   - ID: {message.id}")
            print(f"   - Titre: {message.titre}")
            print(f"   - Type: {message.type_message}")
            print(f"   - Conversation ID: {message.conversation.id}")
            print(f"   - De: {message.expediteur.username} → À: {message.destinataire.username}")
            print(f"   - Participants conversation: {[p.username for p in message.conversation.participants.all()]}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_formulaire_final()