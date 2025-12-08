# correcteur_formulaire_urgence.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def correcteur_formulaire_urgence():
    """Correcteur d'urgence pour forcer la méthode save() corrigée"""
    print("=== CORRECTEUR URGENCE FORMULAIRE ===")
    
    # Réimporter le formulaire pour forcer la mise à jour
    import importlib
    import communication.forms
    importlib.reload(communication.forms)
    
    from communication.forms import MessageForm
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Forcer la méthode save corrigée
    def save_corrigee(self, commit=True):
        from communication.utils import get_or_create_conversation
        from communication.models import PieceJointe
        
        print("🔧 Utilisation de save() corrigée")
        
        # Appeler la méthode save originale mais sans commit
        message = super(MessageForm, self).save(commit=False)
        
        # Assigner l'expéditeur
        if hasattr(self, 'expediteur') and self.expediteur:
            message.expediteur = self.expediteur
            print(f"✅ Expéditeur assigné: {self.expediteur.username}")
        
        # Créer automatiquement une conversation
        if hasattr(message, 'expediteur') and hasattr(message, 'destinataire'):
            if message.expediteur and message.destinataire:
                conversation = get_or_create_conversation(message.expediteur, message.destinataire)
                message.conversation = conversation
                print(f"✅ Conversation assignée: {conversation.id}")
            else:
                print("❌ Expéditeur ou destinataire manquant")
        else:
            print("❌ Champs expediteur/destinataire manquants dans le modèle")
        
        if commit:
            try:
                message.save()
                print(f"✅ Message sauvegardé: {message.id}")
                
                # Gérer les pièces jointes
                pieces_jointes = self.cleaned_data.get('pieces_jointes', [])
                if pieces_jointes:
                    if not isinstance(pieces_jointes, list):
                        pieces_jointes = [pieces_jointes]
                    
                    for fichier in pieces_jointes:
                        if fichier:
                            PieceJointe.objects.create(
                                message=message,
                                fichier=fichier,
                                nom_original=fichier.name,
                                taille=fichier.size
                            )
                            print(f"✅ Pièce jointe ajoutée: {fichier.name}")
            except Exception as e:
                print(f"❌ Erreur sauvegarde: {e}")
                raise
        
        return message
    
    # Remplacer la méthode save
    MessageForm.save = save_corrigee
    print("✅ Méthode save() FORCÉE avec correction conversation")
    
    # Test immédiat
    expediteur = User.objects.filter(username='assureur_test').first()
    destinataire = User.objects.filter(username='koffitanoh').first()
    
    if expediteur and destinataire:
        test_data = {
            'destinataire': destinataire.id,
            'titre': 'Test correcteur urgence',
            'contenu': 'Ce message teste le correcteur d\'urgence',
            'type_message': 'MESSAGE',
        }
        
        form = MessageForm(data=test_data, expediteur=expediteur)
        
        if form.is_valid():
            try:
                message = form.save()
                print("🎉 SUCCÈS: Message créé avec le correcteur d'urgence!")
                print(f"   - ID: {message.id}")
                print(f"   - Conversation: {message.conversation.id}")
                print(f"   - De: {message.expediteur.username}")
                print(f"   - À: {message.destinataire.username}")
            except Exception as e:
                print(f"❌ Échec même avec correcteur: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("❌ Formulaire invalide avec correcteur:")
            for field, errors in form.errors.items():
                print(f"   - {field}: {errors}")
    else:
        print("❌ Utilisateurs non trouvés")

if __name__ == "__main__":
    correcteur_formulaire_urgence()