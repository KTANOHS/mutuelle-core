# agents/admin.py - CODE COMPLET CORRIGÉ
from django.contrib import admin
from django.utils.html import format_html
from .models import Agent, RoleAgent, PermissionAgent, BonSoin, VerificationCotisation, ActiviteAgent, PerformanceAgent

# =============================================================================
# ADMIN POUR LES RÔLES ET PERMISSIONS
# =============================================================================

@admin.register(RoleAgent)
class RoleAgentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description_courte', 'actif', 'date_creation')
    list_filter = ('actif', 'date_creation')
    search_fields = ('nom', 'description')
    ordering = ('nom',)
    
    def description_courte(self, obj):
        return obj.description[:100] + '...' if len(obj.description) > 100 else obj.description
    description_courte.short_description = 'Description'

@admin.register(PermissionAgent)
class PermissionAgentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code', 'module', 'actif', 'date_creation')
    list_filter = ('module', 'actif')
    search_fields = ('nom', 'code', 'description')
    ordering = ('module', 'nom')

# =============================================================================
# ADMIN POUR LES AGENTS
# =============================================================================

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'nom_complet', 'poste', 'assureur', 'est_actif', 'date_embauche')
    list_filter = ('est_actif', 'poste', 'date_embauche')
    search_fields = ('matricule', 'user__first_name', 'user__last_name', 'user__email', 'poste')
    readonly_fields = ('matricule', 'date_embauche')
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('user', 'matricule', 'poste', 'assureur', 'role')
        }),
        ('Informations de contact', {
            'fields': ('telephone', 'email_professionnel')
        }),
        ('Paramètres', {
            'fields': ('est_actif', 'limite_bons_quotidienne', 'date_embauche')
        }),
    )
    
    def nom_complet(self, obj):
        return obj.user.get_full_name() if obj.user else ''
    nom_complet.short_description = 'Nom complet'
    
    def save_model(self, request, obj, form, change):
        if not obj.matricule:
            # Générer un matricule si non fourni
            obj._generer_matricule()
        super().save_model(request, obj, form, change)

# =============================================================================
# ADMIN POUR LES BONS DE SOIN - CORRIGÉ
# =============================================================================

@admin.register(BonSoin)
class BonSoinAdmin(admin.ModelAdmin):
    list_display = ('code', 'membre_info', 'agent_info', 'statut_badge', 'montant_max', 'jours_restants', 'date_creation')
    list_filter = ('statut', 'urgence', 'date_creation', 'agent')
    search_fields = ('code', 'membre__user__first_name', 'membre__user__last_name', 'motif_consultation')
    readonly_fields = ('code', 'date_creation', 'date_utilisation', 'montant_utilise')
    
    # ✅ CORRECTION: Suppression de 'message_interne' qui n'existe plus
    raw_id_fields = ('membre', 'agent', 'medecin_destinataire')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('code', 'membre', 'agent', 'statut', 'date_creation', 'date_expiration')
        }),
        ('Détails médicaux', {
            'fields': ('motif_consultation', 'type_soin', 'urgence', 'medecin_destinataire', 'etablissement_medical', 'notes')
        }),
        ('Informations financières', {
            'fields': ('montant_max', 'montant_utilise', 'date_utilisation')
        }),
    )
    
    def membre_info(self, obj):
        return f"{obj.membre.nom_complet} ({obj.membre.numero_unique})" if obj.membre else "-"
    membre_info.short_description = 'Membre'
    
    def agent_info(self, obj):
        if obj.agent and obj.agent.user:
            return f"{obj.agent.user.get_full_name()} ({obj.agent.matricule if hasattr(obj.agent, 'matricule') else 'N/A'})"
        return "-"
    agent_info.short_description = 'Agent'
    
    def statut_badge(self, obj):
        couleurs = {
            'en_attente': 'orange',
            'valide': 'green',
            'rejete': 'red',
            'utilise': 'blue',
            'expire': 'gray',
            'annule': 'black'
        }
        couleur = couleurs.get(obj.statut, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px;">{}</span>',
            couleur, obj.get_statut_display()
        )
    statut_badge.short_description = 'Statut'
    
    def jours_restants(self, obj):
        return obj.jours_restants if hasattr(obj, 'jours_restants') else 0
    jours_restants.short_description = 'Jours restants'
    
    # ✅ CORRECTION: Ajouter allow_tags pour la méthode statut_badge
    statut_badge.allow_tags = True
    
# =============================================================================
# ADMIN POUR LES VÉRIFICATIONS DE COTISATION
# =============================================================================

