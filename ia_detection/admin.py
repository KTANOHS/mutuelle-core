from django.contrib import admin
from .models import ModeleIA, AnalyseIA

@admin.register(ModeleIA)
class ModeleIAAdmin(admin.ModelAdmin):
    list_display = ['nom', 'version', 'type_modele', 'est_actif', 'date_entrainement']
    list_filter = ['type_modele', 'est_actif']
    search_fields = ['nom', 'version']
    readonly_fields = ['date_entrainement']

@admin.register(AnalyseIA)
class AnalyseIAAdmin(admin.ModelAdmin):
    list_display = ['membre', 'type_analyse', 'score_confiance', 'date_analyse']
    list_filter = ['type_analyse', 'date_analyse']
    search_fields = ['membre__nom', 'membre__email']
    readonly_fields = ['date_analyse']
    date_hierarchy = 'date_analyse'
