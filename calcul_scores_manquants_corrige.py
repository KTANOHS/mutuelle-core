# calcul_scores_manquants_corrige.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from scoring.models import HistoriqueScore
from scoring.calculators import CalculateurScoreMembre

print("🎯 CALCUL DES SCORES MANQUANTS - CORRIGÉ")
print("=" * 50)

def identifier_membres_sans_score():
    """Identifie les membres sans score calculé"""
    print("🔍 Identification des membres sans score...")
    
    # Méthode 1: Membres sans entrée dans HistoriqueScore
    membres_avec_score = HistoriqueScore.objects.values_list('membre_id', flat=True).distinct()
    membres_sans_score = Membre.objects.exclude(id__in=membres_avec_score)
    
    print(f"📊 Membres sans score: {membres_sans_score.count()}/{Membre.objects.count()}")
    return membres_sans_score

def calculer_scores_manquants():
    """Calcule les scores pour les membres qui n'en ont pas"""
    calculateur = CalculateurScoreMembre()
    membres_sans_score = identifier_membres_sans_score()
    
    print("\\n🎯 Calcul des scores manquants...")
    compteur = 0
    
    for membre in membres_sans_score:
        try:
            resultat = calculateur.calculer_score_complet(membre)
            compteur += 1
            print(f"✅ {membre.nom}: {resultat['score_final']} ({resultat['niveau_risque']})")
        except Exception as e:
            print(f"❌ {membre.nom}: {e}")
    
    return compteur

def statistiques_finales():
    """Affiche les statistiques finales"""
    print("\\n📈 STATISTIQUES FINALES:")
    
    total_membres = Membre.objects.count()
    total_scores = HistoriqueScore.objects.count()
    
    print(f"👥 Membres totaux:   {total_membres}")
    print(f"📋 Scores calculés:  {total_scores}")
    print(f"📊 Couverture:       {(total_scores/total_membres*100):.1f}%")
    
    # Derniers scores calculés
    print("\\n🆕 DERNIERS SCORES CALCULÉS:")
    derniers_scores = HistoriqueScore.objects.select_related('membre').order_by('-date_calcul')[:5]
    
    for score in derniers_scores:
        print(f"   {score.membre.nom}: {score.score} → {score.niveau_risque}")

if __name__ == "__main__":
    scores_ajoutes = calculer_scores_manquants()
    
    if scores_ajoutes > 0:
        print(f"\\n🎉 {scores_ajoutes} nouveaux scores calculés!")
    else:
        print("\\n✅ Tous les membres ont déjà un score!")
    
    statistiques_finales()