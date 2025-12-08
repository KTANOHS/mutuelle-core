# test_systeme_complet.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_systeme_complet():
    from django.contrib.auth import get_user_model
    from communication.models import Message
    from django.contrib.auth.models import Group
    
    User = get_user_model()
    
    print("=== TEST SYSTÈME COMPLET ===")
    
    # 1. Vérifier l'utilisateur assureur_test
    assureur = User.objects.filter(username='assureur_test').first()
    if assureur:
        print("✅ Utilisateur assureur_test trouvé")
        print(f"   - Groupes: {[g.name for g in assureur.groups.all()]}")
    else:
        print("❌ Utilisateur assureur_test non trouvé")
        return
    
    # 2. Vérifier un destinataire
    destinataire = User.objects.filter(groups__name='Agent').first()
    if not destinataire:
        destinataire = User.objects.exclude(username='assureur_test').first()
    
    if destinataire:
        print(f"✅ Destinataire trouvé: {destinataire.username}")
    else:
        print("❌ Aucun destinataire trouvé")
        return
    
    # 3. Créer un message directement via le modèle
    try:
        message = Message.objects.create(
            expediteur=assureur,
            destinataire=destinataire,
            titre="Test système complet",
            contenu="Ce message teste le système de communication",
            type_message="MESSAGE"
        )
        print("✅ Message créé directement via modèle")
        print(f"   - ID: {message.id}")
        print(f"   - Titre: {message.titre}")
        print(f"   - Type: {message.type_message}")
        print(f"   - De: {message.expediteur.username} → À: {message.destinataire.username}")
    except Exception as e:
        print(f"❌ Erreur création message: {e}")
    
    # 4. Vérifier le comptage
    messages_count = Message.objects.count()
    print(f"📊 Total messages dans le système: {messages_count}")

if __name__ == "__main__":
    test_systeme_complet()