from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import (
    Medecin, SpecialiteMedicale, EtablissementMedical,
    DisponibiliteMedecin, Consultation, Ordonnance, AvisMedecin
)


class MedecinInline(admin.StackedInline):
    """Inline pour afficher le profil médecin dans l'admin User"""
    model = Medecin
    can_delete = False
    verbose_name_plural = 'Profil Médecin'
    fk_name = 'user'
    fields = ['numero_ordre', 'specialite', 'etablissement', 'actif', 'disponible']


class CustomUserAdmin(UserAdmin):
    """Admin User personnalisé avec le profil médecin"""
    inlines = [MedecinInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'get_medecin_profile']
    
    def get_medecin_profile(self, obj):
        if hasattr(obj, 'medecin'):
            return format_html(
                '<a href="{}">Voir profil médecin</a>',
                reverse('admin:medecin_medecin_change', args=[obj.medecin.id])
            )
        return "Non"
    get_medecin_profile.short_description = 'Profil Médecin'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


@admin.register(Medecin)
class MedecinAdmin(admin.ModelAdmin):
    """Admin pour le modèle Medecin"""
    list_display = [
        'numero_ordre', 'get_full_name', 'specialite', 'etablissement', 
        'actif', 'disponible', 'get_consultations_count', 'get_ordonnances_count'
    ]
    list_filter = ['actif', 'disponible', 'specialite', 'etablissement', 'date_inscription']
    search_fields = ['user__first_name', 'user__last_name', 'numero_ordre', 'user__email']
    readonly_fields = [
        'date_inscription', 'date_derniere_modif', 'get_consultations_count', 
        'get_ordonnances_count', 'get_user_link'
    ]
    list_editable = ['actif', 'disponible']
    list_per_page = 20
    
    # ✅ CORRECTION : Définir actions comme liste
    actions = ['marquer_comme_actif', 'marquer_comme_inactif']
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('get_user_link', 'numero_ordre')
        }),
        ('Informations professionnelles', {
            'fields': ('specialite', 'etablissement', 'annees_experience', 'tarif_consultation')
        }),
        ('Coordonnées', {
            'fields': ('telephone_pro', 'email_pro')
        }),
        ('Statut', {
            'fields': ('actif', 'disponible', 'diplome_verifie')
        }),
        ('Documents', {
            'fields': ('cv_document', 'horaires_travail')
        }),
        ('Statistiques', {
            'fields': ('get_consultations_count', 'get_ordonnances_count')
        }),
        ('Dates', {
            'fields': ('date_inscription', 'date_derniere_modif')
        }),
    )

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Nom complet'
    get_full_name.admin_order_field = 'user__last_name'

    def get_consultations_count(self, obj):
        count = Consultation.objects.filter(medecin=obj).count()
        url = reverse('admin:medecin_consultation_changelist') + f'?medecin__id__exact={obj.id}'
        return format_html('<a href="{}">{} consultations</a>', url, count)
    get_consultations_count.short_description = 'Consultations'

    def get_ordonnances_count(self, obj):
        count = Ordonnance.objects.filter(medecin=obj.user).count()
        url = reverse('admin:medecin_ordonnance_changelist') + f'?medecin__id__exact={obj.user.id}'
        return format_html('<a href="{}">{} ordonnances</a>', url, count)
    get_ordonnances_count.short_description = 'Ordonnances'

    def get_user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.get_full_name())
    get_user_link.short_description = 'Utilisateur'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'specialite', 'etablissement')
    
    # ✅ CORRECTION : Méthodes d'action définies dans la classe
    def marquer_comme_actif(self, request, queryset):
        updated = queryset.update(actif=True)
        self.message_user(request, f'{updated} médecin(s) marqué(s) comme actif(s).')
    marquer_comme_actif.short_description = "Marquer comme actif"
    
    def marquer_comme_inactif(self, request, queryset):
        updated = queryset.update(actif=False)
        self.message_user(request, f'{updated} médecin(s) marqué(s) comme inactif(s).')
    marquer_comme_inactif.short_description = "Marquer comme inactif"