@admin.register(VerificationCotisation)
class VerificationCotisationAdmin(admin.ModelAdmin):
    list_display = ('membre_info', 'agent_info', 'statut_badge', 'jours_retard', 'montant_dette', 'date_verification')
    list_filter = ('statut_cotisation', 'date_verification', 'agent')
    search_fields = ('membre__user__first_name', 'membre__user__last_name', 'membre__numero_unique')
    readonly_fields = ('date_verification', 'jours_retard')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('agent', 'membre', 'date_verification', 'statut_cotisation')
        }),
        ('Informations de paiement', {
            'fields': ('date_dernier_paiement', 'montant_dernier_paiement', 'prochaine_echeance')
        }),
        ('Détails de la vérification', {
            'fields': ('jours_retard', 'montant_dette', 'observations', 'pieces_justificatives')
        }),
        ('Notification', {
            'fields': ('notifier_membre',)
        }),
    )
    
    def membre_info(self, obj):
        return f"{obj.membre.nom_complet} ({obj.membre.numero_unique})"
    membre_info.short_description = 'Membre'
    
    def agent_info(self, obj):
        return f"{obj.agent.user.get_full_name()} ({obj.agent.matricule})"
    agent_info.short_description = 'Agent'
    
    def statut_badge(self, obj):
        couleurs = {
            'a_jour': 'green',
            'en_retard': 'orange',
            'impayee': 'red',
            'exoneree': 'blue'
        }
        couleur = couleurs.get(obj.statut_cotisation, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px;">{}</span>',
            couleur, obj.get_statut_cotisation_display()
        )
    statut_badge.short_description = 'Statut'
    statut_badge.allow_tags = True

# =============================================================================
# ADMIN POUR LES ACTIVITÉS DES AGENTS
# =============================================================================

@admin.register(ActiviteAgent)
class ActiviteAgentAdmin(admin.ModelAdmin):
    list_display = ('agent_info', 'type_activite_display', 'description_courte', 'date_activite_formatee', 'ip_address')
    list_filter = ('type_activite', 'date_activite', 'agent')
    search_fields = ('agent__user__first_name', 'agent__user__last_name', 'description', 'ip_address')
    readonly_fields = ('date_activite', 'ip_address', 'user_agent')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('agent', 'type_activite', 'description', 'date_activite')
        }),
        ('Données techniques', {
            'fields': ('donnees_concernees', 'ip_address', 'user_agent')
        }),
    )
    
    def agent_info(self, obj):
        return f"{obj.agent.user.get_full_name()} ({obj.agent.matricule})"
    agent_info.short_description = 'Agent'
    
    def type_activite_display(self, obj):
        return obj.get_type_activite_display()
    type_activite_display.short_description = 'Type d\'activité'
    
    def description_courte(self, obj):
        return obj.description[:100] + '...' if len(obj.description) > 100 else obj.description
    description_courte.short_description = 'Description'
    
    def date_activite_formatee(self, obj):
        return obj.date_activite.strftime('%d/%m/%Y %H:%M')
    date_activite_formatee.short_description = 'Date et heure'

# =============================================================================
# ADMIN POUR LES PERFORMANCES DES AGENTS
# =============================================================================

@admin.register(PerformanceAgent)
class PerformanceAgentAdmin(admin.ModelAdmin):
    list_display = ('agent_info', 'mois_formate', 'bons_crees', 'verifications_effectuees', 'taux_validation', 'objectif_atteint_badge')
    list_filter = ('mois', 'objectif_atteint', 'agent')
    search_fields = ('agent__user__first_name', 'agent__user__last_name')
    readonly_fields = ('taux_validation', 'satisfaction_membres')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('agent', 'mois', 'objectif_atteint')
        }),
        ('Statistiques de performance', {
            'fields': ('bons_crees', 'verifications_effectuees', 'membres_contactes', 'recherches_effectuees')
        }),
        ('Indicateurs de qualité', {
            'fields': ('taux_validation', 'satisfaction_membres')
        }),
    )
    
    def agent_info(self, obj):
        return f"{obj.agent.user.get_full_name()} ({obj.agent.matricule})"
    agent_info.short_description = 'Agent'
    
    def mois_formate(self, obj):
        return obj.mois.strftime('%B %Y')
    mois_formate.short_description = 'Mois'
    
    def objectif_atteint_badge(self, obj):
        if obj.objectif_atteint:
            return format_html(
                '<span style="background-color: green; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px;">✓ Atteint</span>'
            )
        else:
            return format_html(
                '<span style="background-color: orange; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px;">✗ Non atteint</span>'
            )
    objectif_atteint_badge.short_description = 'Objectif'
    objectif_atteint_badge.allow_tags = True

# =============================================================================
# ACTIONS PERSONNALISÉES
# =============================================================================

def marquer_comme_actif(modeladmin, request, queryset):
    queryset.update(est_actif=True)
marquer_comme_actif.short_description = "Marquer comme actif"

def marquer_comme_inactif(modeladmin, request, queryset):
    queryset.update(est_actif=False)
marquer_comme_inactif.short_description = "Marquer comme inactif"

def valider_bons_soin(modeladmin, request, queryset):
    queryset.update(statut='valide')
valider_bons_soin.short_description = "Valider les bons de soin sélectionnés"

def rejeter_bons_soin(modeladmin, request, queryset):
    queryset.update(statut='rejete')
rejeter_bons_soin.short_description = "Rejeter les bons de soin sélectionnés"

# Ajouter les actions aux admins
AgentAdmin.actions = [marquer_comme_actif, marquer_comme_inactif]
BonSoinAdmin.actions = [valider_bons_soin, rejeter_bons_soin]

# =============================================================================
# CONFIGURATION DU SITE ADMIN
# =============================================================================

admin.site.site_header = "Administration de la Mutuelle"
admin.site.site_title = "Mutuelle Admin"
admin.site.index_title = "Tableau de bord d'administration"