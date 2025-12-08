# communication/forms.py - FORMULAIRE CORRIGÉ
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['type_message', 'destinataire', 'titre', 'contenu']  # 'titre' au lieu de 'sujet'
        
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