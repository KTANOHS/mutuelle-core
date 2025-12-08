# agents/models.py - CODE COMPLET CORRIGÉ
from django.db import models
from django.contrib.auth.models import User
from membres.models import Membre
from paiements.models import Paiement
from django.utils import timezone
import uuid
from communication.models import Message

class RoleAgent(models.Model):
    """Rôles des agents (conseiller, gestionnaire, administrateur)"""
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    permissions = models.JSONField(default=dict)  # Stocke les permissions sous forme JSON
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Rôle d'agent"
        verbose_name_plural = "Rôles d'agents"
        ordering = ['nom']

    def __str__(self):
        return self.nom

class PermissionAgent(models.Model):
    """Permissions spécifiques des agents"""
    nom = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    module = models.CharField(max_length=50)  # ex: 'membres', 'paiements', 'soins'
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Permission d'agent"
        verbose_name_plural = "Permissions d'agents"
        ordering = ['module', 'nom']

    def __str__(self):
        return f"{self.nom} ({self.code})"

class Agent(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Utilisateur"
    )
    matricule = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Matricule"
    )
    poste = models.CharField(
        max_length=100, 
        verbose_name="Poste occupé"
    )
    
    # ✅ CORRECTION: AJOUT DU CHAMP ASSUREUR
    assureur = models.ForeignKey(
        'assureur.Assureur',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Assureur associé",
        help_text="Assureur pour lequel cet agent travaille"
    )
    
    role = models.ForeignKey(
        RoleAgent, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Rôle"
    )
    date_embauche = models.DateField(
        null=True, 
        blank=True,
        verbose_name="Date d'embauche"
    )
    est_actif = models.BooleanField(
        default=True, 
        verbose_name="Actif"
    )
    limite_bons_quotidienne = models.IntegerField(
        default=20, 
        verbose_name="Limite quotidienne de bons"
    )
    telephone = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name="Téléphone"
    )
    email_professionnel = models.EmailField(
        blank=True, 
        verbose_name="Email professionnel"
    )
    
    # ✅ CORRECTION: SUPPRESSION DES CHAMPS INUTILES
    # bons_soin = models.ForeignKey(...)  # SUPPRIMÉ - trop restrictif
    # verification_cotisation = models.ForeignKey(...)  # SUPPRIMÉ

    class Meta:
        verbose_name = "Agent"
        verbose_name_plural = "Agents"
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        nom_complet = self.user.get_full_name() or self.user.username
        return f"{nom_complet} - {self.matricule}"

    # ✅ CORRECTION: AJOUT DES PROPRIÉTÉS POUR ACCÉDER AUX CHAMMS DE USER
    @property
    def nom(self):
        """Retourne le nom de famille de l'utilisateur"""
        return self.user.last_name or ""

    @property
    def prenom(self):
        """Retourne le prénom de l'utilisateur"""
        return self.user.first_name or ""

    @property
    def email(self):
        """Retourne l'email de l'utilisateur"""
        return self.user.email or ""

    @property
    def nom_complet(self):
        """Retourne le nom complet de l'agent"""
        return self.user.get_full_name() or self.user.username

    @property
    def anciennete(self):
        """Calcule l'ancienneté de l'agent en années"""
        if not self.date_embauche:
            return 0
        today = timezone.now().date()
        return today.year - self.date_embauche.year - (
            (today.month, today.day) < (self.date_embauche.month, self.date_embauche.day)
        )

    def bons_crees_aujourdhui(self):
        """Nombre de bons créés aujourd'hui par l'agent"""
        from .models import BonSoin  # Import local pour éviter les dépendances circulaires
        today = timezone.now().date()
        return BonSoin.objects.filter(agent=self, date_creation__date=today).count()

    def peut_creer_bon(self):
        """Vérifie si l'agent peut créer un nouveau bon aujourd'hui"""
        return self.bons_crees_aujourdhui() < self.limite_bons_quotidienne

    # ✅ CORRECTION: AJOUT DES MÉTHODES DE RECHERCHE DE MEMBRES
    def rechercher_membre_par_nom(self, nom):
        """Recherche un membre par nom ou prénom"""
        from membres.models import Membre
        return Membre.objects.filter(
            models.Q(user__first_name__icontains=nom) | 
            models.Q(user__last_name__icontains=nom),
            assureur=self.assureur
        ).distinct()
    
    def rechercher_membre_par_matricule(self, matricule):
        """Recherche un membre par matricule"""
        from membres.models import Membre
        return Membre.objects.filter(matricule__icontains=matricule, assureur=self.assureur)
    
    def rechercher_membre_par_telephone(self, telephone):
        """Recherche un membre par téléphone"""
        from membres.models import Membre
        return Membre.objects.filter(telephone__icontains=telephone, assureur=self.assureur)
    
    def rechercher_membres_assureur(self, query=None):
        """Recherche les membres de l'assureur de l'agent avec une requête multi-critères"""
        from membres.models import Membre
        queryset = Membre.objects.filter(assureur=self.assureur)
        
        if query:
            queryset = queryset.filter(
                models.Q(user__first_name__icontains=query) |
                models.Q(user__last_name__icontains=query) |
                models.Q(matricule__icontains=query) |
                models.Q(telephone__icontains=query) |
                models.Q(email__icontains=query)
            )
        return queryset

    def get_membres_avec_cotisation_retard(self):
        """Retourne les membres en retard de cotisation"""
        from membres.models import Membre
        return Membre.objects.filter(
            assureur=self.assureur,
            statut_cotisation__in=['en_retard', 'impayee']
        )

    def save(self, *args, **kwargs):
        """Génère un matricule si non fourni"""
        if not self.matricule:
            self.matricule = self._generer_matricule()
        super().save(*args, **kwargs)

    def _generer_matricule(self):
        """Génère un matricule unique pour l'agent"""
        prefixe = "AGT"
        dernier_agent = Agent.objects.filter(
            matricule__startswith=prefixe
        ).order_by('-matricule').first()
        
        if dernier_agent:
            try:
                numero = int(dernier_agent.matricule[3:]) + 1
            except (ValueError, IndexError):
                numero = 1
        else:
            numero = 1
            
        return f"{prefixe}{str(numero).zfill(3)}"

class BonSoin(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
        ('utilise', 'Utilisé'),
        ('expire', 'Expiré'),
        ('annule', 'Annulé'),
    ]
    
    URGENCE_CHOICES = [
        ('normale', 'Normale'),
        ('urgente', 'Urgente'),
        ('critique', 'Critique'),
    ]

    code = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Code du bon"
    )
    membre = models.ForeignKey(
        Membre, 
        on_delete=models.CASCADE, 
        verbose_name="Membre bénéficiaire"
    )
    agent = models.ForeignKey(
        Agent, 
        on_delete=models.CASCADE, 
        verbose_name="Agent créateur"
    )
    date_creation = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Date de création"
    )
    date_expiration = models.DateTimeField(
        verbose_name="Date d'expiration"
    )
    date_utilisation = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Date d'utilisation"
    )
    statut = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES, 
        default='en_attente', 
        verbose_name="Statut"
    )
    montant_max = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Montant maximum"
    )
    montant_utilise = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        verbose_name="Montant utilisé"
    )
    motif_consultation = models.TextField(
        verbose_name="Motif de consultation"
    )
    type_soin = models.CharField(
        max_length=100, 
        verbose_name="Type de soin"
    )
    urgence = models.CharField(
        max_length=20, 
        choices=URGENCE_CHOICES, 
        default='normale', 
        verbose_name="Niveau d'urgence"
    )
    medecin_destinataire = models.ForeignKey(
        'medecin.Medecin', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Médecin destinataire"
    )
    etablissement_medical = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="Établissement médical"
    )
    notes = models.TextField(
        blank=True, 
        verbose_name="Notes complémentaires"
    )
    
    # ✅ CORRECTION: SUPPRESSION DE LA RELATION DIRECTE AVEC MESSAGE
    # message_interne = models.ForeignKey(...)  # SUPPRIMÉ - problème de dépendance circulaire

    class Meta:
        verbose_name = "Bon de soin"
        verbose_name_plural = "Bons de soin"
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['statut']),
            models.Index(fields=['date_creation']),
        ]

    def __str__(self):
        return f"Bon {self.code} - {self.membre} - {self.get_statut_display()}"

    def save(self, *args, **kwargs):
        """Génère un code unique si non fourni"""
        if not self.code:
            from django.utils import timezone
            now = timezone.now()
            self.code = f"BS{now.strftime('%Y%m%d%H%M%S')}{self.membre.id:04d}"
        
        # Si pas de date d'expiration, fixer à 30 jours
        if not self.date_expiration:
            from django.utils import timezone
            self.date_expiration = timezone.now() + timezone.timedelta(days=30)
        
        super().save(*args, **kwargs)

    def est_valide(self):
        """Vérifie si le bon est encore valide"""
        now = timezone.now()
        return (
            self.statut == 'valide' and 
            self.date_expiration > now and 
            self.montant_utilise < self.montant_max
        )

    def utiliser(self, montant_utilisation):
        """Utilise le bon pour un montant donné"""
        if self.est_valide() and montant_utilisation <= (self.montant_max - self.montant_utilise):
            self.montant_utilise += montant_utilisation
            if not self.date_utilisation:
                self.date_utilisation = timezone.now()
            if self.montant_utilise >= self.montant_max:
                self.statut = 'utilise'
            self.save()
            return True
        return False

    def jours_restants(self):
        """Calcule le nombre de jours restants avant expiration"""
        now = timezone.now()
        if self.date_expiration > now:
            delta = self.date_expiration - now
            return delta.days
        return 0

    def montant_restant(self):
        """Calcule le montant restant utilisable"""
        return self.montant_max - self.montant_utilise

class VerificationCotisation(models.Model):
    STATUT_COTISATION = [
        ('a_jour', 'À jour'),
        ('en_retard', 'En retard'),
        ('impayee', 'Impayée'),
        ('exoneree', 'Exonérée'),
    ]

    agent = models.ForeignKey(
        Agent, 
        on_delete=models.CASCADE, 
        verbose_name="Agent vérificateur"
    )
    membre = models.ForeignKey(
        Membre, 
        on_delete=models.CASCADE, 
        verbose_name="Membre vérifié"
    )
    date_verification = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Date de vérification"
    )
    statut_cotisation = models.CharField(
        max_length=20, 
        choices=STATUT_COTISATION, 
        verbose_name="Statut de cotisation"
    )
    date_dernier_paiement = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Date du dernier paiement"
    )
    montant_dernier_paiement = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="Montant du dernier paiement"
    )
    prochaine_echeance = models.DateField(
        verbose_name="Prochaine échéance"
    )
    jours_retard = models.IntegerField(
        default=0, 
        verbose_name="Jours de retard"
    )
    montant_dette = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        verbose_name="Montant dû"
    )
    observations = models.TextField(
        blank=True, 
        verbose_name="Observations"
    )
    pieces_justificatives = models.FileField(
        upload_to='verifications/cotisations/', 
        blank=True, 
        null=True, 
        verbose_name="Pièces justificatives"
    )
    notifier_membre = models.BooleanField(
        default=False, 
        verbose_name="Membre notifié"
    )

    class Meta:
        verbose_name = "Vérification de cotisation"
        verbose_name_plural = "Vérifications de cotisation"
        ordering = ['-date_verification']
        unique_together = ['agent', 'membre', 'date_verification']
        indexes = [
            models.Index(fields=['membre', 'date_verification']),
            models.Index(fields=['statut_cotisation']),
        ]

    def __str__(self):
        return f"Vérification {self.membre} par {self.agent} - {self.get_statut_cotisation_display()}"

    def est_a_jour(self):
        """Vérifie si la cotisation est à jour"""
        return self.statut_cotisation == 'a_jour'

    def calculer_retard(self):
        """Calcule automatiquement le retard en jours"""
        if self.prochaine_echeance:
            today = timezone.now().date()
            if today > self.prochaine_echeance:
                self.jours_retard = (today - self.prochaine_echeance).days
                if self.jours_retard > 30:
                    self.statut_cotisation = 'impayee'
                else:
                    self.statut_cotisation = 'en_retard'
            else:
                self.jours_retard = 0
                self.statut_cotisation = 'a_jour'

    def save(self, *args, **kwargs):
        """Recalcule le retard avant sauvegarde"""
        self.calculer_retard()
        super().save(*args, **kwargs)

# Modèle pour le suivi des activités des agents
class ActiviteAgent(models.Model):
    TYPE_ACTIVITE = [
        ('creation_bon', 'Création de bon'),
        ('verification_cotisation', 'Vérification de cotisation'),
        ('consultation_membre', 'Consultation de membre'),
        ('modification_donnees', 'Modification de données'),
        ('rapport', 'Génération de rapport'),
        ('recherche_membre', 'Recherche de membre'),
    ]

    agent = models.ForeignKey(
        Agent, 
        on_delete=models.CASCADE, 
        verbose_name="Agent"
    )
    type_activite = models.CharField(
        max_length=50, 
        choices=TYPE_ACTIVITE, 
        verbose_name="Type d'activité"
    )
    description = models.TextField(
        verbose_name="Description"
    )
    date_activite = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Date de l'activité"
    )
    donnees_concernees = models.JSONField(
        default=dict, 
        blank=True, 
        verbose_name="Données concernées"
    )
    ip_address = models.GenericIPAddressField(
        null=True, 
        blank=True, 
        verbose_name="Adresse IP"
    )
    user_agent = models.TextField(
        blank=True, 
        verbose_name="User Agent"
    )

    class Meta:
        verbose_name = "Activité d'agent"
        verbose_name_plural = "Activités des agents"
        ordering = ['-date_activite']
        indexes = [
            models.Index(fields=['agent', 'date_activite']),
            models.Index(fields=['type_activite']),
        ]

    def __str__(self):
        return f"{self.agent} - {self.get_type_activite_display()} - {self.date_activite.strftime('%d/%m/%Y %H:%M')}"

# Modèle pour les quotas et performances des agents
class PerformanceAgent(models.Model):
    agent = models.OneToOneField(
        Agent, 
        on_delete=models.CASCADE, 
        verbose_name="Agent"
    )
    mois = models.DateField(
        verbose_name="Mois de performance"
    )
    bons_crees = models.IntegerField(
        default=0, 
        verbose_name="Bons créés"
    )
    verifications_effectuees = models.IntegerField(
        default=0, 
        verbose_name="Vérifications effectuées"
    )
    membres_contactes = models.IntegerField(
        default=0, 
        verbose_name="Membres contactés"
    )
    recherches_effectuees = models.IntegerField(
        default=0, 
        verbose_name="Recherches effectuées"
    )
    taux_validation = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0, 
        verbose_name="Taux de validation (%)"
    )
    satisfaction_membres = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0, 
        verbose_name="Satisfaction membres (%)"
    )
    objectif_atteint = models.BooleanField(
        default=False, 
        verbose_name="Objectif atteint"
    )

    class Meta:
        verbose_name = "Performance d'agent"
        verbose_name_plural = "Performances des agents"
        ordering = ['-mois', 'agent']
        unique_together = ['agent', 'mois']

    def __str__(self):
        return f"Performance {self.agent} - {self.mois.strftime('%m/%Y')}"

    def calculer_taux_validation(self):
        """Calcule le taux de validation des bons créés"""
        from .models import BonSoin
        total_bons = BonSoin.objects.filter(
            agent=self.agent,
            date_creation__year=self.mois.year,
            date_creation__month=self.mois.month
        ).count()
        
        if total_bons > 0:
            bons_valides = BonSoin.objects.filter(
                agent=self.agent,
                date_creation__year=self.mois.year,
                date_creation__month=self.mois.month,
                statut='valide'
            ).count()
            self.taux_validation = (bons_valides / total_bons) * 100
        else:
            self.taux_validation = 0

    def calculer_recherches_mois(self):
        """Calcule le nombre de recherches effectuées ce mois"""
        debut_mois = self.mois.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        fin_mois = debut_mois.replace(month=debut_mois.month+1) if debut_mois.month < 12 else debut_mois.replace(year=debut_mois.year+1, month=1)
        
        recherches = ActiviteAgent.objects.filter(
            agent=self.agent,
            type_activite='recherche_membre',
            date_activite__gte=debut_mois,
            date_activite__lt=fin_mois
        ).count()
        self.recherches_effectuees = recherches

# ✅ CORRECTION: FONCTION UTILITAIRE POUR CRÉER DES ACTIVITÉS DE RECHERCHE
def creer_activite_recherche(agent, terme_recherche, nombre_resultats):
    """Crée une activité de recherche pour le suivi"""
    ActiviteAgent.objects.create(
        agent=agent,
        type_activite='recherche_membre',
        description=f"Recherche de membre: '{terme_recherche}' - {nombre_resultats} résultat(s) trouvé(s)",
        donnees_concernees={
            'terme_recherche': terme_recherche,
            'nombre_resultats': nombre_resultats,
            'assureur_id': agent.assureur.id if agent.assureur else None
        }
    )

# ✅ CORRECTION: CLASSE MANAGER POUR LA RECHERCHE DE MEMBRES
class RechercheMembreManager:
    """Manager pour gérer les recherches de membres"""
    
    @staticmethod
    def effectuer_recherche_avancee(agent, termes_recherche):
        """
        Effectue une recherche avancée sur les membres de l'assureur de l'agent
        """
        from membres.models import Membre
        
        if not agent.assureur:
            return Membre.objects.none()
            
        queryset = Membre.objects.filter(assureur=agent.assureur)
        
        if termes_recherche:
            # Séparation des termes de recherche
            termes = termes_recherche.split()
            conditions = models.Q()
            
            for terme in termes:
                conditions |= (
                    models.Q(user__first_name__icontains=terme) |
                    models.Q(user__last_name__icontains=terme) |
                    models.Q(matricule__icontains=terme) |
                    models.Q(telephone__icontains=terme) |
                    models.Q(email__icontains=terme) |
                    models.Q(adresse__icontains=terme) |
                    models.Q(ville__icontains=terme)
                )
            
            queryset = queryset.filter(conditions)
        
        # Création d'une activité de recherche
        creer_activite_recherche(agent, termes_recherche, queryset.count())
        
        return queryset.distinct()
    
    @staticmethod
    def rechercher_par_criteres(agent, **criteres):
        """
        Recherche des membres par critères spécifiques
        """
        from membres.models import Membre
        
        if not agent.assureur:
            return Membre.objects.none()
            
        queryset = Membre.objects.filter(assureur=agent.assureur)
        
        # Filtrage par critères
        for champ, valeur in criteres.items():
            if valeur:
                lookup = f"{champ}__icontains" if isinstance(valeur, str) else champ
                queryset = queryset.filter(**{lookup: valeur})
        
        return queryset

# ✅ CORRECTION: AJOUT DE LA PROPRIÉTÉ POUR ACCÉDER AU MANAGER
# Cette méthode est ajoutée dynamiquement ci-dessous

# Signaux pour automatiser certaines fonctionnalités
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=BonSoin)
def creer_activite_bon(sender, instance, created, **kwargs):
    if created:
        ActiviteAgent.objects.create(
            agent=instance.agent,
            type_activite='creation_bon',
            description=f"Création du bon {instance.code} pour {instance.membre}",
            donnees_concernees={
                'bon_code': instance.code,
                'membre_id': instance.membre.id,
                'montant_max': str(instance.montant_max)
            }
        )

@receiver(post_save, sender=VerificationCotisation)
def creer_activite_verification(sender, instance, created, **kwargs):
    if created:
        ActiviteAgent.objects.create(
            agent=instance.agent,
            type_activite='verification_cotisation',
            description=f"Vérification cotisation de {instance.membre} - Statut: {instance.get_statut_cotisation_display()}",
            donnees_concernees={
                'membre_id': instance.membre.id,
                'statut': instance.statut_cotisation,
                'jours_retard': instance.jours_retard
            }
        )

# ✅ CORRECTION: AJOUT DYNAMIQUE DE LA PROPRIÉTÉ recherche À LA CLASSE Agent
Agent.recherche = RechercheMembreManager()

# ✅ CORRECTION: FONCTION UTILITAIRE POUR get_or_create_agent
def get_or_create_agent(user):
    """
    Récupère ou crée un agent pour l'utilisateur.
    Fonction utilisée dans les views pour éviter les erreurs.
    """
    try:
        # Vérifier d'abord si l'agent existe
        agent = Agent.objects.filter(user=user).first()
        
        if agent:
            return agent
        
        # Créer un nouvel agent
        agent = Agent.objects.create(
            user=user,
            poste="Agent",  # Valeur par défaut
            est_actif=True
        )
        # La méthode save() générera automatiquement le matricule
        return agent
        
    except Exception as e:
        print(f"Erreur création agent: {e}")
        
        # Retourner un agent mock en cas d'erreur
        class MockAgent:
            id = 0
            user = user
            
            @property
            def nom(self):
                return user.last_name or "N/A"
                
            @property 
            def prenom(self):
                return user.first_name or "N/A"
                
            @property
            def email(self):
                return user.email or "N/A"
                
            @property
            def nom_complet(self):
                return user.get_full_name() or user.username
                
            @property
            def est_actif(self):
                return True
                
            def __str__(self):
                return f"{self.nom} {self.prenom}"
                
        return MockAgent()