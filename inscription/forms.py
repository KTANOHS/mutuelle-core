# inscription/forms.py
from django import forms
from membres.models import Membre
from django.contrib.auth.models import User

class DemandeRappelForm(forms.Form):
    """Formulaire pour demander un rappel téléphonique"""
    nom = forms.CharField(
        label="Nom",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom'
        })
    )
    
    prenom = forms.CharField(
        label="Prénom",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre prénom'
        })
    )
    
    telephone = forms.CharField(
        label="Numéro de téléphone",
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '07 00 00 00 00'
        })
    )
    
    email = forms.EmailField(
        label="Email",
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre@email.fr'
        })
    )
    
    creneau_horaire = forms.ChoiceField(
        label="Créneau horaire préféré",
        choices=[
            ('', 'Sélectionnez un créneau'),
            ('9-12', '9h-12h'),
            ('12-14', '12h-14h'),
            ('14-16', '14h-16h'),
            ('16-18', '16h-18h'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    message = forms.CharField(
        label="Informations complémentaires",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Avez-vous des questions spécifiques ?'
        })
    )
    
    consentement = forms.BooleanField(
        label="J'accepte d'être contacté par téléphone pour mon inscription",
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )