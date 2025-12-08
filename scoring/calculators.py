from django.db.models import Avg, Count, Sum
from membres.models import Membre
from scoring.models import HistoriqueScore, RegleScoring
from django.utils import timezone
from datetime import timedelta
import decimal

class CalculateurScoreMembre:
    def __init__(self):
        self.regles = self.charger_regles_actives()
    
    def charger_regles_actives(self):
        """Charge les règles de scoring actives"""
        return RegleScoring.objects.filter(est_active=True)
    
    def calculer_score_complet(self, membre):
        """Calcule le score complet d'un membre"""
        scores_criteres = {}
        
        for regle in self.regles:
            score_critere = self.calculer_critere(regle.critere, membre)
            scores_criteres[regle.critere] = {
                'score': float(score_critere),  # Convertir en float pour éviter les problèmes Decimal
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
        
        # Sauvegarder l'historique
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
        verifications = membre.verificationcotisation_set.all()
        if not verifications.exists():
            return 0.5
        
        paiements_ponctuels = verifications.filter(jours_retard=0).count()
        return float(paiements_ponctuels) / verifications.count()
    
    def calculer_historique_retards(self, membre):
        """Calcule l'historique des retards"""
        retard_moyen = membre.verificationcotisation_set.aggregate(
            avg_retard=Avg('jours_retard')
        )['avg_retard'] or 0
        
        return max(0, 1 - (float(retard_moyen) / 30))
    
    def calculer_niveau_dette(self, membre):
        """Calcule le score basé sur le niveau d'endettement"""
        dette_totale = membre.verificationcotisation_set.aggregate(
            total_dette=Sum('montant_dette')
        )['total_dette'] or 0
        
        return max(0, 1 - (float(dette_totale) / 1000))
    
    def calculer_anciennete_membre(self, membre):
        """Calcule le score basé sur l'ancienneté"""
        # Si pas de date création, retourner score neutre
        if not hasattr(membre, 'date_creation'):
            return 0.7
        
        try:
            anciennete_jours = (timezone.now() - membre.date_creation).days
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
    
    def calculer_frequence_verifications(self, membre):
        """Calcule le score basé sur la fréquence des vérifications"""
        verifications = membre.verificationcotisation_set.all()
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

def recalculer_scores_automatique():
    """Fonction pour recalculer tous les scores automatiquement"""
    membres = Membre.objects.all()
    calculateur = CalculateurScoreMembre()
    compteur = 0
    
    for membre in membres:
        try:
            calculateur.calculer_score_complet(membre)
            compteur += 1
        except Exception as e:
            print(f"❌ Erreur pour {membre.nom}: {e}")
    
    print(f"✅ Scores recalculés pour {compteur} membres")
    return compteur
