from django.contrib import admin
from scoring.models import RegleScoring

# ✅ SEULEMENT les modèles de l'app scoring
@admin.register(RegleScoring)
class RegleScoringAdmin(admin.ModelAdmin):
    list_display = ['nom', 'critere', 'poids', 'est_active']
    list_filter = ['est_active']
    list_editable = ['poids', 'est_active']

# NOTE: HistoriqueScore est temporairement désactivé à cause de l'erreur de champ
# from scoring.models import HistoriqueScore
# @admin.register(HistoriqueScore)
# class HistoriqueScoreAdmin(admin.ModelAdmin):
#     list_display = ['get_membre_id', 'score', 'niveau_risque', 'date_calcul']
#     
#     def get_membre_id(self, obj):
#         return f"Membre ID: {obj.membre_id}"