# verification_formulaire_corrige.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_formulaire_corrige():
    print("=== VÉRIFICATION FORMULAIRE CORRIGÉ ===")
    
    try:
        from communication.forms import MessageForm
        form = MessageForm()
        
        # Vérifier si la méthode save est celle de la classe parente ou notre surcharge
        import inspect
        save_method = inspect.getsource(form.save)
        if 'get_or_create_conversation' in save_method:
            print("✅ Formulaire utilise la méthode save() corrigée avec gestion de conversation")
        else:
            print("❌ Formulaire n'utilise PAS la méthode save() corrigée")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def corriger_formulaire_manuellement():
    """Correction manuelle du formulaire si nécessaire"""
    print("\n=== CORRECTION MANUELLE FORMULAIRE ===")
    
    forms_path = 'communication/forms.py'
    
    # Lire le fichier
    with open(forms_path, 'r') as f:
        content = f.read()
    
    # Vérifier si la méthode save corrigée existe
    if 'def save(self, commit=True):' in content and 'get_or_create_conversation' in content:
        print("✅ Méthode save() corrigée déjà présente")
        return
    
    # Ajouter la méthode save manuellement
    save_method = '''
    def save(self, commit=True):
        """Surcharge de la méthode save pour gérer automatiquement la conversation et l'expéditeur"""
        from .utils import get_or_create_conversation
        
        message = super().save(commit=False)
        
        # Assigner l'expéditeur
        if self.expediteur:
            message.expediteur = self.expediteur
        
        # Créer automatiquement une conversation si elle n'existe pas
        if hasattr(message, 'expediteur') and hasattr(message, 'destinataire'):
            if message.expediteur and message.destinataire:
                conversation = get_or_create_conversation(
                    message.expediteur, 
                    message.destinataire
                )
                message.conversation = conversation
        
        if commit:
            message.save()
            
            # Gérer les pièces jointes après sauvegarde du message
            pieces_jointes = self.cleaned_data.get('pieces_jointes', [])
            if pieces_jointes:
                if not isinstance(pieces_jointes, list):
                    pieces_jointes = [pieces_jointes]
                
                for fichier in pieces_jointes:
                    if fichier:  # Vérifier que le fichier existe
                        from .models import PieceJointe
                        PieceJointe.objects.create(
                            message=message,
                            fichier=fichier,
                            nom_original=fichier.name,
                            taille=fichier.size
                        )
            
        return message
    '''
    
    # Trouver la classe MessageForm et insérer la méthode save après __init__
    if 'class MessageForm' in content:
        # Remplacer la méthode save existante ou l'ajouter
        if 'def save(self, commit=True):' in content:
            # Trouver le début et la fin de la méthode save existante
            start = content.find('def save(self, commit=True):')
            # Trouver la fin de la méthode (niveau d'indentation)
            lines = content[start:].split('\n')
            indent_level = len(lines[0]) - len(lines[0].lstrip())
            method_lines = []
            for i, line in enumerate(lines):
                if i > 0 and len(line) - len(line.lstrip()) <= indent_level and line.strip() and not line.startswith(' ' * (indent_level + 4)):
                    break
                method_lines.append(line)
            old_method = '\n'.join(method_lines)
            
            content = content.replace(old_method, save_method.strip())
            print("✅ Méthode save() remplacée")
        else:
            # Ajouter la méthode save après __init__
            init_end = content.find('def __init__')
            if init_end != -1:
                # Trouver la fin de la méthode __init__
                lines = content[init_end:].split('\n')
                indent_level = len(lines[0]) - len(lines[0].lstrip())
                method_lines = []
                for i, line in enumerate(lines):
                    if i > 0 and len(line) - len(line.lstrip()) <= indent_level and line.strip() and not line.startswith(' ' * (indent_level + 4)):
                        break
                    method_lines.append(line)
                init_method = '\n'.join(method_lines)
                
                # Insérer save après __init__
                content = content.replace(init_method, init_method + '\n\n    ' + save_method)
                print("✅ Méthode save() ajoutée")
        
        # Écrire le fichier corrigé
        with open(forms_path, 'w') as f:
            f.write(content)
        print("✅ Fichier forms.py mis à jour")
    
    else:
        print("❌ Classe MessageForm non trouvée")

if __name__ == "__main__":
    verifier_formulaire_corrige()
    corriger_formulaire_manuellement()