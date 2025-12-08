# forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, time
import json

from .models import (
    Medecin, SpecialiteMedicale, EtablissementMedical, 
    DisponibiliteMedecin, Consultation, Ordonnance
)
from soins.models import BonDeSoin, TypeSoin
from membres.models import Membre

class MedecinProfileForm(forms.ModelForm):
    """Formulaire pour le profil médecin"""
    first_name = forms.CharField(
        label='Prénom',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Nom',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Medecin
        fields = [
            'first_name', 'last_name', 'email', 'telephone_pro', 
            'annees_experience', 'tarif_consultation', 'specialite',
            'etablissement', 'actif', 'disponible'
        ]
        widgets = {
            'telephone_pro': forms.TextInput(attrs={'class': 'form-control'}),
            'annees_experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'tarif_consultation': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'specialite': forms.Select(attrs={'class': 'form-control'}),
            'etablissement': forms.Select(attrs={'class': 'form-control'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        medecin = super().save(commit=False)
        if commit:
            # Mettre à jour les informations de l'utilisateur
            medecin.user.first_name = self.cleaned_data['first_name']
            medecin.user.last_name = self.cleaned_data['last_name']
            medecin.user.email = self.cleaned_data['email']
            medecin.user.save()
            medecin.save()
        return medecin

class BonDeSoinFilterForm(forms.Form):
    """Formulaire de filtrage pour les bons de soin"""
    STATUT_CHOICES = [
        ('', 'Tous les statuts'),
        ('BROUILLON', 'Brouillon'),
        ('EN_ATTENTE', 'En attente'),
        ('VALIDE', 'Validé'),
        ('REFUSE', 'Refusé'),
    ]
    
    statut = forms.ChoiceField(
        choices=STATUT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    patient = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom du patient...'
        })
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

class BonDeSoinValidationForm(forms.ModelForm):
    """Formulaire pour valider/refuser un bon de soin"""
    motif_refus = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Motif du refus...'
        }),
        label="Motif de refus"
    )
    
    class Meta:
        model = BonDeSoin
        fields = ['motif_refus']

class ConsultationForm(forms.ModelForm):
    """Formulaire pour les consultations"""
    class Meta:
        model = Consultation
        fields = [
            'membre', 'type_consultation', 'date_consultation',
            'heure_consultation', 'duree', 'notes', 'symptomes',
            'diagnostic', 'traitement_prescrit'
        ]
        widgets = {
            'membre': forms.Select(attrs={'class': 'form-control'}),
            'type_consultation': forms.Select(attrs={'class': 'form-control'}),
            'date_consultation': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'heure_consultation': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'duree': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Durée en minutes'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notes sur la consultation...'
            }),
            'symptomes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Symptômes décrits par le patient...'
            }),
            'diagnostic': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Diagnostic établi...'
            }),
            'traitement_prescrit': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Traitement prescrit...'
            }),
        }
    
    def clean_date_consultation(self):
        date_consultation = self.cleaned_data.get('date_consultation')
        if date_consultation and date_consultation < timezone.now().date():
            raise ValidationError("La date de consultation ne peut pas être dans le passé.")
        return date_consultation

class ConsultationFilterForm(forms.Form):
    """Formulaire de filtrage pour les consultations"""
    STATUT_CHOICES = [
        ('', 'Tous les statuts'),
        ('PLANIFIEE', 'Planifiée'),
        ('EN_COURS', 'En cours'),
        ('TERMINEE', 'Terminée'),
        ('ANNULEE', 'Annulée'),
    ]
    
    TYPE_CONSULTATION_CHOICES = [
        ('', 'Tous les types'),
        ('GENERALE', 'Consultation générale'),
        ('SPECIALISEE', 'Consultation spécialisée'),
        ('SUIVI', 'Consultation de suivi'),
        ('URGENCE', 'Urgence'),
    ]
    
    statut = forms.ChoiceField(
        choices=STATUT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    patient = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom du patient...'
        })
    )
    type_consult = forms.ChoiceField(
        choices=TYPE_CONSULTATION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class OrdonnanceForm(forms.ModelForm):
    """Formulaire principal pour les ordonnances"""
    class Meta:
        model = Ordonnance
        fields = [
            'patient', 'type_ordonnance', 'diagnostic', 'renouvelable',
            'nombre_renouvellements', 'est_urgent', 'notes', 'consultation'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'type_ordonnance': forms.Select(attrs={'class': 'form-control'}),
            'diagnostic': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Diagnostic principal...'
            }),
            'renouvelable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nombre_renouvellements': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 12
            }),
            'est_urgent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Notes supplémentaires...'
            }),
            'consultation': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.medecin = kwargs.pop('medecin', None)
        super().__init__(*args, **kwargs)
        
        # Filtrer les consultations par médecin
        if self.medecin:
            self.fields['consultation'].queryset = Consultation.objects.filter(
                medecin=self.medecin
            )

class MedicamentForm(forms.Form):
    """Formulaire pour un médicament (utilisé en JavaScript)"""
    nom = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom du médicament'
        })
    )
    posologie = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Posologie (ex: 1 comprimé 3 fois par jour)'
        })
    )
    duree_traitement = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Durée (ex: 7 jours)'
        })
    )

class OrdonnanceFilterForm(forms.Form):
    """Formulaire de filtrage pour les ordonnances"""
    STATUT_CHOICES = [
        ('', 'Tous les statuts'),
        ('ACTIVE', 'Active'),
        ('EXPIREE', 'Expirée'),
        ('ANNULEE', 'Annulée'),
    ]
    
    statut = forms.ChoiceField(
        choices=STATUT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    patient = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom du patient...'
        })
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

class DisponibiliteMedecinForm(forms.ModelForm):
    """Formulaire pour les disponibilités du médecin"""
    class Meta:
        model = DisponibiliteMedecin
        fields = ['jour_semaine', 'heure_debut', 'heure_fin', 'actif']
        widgets = {
            'jour_semaine': forms.Select(attrs={'class': 'form-control'}),
            'heure_debut': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'heure_fin': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        heure_debut = cleaned_data.get('heure_debut')
        heure_fin = cleaned_data.get('heure_fin')
        
        if heure_debut and heure_fin:
            if heure_debut >= heure_fin:
                raise ValidationError("L'heure de fin doit être après l'heure de début.")
        
        return cleaned_data

class StatistiquesFilterForm(forms.Form):
    """Formulaire pour filtrer les statistiques"""
    PERIODE_CHOICES = [
        (7, '7 derniers jours'),
        (30, '30 derniers jours'),
        (90, '3 derniers mois'),
        (180, '6 derniers mois'),
        (365, '1 an'),
    ]
    
    periode = forms.ChoiceField(
        choices=PERIODE_CHOICES,
        initial=30,
        widget=forms.Select(attrs={'class': 'form-control'})
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

class RendezVousStatutForm(forms.Form):
    """Formulaire pour modifier le statut d'un rendez-vous"""
    STATUT_CHOICES = [
        ('PLANIFIEE', 'Planifiée'),
        ('EN_COURS', 'En cours'),
        ('TERMINEE', 'Terminée'),
        ('ANNULEE', 'Annulée'),
    ]
    
    statut = forms.ChoiceField(
        choices=STATUT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )