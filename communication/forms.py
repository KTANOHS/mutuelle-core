# communication/forms.py - VERSION COMPLÈTE CORRIGÉE
from django import forms
from django.contrib.auth import get_user_model
from .models import Message, PieceJointe, Notification, GroupeCommunication, MessageGroupe

User = get_user_model()

class MultipleFileInput(forms.ClearableFileInput):
    """Widget personnalisé pour l'upload de fichiers multiples"""
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    """Champ personnalisé pour les fichiers multiples"""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class MessageForm(forms.ModelForm):
    """Formulaire pour envoyer un message - CORRIGÉ"""
    pieces_jointes = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.txt,.zip,.rar'
        }),
        help_text="Vous pouvez sélectionner plusieurs fichiers (max 10MB par fichier)"
    )
    
    class Meta:
        model = Message
        fields = ['destinataire', 'titre', 'contenu', 'type_message']
        widgets = {
            'destinataire': forms.Select(attrs={
                'class': 'form-select',
                'data-placeholder': 'Choisir un destinataire...'
            }),
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sujet du message...'
            }),
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Tapez votre message ici...'
            }),
            'type_message': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'destinataire': 'Destinataire',
            'titre': 'Sujet',
            'contenu': 'Message',
            'type_message': 'Type de message'
        }
    
    def __init__(self, *args, **kwargs):
        self.expediteur = kwargs.pop('expediteur', None)
        super().__init__(*args, **kwargs)
        
        # CORRECTION : Filtrer les destinataires (exclure l'utilisateur courant)
        if self.expediteur:
            self.fields['destinataire'].queryset = User.objects.exclude(id=self.expediteur.id)
        
        # CORRECTION : Définir une valeur par défaut et rendre le champ optionnel
        self.fields['type_message'].initial = 'MESSAGE'
        self.fields['type_message'].required = False
    
    def clean_pieces_jointes(self):
        fichiers = self.cleaned_data.get('pieces_jointes', [])
        if not isinstance(fichiers, list):
            fichiers = [fichiers]
        
        for fichier in fichiers:
            if fichier:  # Vérifier que le fichier existe
                # Vérifier la taille du fichier (max 10MB)
                if fichier.size > 10 * 1024 * 1024:
                    raise forms.ValidationError(
                        f"Le fichier {fichier.name} est trop volumineux. Taille max: 10MB"
                    )
                
                # Vérifier l'extension
                extension = fichier.name.split('.')[-1].lower()
                extensions_autorisees = [
                    'pdf', 'doc', 'docx', 'xls', 'xlsx', 
                    'jpg', 'jpeg', 'png', 'txt', 'zip', 'rar'
                ]
                if extension not in extensions_autorisees:
                    raise forms.ValidationError(
                        f"Type de fichier {extension} non autorisé. "
                        f"Types autorisés: {', '.join(extensions_autorisees)}"
                    )
        
        return fichiers

    def save(self, commit=True):
        """Surcharge de la méthode save pour gérer automatiquement l'expéditeur"""
        message = super().save(commit=False)
        
        # CORRECTION : Assigner l'expéditeur
        if self.expediteur:
            message.expediteur = self.expediteur
        
        # CORRECTION : S'assurer que type_message a une valeur
        if not message.type_message:
            message.type_message = 'MESSAGE'
        
        if commit:
            message.save()
            
            # Gérer les pièces jointes après sauvegarde du message
            pieces_jointes = self.cleaned_data.get('pieces_jointes', [])
            if pieces_jointes:
                if not isinstance(pieces_jointes, list):
                    pieces_jointes = [pieces_jointes]
                
                for fichier in pieces_jointes:
                    if fichier:  # Vérifier que le fichier existe
                        PieceJointe.objects.create(
                            message=message,
                            fichier=fichier,
                            nom_original=fichier.name,
                            taille=fichier.size
                        )
            
        return message

class MessageFormSimple(forms.ModelForm):
    """Formulaire simplifié pour envoyer un message - SANS type_message obligatoire"""
    pieces_jointes = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.txt,.zip,.rar'
        }),
        help_text="Vous pouvez sélectionner plusieurs fichiers (max 10MB par fichier)"
    )
    
    class Meta:
        model = Message
        fields = ['destinataire', 'titre', 'contenu']  # CORRECTION : type_message retiré
        widgets = {
            'destinataire': forms.Select(attrs={
                'class': 'form-select',
                'data-placeholder': 'Choisir un destinataire...'
            }),
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sujet du message...'
            }),
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Tapez votre message ici...'
            }),
        }
        labels = {
            'destinataire': 'Destinataire',
            'titre': 'Sujet',
            'contenu': 'Message'
        }
    
    def __init__(self, *args, **kwargs):
        self.expediteur = kwargs.pop('expediteur', None)
        super().__init__(*args, **kwargs)
        
        if self.expediteur:
            self.fields['destinataire'].queryset = User.objects.exclude(id=self.expediteur.id)
    
    def save(self, commit=True):
        """Surcharge de la méthode save"""
        message = super().save(commit=False)
        
        if self.expediteur:
            message.expediteur = self.expediteur
        
        # CORRECTION : Définir automatiquement le type_message
        message.type_message = 'MESSAGE'
        
        if commit:
            message.save()
            
            # Gérer les pièces jointes
            pieces_jointes = self.cleaned_data.get('pieces_jointes', [])
            if pieces_jointes:
                if not isinstance(pieces_jointes, list):
                    pieces_jointes = [pieces_jointes]
                
                for fichier in pieces_jointes:
                    if fichier:
                        PieceJointe.objects.create(
                            message=message,
                            fichier=fichier,
                            nom_original=fichier.name,
                            taille=fichier.size
                        )
            
        return message