@admin.register(SpecialiteMedicale)
class SpecialiteMedicaleAdmin(admin.ModelAdmin):
    """Admin pour les spécialités médicales"""
    list_display = ['nom', 'get_medecins_count', 'actif']
    list_filter = ['actif']
    search_fields = ['nom', 'description']
    list_editable = ['actif']
    
    # ✅ CORRECTION : Définir actions comme liste de strings
    actions = ['activate_specialites', 'deactivate_specialites']

    def get_medecins_count(self, obj):
        count = obj.medecins.count()
        url = reverse('admin:medecin_medecin_changelist') + f'?specialite__id__exact={obj.id}'
        return format_html('<a href="{}">{} médecins</a>', url, count)
    get_medecins_count.short_description = 'Médecins'

    def activate_specialites(self, request, queryset):
        updated = queryset.update(actif=True)
        self.message_user(request, f'{updated} spécialité(s) activée(s) avec succès.')
    activate_specialites.short_description = "Activer les spécialités sélectionnées"

    def deactivate_specialites(self, request, queryset):
        updated = queryset.update(actif=False)
        self.message_user(request, f'{updated} spécialité(s) désactivée(s) avec succès.')
    deactivate_specialites.short_description = "Désactiver les spécialités sélectionnées"


@admin.register(EtablissementMedical)
class EtablissementMedicalAdmin(admin.ModelAdmin):
    """Admin pour les établissements médicaux"""
    list_display = ['nom', 'type_etablissement', 'ville', 'get_medecins_count', 'actif']
    list_filter = ['type_etablissement', 'ville', 'actif']
    search_fields = ['nom', 'ville', 'adresse']
    list_editable = ['actif']
    
    # ✅ CORRECTION : Définir actions (même si vide)
    actions = []
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'type_etablissement', 'actif')
        }),
        ('Coordonnées', {
            'fields': ('adresse', 'ville', 'pays', 'telephone', 'email')
        }),
    )

    def get_medecins_count(self, obj):
        count = obj.medecins.count()
        url = reverse('admin:medecin_medecin_changelist') + f'?etablissement__id__exact={obj.id}'
        return format_html('<a href="{}">{} médecins</a>', url, count)
    get_medecins_count.short_description = 'Médecins'


@admin.register(DisponibiliteMedecin)
class DisponibiliteMedecinAdmin(admin.ModelAdmin):
    """Admin pour les disponibilités des médecins"""
    list_display = ['medecin', 'get_jour_display', 'heure_debut', 'heure_fin', 'actif']
    list_filter = ['jour_semaine', 'actif', 'medecin']
    list_editable = ['heure_debut', 'heure_fin', 'actif']
    search_fields = ['medecin__user__first_name', 'medecin__user__last_name']
    
    # ✅ CORRECTION : Définir actions
    actions = []
    
    def get_jour_display(self, obj):
        return obj.get_jour_semaine_display()
    get_jour_display.short_description = 'Jour'
    get_jour_display.admin_order_field = 'jour_semaine'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('medecin__user')


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    """Admin pour les consultations"""
    list_display = [
        'id', 'medecin', 'membre', 'date_consultation', 'type_consultation', 
        'statut', 'get_duree_display', 'est_passee'
    ]
    list_filter = ['statut', 'type_consultation', 'date_consultation', 'medecin']
    search_fields = [
        'membre__user__first_name', 'membre__user__last_name', 
        'medecin__user__first_name', 'medecin__user__last_name'
    ]
    readonly_fields = ['date_creation', 'date_modification', 'est_passee']
    list_editable = ['statut']
    date_hierarchy = 'date_consultation'
    list_per_page = 25
    
    # ✅ CORRECTION : Définir actions
    actions = []
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('medecin', 'membre', 'date_consultation', 'duree', 'type_consultation', 'statut')
        }),
        ('Détails médicaux', {
            'fields': ('motifs', 'observations', 'diagnostic', 'recommandations')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification')
        }),
    )

    def get_duree_display(self, obj):
        return f"{obj.duree} min"
    get_duree_display.short_description = 'Durée'

    def est_passee(self, obj):
        if obj.est_passee:
            return format_html('<span style="color: green;">✓ Passée</span>')
        else:
            return format_html('<span style="color: orange;">⏳ À venir</span>')
    est_passee.short_description = 'Statut'
    est_passee.admin_order_field = 'date_consultation'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'medecin__user', 'membre__user'
        )

    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une nouvelle consultation
            obj.date_creation = timezone.now()
        obj.date_modification = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(Ordonnance)
