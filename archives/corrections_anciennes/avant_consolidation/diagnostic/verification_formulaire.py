# verification_formulaire.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_formulaire():
    print("=== VÉRIFICATION FORMULAIRE MESSAGE ===")
    
    try:
        from communication.forms import MessageForm
        print("✅ MessageForm existe dans communication.forms")
        
        # Tester l'import du modèle
        from communication.models import Message
        print("✅ Modèle Message importé avec succès")
        
        # Vérifier les champs du formulaire
        form = MessageForm()
        print("✅ Formulaire instancié")
        print(f"Champs du formulaire: {list(form.fields.keys())}")
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("Création du formulaire MessageForm...")
        creer_formulaire()
    except Exception as e:
        print(f"❌ Autre erreur: {e}")

def creer_formulaire():
    """Crée le fichier forms.py s'il n'existe pas"""
    forms_content = '''# communication/forms.py
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['type_message', 'destinataire', 'titre', 'contenu']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre le champ type_message obligatoire avec une valeur par défaut
        self.fields['type_message'].required = True
        self.fields['type_message'].initial = 'MESSAGE'  # Valeur par défaut
        self.fields['type_message'].widget.attrs.update({
            'class': 'form-control',
            'required': 'required'
        })
        
        self.fields['titre'].required = True
        self.fields['titre'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Sujet du message'
        })
        
        self.fields['contenu'].widget.attrs.update({
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Contenu du message'
        })
        
        self.fields['destinataire'].widget.attrs.update({
            'class': 'form-control'
        })
'''
    
    try:
        with open('communication/forms.py', 'w') as f:
            f.write(forms_content)
        print("✅ Fichier communication/forms.py créé avec succès")
    except Exception as e:
        print(f"❌ Erreur création fichier: {e}")

if __name__ == "__main__":
    verifier_formulaire()