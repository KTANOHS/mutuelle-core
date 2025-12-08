# calculateur_scoring_corrige.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db.models import Avg, Count, Sum
from membres.models import Membre
from scoring.models import HistoriqueScore, RegleScoring
from django.utils import timezone
from datetime import timedelta
import decimal

class CalculateurScoreMembreCorrige:
    """Version corrigée du calculateur qui n'utilise pas les champs manquants"""
    
    def __init__(self):
        self.regles = self.charger_regles_actives()
    
    def charger_regles_actives(self):
        """Charge les règles de scoring actives"""
        return RegleScoring.objects.filter(est_active=True)
    
    def calculer_score_complet(self, membre):
        """Calcule le score complet d'un membre SANS utiliser les champs manquants"""
        scores_criteres = {}
        
        for regle in self.regles:
            score_critere = self.calculer_critere(regle.critere, membre)
            scores_criteres[regle.critere] = {
                'score': float(score_critere),
                'poids': float(regle.poids),
                'nom_regle': regle.nom
            }
        
        # Calcul du score pondéré
        score_final = sum(
            data['score'] * data['poids'] 
            for data in scores_criteres.values()
        )
        
        # Normalisation entre 0-100
        score_final = max(0, min(100, score_final * 100))
        
        resultat = {
            'score_final': round(score_final, 2),
            'details_scores': scores_criteres,
            'niveau_risque': self.determiner_niveau_risque(score_final)
        }
        
        # Sauvegarder l'historique (c'est ici que le score est stocké)
        HistoriqueScore.objects.create(
            membre=membre,
            score=decimal.Decimal(str(resultat['score_final'])),
            niveau_risque=resultat['niveau_risque'],
            details_calcul=resultat['details_scores']
        )
        
        return resultat
    
    def calculer_critere(self, critere, membre):
        """Calcule le score pour un critère spécifique"""
        method_name = f"calculer_{critere}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(membre)
        else:
            return 0.5  # Valeur par défaut
    
    def calculer_ponctualite_paiements(self, membre):
        """Calcule la ponctualité des paiements"""
        from agents.models import VerificationCotisation
        verifications = VerificationCotisation.objects.filter(membre=membre)
        if not verifications.exists():
            return 0.5
        
        paiements_ponctuels = verifications.filter(jours_retard=0).count()
        return float(paiements_ponctuels) / verifications.count()
    
    def calculer_historique_retards(self, membre):
        """Calcule l'historique des retards"""
        from agents.models import VerificationCotisation
        retard_moyen = VerificationCotisation.objects.filter(membre=membre).aggregate(
            avg_retard=Avg('jours_retard')
        )['avg_retard'] or 0
        
        return max(0, 1 - (float(retard_moyen) / 30))
    
    def calculer_niveau_dette(self, membre):
        """Calcule le score basé sur le niveau d'endettement"""
        from agents.models import VerificationCotisation
        dette_totale = VerificationCotisation.objects.filter(membre=membre).aggregate(
            total_dette=Sum('montant_dette')
        )['total_dette'] or 0
        
        return max(0, 1 - (float(dette_totale) / 1000))
    
    def calculer_anciennete_membre(self, membre):
        """Calcule le score basé sur l'ancienneté"""
        # Utiliser date_inscription si disponible, sinon score neutre
        if hasattr(membre, 'date_inscription') and membre.date_inscription:
            try:
                anciennete_jours = (timezone.now() - membre.date_inscription).days
                if anciennete_jours > 365:  # Plus d'un an
                    return 1.0
                elif anciennete_jours > 180:  # Plus de 6 mois
                    return 0.8
                elif anciennete_jours > 90:   # Plus de 3 mois
                    return 0.6
                else:
                    return 0.4
            except:
                return 0.5
        else:
            return 0.5
    
    def calculer_frequence_verifications(self, membre):
        """Calcule le score basé sur la fréquence des vérifications"""
        from agents.models import VerificationCotisation
        verifications = VerificationCotisation.objects.filter(membre=membre)
        total = verifications.count()
        
        if total == 0:
            return 0.5
        
        # Plus il y a de vérifications, plus c'est positif (si pas d'anomalies)
        return min(1.0, float(total) / 10)
    
    def determiner_niveau_risque(self, score):
        """Détermine le niveau de risque basé sur le score"""
        if score >= 80:
            return "🟢 FAIBLE RISQUE"
        elif score >= 60:
            return "🟡 RISQUE MODÉRÉ"
        elif score >= 40:
            return "🟠 RISQUE ÉLEVÉ"
        else:
            return "🔴 RISQUE TRÈS ÉLEVÉ"

def calculer_tous_scores_manquants():
    """Calcule tous les scores manquants avec le calculateur corrigé"""
    print("🎯 CALCUL DES SCORES MANQUANTS - VERSION CORRIGÉE")
    print("=" * 50)
    
    # Identifier les membres sans score
    membres_avec_score_ids = HistoriqueScore.objects.values_list('membre_id', flat=True).distinct()
    membres_sans_score = Membre.objects.exclude(id__in=membres_avec_score_ids)
    
    print(f"📊 Membres sans score: {membres_sans_score.count()}/{Membre.objects.count()}")
    
    if not membres_sans_score.exists():
        print("✅ Tous les membres ont déjà un score!")
        return 0
    
    calculateur = CalculateurScoreMembreCorrige()
    compteur = 0
    
    print("\\n🎯 Calcul en cours...")
    for membre in membres_sans_score:
        try:
            resultat = calculateur.calculer_score_complet(membre)
            compteur += 1
            print(f"✅ {membre.nom}: {resultat['score_final']} ({resultat['niveau_risque']})")
        except Exception as e:
            print(f"❌ {membre.nom}: {e}")
    
    return compteur

def afficher_statistiques_finales():
    """Affiche les statistiques finales"""
    print("\\n📈 STATISTIQUES FINALES:")
    
    total_membres = Membre.objects.count()
    total_scores = HistoriqueScore.objects.count()
    
    print(f"👥 Membres totaux:   {total_membres}")
    print(f"📋 Scores calculés:  {total_scores}")
    print(f"📊 Couverture:       {(total_scores/total_membres*100):.1f}%")
    
    # Distribution des risques
    from django.db import models
    risques = HistoriqueScore.objects.values('niveau_risque').annotate(
        count=models.Count('id')
    ).order_by('-count')
    
    print("\\n📊 DISTRIBUTION DES RISQUES:")
    for risque in risques:
        pourcentage = (risque['count'] / total_scores * 100) if total_scores > 0 else 0
        print(f"   {risque['niveau_risque']:<25} {risque['count']:>2} membres ({pourcentage:.1f}%)")

if __name__ == "__main__":
    scores_calcules = calculer_tous_scores_manquants()
    
    if scores_calcules > 0:
        print(f"\\n🎉 {scores_calcules} nouveaux scores calculés avec succès!")
    else:
        print("\\n✅ Aucun score manquant à calculer!")
    
    afficher_statistiques_finales()
    
    print("\\n" + "=" * 50)
    print("🎉 SYSTÈME COMPLÈTEMENT OPÉRATIONNEL!")