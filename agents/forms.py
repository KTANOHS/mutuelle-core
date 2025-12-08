from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
import re

from .models import Agent, BonSoin, VerificationCotisation, RoleAgent, PermissionAgent, ActiviteAgent, PerformanceAgent
from membres.models import Membre
from medecin.models import Medecin

class AgentForm(forms.ModelForm):
    """Formulaire pour la création et modification d'un agent"""
    
    # Champs supplémentaires pour l'utilisateur
    username = forms.CharField(
        max_length=150,
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom d\'utilisateur unique'
        })
    )
    
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@exemple.com'
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        label="Prénom",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prénom'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        label="Nom",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        }),
        required=False,
        label="Mot de passe"
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe'
        }),
        required=False,
        label="Confirmation du mot de passe"
    )

    class Meta:
        model = Agent
        fields = [
            'matricule', 'poste', 'role', 'date_embauche', 
            'est_actif', 'limite_bons_quotidienne', 'telephone', 
            'email_professionnel'
        ]
        widgets = {
            'matricule': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'MAT001'
            }),
            'poste': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Conseiller clientèle'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date_embauche': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'est_actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'limite_bons_quotidienne': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '100'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+225 01 02 03 04 05'
            }),
            'email_professionnel': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'agent@mutuelle.ci'
            }),
        }
        labels = {
            'matricule': 'Matricule',
            'poste': 'Poste occupé',
            'role': 'Rôle',
            'date_embauche': 'Date d\'embauche',
            'est_actif': 'Agent actif',
            'limite_bons_quotidienne': 'Limite quotidienne de bons',
            'telephone': 'Téléphone',
            'email_professionnel': 'Email professionnel',
        }

    def clean_matricule(self):
        matricule = self.cleaned_data.get('matricule')
        if not re.match(r'^[A-Z0-9]{3,20}$', matricule):
            raise ValidationError("Le matricule doit contenir uniquement des lettres majuscules et des chiffres.")
        return matricule

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if telephone and not re.match(r'^(\+225|0)[0-9]{8,10}$', telephone.replace(' ', '')):
            raise ValidationError("Format de téléphone invalide. Exemple: +225 01 23 45 67 89 ou 0123456789")
        return telephone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and password != confirm_password:
            raise ValidationError({
                'confirm_password': 'Les mots de passe ne correspondent pas.'
            })
        
        return cleaned_data

