from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date
import re
from core.utils import generer_numero_unique
from .models import Membre, Bon, LigneBon
from django.core.validators import FileExtensionValidator
import os


class InscriptionMembreForm(forms.ModelForm):
    # Champs supplémentaires pour l'utilisateur si nécessaire
    username = forms.CharField(
        max_length=150,
        required=False,
        label="Nom d'utilisateur",
        help_text="Optionnel - pour créer un compte de connexion"
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="Mot de passe",
        help_text="Optionnel - pour créer un compte de connexion"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="Confirmer le mot de passe"
    )
    email = forms.EmailField(required=False, label="Adresse email")

    class Meta:
        model = Membre
        fields = [
            'nom', 'prenom', 'telephone', 'numero_urgence', 
            'categorie', 'cmu_option', 'date_naissance', 
            'adresse', 'profession', 'email'
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'adresse': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'cmu_option': 'Option CMU',
            'numero_urgence': 'Numéro de téléphone d\'urgence',
        }

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if telephone:
            # Nettoyer le numéro de téléphone
            telephone = re.sub(r'[^\d+]', '', telephone)
            if len(telephone) < 8:
                raise ValidationError("Le numéro de téléphone doit contenir au moins 8 chiffres.")
        return telephone

    def clean_numero_urgence(self):
        numero_urgence = self.cleaned_data.get('numero_urgence')
        if numero_urgence:
            numero_urgence = re.sub(r'[^\d+]', '', numero_urgence)
            if len(numero_urgence) < 8:
                raise ValidationError("Le numéro d'urgence doit contenir au moins 8 chiffres.")
        return numero_urgence

    def clean_date_naissance(self):
        date_naissance = self.cleaned_data.get('date_naissance')
        if date_naissance and date_naissance > date.today():
            raise ValidationError("La date de naissance ne peut pas être dans le futur.")
        return date_naissance

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        username = cleaned_data.get('username')

        # Vérifier la cohérence des mots de passe si un username est fourni
        if username:
            if not password:
                raise ValidationError({
                    'password': 'Un mot de passe est requis lorsque vous créez un nom d\'utilisateur.'
                })
            if password != confirm_password:
                raise ValidationError({
                    'confirm_password': 'Les mots de passe ne correspondent pas.'
                })

        return cleaned_data

    def save(self, commit=True):
        membre = super().save(commit=False)
        
        # Créer un utilisateur si username et password sont fournis
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')

        if username and password:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email or '',
                first_name=self.cleaned_data.get('prenom'),
                last_name=self.cleaned_data.get('nom')
            )
            membre.user = user

        if commit:
            membre.save()
        
        return membre


    # Champs pour les pièces d'identité
    piece_identite_recto = forms.FileField(
        label="Recto de la pièce d'identité",
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
        help_text="Format acceptés: PDF, JPG, PNG (max 5MB). Photo claire du recto.",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.jpg,.jpeg,.png'
        })
    )
    
    piece_identite_verso = forms.FileField(
        label="Verso de la pièce d'identité",
        required=False,
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
        help_text="Format acceptés: PDF, JPG, PNG (max 5MB). Obligatoire pour CNI.",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.jpg,.jpeg,.png'
        })
    )
    
    photo_identite = forms.ImageField(
        label="Photo d'identité",
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        help_text="Photo récente, format JPG/PNG (max 2MB). Fond clair, visage visible.",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.jpg,.jpeg,.png'
        })
    )
    
    confirmer_numero_piece = forms.CharField(
        label="Confirmer le numéro de pièce",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Resaisir le numéro pour confirmation'
        })
    )
    
    accepte_conditions = forms.BooleanField(
        label="J'accepte que mes documents d'identité soient utilisés pour vérifier mon identité",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Membre
        fields = [
            'type_piece_identite', 'numero_piece_identite', 'confirmer_numero_piece',
            'piece_identite_recto', 'piece_identite_verso', 'photo_identite',
            'date_expiration_piece', 'accepte_conditions',
            # ... autres champs existants ...
        ]
        widgets = {
            'type_piece_identite': forms.Select(attrs={'class': 'form-control'}),
            'numero_piece_identite': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro complet de la pièce'
            }),
            'date_expiration_piece': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        numero_piece = cleaned_data.get('numero_piece_identite')
        confirmer_numero = cleaned_data.get('confirmer_numero_piece')
        type_piece = cleaned_data.get('type_piece_identite')
        piece_verso = cleaned_data.get('piece_identite_verso')
        
        # Vérification de la correspondance des numéros
        if numero_piece and confirmer_numero and numero_piece != confirmer_numero:
            raise forms.ValidationError("Les numéros de pièce d'identité ne correspondent pas.")
        
        # Vérification que le verso est obligatoire pour CNI
        if type_piece == 'CNI' and not piece_verso:
            raise forms.ValidationError("Le verso de la CNI est obligatoire.")
        
        # Vérification de la taille des fichiers
        for field_name in ['piece_identite_recto', 'piece_identite_verso', 'photo_identite']:
            fichier = cleaned_data.get(field_name)
            if fichier:
                max_size = 5 * 1024 * 1024  # 5MB pour les pièces
                if field_name == 'photo_identite':
                    max_size = 2 * 1024 * 1024  # 2MB pour la photo
                
                if fichier.size > max_size:
                    raise forms.ValidationError(
                        f"Le fichier {field_name} est trop volumineux. "
                        f"Taille maximale: {max_size//1024//1024}MB."
                    )
        
        return cleaned_data

    def clean_numero_piece_identite(self):
        numero = self.cleaned_data.get('numero_piece_identite')
        if numero:
            # Vérifier l'unicité
            if Membre.objects.filter(numero_piece_identite=numero).exists():
                raise forms.ValidationError("Ce numéro de pièce d'identité est déjà utilisé.")
        return numero

