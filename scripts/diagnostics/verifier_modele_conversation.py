# verifier_modele_conversation.py
import os
import django
import sys

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from communication.models import Conversation

def verifier_champs_conversation():
    print("🔍 VÉRIFICATION DU MODÈLE CONVERSATION")
    print("=" * 50)
    
    # Vérifier les champs existants
    champs = [f.name for f in Conversation._meta.get_fields()]
    print("📋 Champs disponibles dans Conversation:")
    for champ in champs:
        print(f"   • {champ}")
    
    # Vérifier si on peut créer une instance
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.first()
        
        if user:
            conversations = Conversation.objects.filter(participants=user)[:1]
            if conversations.exists():
                conv = conversations.first()
                print(f"\n✅ Test réussi - Conversation trouvée: {conv}")
                print(f"   Date création: {conv.date_creation}")
                print(f"   Date modification: {conv.date_modification}")
            else:
                print("\n⚠️  Aucune conversation trouvée pour l'utilisateur")
        else:
            print("\n⚠️  Aucun utilisateur trouvé pour le test")
            
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")

if __name__ == "__main__":
    verifier_champs_conversation()