# correction_admin_urgence.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("🚨 CORRECTION URGENTE DE L'ADMIN")
print("=" * 50)

def corriger_admin_historiquescore():
    """Corrige le fichier admin pour HistoriqueScore"""
    
    admin_content = '''from django.contrib import admin
from .models import HistoriqueScore

@admin.register(HistoriqueScore)
class HistoriqueScoreAdmin(admin.ModelAdmin):
    """Admin corrigé pour HistoriqueScore - sans accès aux champs problématiques"""
    
    # Champs à afficher (sans relation vers Membre qui cause l'erreur)
    list_display = ['get_membre_id', 'score', 'niveau_risque', 'date_calcul']
    list_filter = ['niveau_risque', 'date_calcul']
    search_fields = ['membre_id']  # Recherche par ID seulement
    readonly_fields = ['date_calcul']
    date_hierarchy = 'date_calcul'
    
    def get_membre_id(self, obj):
        """Affiche seulement l'ID du membre pour éviter l'erreur"""
        return f"Membre ID: {obj.membre_id}"
    get_membre_id.short_description = 'Membre'
    
    # Désactiver les actions qui pourraient causer des erreurs
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def get_queryset(self, request):
        """Queryset de base sans jointures problématiques"""
        return super().get_queryset(request).defer('membre')  # Évite de charger la relation

    # Formulaire personnalisé pour éviter les problèmes
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "membre":
            # Limiter les choix si nécessaire
            pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
'''

    with open('scoring/admin_corrige.py', 'w', encoding='utf-8') as f:
        f.write(admin_content)
    
    print("✅ Admin corrigé créé: scoring/admin_corrige.py")

def corriger_admin_principal():
    """Corrige le fichier admin principal pour désactiver HistoriqueScore problématique"""
    
    admin_principal_content = '''from django.contrib import admin
from scoring.models import RegleScoring
from relances.models import TemplateRelance, RelanceProgrammee
from ia_detection.models import ModeleIA, AnalyseIA

# Apps qui fonctionnent parfaitement
@admin.register(RegleScoring)
class RegleScoringAdmin(admin.ModelAdmin):
    list_display = ['nom', 'critere', 'poids', 'est_active']
    list_filter = ['est_active']
    list_editable = ['poids', 'est_active']

@admin.register(TemplateRelance)
class TemplateRelanceAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type_relance', 'delai_jours']
    list_filter = ['type_relance']

@admin.register(RelanceProgrammee)
class RelanceProgrammeeAdmin(admin.ModelAdmin):
    list_display = ['get_membre_id', 'template', 'date_programmation', 'statut']
    list_filter = ['statut', 'date_programmation']
    
    def get_membre_id(self, obj):
        return f"Membre ID: {obj.membre_id}"
    get_membre_id.short_description = 'Membre'

@admin.register(ModeleIA)
class ModeleIAAdmin(admin.ModelAdmin):
    list_display = ['nom', 'version', 'type_modele', 'est_actif']

@admin.register(AnalyseIA)
class AnalyseIAAdmin(admin.ModelAdmin):
    list_display = ['get_membre_id', 'type_analyse', 'score_confiance', 'date_analyse']
    
    def get_membre_id(self, obj):
        return f"Membre ID: {obj.membre_id}"
    get_membre_id.short_description = 'Membre'

# NOTE: HistoriqueScore est temporairement désactivé à cause de l'erreur de champ
# from scoring.models import HistoriqueScore
# @admin.register(HistoriqueScore)
# class HistoriqueScoreAdmin(admin.ModelAdmin):
#     list_display = ['get_membre_id', 'score', 'niveau_risque', 'date_calcul']
#     
#     def get_membre_id(self, obj):
#         return f"Membre ID: {obj.membre_id}"
'''

    with open('scoring/admin.py', 'w', encoding='utf-8') as f:
        f.write(admin_principal_content)
    
    print("✅ Admin principal corrigé")

def creer_interface_alternative():
    """Crée une interface alternative pour voir les scores"""
    
    interface_content = '''import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from scoring.models import HistoriqueScore
from django.db import models

def afficher_scores_interface():
    """Interface alternative pour afficher les scores sans erreur"""
    print("📊 INTERFACE ALTERNATIVE - SCORES DES MEMBRES")
    print("=" * 50)
    
    # Récupérer les scores avec une requête simple
    scores = HistoriqueScore.objects.all().order_by('-date_calcul')
    
    print(f"📋 Total scores dans le système: {scores.count()}")
    print("\\n🎯 DERNIERS SCORES CALCULÉS:")
    print("-" * 40)
    
    for score in scores[:10]:  # 10 derniers scores
        print(f"👤 Membre ID: {score.membre_id}")
        print(f"   🎯 Score: {score.score}")
        print(f"   📊 Risque: {score.niveau_risque}")
        print(f"   📅 Date: {score.date_calcul.strftime('%d/%m/%Y %H:%M')}")
        print()
    
    # Statistiques
    stats = scores.aggregate(
        moyenne=models.Avg('score'),
        min_score=models.Min('score'),
        max_score=models.Max('score')
    )
    
    print("📈 STATISTIQUES:")
    print(f"   📊 Score moyen: {stats['moyenne']:.1f}")
    print(f"   📉 Score min: {stats['min_score']:.1f}")
    print(f"   📈 Score max: {stats['max_score']:.1f}")
    
    # Distribution des risques
    distribution = scores.values('niveau_risque').annotate(
        count=models.Count('id')
    ).order_by('-count')
    
    print("\\n📋 DISTRIBUTION DES RISQUES:")
    for item in distribution:
        pourcentage = (item['count'] / scores.count() * 100)
        print(f"   {item['niveau_risque']}: {item['count']} scores ({pourcentage:.1f}%)")

if __name__ == "__main__":
    afficher_scores_interface()
'''

    with open('interface_scores.py', 'w', encoding='utf-8') as f:
        f.write(interface_content)
    
    print("✅ Interface alternative créée: interface_scores.py")

def main():
    print("🚨 CORRECTION DE L'ERREUR ADMIN EN COURS...")
    print("=" * 50)
    
    # 1. Corriger l'admin principal
    corriger_admin_principal()
    
    # 2. Créer une interface alternative
    creer_interface_alternative()
    
    print("\\n" + "=" * 50)
    print("🎉 CORRECTIONS APPLIQUÉES!")
    print("\\n📋 CE QUI A ÉTÉ CORRIGÉ:")
    print("   ✅ Admin principal - Désactive HistoriqueScore problématique")
    print("   ✅ Interface alternative - Affiche les scores sans erreur")
    print("   ✅ Autres fonctionnalités - Toujours accessibles")
    
    print("\\n🚀 REDÉMARRAGE REQUIS:")
    print("   1. Arrêtez le serveur (Ctrl+C)")
    print("   2. Redémarrez: python manage.py runserver")
    print("   3. Accédez à: http://127.0.0.1:8000/admin/")
    
    print("\\n💡 ACCÈS AUX SCORES:")
    print("   python interface_scores.py")

if __name__ == "__main__":
    main()