import os
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
    print("\n🎯 DERNIERS SCORES CALCULÉS:")
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
    
    print("\n📋 DISTRIBUTION DES RISQUES:")
    for item in distribution:
        pourcentage = (item['count'] / scores.count() * 100)
        print(f"   {item['niveau_risque']}: {item['count']} scores ({pourcentage:.1f}%)")

if __name__ == "__main__":
    afficher_scores_interface()