class OrdonnanceAdmin(admin.ModelAdmin):
    """Admin pour les ordonnances"""
    list_display = [
        'numero', 'medecin', 'patient', 'date_prescription', 
        'type_ordonnance', 'statut', 'est_urgent', 'est_valide', 'jours_restants'
    ]
    list_filter = ['statut', 'type_ordonnance', 'est_urgent', 'date_prescription']
    search_fields = [
        'numero', 'patient__user__first_name', 'patient__user__last_name',
        'medecin__first_name', 'medecin__last_name'
    ]
    readonly_fields = [
        'numero', 'date_creation', 'date_modification', 'est_valide', 
        'jours_restants', 'medicaments_liste_display'
    ]
    list_editable = ['statut', 'est_urgent']
    date_hierarchy = 'date_prescription'
    list_per_page = 25
    
    # ✅ CORRECTION : Définir actions
    actions = []
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('numero', 'medecin', 'patient', 'consultation')
        }),
        ('Dates', {
            'fields': ('date_prescription', 'date_expiration', 'date_creation', 'date_modification')
        }),
        ('Détails médicaux', {
            'fields': ('type_ordonnance', 'diagnostic', 'medicaments', 'posologie', 'duree_traitement')
        }),
        ('Renouvellement', {
            'fields': ('renouvelable', 'nombre_renouvellements', 'renouvellements_effectues')
        }),
        ('Statut', {
            'fields': ('statut', 'est_urgent', 'notes')
        }),
        ('Informations calculées', {
            'fields': ('est_valide', 'jours_restants', 'medicaments_liste_display')
        }),
    )

    def medicaments_liste_display(self, obj):
        medicaments = obj.medicaments_liste
        if medicaments:
            html = '<ul>'
            for med in medicaments[:5]:  # Limiter à 5 médicaments
                html += f'<li>{med}</li>'
            if len(medicaments) > 5:
                html += f'<li>... et {len(medicaments) - 5} autres</li>'
            html += '</ul>'
            return format_html(html)
        return "Aucun médicament"
    medicaments_liste_display.short_description = 'Médicaments (liste)'

    def est_valide(self, obj):
        if obj.est_valide:
            return format_html('<span style="color: green;">✓ Valide</span>')
        else:
            return format_html('<span style="color: red;">✗ Expirée</span>')
    est_valide.short_description = 'Valide'
    est_valide.admin_order_field = 'date_expiration'

    def jours_restants(self, obj):
        jours = obj.jours_restants
        if jours > 7:
            color = 'green'
        elif jours > 3:
            color = 'orange'
        else:
            color = 'red'
        return format_html(f'<span style="color: {color}; font-weight: bold;">{jours} jours</span>')
    jours_restants.short_description = 'Jours restants'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'medecin', 'patient__user', 'consultation'
        )

    def save_model(self, request, obj, form, change):
        if not change and not obj.numero:
            # La sauvegarde générera automatiquement le numéro
            pass
        super().save_model(request, obj, form, change)


@admin.register(AvisMedecin)
class AvisMedecinAdmin(admin.ModelAdmin):
    """Admin pour les avis sur les médecins"""
    list_display = ['medecin', 'membre', 'note_etoiles', 'date_creation', 'approuve']
    list_filter = ['note', 'approuve', 'date_creation']
    list_editable = ['approuve']
    search_fields = [
        'medecin__user__first_name', 'medecin__user__last_name',
        'membre__user__first_name', 'membre__user__last_name'
    ]
    readonly_fields = ['date_creation', 'note_etoiles_display']
    list_per_page = 20
    
    # ✅ CORRECTION : Définir actions comme liste de strings
    actions = ['approuver_avis', 'desapprouver_avis']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('medecin', 'membre', 'note', 'approuve')
        }),
        ('Commentaire', {
            'fields': ('commentaire',)
        }),
        ('Affichage', {
            'fields': ('note_etoiles_display',)
        }),
        ('Date', {
            'fields': ('date_creation',)
        }),
    )

    def note_etoiles(self, obj):
        return obj.note_etoiles
    note_etoiles.short_description = 'Note'

    def note_etoiles_display(self, obj):
        return format_html('<span style="font-size: 16px; color: gold;">{}</span>', obj.note_etoiles)
    note_etoiles_display.short_description = 'Note en étoiles'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'medecin__user', 'membre__user'
        )
    
    # ✅ CORRECTION : Méthodes d'action définies dans la classe
    def approuver_avis(self, request, queryset):
        updated = queryset.update(approuve=True)
        self.message_user(request, f"{updated} avis approuvé(s).")
    approuver_avis.short_description = "Approuver les avis sélectionnés"
    
    def desapprouver_avis(self, request, queryset):
        updated = queryset.update(approuve=False)
        self.message_user(request, f"{updated} avis désapprouvé(s).")
    desapprouver_avis.short_description = "Désapprouver les avis sélectionnés"


# ✅ SUPPRIMER les anciennes fonctions d'actions externes qui causent des problèmes
# Ces fonctions ne sont plus nécessaires car les actions sont maintenant définies
# comme méthodes dans les classes respectives

# Réenregistrer UserAdmin avec l'inline Medecin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# Configuration du titre de l'admin
admin.site.site_header = "Administration du Système Médical"
admin.site.site_title = "Système Médical"
admin.site.index_title = "Tableau de bord de l'administration"