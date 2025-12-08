from django import forms
from django.core.exceptions import ValidationError
from .models import Paiement, Remboursement
from assureur.models import BonPriseEnCharge

class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = [
            'bon', 'montant', 'mode_paiement', 'statut',
            'numero_transaction', 'banque', 'date_valeur', 'notes'
        ]
        widgets = {
            'bon': forms.Select(attrs={'class': 'form-select'}),
            'montant': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'mode_paiement': forms.Select(attrs={'class': 'form-select'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'numero_transaction': forms.TextInput(attrs={'class': 'form-control'}),
            'banque': forms.TextInput(attrs={'class': 'form-control'}),
            'date_valeur': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les bons éligibles pour paiement
        self.fields['bon'].queryset = BonPriseEnCharge.objects.filter(
            statut='VALIDE'
        ).select_related('membre', 'soin')

    def clean_montant(self):
        montant = self.cleaned_data.get('montant')
        bon = self.cleaned_data.get('bon')
        
        if bon and montant:
            if montant > bon.montant_prise_en_charge:
                raise ValidationError(
                    f"Le montant ne peut pas dépasser {bon.montant_prise_en_charge} FCFA "
                    f"(montant du bon)"
                )
            if montant <= 0:
                raise ValidationError("Le montant doit être positif")
        
        return montant

    def clean(self):
        cleaned_data = super().clean()
        bon = cleaned_data.get('bon')
        statut = cleaned_data.get('statut')
        
        if bon and statut == 'PAYE':
            # Vérifier s'il n'y a pas déjà un paiement payé pour ce bon
            paiement_existant = Paiement.objects.filter(
                bon=bon, 
                statut='PAYE'
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if paiement_existant.exists():
                raise ValidationError(
                    "Un paiement a déjà été effectué pour ce bon de prise en charge."
                )
        
        return cleaned_data


class RemboursementForm(forms.ModelForm):
    class Meta:
        model = Remboursement
        fields = ['montant_rembourse', 'motif']
        widgets = {
            'montant_rembourse': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'motif': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Détaillez le motif du remboursement...'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.paiement = kwargs.pop('paiement', None)
        super().__init__(*args, **kwargs)
        
        if self.paiement:
            self.fields['montant_rembourse'].initial = self.paiement.montant

    def clean_montant_rembourse(self):
        montant = self.cleaned_data.get('montant_rembourse')
        
        if self.paiement and montant:
            if montant > self.paiement.montant:
                raise ValidationError(
                    f"Le montant remboursé ne peut pas dépasser {self.paiement.montant} FCFA "
                    f"(montant initial du paiement)"
                )
        
        return montant


class PaiementFiltreForm(forms.Form):
    STATUT_CHOICES = [('', 'Tous les statuts')] + Paiement.STATUT_CHOICES
    MODE_PAIEMENT_CHOICES = [('', 'Tous les modes')] + Paiement.MODE_PAIEMENT_CHOICES

    statut = forms.ChoiceField(
        choices=STATUT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    mode_paiement = forms.ChoiceField(
        choices=MODE_PAIEMENT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    reference = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Référence...'
        })
    )