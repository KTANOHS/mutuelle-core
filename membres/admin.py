# membres/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Membre

@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    # Colonnes visibles dans la liste
    list_display = (
        'numero_unique', 'nom_complet', 'telephone',
        'statut_colore', 'categorie', 'date_inscription',
        'est_a_jour_display'
    )

    # Filtres à droite
    list_filter = ('statut', 'categorie', 'date_inscription', 'cmu_option')

    # Barre de recherche
    search_fields = ('numero_unique', 'nom', 'prenom', 'telephone')

    # Champs en lecture seule dans le formulaire
    # readonly_fields = ('numero_unique', 'date_inscription', 'age_display')  # ⚠️ COMMENTÉ - vérifier les champs

    # Champs organisés par sections
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('numero_unique', 'nom', 'prenom', 'date_naissance', 'age_display')
        }),
        ('Coordonnées', {
            'fields': ('telephone', 'email', 'adresse', 'profession')
        }),
        ('Informations assurance', {
            'fields': ('statut', 'categorie', 'cmu_option', 'numero_urgence')
        }),
        ('Cotisations', {
            'fields': ('date_derniere_cotisation', 'prochain_paiement_le')
        }),
        ('Système', {
            'fields': ('user', 'date_inscription')
        }),
    )

    # Afficher est_a_jour_display uniquement sur la modification
    # def get_readonly_fields(self, request, obj=None):  # ⚠️ COMMENTÉ - vérifier les champs
    #     if obj:  # change_view
    #         return self.readonly_fields + ('est_a_jour_display',)
    #     return self.readonly_fields

    # ------------------------
    # Méthodes pour l'affichage
    # ------------------------
    def nom_complet(self, obj):
        return f"{obj.nom} {obj.prenom}"
    nom_complet.short_description = 'Nom complet'

    def statut_colore(self, obj):
        couleurs = {'AC': 'success', 'RE': 'danger', 'IN': 'warning'}
        libelle = obj.get_statut_display()
        couleur = couleurs.get(obj.statut, 'secondary')
        return format_html('<span class="badge badge-{}">{}</span>', couleur, libelle)
    statut_colore.short_description = 'Statut'

    def age_display(self, obj):
        return f"{obj.age} ans" if obj.age else "Non renseigné"
    age_display.short_description = 'Âge'

    def est_a_jour_display(self, obj):
        if obj.est_a_jour():
            return format_html('<span style="color: green;">✓ À jour</span>')
        return format_html('<span style="color: red;">✘ En retard</span>')
    est_a_jour_display.short_description = 'Cotisation'

    # ------------------------
    # CSS personnalisé (optionnel)
    # ------------------------
    class Media:
        css = {
            'all': ('admin/css/membre_admin.css',)
        }