# ajax_forms.py
from django import forms
import json

class AjaxOrdonnanceForm(forms.Form):
    """Formulaire AJAX pour la création d'ordonnance"""
    patient = forms.IntegerField()  # ID du patient
    type_ordonnance = forms.CharField(max_length=50)
    diagnostic = forms.CharField(required=False)
    medicaments = forms.CharField()  # JSON string
    renouvelable = forms.BooleanField(required=False)
    nombre_renouvellements = forms.IntegerField(required=False, min_value=0)
    est_urgent = forms.BooleanField(required=False)
    notes = forms.CharField(required=False)
    consultation = forms.IntegerField(required=False)  # ID de consultation
    
    def clean_medicaments(self):
        medicaments_json = self.cleaned_data['medicaments']
        try:
            medicaments = json.loads(medicaments_json)
            if not isinstance(medicaments, list):
                raise forms.ValidationError("Format de médicaments invalide")
            return medicaments
        except json.JSONDecodeError:
            raise forms.ValidationError("Format JSON invalide pour les médicaments")

class AjaxToggleDisponibiliteForm(forms.Form):
    """Formulaire pour basculer la disponibilité"""
    disponible = forms.BooleanField(required=False)

class AjaxMedicamentForm(forms.Form):
    """Formulaire pour ajouter un médicament via AJAX"""
    nom = forms.CharField(max_length=200)
    posologie = forms.CharField(max_length=200)
    duree_traitement = forms.CharField(max_length=100)