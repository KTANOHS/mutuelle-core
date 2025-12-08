from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
import re
from .models import Bon, ConfigurationAssurance, Paiement, Soin
from agents.models import Membre


class ConfigurationAssuranceForm(forms.ModelForm):
    class Meta:
        model = ConfigurationAssurance
        fields = ['nom_assureur', 'taux_couverture_defaut', 'delai_validite_bon']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

# CORRECTION : Formulaire adapté au modèle Paiement réel

class PaiementForm(forms.ModelForm):
    """Formulaire complet pour enregistrer un paiement - VERSION CORRIGÉE"""
    
    # SUPPRIMEZ la redéfinition manuelle de mode_paiement et statut
    # Utilisez plutôt le modèle pour définir les choix
    
    # Champ pour sélectionner un soin (optionnel)
    soin = forms.ModelChoiceField(
        queryset=Soin.objects.all(),
        required=False,
        label="Soin associé",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Sélectionner un soin (optionnel)'
        })
    )
    
    # Champs personnalisés avec widgets (gardez seulement les champs personnalisés)
    membre = forms.ModelChoiceField(
        queryset=Membre.objects.filter(statut='actif'),
        label="Membre",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Sélectionner un membre'
        })
    )
    
    montant = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Montant (FCFA)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0'
        })
    )
    
    date_paiement = forms.DateField(
        label="Date de paiement",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        initial=timezone.now().date
    )
    
    reference = forms.CharField(
        required=False,
        label="Référence",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Référence du paiement'
        }),
        help_text="Référence unique du paiement (générée automatiquement si vide)"
    )
    
    banque = forms.CharField(
        required=False,
        max_length=100,
        label="Banque",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom de la banque'
        })
    )
    
    numero_transaction = forms.CharField(
        required=False,
        max_length=50,
        label="Numéro de transaction",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'N° de transaction'
        })
    )
    
    numero_compte = forms.CharField(
        required=False,
        max_length=50,
        label="Numéro de compte",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'N° de compte bancaire'
        })
    )
    
    notes = forms.CharField(
        required=False,
        label="Notes",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Notes supplémentaires...'
        })
    )
    
    class Meta:
        model = Paiement
        fields = [
            'membre', 'soin', 'montant', 'date_paiement', 'mode_paiement',
            'statut', 'reference', 'banque', 'numero_transaction', 
            'numero_compte', 'notes'
        ]
        # Supprimez les widgets redéfinis pour mode_paiement et statut
        # Ils utiliseront automatiquement les choix du modèle
    
    def __init__(self, *args, **kwargs):
        self.bon = kwargs.pop('bon', None)
        super().__init__(*args, **kwargs)
        
        # Personnalisez les widgets pour mode_paiement et statut si nécessaire
        self.fields['mode_paiement'].widget.attrs.update({'class': 'form-control'})
        self.fields['statut'].widget.attrs.update({'class': 'form-control'})
        
        # Si un bon est fourni, filtrer les membres et soins
        if self.bon:
            self.fields['membre'].initial = self.bon.membre
            self.fields['membre'].widget.attrs['readonly'] = True
            
            self.fields['soin'].queryset = Soin.objects.filter(bon=self.bon)
            
            if self.bon.montant_total:
                self.fields['montant'].initial = self.bon.montant_total
        
        # Définir le queryset initial pour les soins
        if 'soin' in self.fields:
            self.fields['soin'].queryset = Soin.objects.filter(
                statut='valide'
            ).select_related('membre').order_by('-date_soin')
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Générer une référence automatique si non fournie
        if not cleaned_data.get('reference'):
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            cleaned_data['reference'] = f"PAY-{timestamp}"
        
        # Validation supplémentaire
        montant = cleaned_data.get('montant')
        if montant and montant <= 0:
            raise forms.ValidationError("Le montant doit être supérieur à zéro.")
        
        return cleaned_data




class FiltreBonsForm(forms.Form):
    STATUT_CHOICES = [
        ('', 'Tous les statuts'),
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
        ('paye', 'Payé'),
    ]
    
    TYPE_SOIN_CHOICES = [
        ('', 'Tous les types'),
        ('consultation', 'Consultation'),
        ('hospitalisation', 'Hospitalisation'),
        ('pharmacie', 'Pharmacie'),
        ('radiologie', 'Radiologie'),
        ('laboratoire', 'Laboratoire'),
        ('dentaire', 'Dentaire'),
        ('optique', 'Optique'),
    ]

    numero = forms.CharField(required=False, label="Numéro de bon")
    membre = forms.CharField(required=False, label="Nom du membre")
    date_debut = forms.DateField(
        required=False, 
        label="Date de début",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_fin = forms.DateField(
        required=False, 
        label="Date de fin",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    statut = forms.ChoiceField(
        choices=STATUT_CHOICES, 
        required=False, 
        label="Statut",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    type_soin = forms.ChoiceField(
        choices=TYPE_SOIN_CHOICES, 
        required=False, 
        label="Type de soin",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ValidationBonForm(forms.Form):
    action = forms.ChoiceField(
        choices=[('valider', 'Valider'), ('rejeter', 'Rejeter')],
        widget=forms.RadioSelect,
        label="Action"
    )
    motif_rejet = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label="Motif du rejet (si rejet)"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('action')
        motif_rejet = cleaned_data.get('motif_rejet')
        
        if action == 'rejeter' and not motif_rejet:
            raise ValidationError("Veuillez indiquer le motif du rejet.")
        
        return cleaned_data

# Alias pour compatibilité
ConfigurationForm = ConfigurationAssuranceForm