class MessageGroupeForm(forms.ModelForm):
    """Formulaire pour envoyer un message dans un groupe"""
    pieces_jointes = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.txt,.zip,.rar'
        })
    )
    
    class Meta:
        model = MessageGroupe
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tapez votre message pour le groupe...'
            }),
        }
        labels = {
            'contenu': 'Message'
        }

class UploadFileForm(forms.Form):
    """Formulaire pour uploader un fichier"""
    fichier = forms.FileField(
        label="Fichier à uploader",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.txt,.zip,.rar'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Description optionnelle du fichier...'
        })
    )
    
    def clean_fichier(self):
        fichier = self.cleaned_data['fichier']
        
        # Vérifier la taille
        if fichier.size > 10 * 1024 * 1024:  # 10MB
            raise forms.ValidationError("Le fichier est trop volumineux. Taille max: 10MB")
        
        # Vérifier l'extension
        extension = fichier.name.split('.')[-1].lower()
        extensions_autorisees = [
            'pdf', 'doc', 'docx', 'xls', 'xlsx', 
            'jpg', 'jpeg', 'png', 'txt', 'zip', 'rar'
        ]
        if extension not in extensions_autorisees:
            raise forms.ValidationError(
                f"Type de fichier non autorisé. Types autorisés: {', '.join(extensions_autorisees)}"
            )
        
        return fichier

class GroupeCommunicationForm(forms.ModelForm):
    """Formulaire pour créer ou modifier un groupe de communication"""
    membres = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'data-placeholder': 'Sélectionner les membres...'
        }),
        required=True,
        help_text="Sélectionnez les membres à ajouter au groupe"
    )
    
    class Meta:
        model = GroupeCommunication
        fields = ['nom', 'description', 'membres']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du groupe...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description du groupe...'
            }),
        }
        labels = {
            'nom': 'Nom du groupe',
            'description': 'Description',
            'membres': 'Membres du groupe'
        }
    
    def __init__(self, *args, **kwargs):
        self.createur = kwargs.pop('createur', None)
        super().__init__(*args, **kwargs)
        
        if self.createur:
            # Exclure le créateur de la liste des membres (il sera ajouté automatiquement)
            self.fields['membres'].queryset = User.objects.exclude(id=self.createur.id)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.createur:
            instance.createur = self.createur
        
        if commit:
            instance.save()
            self.save_m2m()  # Sauvegarder la relation ManyToMany
        
        # Ajouter le créateur comme membre
        if self.createur and instance.pk:
            instance.membres.add(self.createur)
        
        return instance

class NotificationForm(forms.ModelForm):
    """Formulaire pour créer une notification (usage admin)"""
    class Meta:
        model = Notification
        fields = ['user', 'titre', 'message', 'type_notification']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de la notification...'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Message de la notification...'
            }),
            'type_notification': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'user': 'Utilisateur',
            'titre': 'Titre',
            'message': 'Message',
            'type_notification': 'Type de notification'
        }

class RechercheMessageForm(forms.Form):
    """Formulaire de recherche de messages"""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher dans les messages...',
            'aria-label': 'Recherche'
        })
    )
    type_message = forms.ChoiceField(
        required=False,
        choices=[('', 'Tous les types')] + Message.TYPE_MESSAGE,
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
    
    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        
        if date_debut and date_fin and date_debut > date_fin:
            raise forms.ValidationError("La date de début ne peut pas être après la date de fin.")
        
        return cleaned_data

class FiltreNotificationForm(forms.Form):
    """Formulaire pour filtrer les notifications"""
    type_notification = forms.ChoiceField(
        required=False,
        choices=[('', 'Tous les types')] + [
            ('INFO', 'Information'),
            ('ALERTE', 'Alerte'),
            ('SUCCES', 'Succès'),
            ('ERREUR', 'Erreur'),
            ('BON_SOIN', 'Bon de Soin'),
            ('RDV', 'Rendez-vous'),
            ('PAIEMENT', 'Paiement'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    est_lue = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Tous'),
            ('non_lues', 'Non lues'),
            ('lues', 'Lues')
        ],
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

class ReplyMessageForm(forms.ModelForm):
    """Formulaire pour répondre à un message"""
    class Meta:
        model = Message
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tapez votre réponse...'
            }),
        }
        labels = {
            'contenu': 'Réponse'
        }

