from django import forms
from django.core.exceptions import ValidationError
from soins.models import Ordonnance

class ValiderOrdonnanceForm(forms.ModelForm):
    """Formulaire pour valider une ordonnance"""
    notes_pharmacien = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Notes optionnelles du pharmacien...',
            'class': 'form-control'
        }),
        required=False,
        label='Notes du pharmacien'
    )
    
    class Meta:
        model = Ordonnance
        fields = []  # Aucun champ du modèle n'est édité directement
        
    def clean(self):
        cleaned_data = super().clean()
        
        # Vérifier que l'ordonnance n'est pas déjà validée
        if self.instance and self.instance.statut == 'valide':
            raise ValidationError("Cette ordonnance est déjà validée.")
            
        return cleaned_data

class RechercheOrdonnanceForm(forms.Form):
    """Formulaire de recherche d'ordonnances"""
    STATUT_CHOICES = [
        ('', 'Tous les statuts'),
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
        ('termine', 'Terminé'),
    ]
    
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Rechercher par patient, médecin ou médicament...',
            'class': 'form-control'
        }),
        label='Recherche'
    )
    
    statut = forms.ChoiceField(
        choices=STATUT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Statut'
    )
    
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='Date de début'
    )
    
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='Date de fin'
    )

class FiltreOrdonnanceForm(forms.Form):
    """Formulaire de filtrage des ordonnances"""
    TRI_CHOICES = [
        ('-date_creation', 'Plus récentes'),
        ('date_creation', 'Plus anciennes'),
        ('medicament', 'Médicament (A-Z)'),
        ('-medicament', 'Médicament (Z-A)'),
    ]
    
    tri = forms.ChoiceField(
        choices=TRI_CHOICES,
        required=False,
        initial='-date_creation',
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Trier par'
    )
    
    items_par_page = forms.ChoiceField(
        choices=[('10', '10'), ('25', '25'), ('50', '50'), ('100', '100')],
        required=False,
        initial='25',
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Items par page'
    )

class PharmacienProfileForm(forms.ModelForm):
    """Formulaire de profil du pharmacien"""
    class Meta:
        from .models import Pharmacien
        model = Pharmacien
        fields = ['numero_pharmacien', 'nom_pharmacie', 'adresse_pharmacie', 'telephone']
        
        widgets = {
            'numero_pharmacien': forms.TextInput(attrs={'class': 'form-control'}),
            'nom_pharmacie': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse_pharmacie': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        # Validation basique du numéro de téléphone
        if telephone and not telephone.replace(' ', '').replace('+', '').isdigit():
            raise ValidationError("Le numéro de téléphone ne doit contenir que des chiffres, espaces et le signe +.")
        return telephone