class AgentUpdateForm(forms.ModelForm):
    """Formulaire pour la modification d'un agent existant (sans champs utilisateur)"""
    
    class Meta:
        model = Agent
        fields = [
            'matricule', 'poste', 'role', 'date_embauche', 
            'est_actif', 'limite_bons_quotidienne', 'telephone', 
            'email_professionnel'
        ]
        widgets = {
            'matricule': forms.TextInput(attrs={'class': 'form-control'}),
            'poste': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'date_embauche': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'est_actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'limite_bons_quotidienne': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '100'
            }),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email_professionnel': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class BonSoinForm(forms.ModelForm):
    """Formulaire pour la création et modification d'un bon de soin"""
    
    # Champ personnalisé pour la date d'expiration
    duree_validite = forms.ChoiceField(
        choices=[
            (7, '7 jours'),
            (15, '15 jours'),
            (30, '30 jours'),
            (60, '60 jours'),
            (90, '90 jours'),
        ],
        initial=30,
        label="Durée de validité",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Champ pour rechercher un membre
    recherche_membre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher par nom, prénom ou code membre...',
            'id': 'recherche-membre'
        }),
        label="Rechercher un membre"
    )

    class Meta:
        model = BonSoin
        fields = [
            'membre', 'montant_max', 'motif_consultation', 'type_soin', 
            'urgence', 'medecin_destinataire', 'etablissement_medical', 'notes'
        ]
        widgets = {
            'membre': forms.Select(attrs={
                'class': 'form-control select2',
                'id': 'select-membre'
            }),
            'montant_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '100',
                'min': '1000',
                'max': '1000000'
            }),
            'motif_consultation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Décrire le motif de la consultation...'
            }),
            'type_soin': forms.Select(attrs={
                'class': 'form-control'
            }),
            'urgence': forms.Select(attrs={
                'class': 'form-control'
            }),
            'medecin_destinataire': forms.Select(attrs={
                'class': 'form-control select2'
            }),
            'etablissement_medical': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de l\'établissement médical'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Notes complémentaires...'
            }),
        }
        labels = {
            'membre': 'Membre bénéficiaire',
            'montant_max': 'Montant maximum (FCFA)',
            'motif_consultation': 'Motif de consultation',
            'type_soin': 'Type de soin',
            'urgence': 'Niveau d\'urgence',
            'medecin_destinataire': 'Médecin destinataire',
            'etablissement_medical': 'Établissement médical',
            'notes': 'Notes complémentaires',
        }

    def __init__(self, *args, **kwargs):
        self.agent = kwargs.pop('agent', None)
        super().__init__(*args, **kwargs)
        
        # CORRIGÉ : Utiliser le champ 'statut' au lieu de 'est_actif' pour Membre
        self.fields['membre'].queryset = Membre.objects.filter(statut='ACTIF')
        
        # CORRIGÉ : Utiliser le champ 'actif' au lieu de 'est_actif' pour Medecin
        self.fields['medecin_destinataire'].queryset = Medecin.objects.filter(actif=True)
        
        # Options pour le type de soin
        self.fields['type_soin'].widget = forms.Select(choices=[
            ('consultation_generale', 'Consultation générale'),
            ('soins_dentaires', 'Soins dentaires'),
            ('soins_ophtalmologiques', 'Soins ophtalmologiques'),
            ('analyses_medicales', 'Analyses médicales'),
            ('imagerie_medicale', 'Imagerie médicale'),
            ('hospitalisation', 'Hospitalisation'),
            ('chirurgie', 'Chirurgie'),
            ('maternite', 'Maternité'),
            ('urgence', 'Urgence'),
            ('pharmacie', 'Pharmacie'),
            ('autres', 'Autres soins'),
        ], attrs={'class': 'form-control'})

    def clean_montant_max(self):
        montant_max = self.cleaned_data.get('montant_max')
        if montant_max and montant_max < 1000:
            raise ValidationError("Le montant maximum doit être d'au moins 1 000 FCFA.")
        if montant_max and montant_max > 1000000:
            raise ValidationError("Le montant maximum ne peut pas dépasser 1 000 000 FCFA.")
        return montant_max

    def clean(self):
        cleaned_data = super().clean()
        
        # Vérifier si l'agent peut créer un bon
        if self.agent and not self.agent.peut_creer_bon():
            raise ValidationError(
                f"Vous avez atteint votre limite quotidienne de {self.agent.limite_bons_quotidienne} bons."
            )
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Associer l'agent créateur
        if self.agent:
            instance.agent = self.agent
        
        # Calculer la date d'expiration
        duree_validite = int(self.cleaned_data.get('duree_validite', 30))
        instance.date_expiration = timezone.now() + timedelta(days=duree_validite)
        
        if commit:
            instance.save()
        
        return instance

