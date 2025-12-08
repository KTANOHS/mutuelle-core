

# Register your models here.
# pharmacie_public/admin.py
from django.contrib import admin
from .models import PharmaciePublic, MedicamentPublic, CommandePublic, LigneCommandePublic, GardePublic

@admin.register(PharmaciePublic)
class PharmaciePublicAdmin(admin.ModelAdmin):
    list_display = ['nom_pharmacie', 'ville', 'type_pharmacie', 'statut', 'est_de_garde', 'partenaire_mutuelle']
    list_filter = ['statut', 'type_pharmacie', 'est_de_garde', 'partenaire_mutuelle', 'ville']
    search_fields = ['nom_pharmacie', 'ville', 'code_postal']
#     readonly_fields = ['date_inscription']  # ⚠️ COMMENTÉ - vérifier les champs
# 
# @admin.register(MedicamentPublic)
class MedicamentPublicAdmin(admin.ModelAdmin):
    list_display = ['nom', 'pharmacie', 'categorie', 'prix', 'stock', 'necessite_ordonnance']
    list_filter = ['categorie', 'necessite_ordonnance', 'pharmacie']
    search_fields = ['nom', 'principe_actif', 'laboratoire']

@admin.register(CommandePublic)
class CommandePublicAdmin(admin.ModelAdmin):
    list_display = ['numero_commande', 'client', 'pharmacie', 'statut', 'montant_total', 'date_commande']
    list_filter = ['statut', 'pharmacie']
    search_fields = ['numero_commande', 'client__username', 'pharmacie__nom_pharmacie']
#     readonly_fields = ['date_commande']  # ⚠️ COMMENTÉ - vérifier les champs
# 
# admin.site.register(LigneCommandePublic)
admin.site.register(GardePublic)