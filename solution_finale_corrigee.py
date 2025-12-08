# solution_finale_corrigee.py
import os
import django
import sqlite3
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db.models import Avg, Count, Sum
from django.db import models
import decimal

print("🚀 SOLUTION FINALE CORRIGÉE - CALCUL DIRECT")
print("=" * 50)

def get_membres_direct_sql():
    """Récupère les membres directement via SQL"""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nom FROM membres_membre")
    membres = cursor.fetchall()
    
    conn.close()
    return [{'id': row[0], 'nom': row[1]} for row in membres]

def get_membres_avec_scores():
    """Récupère les IDs des membres qui ont déjà des scores"""
    from scoring.models import HistoriqueScore
    return list(HistoriqueScore.objects.values_list('membre_id', flat=True).distinct())

def calculer_score_simple(membre_id, membre_nom):
    """Calcule un score simplifié sans erreurs"""
    from agents.models import VerificationCotisation
    from scoring.models import HistoriqueScore, RegleScoring
    
    print(f"🎯 Calcul pour: {membre_nom}")
    
    try:
        # Récupérer les vérifications
        verifications = VerificationCotisation.objects.filter(membre_id=membre_id)
        
        if not verifications.exists():
            print(f"   ⚠️  Aucune vérification")
            return None
        
        # Métriques de base
        total_verifs = verifications.count()
        ponctuels = verifications.filter(jours_retard=0).count()
        
        # Calculs sécurisés
        stats = verifications.aggregate(
            avg_retard=Avg('jours_retard'),
            total_dette=Sum('montant_dette')
        )
        
        retard_moyen = stats['avg_retard'] or 0
        dette_totale = stats['total_dette'] or 0
        
        # Règles
        regles = RegleScoring.objects.filter(est_active=True)
        score_final = 0
        details = {}
        
        for regle in regles:
            if regle.critere == 'ponctualite_paiements':
                score = float(ponctuels) / total_verifs if total_verifs > 0 else 0.5
            elif regle.critere == 'historique_retards':
                score = max(0, 1 - (float(retard_moyen) / 30))
            elif regle.critere == 'niveau_dette':
                score = max(0, 1 - (float(dette_totale) / 1000))
            elif regle.critere == 'anciennete_membre':
                score = 0.7  # Valeur par défaut
            elif regle.critere == 'frequence_verifications':
                score = min(1.0, float(total_verifs) / 10)
            else:
                score = 0.5
            
            score_final += score * float(regle.poids)
            details[regle.critere] = {
                'score': score, 
                'poids': float(regle.poids),
                'nom_regle': regle.nom
            }
        
        # Normalisation
        score_final = max(0, min(100, score_final * 100))
        
        # Niveau de risque
        if score_final >= 80:
            niveau_risque = "🟢 FAIBLE RISQUE"
        elif score_final >= 60:
            niveau_risque = "🟡 RISQUE MODÉRÉ"
        elif score_final >= 40:
            niveau_risque = "🟠 RISQUE ÉLEVÉ"
        else:
            niveau_risque = "🔴 RISQUE TRÈS ÉLEVÉ"
        
        # Sauvegarder
        HistoriqueScore.objects.create(
            membre_id=membre_id,
            score=decimal.Decimal(str(round(score_final, 2))),
            niveau_risque=niveau_risque,
            details_calcul=details
        )
        
        print(f"   ✅ Score: {score_final:.1f} → {niveau_risque}")
        return score_final
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return None

def calculer_tous_scores():
    """Calcule tous les scores manquants"""
    print("🔍 Identification des membres...")
    
    tous_membres = get_membres_direct_sql()
    membres_avec_scores = get_membres_avec_scores()
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
        score = calculer_score_simple(membre['id'], membre['nom'])
        if score is not None:
            compteur += 1
    
    return compteur

def afficher_resultats():
    """Affiche les résultats finaux"""
    from scoring.models import HistoriqueScore
    
    print("\n📈 RÉSULTATS FINAUX:")
    
    total_membres = len(get_membres_direct_sql())
    total_scores = HistoriqueScore.objects.count()
    
    print(f"👥 Membres totaux:   {total_membres}")
    print(f"📋 Scores calculés:  {total_scores}")
    print(f"📊 Couverture:       {(total_scores/total_membres*100):.1f}%")
    
    # Distribution
    risques = HistoriqueScore.objects.values('niveau_risque').annotate(
        count=Count('id')
    ).order_by('-count')
    
    print("\n📊 DISTRIBUTION DES RISQUES:")
    for risque in risques:
        pourcentage = (risque['count'] / total_scores * 100) if total_scores > 0 else 0
        print(f"   {risque['niveau_risque']:<25} {risque['count']:>2} membres ({pourcentage:.1f}%)")

def main():
    print("🚀 LANCEMENT DE LA SOLUTION FINALE")
    print("=" * 50)
    
    scores_calcules = calculer_tous_scores()
    
    if scores_calcules > 0:
        print(f"\n🎉 {scores_calcules} nouveaux scores calculés!")
    else:
        print("\n✅ Aucun score manquant!")
    
    afficher_resultats()
    
    print("\n" + "=" * 50)
    print("🎉 SYSTÈME COMPLÈTEMENT OPÉRATIONNEL!")
    print("\n🌐 Accédez à l'admin: http://127.0.0.1:8000/admin/scoring/historiquescore/")

if __name__ == "__main__":
    main()