class VerificationCotisationForm(forms.ModelForm):
    """Formulaire pour la vérification de cotisation"""
    
    recherche_membre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher un membre...',
            'id': 'recherche-membre-verif'
        }),
        label="Rechercher un membre"
    )
    
    notifier_membre = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label="Notifier le membre par email/SMS"
    )

    class Meta:
        model = VerificationCotisation
        fields = [
            'membre', 'statut_cotisation', 'date_dernier_paiement',
            'montant_dernier_paiement', 'prochaine_echeance',
            'montant_dette', 'observations', 'pieces_justificatives'
        ]
        widgets = {
            'membre': forms.Select(attrs={
                'class': 'form-control select2',
                'id': 'select-membre-verif'
            }),
            'statut_cotisation': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date_dernier_paiement': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'montant_dernier_paiement': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '100',
                'min': '0'
            }),
            'prochaine_echeance': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'montant_dette': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '100',
                'min': '0'
            }),
            'observations': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Observations sur la situation de cotisation...'
            }),
            'pieces_justificatives': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'membre': 'Membre à vérifier',
            'statut_cotisation': 'Statut de cotisation',
            'date_dernier_paiement': 'Date du dernier paiement',
            'montant_dernier_paiement': 'Montant du dernier paiement (FCFA)',
            'prochaine_echeance': 'Prochaine échéance',
            'montant_dette': 'Montant dû (FCFA)',
            'observations': 'Observations',
            'pieces_justificatives': 'Pièces justificatives',
        }

    def __init__(self, *args, **kwargs):
        self.agent = kwargs.pop('agent', None)
        super().__init__(*args, **kwargs)
        
        # CORRIGÉ : Utiliser le champ 'statut' au lieu de 'est_actif' pour Membre
        self.fields['membre'].queryset = Membre.objects.filter(statut='ACTIF')

    def clean_prochaine_echeance(self):
        prochaine_echeance = self.cleaned_data.get('prochaine_echeance')
        if prochaine_echeance and prochaine_echeance < timezone.now().date():
            raise ValidationError("La prochaine échéance ne peut pas être dans le passé.")
        return prochaine_echeance

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Associer l'agent
        if self.agent:
            instance.agent = self.agent
        
        # Calculer automatiquement le retard si nécessaire
        instance.calculer_retard()
        
        if commit:
            instance.save()
        
        return instance

class RoleAgentForm(forms.ModelForm):
    """Formulaire pour la gestion des rôles d'agents"""
    
    permissions_list = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        label="Permissions"
    )

    class Meta:
        model = RoleAgent
        fields = ['nom', 'description', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Conseiller clientèle'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description du rôle...'
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'nom': 'Nom du rôle',
            'description': 'Description',
            'actif': 'Rôle actif',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Récupérer toutes les permissions disponibles
        permissions = PermissionAgent.objects.filter(actif=True)
        self.fields['permissions_list'].choices = [
            (perm.id, f"{perm.nom} - {perm.description}") 
            for perm in permissions
        ]
        
        # Pré-sélectionner les permissions existantes
        if self.instance and self.instance.pk:
            existing_permissions = list(self.instance.permissions.keys())
            self.fields['permissions_list'].initial = existing_permissions

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Sauvegarder les permissions sous forme JSON
        selected_permissions = self.cleaned_data.get('permissions_list', [])
        permissions_dict = {}
        
        for perm_id in selected_permissions:
            try:
                perm = PermissionAgent.objects.get(id=perm_id)
                permissions_dict[perm.code] = {
                    'nom': perm.nom,
                    'description': perm.description,
                    'module': perm.module
                }
            except PermissionAgent.DoesNotExist:
                continue
        
        instance.permissions = permissions_dict
        
        if commit:
            instance.save()
        
        return instance

class PermissionAgentForm(forms.ModelForm):
    """Formulaire pour la gestion des permissions d'agents"""

    class Meta:
        model = PermissionAgent
        fields = ['nom', 'code', 'description', 'module', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Créer des bons de soin'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: bons_creer'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Description de la permission...'
            }),
            'module': forms.Select(attrs={
                'class': 'form-control'
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'nom': 'Nom de la permission',
            'code': 'Code technique',
            'description': 'Description',
            'module': 'Module',
            'actif': 'Permission active',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Options pour les modules
        self.fields['module'].widget = forms.Select(choices=[
            ('membres', 'Membres'),
            ('paiements', 'Paiements'),
            ('soins', 'Soins'),
            ('bons', 'Bons de soin'),
            ('verifications', 'Vérifications'),
            ('rapports', 'Rapports'),
            ('administration', 'Administration'),
        ])

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code and not re.match(r'^[a-z_]+$', code):
            raise ValidationError(
                "Le code doit contenir uniquement des lettres minuscules et des underscores."
            )
        return code

class RechercheMembreForm(forms.Form):
    """Formulaire de recherche de membres"""
    
    search = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher par nom, prénom, code membre...',
            'autocomplete': 'off'
        }),
        label=""
    )
    
    statut_cotisation = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Tous statuts'),
            ('a_jour', 'À jour'),
            ('en_retard', 'En retard'),
            ('impayee', 'Impayée'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Statut cotisation"
    )
    
    date_inscription_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="Inscrit à partir du"
    )
    
    date_inscription_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="Inscrit jusqu'au"
    )

