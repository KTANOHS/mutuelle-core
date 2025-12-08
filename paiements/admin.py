from django.contrib import admin
from django.utils import timezone
from .models import Paiement, Remboursement, HistoriquePaiement

# ==============================================================================
# ADMIN INLINE POUR L'HISTORIQUE DES PAIEMENTS
# ==============================================================================

class HistoriquePaiementInline(admin.TabularInline):
    model = HistoriquePaiement
    extra = 0
    # readonly_fields = ['date_modification', 'modifie_par', 'ancien_statut', 'nouveau_statut', 'motif']  # ⚠️ COMMENTÉ - vérifier les champs
    # can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


# ==============================================================================
# ADMIN POUR LES PAIEMENTS - CORRESPOND AU MODÈLE RÉEL
# ==============================================================================

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = [
        'reference', 
        'bon', 
        'montant', 
        'statut', 
        'mode_paiement', 
        'date_paiement', 
        'created_by'
    ]
    
    list_filter = [
        'statut', 
        'mode_paiement',
        'date_paiement'
    ]
    
    search_fields = [
        'reference',
        'bon__numero_bon',
        'numero_transaction',
        'banque'
    ]
    
    # readonly_fields = [  # ⚠️ COMMENTÉ - vérifier les champs
    #     'reference',
    #     'date_creation',
    #     'date_modification',
    #     'created_by'
    # ]
    
    fieldsets = (
        ('Informations générales', {
            'fields': (
                'reference',
                'bon',
                'montant',
                'statut',
                'mode_paiement'
            )
        }),
        ('Dates', {
            'fields': (
                'date_paiement',
                'date_valeur',
            )
        }),
        ('Informations de transaction', {
            'fields': (
                'numero_transaction',
                'banque',
            )
        }),
        ('Documents', {
            'fields': (
                'preuve_paiement',
            )
        }),
        ('Suivi et audit', {
            'fields': (
                'notes',
                'created_by',
                'date_creation',
                'date_modification'
            )
        }),
    )
    
    inlines = [HistoriquePaiementInline]
    
    def save_model(self, request, obj, form, change):
        """S'assure que created_by est défini"""
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Optimise les requêtes pour l'admin"""
        return super().get_queryset(request).select_related(
            'bon', 
            'created_by'
        )


# ==============================================================================
# ADMIN POUR LES REMBOURSEMENTS - CORRESPOND AU MODÈLE RÉEL
# ==============================================================================

@admin.register(Remboursement)
class RemboursementAdmin(admin.ModelAdmin):
    list_display = [
        'paiement',
        'montant_rembourse',
        'statut',
        'date_demande',
        'traite_par'
    ]
    
    list_filter = [
        'statut',
        'date_demande'
    ]
    
    search_fields = [
        'paiement__reference',
        'motif',
        'traite_par__username'
    ]
    
    # readonly_fields = [  # ⚠️ COMMENTÉ - vérifier les champs
    #     'date_demande'
    # ]
    
    fieldsets = (
        ('Informations du remboursement', {
            'fields': (
                'paiement',
                'montant_rembourse',
                'statut',
                'motif'
            )
        }),
        ('Traitement', {
            'fields': (
                'date_demande',
                'date_traitement',
                'traite_par'
            )
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Gère la date de traitement et le traité par"""
        if obj.statut in ['VALIDEE', 'REJETEE', 'PAYEE'] and not obj.date_traitement:
            obj.date_traitement = timezone.now()
            obj.traite_par = request.user
        super().save_model(request, obj, form, change)


# ==============================================================================
# ADMIN POUR L'HISTORIQUE DES PAIEMENTS
# ==============================================================================

@admin.register(HistoriquePaiement)
class HistoriquePaiementAdmin(admin.ModelAdmin):
    list_display = [
        'paiement',
        'ancien_statut',
        'nouveau_statut',
        'modifie_par',
        'date_modification'
    ]
    
    list_filter = [
        'nouveau_statut',
        'date_modification',
        'modifie_par'
    ]
    
    search_fields = [
        'paiement__reference',
        'motif',
        'modifie_par__username'
    ]
    
    # readonly_fields = [  # ⚠️ COMMENTÉ - vérifier les champs
    #     'paiement',
    #     'ancien_statut',
    #     'nouveau_statut',
    #     'modifie_par',
    #     'date_modification',
    #     'motif'
    # ]
    
    def has_add_permission(self, request):
        """Empêche l'ajout manuel d'historique"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Empêche la modification de l'historique"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Empêche la suppression de l'historique"""
        return False