class ValidationDocumentForm(forms.ModelForm):
    """Formulaire pour la validation des documents par les agents"""
    class Meta:
        model = Membre
        fields = ['statut_documents', 'motif_rejet']
        widgets = {
            'statut_documents': forms.Select(attrs={'class': 'form-control'}),
            'motif_rejet': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Raison du rejet (si applicable)...'
            }),
        }

class MembreUpdateForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = [
            'nom', 'prenom', 'telephone', 'numero_urgence',
            'categorie', 'cmu_option', 'date_naissance',
            'adresse', 'profession', 'email', 'statut'
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'adresse': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if telephone:
            telephone = re.sub(r'[^\d+]', '', telephone)
            if len(telephone) < 8:
                raise ValidationError("Le numéro de téléphone doit contenir au moins 8 chiffres.")
        return telephone

    def clean_date_naissance(self):
        date_naissance = self.cleaned_data.get('date_naissance')
        if date_naissance and date_naissance > date.today():
            raise ValidationError("La date de naissance ne peut pas être dans le futur.")
        return date_naissance

class BonForm(forms.ModelForm):
    class Meta:
        model = Bon
        fields = [
            'membre', 'type_soin', 'description', 'lieu_soins', 
            'date_soins', 'diagnostic', 'medecin_traitant',
            'numero_ordonnance', 'montant_total', 'taux_remboursement',
            'frais_dossier', 'piece_jointe', 'facture'
        ]
        widgets = {
            'date_soins': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'diagnostic': forms.Textarea(attrs={'rows': 2}),
        }
        labels = {
            'taux_remboursement': 'Taux de remboursement (%)',
            'frais_dossier': 'Frais de dossier (FCFA)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les membres actifs pour le champ membre
        self.fields['membre'].queryset = Membre.objects.filter(statut=Membre.StatutMembre.ACTIF)

    def clean_montant_total(self):
        montant_total = self.cleaned_data.get('montant_total')
        if montant_total and montant_total < 0:
            raise ValidationError("Le montant total ne peut pas être négatif.")
        return montant_total

    def clean_taux_remboursement(self):
        taux = self.cleaned_data.get('taux_remboursement')
        if taux and (taux < 0 or taux > 100):
            raise ValidationError("Le taux de remboursement doit être entre 0% et 100%.")
        return taux

    def clean_date_soins(self):
        date_soins = self.cleaned_data.get('date_soins')
        if date_soins and date_soins > timezone.now().date():
            raise ValidationError("La date des soins ne peut pas être dans le futur.")
        return date_soins

class LigneBonForm(forms.ModelForm):
    class Meta:
        model = LigneBon
        fields = ['designation', 'quantite', 'prix_unitaire', 'taux_remboursement']
        widgets = {
            'designation': forms.TextInput(attrs={'placeholder': 'Description du soin ou médicament'}),
        }

    def clean_quantite(self):
        quantite = self.cleaned_data.get('quantite')
        if quantite and quantite <= 0:
            raise ValidationError("La quantité doit être supérieure à 0.")
        return quantite

    def clean_prix_unitaire(self):
        prix = self.cleaned_data.get('prix_unitaire')
        if prix and prix < 0:
            raise ValidationError("Le prix unitaire ne peut pas être négatif.")
        return prix

class RechercheMembreForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        label="Rechercher un membre",
        widget=forms.TextInput(attrs={
            'placeholder': 'Nom, prénom, numéro unique...',
            'class': 'form-control'
        })
    )
    statut = forms.ChoiceField(
        choices=[('', 'Tous les statuts')] + list(Membre.StatutMembre.choices),
        required=False,
        label="Statut"
    )
    categorie = forms.ChoiceField(
        choices=[('', 'Toutes les catégories')] + list(Membre.CategorieMembre.choices),
        required=False,
        label="Catégorie"
    )

class PaiementCotisationForm(forms.Form):
    montant = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        label="Montant de la cotisation (FCFA)"
    )
    date_paiement = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now().date,
        label="Date de paiement"
    )
    mode_paiement = forms.ChoiceField(
        choices=[
            ('ESPECES', 'Espèces'),
            ('VIREMENT', 'Virement bancaire'),
            ('MOBILE', 'Paiement mobile'),
            ('CHEQUE', 'Chèque'),
        ],
        initial='ESPECES',
        label="Mode de paiement"
    )
    reference = forms.CharField(
        max_length=100,
        required=False,
        label="Référence du paiement"
    )

    def clean_montant(self):
        montant = self.cleaned_data.get('montant')
        if montant and montant <= 0:
            raise ValidationError("Le montant doit être supérieur à 0.")
        return montant

    def clean_date_paiement(self):
        date_paiement = self.cleaned_data.get('date_paiement')
        if date_paiement and date_paiement > timezone.now().date():
            raise ValidationError("La date de paiement ne peut pas être dans le futur.")
        return date_paiement