class FiltreBonsSoinForm(forms.Form):
    """Formulaire de filtrage des bons de soin"""
    
    STATUT_CHOICES = [
        ('', 'Tous les statuts'),
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
        ('utilise', 'Utilisé'),
        ('expire', 'Expiré'),
        ('annule', 'Annulé'),
    ]
    
    URGENCE_CHOICES = [
        ('', 'Tous niveaux'),
        ('normale', 'Normale'),
        ('urgente', 'Urgente'),
        ('critique', 'Critique'),
    ]
    
    statut = forms.ChoiceField(
        choices=STATUT_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Statut"
    )
    
    urgence = forms.ChoiceField(
        choices=URGENCE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Urgence"
    )
    
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="Date de création (début)"
    )
    
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="Date de création (fin)"
    )
    
    agent = forms.ModelChoiceField(
        queryset=Agent.objects.filter(est_actif=True),  # Agent a bien est_actif
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Agent créateur"
    )

class FiltreVerificationsForm(forms.Form):
    """Formulaire de filtrage des vérifications de cotisation"""
    
    STATUT_CHOICES = [
        ('', 'Tous statuts'),
        ('a_jour', 'À jour'),
        ('en_retard', 'En retard'),
        ('impayee', 'Impayée'),
        ('exoneree', 'Exonérée'),
    ]
    
    statut_cotisation = forms.ChoiceField(
        choices=STATUT_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Statut cotisation"
    )
    
    date_verification_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="Date vérification (début)"
    )
    
    date_verification_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="Date vérification (fin)"
    )
    
    agent = forms.ModelChoiceField(
        queryset=Agent.objects.filter(est_actif=True),  # Agent a bien est_actif
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Agent vérificateur"
    )

class RapportAgentsForm(forms.Form):
    """Formulaire pour générer des rapports sur les agents"""
    
    TYPE_RAPPORT_CHOICES = [
        ('performance', 'Performance des agents'),
        ('activites', 'Activités des agents'),
        ('bons_crees', 'Bons créés par agent'),
        ('verifications', 'Vérifications effectuées'),
    ]
    
    PERIODE_CHOICES = [
        ('7_jours', '7 derniers jours'),
        ('30_jours', '30 derniers jours'),
        ('90_jours', '90 derniers jours'),
        ('personnalise', 'Période personnalisée'),
    ]
    
    type_rapport = forms.ChoiceField(
        choices=TYPE_RAPPORT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Type de rapport"
    )
    
    periode = forms.ChoiceField(
        choices=PERIODE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'periode-select'
        }),
        label="Période"
    )
    
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'date-debut'
        }),
        label="Date de début"
    )
    
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'date-fin'
        }),
        label="Date de fin"
    )
    
    agents = forms.ModelMultipleChoiceField(
        queryset=Agent.objects.filter(est_actif=True),  # Agent a bien est_actif
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control select2'
        }),
        label="Agents (laisser vide pour tous)"
    )
    
    format_export = forms.ChoiceField(
        choices=[
            ('html', 'HTML'),
            ('pdf', 'PDF'),
            ('excel', 'Excel'),
        ],
        initial='html',
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        label="Format d'export"
    )

    def clean(self):
        cleaned_data = super().clean()
        periode = cleaned_data.get('periode')
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        
        if periode == 'personnalise':
            if not date_debut or not date_fin:
                raise ValidationError("Veuillez spécifier les dates de début et de fin pour une période personnalisée.")
            
            if date_debut > date_fin:
                raise ValidationError("La date de début ne peut pas être postérieure à la date de fin.")
        
        return cleaned_data

