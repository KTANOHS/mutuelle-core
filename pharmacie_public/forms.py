# pharmacie_public/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PharmaciePublic

class InscriptionPharmaciePublicForm(UserCreationForm):
    nom_pharmacie = forms.CharField(max_length=255, label="Nom de la pharmacie")
    adresse = forms.CharField(widget=forms.Textarea, label="Adresse complète")
    ville = forms.CharField(max_length=100)
    code_postal = forms.CharField(max_length=10)
    telephone = forms.CharField(max_length=20)
    email = forms.EmailField()
    type_pharmacie = forms.ChoiceField(choices=PharmaciePublic.TYPE_PHARMACIE, label="Type de pharmacie")
    horaires_ouverture = forms.CharField(
        widget=forms.Textarea, 
        label="Horaires d'ouverture",
        help_text="Ex: Lun-Ven: 08:00-19:00, Sam: 08:00-12:00",
        initial="Lun-Ven: 08:00-19:00, Sam: 08:00-12:00"
    )
    partenaire_mutuelle = forms.BooleanField(
        required=False, 
        label="Souhaitez-vous devenir partenaire de la mutuelle ?"
    )
    numero_agrement = forms.CharField(
        max_length=50, 
        required=False, 
        label="Numéro d'agrément (si partenaire)"
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            
            # Générer un numéro de pharmacie unique
            import random
            numero_pharmacie = f"PHP{random.randint(10000, 99999)}"
            
            pharmacie = PharmaciePublic.objects.create(
                user=user,
                nom_pharmacie=self.cleaned_data['nom_pharmacie'],
                adresse=self.cleaned_data['adresse'],
                ville=self.cleaned_data['ville'],
                code_postal=self.cleaned_data['code_postal'],
                telephone=self.cleaned_data['telephone'],
                email=self.cleaned_data['email'],
                type_pharmacie=self.cleaned_data['type_pharmacie'],
                horaires_ouverture=self.cleaned_data['horaires_ouverture'],
                partenaire_mutuelle=self.cleaned_data['partenaire_mutuelle'],
                numero_agrement=self.cleaned_data['numero_agrement'] or ''
            )
        return user

class RecherchePharmacieForm(forms.Form):
    ville = forms.CharField(max_length=100, required=False, label="Ville")
    code_postal = forms.CharField(max_length=10, required=False, label="Code postal")
    type_pharmacie = forms.ChoiceField(
        choices=[('', 'Tous types')] + PharmaciePublic.TYPE_PHARMACIE, 
        required=False,
        label="Type de pharmacie"
    )
    de_garde = forms.BooleanField(required=False, label="De garde uniquement")
    partenaire_mutuelle = forms.BooleanField(required=False, label="Partenaire mutuelle uniquement")

class MedicamentPublicForm(forms.ModelForm):
    class Meta:
        from .models import MedicamentPublic
        model = MedicamentPublic
        fields = ['nom', 'principe_actif', 'dosage', 'forme_galenique', 
                 'laboratoire', 'categorie', 'prix', 'stock', 'necessite_ordonnance']