# pharmacien/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Pharmacien
from soins.models import Ordonnance

@admin.register(Pharmacien)
class PharmacienAdmin(admin.ModelAdmin):
    """Administration des pharmaciens"""
    list_display = ('user', 'numero_pharmacien', 'nom_pharmacie', 'telephone', 'actif', 'date_inscription')
    list_filter = ('actif', 'date_inscription')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'nom_pharmacie', 'numero_pharmacien')
    readonly_fields = ('date_inscription',)
    
    fieldsets = (
        ('Informations de connexion', {
            'fields': ('user', 'actif')
        }),
        ('Informations professionnelles', {
            'fields': ('numero_pharmacien', 'nom_pharmacie', 'adresse_pharmacie', 'telephone')
        }),
        ('Dates', {
            'fields': ('date_inscription',)
        }),
    )


class OrdonnanceAdmin(admin.ModelAdmin):
    """Administration des ordonnances pour les pharmaciens"""
    list_display = ('id', 'medicament', 'get_patient', 'get_medecin', 'statut', 'date_creation', 'date_validation')
    list_filter = ('statut', 'date_creation', 'date_validation')
    search_fields = ('medicament', 'bon_de_soin__patient__first_name', 'bon_de_soin__patient__last_name')
    readonly_fields = ('date_creation', 'date_validation')
    
    def get_patient(self, obj):
        return obj.bon_de_soin.patient if obj.bon_de_soin and obj.bon_de_soin.patient else "Non spécifié"
    get_patient.short_description = 'Patient'
    
    def get_medecin(self, obj):
        return obj.bon_de_soin.medecin if obj.bon_de_soin and obj.bon_de_soin.medecin else "Non spécifié"
    get_medecin.short_description = 'Médecin'
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('bon_de_soin', 'statut', 'date_creation', 'date_validation')
        }),
        ('Prescription médicale', {
            'fields': ('medicament', 'posologie', 'duree', 'instructions')
        }),
    )


# Enregistrement conditionnel pour éviter les conflits
try:
    admin.site.register(Ordonnance, OrdonnanceAdmin)
except admin.sites.AlreadyRegistered:
    # Le modèle est peut-être déjà enregistré dans soins/admin.py
    pass