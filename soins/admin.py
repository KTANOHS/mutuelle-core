from django.contrib import admin
from .models import TypeSoin, Soin, Prescription, DocumentSoin,BonDeSoin, Ordonnance

class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 1

class DocumentSoinInline(admin.TabularInline):
    model = DocumentSoin
    extra = 1

@admin.register(TypeSoin)
class TypeSoinAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prix_reference', 'actif']
    list_filter = ['actif']
    search_fields = ['nom']

@admin.register(Soin)
class SoinAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'patient', 'type_soin', 'date_realisation', 
        'medecin', 'cout_estime', 'statut'
    ]
    list_filter = ['statut', 'type_soin', 'date_realisation']
    search_fields = ['patient__nom', 'patient__prenom', 'diagnostic']
#     readonly_fields = ['created_at', 'updated_at']  # ⚠️ COMMENTÉ - vérifier les champs
#     inlines = [PrescriptionInline, DocumentSoinInline]
    fieldsets = (
        ('Informations générales', {
            'fields': ('patient', 'type_soin', 'date_realisation', 'statut')
        }),
        ('Informations médicales', {
            'fields': ('medecin', 'diagnostic', 'observations', 'duree_sejour')
        }),
        ('Aspects financiers', {
            'fields': ('cout_estime', 'cout_reel', 'taux_prise_charge')
        }),
        ('Validation', {
            'fields': ('valide_par', 'date_validation', 'motif_refus')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['medicament', 'soin', 'posologie', 'duree_traitement']
    list_filter = ['soin__type_soin']

@admin.register(DocumentSoin)
class DocumentSoinAdmin(admin.ModelAdmin):
    list_display = ['nom', 'soin', 'type_document', 'date_upload']
    list_filter = ['type_document']

 

@admin.register(BonDeSoin)
class BonDeSoinAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'medecin', 'date_soin', 'statut', 'montant']
    list_filter = ['statut', 'date_soin']
    search_fields = ['patient__nom', 'patient__prenom', 'diagnostic']
#     readonly_fields = ['date_creation']  # ⚠️ COMMENTÉ - vérifier les champs
# 
# @admin.register(Ordonnance)
class OrdonnanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'bon_de_soin', 'medicament', 'posologie', 'duree']
    list_filter = ['bon_de_soin__statut']
    search_fields = ['medicament', 'bon_de_soin__patient__nom']