from django.contrib import admin
from .models import TemplateRelance, RelanceProgrammee

@admin.register(TemplateRelance)
class TemplateRelanceAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type_relance', 'delai_jours']
    list_filter = ['type_relance']
    search_fields = ['nom', 'sujet']

@admin.register(RelanceProgrammee)
class RelanceProgrammeeAdmin(admin.ModelAdmin):
    list_display = ['membre', 'template', 'date_programmation', 'statut', 'envoyee']
    list_filter = ['statut', 'envoyee', 'date_programmation']
    search_fields = ['membre__nom']
    readonly_fields = ['date_programmation']
    date_hierarchy = 'date_programmation'
