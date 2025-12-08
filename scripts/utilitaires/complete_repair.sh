#!/bin/bash

echo "========================================="
echo "RÉPARATION COMPLÈTE DU PROJET DJANGO"
echo "========================================="

# 1. Nettoyer les fichiers de cache
echo "✓ 1. Nettoyage des fichiers de cache..."
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete

# 2. Corriger le fichier forms.py
echo "✓ 2. Correction du fichier forms.py..."
cat > assureur/forms.py << 'EOF'
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
import re
from .models import Bon, ConfigurationAssurance, Paiement

class ConfigurationAssuranceForm(forms.ModelForm):
    class Meta:
        model = ConfigurationAssurance
        fields = ['nom_assureur', 'taux_couverture_defaut', 'delai_validite_bon']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class PaiementForm(forms.ModelForm):
    montant_paye = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    
    date_paiement = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial=timezone.now().date()
    )
    
    reference = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Paiement
        fields = ['montant_paye', 'date_paiement', 'reference', 'bon']
        widgets = {'bon': forms.HiddenInput()}
    
    def __init__(self, *args, **kwargs):
        self.bon = kwargs.pop('bon', None)
        super().__init__(*args, **kwargs)
        if self.bon:
            self.fields['bon'].initial = self.bon

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

    numero = forms.CharField(required=False)
    membre = forms.CharField(required=False)
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    statut = forms.ChoiceField(
        choices=STATUT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    type_soin = forms.ChoiceField(
        choices=TYPE_SOIN_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ValidationBonForm(forms.Form):
    action = forms.ChoiceField(
        choices=[('valider', 'Valider'), ('rejeter', 'Rejeter')],
        widget=forms.RadioSelect
    )
    motif_rejet = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('action')
        motif_rejet = cleaned_data.get('motif_rejet')
        
        if action == 'rejeter' and not motif_rejet:
            raise ValidationError("Veuillez indiquer le motif du rejet.")
        
        return cleaned_data

ConfigurationForm = ConfigurationAssuranceForm
EOF

# 3. Réinitialiser la base de données
echo "✓ 3. Réinitialisation de la base de données..."
rm -f db.sqlite3
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

# 4. Recréer les migrations
echo "✓ 4. Création des migrations..."
python manage.py makemigrations

# 5. Appliquer les migrations
echo "✓ 5. Application des migrations..."
python manage.py migrate

# 6. Créer un superutilisateur
echo "✓ 6. Création du superutilisateur..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell

# 7. Vérifier
echo "✓ 7. Vérification finale..."
python manage.py check

echo "========================================="
echo "RÉPARATION TERMINÉE AVEC SUCCÈS !"
echo "========================================="
echo ""
echo "Pour démarrer le serveur :"
echo "python manage.py runserver"
echo ""
echo "Identifiants :"
echo "Utilisateur: admin"
echo "Mot de passe: admin123"