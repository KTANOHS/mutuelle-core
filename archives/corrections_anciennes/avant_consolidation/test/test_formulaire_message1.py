# test_formulaire_message.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_formulaire_message():
    from communication.forms import MessageForm  # CORRECTION : import absolu
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    print("=== TEST FORMULAIRE MESSAGE ===")
    
    # Créer des données de test
    test_data = {
        'titre': 'Test de message',
        'contenu': 'Ceci est un test',
        'type_message': 'MESSAGE',
    }
    
    # Essayer de trouver un utilisateur pour le destinataire
    try:
        user = User.objects.first()
        test_data['destinataire'] = user.id
        print(f"✅ Destinataire de test: {user.username}")
    except:
        print("⚠️  Aucun utilisateur trouvé pour le test")
        test_data['destinataire'] = None
    
    # Tester le formulaire
    form = MessageForm(data=test_data)
    
    print(f"Formulaire valide: {form.is_valid()}")
    
    if not form.is_valid():
        print("❌ Erreurs de validation:")
        for field, errors in form.errors.items():
            print(f"   - {field}: {errors}")
    else:
        print("✅ Formulaire valide!")
        
        # Essayer de sauvegarder
        try:
            if user:
                form.instance.expediteur = user
            message = form.save()
            print(f"✅ Message créé avec succès: {message.titre}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")

if __name__ == "__main__":
    test_formulaire_message()