class UtilisationBonForm(forms.Form):
    """Formulaire pour l'utilisation d'un bon de soin"""
    
    montant_utilisation = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '100',
            'placeholder': 'Montant à utiliser...'
        }),
        label="Montant à utiliser (FCFA)"
    )
    
    motif_utilisation = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Détails de l\'utilisation...'
        }),
        label="Motif de l'utilisation"
    )
    
    date_utilisation = forms.DateTimeField(
        initial=timezone.now,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        label="Date d'utilisation"
    )

class ImportMembresForm(forms.Form):
    """Formulaire pour l'import de membres depuis un fichier"""
    
    fichier = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv,.xlsx,.xls'
        }),
        label="Fichier à importer"
    )
    
    type_fichier = forms.ChoiceField(
        choices=[
            ('csv', 'CSV'),
            ('excel', 'Excel'),
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        label="Type de fichier"
    )
    
    ignorer_premiere_ligne = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label="Ignorer la première ligne (en-têtes)"
    )
    
    creer_nouveaux_membres = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label="Créer les nouveaux membres"
    )
    
    mettre_a_jour_existants = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label="Mettre à jour les membres existants"
    )

    def clean_fichier(self):
        fichier = self.cleaned_data.get('fichier')
        if fichier:
            # Vérifier l'extension du fichier
            extension = fichier.name.split('.')[-1].lower()
            if extension not in ['csv', 'xlsx', 'xls']:
                raise ValidationError("Format de fichier non supporté. Utilisez CSV ou Excel.")
            
            # Vérifier la taille du fichier (max 10MB)
            if fichier.size > 10 * 1024 * 1024:
                raise ValidationError("Le fichier est trop volumineux. Taille maximale: 10MB.")
        
        return fichier

# Formulaires pour les API et AJAX
class RechercheMembreAjaxForm(forms.Form):
    """Formulaire pour la recherche AJAX de membres"""
    
    q = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Rechercher un membre...'
        })
    )
    
    limite = forms.IntegerField(
        min_value=1,
        max_value=50,
        initial=10,
        required=False,
        widget=forms.HiddenInput()
    )

class NotificationForm(forms.Form):
    """Formulaire pour les notifications"""
    
    type_notification = forms.ChoiceField(
        choices=[
            ('info', 'Information'),
            ('warning', 'Avertissement'),
            ('urgence', 'Urgence'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    destinataires = forms.ModelMultipleChoiceField(
        queryset=Agent.objects.filter(est_actif=True),  # Agent a bien est_actif
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Contenu de la notification...'
        })
    )
    
    expiration = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        })
    )

class PerformanceAgentForm(forms.ModelForm):
    """Formulaire pour les performances des agents"""
    
    class Meta:
        model = PerformanceAgent
        fields = ['mois', 'bons_crees', 'verifications_effectuees', 'membres_contactes', 'taux_validation', 'satisfaction_membres', 'objectif_atteint']
        widgets = {
            'mois': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'month'
            }),
            'bons_crees': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'verifications_effectuees': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'membres_contactes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'taux_validation': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '0.01'
            }),
            'satisfaction_membres': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '0.01'
            }),
            'objectif_atteint': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'mois': 'Mois de performance',
            'bons_crees': 'Nombre de bons créés',
            'verifications_effectuees': 'Vérifications effectuées',
            'membres_contactes': 'Membres contactés',
            'taux_validation': 'Taux de validation (%)',
            'satisfaction_membres': 'Satisfaction membres (%)',
            'objectif_atteint': 'Objectif atteint',
        }

