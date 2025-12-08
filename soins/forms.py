# soins/forms.py
from django import forms
from django.apps import apps

class SoinForm(forms.ModelForm):
    # CORRECTION : Utiliser 'membres.Membre'
    patient = forms.ModelChoiceField(
        queryset=apps.get_model('membres', 'Membre').objects.all(),
        label="Patient"
    )
    
    medecin = forms.ModelChoiceField(
        queryset=apps.get_model('auth', 'User').objects.filter(groups__name='Medecin'),
        label="Médecin"
    )
    
    class Meta:
        model = apps.get_model('soins', 'Soin')
        fields = [
            'patient', 'type_soin', 'date_realisation', 'medecin',
            'diagnostic', 'observations', 'duree_sejour',
            'cout_estime', 'taux_prise_charge'
        ]
        widgets = {
            'date_realisation': forms.DateInput(attrs={'type': 'date'}),
            'diagnostic': forms.Textarea(attrs={'rows': 3}),
            'observations': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('soins', 'Prescription')
        fields = ['medicament', 'posologie', 'duree_traitement', 'instructions']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class DocumentSoinForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('soins', 'DocumentSoin')
        fields = ['type_document', 'fichier', 'nom']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})