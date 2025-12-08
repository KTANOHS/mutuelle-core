# assureur/admin.py - VERSION CORRIGÉE SANS Membre
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from django.db.models import Count, Sum
from .models import (
    Assureur, Bon, Soin, Paiement, Cotisation, 
    StatistiquesAssurance, ConfigurationAssurance, RapportAssureur,
    BonPriseEnCharge, BonDeSoin
)

# =============================================================================
# FILTRES PERSONNALISÉS
# =============================================================================

class CotisationStatutFilter(admin.SimpleListFilter):
    """Filtre personnalisé pour le statut des cotisations"""
    title = 'Statut cotisation'
    parameter_name = 'statut_cotisation'

    def lookups(self, request, model_admin):
        return [
            ('en_retard', 'En retard'),
            ('due', 'Due'),
            ('payee', 'Payée'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'en_retard':
            return queryset.filter(statut='en_retard')
        elif self.value() == 'due':
            return queryset.filter(statut='due')
        elif self.value() == 'payee':
            return queryset.filter(statut='payee')
        return queryset


# =============================================================================
# CLASSES ADMIN CORRIGÉES
# =============================================================================

@admin.register(Assureur)
class AssureurAdmin(admin.ModelAdmin):
    """Administration des employés assureurs"""
    
    list_display = ['numero_employe', 'user', 'departement', 'date_embauche', 'est_actif']
    list_filter = ['departement', 'est_actif', 'date_embauche']
    search_fields = ['numero_employe', 'user__first_name', 'user__last_name', 'user__email']
    
    def user(self, obj):
        return obj.user.username
    user.short_description = 'Utilisateur'


@admin.register(Bon)
class BonAdmin(admin.ModelAdmin):
    """Administration des bons de prise en charge"""
    
    list_display = [
        'numero_bon', 'get_membre', 'type_soin', 'montant_total', 
        'statut', 'date_soin', 'date_expiration'
    ]
    
    list_filter = ['statut', 'type_soin', 'date_soin']
    search_fields = ['numero_bon', 'membre__nom', 'membre__prenom']
    
    def get_membre(self, obj):
        return f"{obj.membre.prenom} {obj.membre.nom}" if obj.membre else "N/A"
    get_membre.short_description = 'Membre'
    
    actions = ['valider_bons', 'refuser_bons']
    
    def valider_bons(self, request, queryset):
        count = 0
        for bon in queryset.filter(statut='en_attente'):
            bon.statut = 'valide'
            bon.valide_par = request.user
            bon.date_validation = timezone.now()
            bon.save()
            count += 1
        self.message_user(request, f"{count} bons validés avec succès.")
    valider_bons.short_description = "Valider les bons sélectionnés"
    
    def refuser_bons(self, request, queryset):
        updated = queryset.filter(statut='en_attente').update(
            statut='refuse',
            valide_par=request.user,
            date_validation=timezone.now()
        )
        self.message_user(request, f"{updated} bons refusés.")
    refuser_bons.short_description = "Refuser les bons sélectionnés"


@admin.register(Soin)
class SoinAdmin(admin.ModelAdmin):
    """Administration des soins"""
    
    list_display = ['get_membre', 'type_soin', 'montant_facture', 'statut', 'date_soin']
    list_filter = ['statut', 'type_soin']
    search_fields = ['membre__nom', 'membre__prenom', 'type_soin']
    
    def get_membre(self, obj):
        return f"{obj.membre.prenom} {obj.membre.nom}" if obj.membre else "N/A"
    get_membre.short_description = 'Membre'


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    """Administration des paiements"""
    
    list_display = ['reference', 'get_membre', 'montant', 'statut', 'date_paiement']
    list_filter = ['statut', 'mode_paiement']
    search_fields = ['reference', 'membre__nom', 'membre__prenom']
    
    def get_membre(self, obj):
        return f"{obj.membre.prenom} {obj.membre.nom}" if obj.membre else "N/A"
    get_membre.short_description = 'Membre'


@admin.register(Cotisation)
class CotisationAdmin(admin.ModelAdmin):
    """Administration des cotisations"""
    
    list_display = [
        'reference', 'get_membre', 'periode', 'montant', 'statut', 'date_echeance'
    ]
    
    list_filter = [CotisationStatutFilter, 'type_cotisation', 'periode']
    search_fields = ['reference', 'membre__nom', 'membre__prenom']
    
    def get_membre(self, obj):
        return f"{obj.membre.prenom} {obj.membre.nom}" if obj.membre else "N/A"
    get_membre.short_description = 'Membre'
    
    actions = ['marquer_comme_payees']
    
    def marquer_comme_payees(self, request, queryset):
        updated = queryset.filter(statut__in=['due', 'en_retard']).update(
            statut='payee',
            date_paiement=timezone.now(),
            enregistre_par=request.user
        )
        self.message_user(request, f"{updated} cotisations marquées comme payées.")
    marquer_comme_payees.short_description = "Marquer comme payées"


@admin.register(StatistiquesAssurance)
class StatistiquesAssuranceAdmin(admin.ModelAdmin):
    """Administration des statistiques"""
    
    list_display = ['periode', 'total_membres', 'chiffre_affaires', 'total_remboursements']
    list_filter = ['periode']


@admin.register(ConfigurationAssurance)
class ConfigurationAssuranceAdmin(admin.ModelAdmin):
    """Administration de la configuration"""
    
    list_display = ['nom_assureur', 'taux_couverture_defaut', 'delai_validite_bon', 'updated_at']


@admin.register(RapportAssureur)
class RapportAssureurAdmin(admin.ModelAdmin):
    """Administration des rapports"""
    
    list_display = ['titre', 'assureur', 'type_rapport', 'date_generation']
    list_filter = ['type_rapport', 'assureur']


# =============================================================================
# ENREGISTREMENT DES MODÈLES PROXY
# =============================================================================

admin.site.register(BonPriseEnCharge)
admin.site.register(BonDeSoin)

# =============================================================================
# CONFIGURATION DU SITE ADMIN
# =============================================================================

admin.site.site_header = "Plateforme de Gestion d'Assurance"
admin.site.site_title = "Admin Assurance"
admin.site.index_title = "Tableau de Bord"