class ForwardMessageForm(forms.ModelForm):
    """Formulaire pour transférer un message"""
    nouveaux_destinataires = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'data-placeholder': 'Sélectionner les destinataires...'
        }),
        required=True
    )
    
    class Meta:
        model = Message
        fields = ['titre', 'contenu']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sujet du message transféré...'
            }),
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Message original et vos commentaires...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.original_message = kwargs.pop('original_message', None)
        self.expediteur = kwargs.pop('expediteur', None)
        super().__init__(*args, **kwargs)
        
        if self.expediteur:
            self.fields['nouveaux_destinataires'].queryset = User.objects.exclude(id=self.expediteur.id)
        
        if self.original_message:
            # Pré-remplir avec le message original
            self.fields['titre'].initial = f"TR: {self.original_message.titre}"
            self.fields['contenu'].initial = (
                f"\n\n--- Message original ---\n"
                f"De: {self.original_message.expediteur.get_full_name() or self.original_message.expediteur.username}\n"
                f"Date: {self.original_message.date_envoi.strftime('%d/%m/%Y %H:%M')}\n"
                f"Sujet: {self.original_message.titre}\n\n"
                f"{self.original_message.contenu}"
            )

class QuickMessageForm(forms.Form):
    """Formulaire pour un message rapide (popup/modal)"""
    destinataire = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'data-placeholder': 'Choisir un destinataire...'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Tapez votre message rapide...',
            'style': 'resize: none;'
        }),
        max_length=500
    )
    
    def __init__(self, *args, **kwargs):
        self.expediteur = kwargs.pop('expediteur', None)
        super().__init__(*args, **kwargs)
        
        if self.expediteur:
            self.fields['destinataire'].queryset = User.objects.exclude(id=self.expediteur.id)

class BatchNotificationForm(forms.Form):
    """Formulaire pour envoyer des notifications en lot"""
    destinataires = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'data-placeholder': 'Sélectionner les destinataires...'
        }),
        required=True
    )
    titre = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Titre de la notification...'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Message de la notification...'
        })
    )
    type_notification = forms.ChoiceField(
        choices=[
            ('INFO', 'Information'),
            ('ALERTE', 'Alerte'),
            ('SUCCES', 'Succès'),
            ('ERREUR', 'Erreur'),
            ('BON_SOIN', 'Bon de Soin'),
            ('RDV', 'Rendez-vous'),
            ('PAIEMENT', 'Paiement'),
        ],
        initial='INFO',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    envoyer_immediatement = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limiter les destinataires si nécessaire
        # self.fields['destinataires'].queryset = User.objects.filter(is_active=True)

class ImportContactsForm(forms.Form):
    """Formulaire pour importer des contacts"""
    fichier_csv = forms.FileField(
        label="Fichier CSV",
        help_text="Format attendu: nom, email, téléphone (optionnel)",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv,.txt'
        })
    )
    separateur = forms.ChoiceField(
        choices=[
            (',', 'Virgule (,)'),
            (';', 'Point-virgule (;)'),
            ('\t', 'Tabulation')
        ],
        initial=',',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def clean_fichier_csv(self):
        fichier = self.cleaned_data['fichier_csv']
        
        # Vérifier l'extension
        if not fichier.name.endswith('.csv'):
            raise forms.ValidationError("Le fichier doit être au format CSV")
        
        # Vérifier la taille
        if fichier.size > 5 * 1024 * 1024:  # 5MB
            raise forms.ValidationError("Le fichier est trop volumineux. Taille max: 5MB")
        
        return fichier

# Formset pour les pièces jointes multiples
PieceJointeFormSet = forms.inlineformset_factory(
    Message,
    PieceJointe,
    fields=('fichier',),
    extra=3,
    can_delete=True,
    widgets={
        'fichier': forms.FileInput(attrs={
            'class': 'form-control',
        })
    }
)

class MessageAvecPiecesJointesForm(forms.ModelForm):
    """Formulaire combiné message + pièces jointes"""
    class Meta:
        model = Message
        fields = ['destinataire', 'titre', 'contenu', 'type_message']
        widgets = {
            'destinataire': forms.Select(attrs={'class': 'form-select'}),
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'type_message': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.piece_jointe_formset = PieceJointeFormSet(
            instance=self.instance,
            data=kwargs.get('data'),
            files=kwargs.get('files'),
            prefix='pieces_jointes'
        )
    
    def is_valid(self):
        return super().is_valid() and self.piece_jointe_formset.is_valid()
    
    def save(self, commit=True):
        instance = super().save(commit=commit)
        if commit:
            self.piece_jointe_formset.instance = instance
            self.piece_jointe_formset.save()
        return instance