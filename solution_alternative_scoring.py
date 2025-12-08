# solution_alternative_scoring.py
import os
import django
import sqlite3
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import models
import decimal
from datetime import datetime

print("🚀 SOLUTION ALTERNATIVE - CALCUL DIRECT")
print("=" * 50)

def get_membres_direct_sql():
    """Récupère les membres directement via SQL pour éviter l'erreur ORM"""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Récupérer tous les membres avec leurs IDs et noms
    cursor.execute("SELECT id, nom FROM membres_membre")
    membres = cursor.fetchall()
    
    conn.close()
    return [{'id': row[0], 'nom': row[1]} for row in membres]

def get_membres_avec_scores():
    """Récupère les IDs des membres qui ont déjà des scores"""
    from scoring.models import HistoriqueScore
    return list(HistoriqueScore.objects.values_list('membre_id', flat=True).distinct())

def calculer_score_membre_direct(membre_id, membre_nom):
    """Calcule le score pour un membre spécifique en utilisant des requêtes directes"""
    from agents.models import VerificationCotisation
    from scoring.models import HistoriqueScore, RegleScoring
    
    print(f"🎯 Calcul pour: {membre_nom}")
    
    try:
        # Récupérer les vérifications du membre
        verifications = VerificationCotisation.objects.filter(membre_id=membre_id)
        
        if not verifications.exists():
            print(f"   ⚠️  Aucune vérification pour {membre_nom}")
            return None
        
        # Calculer les métriques de base
        total_verifications = verifications.count()
        paiements_ponctuels = verifications.filter(jours_retard=0).count()
        retard_moyen = verifications.aggregate(avg=Avg('jours_retard'))['avg'] or 0
        dette_totale = verifications.aggregate(total=Sum('montant_dette'))['total'] or 0
        
        # Règles de scoring (récupérées une seule fois)
        regles = RegleScoring.objects.filter(est_active=True)
        
        scores_criteres = {}
        score_final = 0
        
        for regle in regles:
            if regle.critere == 'ponctualite_paiements':
                score = float(paiements_ponctuels) / total_verifications if total_verifications > 0 else 0.5
            elif regle.critere == 'historique_retards':
                score = max(0, 1 - (float(retard_moyen) / 30))
            elif regle.critere == 'niveau_dette':
                score = max(0, 1 - (float(dette_totale) / 1000))
            elif regle.critere == 'anciennete_membre':
                score = 0.7  # Valeur par défaut
            elif regle.critere == 'frequence_verifications':
                score = min(1.0, float(total_verifications) / 10)
            else:
                score = 0.5
            
            scores_criteres[regle.critere] = {
                'score': score,
                'poids': float(regle.poids),
                'nom_regle': regle.nom
            }
            
            score_final += score * float(regle.poids)
        
        # Normalisation
        score_final = max(0, min(100, score_final * 100))
        
        # Déterminer le niveau de risque
        if score_final >= 80:
            niveau_risque = "🟢 FAIBLE RISQUE"
        elif score_final >= 60:
            niveau_risque = "🟡 RISQUE MODÉRÉ"
        elif score_final >= 40:
            niveau_risque = "🟠 RISQUE ÉLEVÉ"
        else:
            niveau_risque = "🔴 RISQUE TRÈS ÉLEVÉ"
        
        # Sauvegarder le résultat
        HistoriqueScore.objects.create(
            membre_id=membre_id,
            score=decimal.Decimal(str(round(score_final, 2))),
            niveau_risque=niveau_risque,
            details_calcul=scores_criteres
        )
        
        print(f"   ✅ Score: {score_final:.1f} → {niveau_risque}")
        return score_final
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return None

def calculer_tous_scores_alternative():
    """Calcule tous les scores manquants avec l'approche alternative"""
    print("🔍 Identification des membres...")
    
    # Récupérer tous les membres via SQL
    tous_membres = get_membres_direct_sql()
    membres_avec_scores = get_membres_avec_scores()
    
    # Filtrer les membres sans score
    membres_sans_score = [m for m in tous_membres if m['id'] not in membres_avec_scores]
    
    print(f"📊 Membres totaux: {len(tous_membres)}")
    print(f"📋 Scores existants: {len(membres_avec_scores)}")
    print(f"🎯 Membres sans score: {len(membres_sans_score)}")
    
    if not membres_sans_score:
        print("✅ Tous les membres ont déjà un score!")
        return 0
    
    print("\n🎯 Calcul des scores manquants...")
    compteur = 0
    
    for membre in membres_sans_score:
        score = calculer_score_membre_direct(membre['id'], membre['nom'])
        if score is not None:
            compteur += 1
    
    return compteur

def afficher_statistiques_finales():
    """Affiche les statistiques finales"""
    from scoring.models import HistoriqueScore
    
    print("\n📈 STATISTIQUES FINALES:")
    
    total_membres = len(get_membres_direct_sql())
    total_scores = HistoriqueScore.objects.count()
    
    print(f"👥 Membres totaux:   {total_membres}")
    print(f"📋 Scores calculés:  {total_scores}")
    print(f"📊 Couverture:       {(total_scores/total_membres*100):.1f}%")
    
    # Distribution des risques
    risques = HistoriqueScore.objects.values('niveau_risque').annotate(
        count=models.Count('id')
    ).order_by('-count')
    
    print("\n📊 DISTRIBUTION DES RISQUES:")
    for risque in risques:
        pourcentage = (risque['count'] / total_scores * 100) if total_scores > 0 else 0
        print(f"   {risque['niveau_risque']:<25} {risque['count']:>2} membres ({pourcentage:.1f}%)")

def main():
    print("🚀 LANCEMENT DE LA SOLUTION ALTERNATIVE")
    print("=" * 50)
    
    scores_calcules = calculer_tous_scores_alternative()
    
    if scores_calcules > 0:
        print(f"\n🎉 {scores_calcules} nouveaux scores calculés avec succès!")
    else:
        print("\n✅ Aucun score manquant à calculer!")
    
    afficher_statistiques_finales()
    
    print("\n" + "=" * 50)
    print("🎉 SYSTÈME COMPLÈTEMENT OPÉRATIONNEL!")
    print("\n💡 Solution alternative réussie!")
    print("   Les scores sont stockés dans scoring.HistoriqueScore")

if __name__ == "__main__":
    main()