class MembreCreationForm(forms.ModelForm):
    """Formulaire de création de membre par les agents"""
    
    # Champs pour créer l'utilisateur
    username = forms.CharField(
        max_length=150,
        label="Nom d'utilisateur",
        help_text="Nom d'utilisateur pour la connexion du membre"
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Mot de passe",
        help_text="Mot de passe pour le compte du membre"
    )
    email = forms.EmailField(
        required=False,
        label="Email",
        help_text="Email du membre (optionnel)"
    )
    
    class Meta:
        model = Membre
        fields = [
            'nom', 'prenom', 'telephone', 'numero_urgence',
            'date_naissance', 'adresse', 'profession',
            'categorie', 'cmu_option', 'type_piece_identite',
            'numero_piece_identite', 'date_expiration_piece'
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'date_expiration_piece': forms.DateInput(attrs={'type': 'date'}),
            'adresse': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'cmu_option': 'Option CMU',
            'type_piece_identite': 'Type de pièce d\'identité',
            'numero_piece_identite': 'Numéro de pièce d\'identité',
            'date_expiration_piece': 'Date d\'expiration',
            'numero_urgence': 'Numéro d\'urgence',
        }
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur existe déjà.")
        return username
    
    def save(self, commit=True, agent_createur=None):
        # Créer l'utilisateur d'abord
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data.get('email', '')
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=self.cleaned_data['prenom'],
            last_name=self.cleaned_data['nom']
        )
        
        # Créer le membre
        membre = super().save(commit=False)
        membre.user = user
        membre.agent_createur = agent_createur
        membre.numero_unique = generer_numero_unique()
        membre.statut = 'actif'
        membre.statut_documents = 'en_attente'
        
        if commit:
            membre.save()
        
        return membre

class MembreDocumentForm(forms.ModelForm):
    """Formulaire pour l'upload des documents"""
    
    class Meta:
        model = Membre
        fields = [
            'piece_identite_recto',
            'piece_identite_verso', 
            'photo_identite'
        ]
        labels = {
            'piece_identite_recto': 'Recto de la pièce d\'identité',
            'piece_identite_verso': 'Verso de la pièce d\'identité',
            'photo_identite': 'Photo d\'identité',
        }
        help_texts = {
            'piece_identite_recto': 'Photo ou scan du recto',
            'piece_identite_verso': 'Photo ou scan du verso',
            'photo_identite': 'Photo portrait du membre',
        }