class ActiviteAgentForm(forms.ModelForm):
    """Formulaire pour les activités des agents"""
    
    class Meta:
        model = ActiviteAgent
        fields = ['type_activite', 'description', 'donnees_concernees']
        widgets = {
            'type_activite': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description de l\'activité...'
            }),
            'donnees_concernees': forms.HiddenInput(),  # Généralement rempli automatiquement
        }
        labels = {
            'type_activite': 'Type d\'activité',
            'description': 'Description',
            'donnees_concernees': 'Données concernées',
        }

class QuickStatsForm(forms.Form):
    """Formulaire pour les statistiques rapides"""
    
    periode = forms.ChoiceField(
        choices=[
            ('today', "Aujourd'hui"),
            ('week', 'Cette semaine'),
            ('month', 'Ce mois'),
            ('quarter', 'Ce trimestre'),
            ('year', 'Cette année'),
        ],
        initial='today',
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm'
        })
    )

class BulkActionForm(forms.Form):
    """Formulaire pour les actions groupées"""
    
    ACTION_CHOICES = [
        ('valider', 'Valider sélection'),
        ('rejeter', 'Rejeter sélection'),
        ('exporter', 'Exporter sélection'),
        ('notifier', 'Notifier sélection'),
    ]
    
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm'
        })
    )
    
    objets_ids = forms.CharField(
        widget=forms.HiddenInput()
    )

class PasswordChangeAgentForm(forms.Form):
    """Formulaire pour le changement de mot de passe des agents"""
    
    ancien_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ancien mot de passe'
        }),
        label="Ancien mot de passe"
    )
    
    nouveau_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nouveau mot de passe'
        }),
        label="Nouveau mot de passe",
        min_length=8
    )
    
    confirmer_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmer le nouveau mot de passe'
        }),
        label="Confirmer le mot de passe"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        nouveau_mot_de_passe = cleaned_data.get('nouveau_mot_de_passe')
        confirmer_mot_de_passe = cleaned_data.get('confirmer_mot_de_passe')
        
        if nouveau_mot_de_passe and confirmer_mot_de_passe:
            if nouveau_mot_de_passe != confirmer_mot_de_passe:
                raise ValidationError("Les mots de passe ne correspondent pas.")
        
        return cleaned_data

# Formulaire pour le dashboard agent
class DashboardFilterForm(forms.Form):
    """Formulaire de filtrage pour le dashboard agent"""
    
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="Du"
    )
    
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="Au"
    )
    
    type_activite = forms.ChoiceField(
        choices=[
            ('', 'Toutes les activités'),
            ('creation_bon', 'Création de bons'),
            ('verification_cotisation', 'Vérifications'),
            ('consultation_membre', 'Consultations'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Type d'activité"
    )

# Formulaire pour les statistiques détaillées
class StatistiquesDetailForm(forms.Form):
    """Formulaire pour les statistiques détaillées"""
    
    annee = forms.ChoiceField(
        choices=[(str(year), str(year)) for year in range(2020, 2031)],
        initial=str(timezone.now().year),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Année"
    )
    
    mois = forms.ChoiceField(
        choices=[
            ('', 'Tous les mois'),
            ('1', 'Janvier'),
            ('2', 'Février'),
            ('3', 'Mars'),
            ('4', 'Avril'),
            ('5', 'Mai'),
            ('6', 'Juin'),
            ('7', 'Juillet'),
            ('8', 'Août'),
            ('9', 'Septembre'),
            ('10', 'Octobre'),
            ('11', 'Novembre'),
            ('12', 'Décembre'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Mois"
    )
    
    agent = forms.ModelChoiceField(
        queryset=Agent.objects.filter(est_actif=True),  # Agent a bien est_actif
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Agent spécifique"
    )