# agents/analysis_script.py
import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Count, Sum, Avg, Q, F
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Agent, BonSoin, VerificationCotisation, ActiviteAgent, PerformanceAgent
from membres.models import Membre
from communication.models import Notification, Message

class DashboardAgentAnalyzer:
    """Classe pour analyser les données du dashboard agent"""
    
    def __init__(self, agent_id=None):
        self.agent = None
        if agent_id:
            self.agent = Agent.objects.get(id=agent_id)
        self.today = timezone.now().date()
        self.start_of_week = self.today - timedelta(days=self.today.weekday())
        self.start_of_month = self.today.replace(day=1)
    
    def get_agent_stats(self, agent_id=None):
        """Obtenir les statistiques principales d'un agent"""
        if agent_id:
            self.agent = Agent.objects.get(id=agent_id)
        
        if not self.agent:
            return {"error": "Aucun agent spécifié"}
        
        stats = {
            'agent': {
                'nom_complet': self.agent.nom_complet(),
                'matricule': self.agent.matricule,
                'poste': self.agent.poste,
                'anciennete': self.agent.anciennete(),
                'limite_quotidienne': self.agent.limite_bons_quotidienne
            },
            'periode_analyse': {
                'date': self.today.strftime('%d/%m/%Y'),
                'debut_semaine': self.start_of_week.strftime('%d/%m/%Y'),
                'debut_mois': self.start_of_month.strftime('%d/%m/%Y')
            }
        }
        
        # Statistiques quotidiennes
        stats.update(self._get_daily_stats())
        
        # Statistiques hebdomadaires
        stats.update(self._get_weekly_stats())
        
        # Statistiques mensuelles
        stats.update(self._get_monthly_stats())
        
        # Alertes et recommandations
        stats.update(self._get_alerts_and_recommendations())
        
        return stats
    
    def _get_daily_stats(self):
        """Statistiques du jour"""
        today_start = timezone.make_aware(datetime.combine(self.today, datetime.min.time()))
        today_end = timezone.make_aware(datetime.combine(self.today, datetime.max.time()))
        
        # Bons du jour
        bons_today = BonSoin.objects.filter(
            agent=self.agent,
            date_creation__range=(today_start, today_end)
        )
        
        # Vérifications du jour
        verifs_today = VerificationCotisation.objects.filter(
            agent=self.agent,
            date_verification__range=(today_start, today_end)
        )
        
        return {
            'quotidien': {
                'bons_crees': bons_today.count(),
                'bons_par_heure': self._get_bons_par_heure(today_start, today_end),
                'verifications_effectuees': verifs_today.count(),
                'membres_verifies': verifs_today.values('membre').distinct().count(),
                'taux_success_verifications': self._calculate_success_rate(verifs_today),
                'limite_restante': max(0, self.agent.limite_bons_quotidienne - bons_today.count()),
                'pourcentage_limite': (bons_today.count() / self.agent.limite_bons_quotidienne * 100) if self.agent.limite_bons_quotidienne > 0 else 0
            }
        }
    
    def _get_weekly_stats(self):
        """Statistiques de la semaine"""
        week_start = timezone.make_aware(datetime.combine(self.start_of_week, datetime.min.time()))
        week_end = timezone.make_aware(datetime.combine(self.today, datetime.max.time()))
        
        bons_semaine = BonSoin.objects.filter(
            agent=self.agent,
            date_creation__range=(week_start, week_end)
        )
        
        verifs_semaine = VerificationCotisation.objects.filter(
            agent=self.agent,
            date_verification__range=(week_start, week_end)
        )
        
        return {
            'hebdomadaire': {
                'bons_crees': bons_semaine.count(),
                'moyenne_quotidienne': round(bons_semaine.count() / 7, 1),
                'verifications_effectuees': verifs_semaine.count(),
                'jours_actifs': self._get_jours_actifs_semaine(week_start, week_end),
                'tendance_bons': self._calculate_tendance(bons_semaine, 'date_creation'),
                'types_soins_populaires': self._get_types_soins_populaires(bons_semaine)
            }
        }
    
    def _get_monthly_stats(self):
        """Statistiques du mois"""
        month_start = timezone.make_aware(datetime.combine(self.start_of_month, datetime.min.time()))
        month_end = timezone.make_aware(datetime.combine(self.today, datetime.max.time()))
        
        bons_mois = BonSoin.objects.filter(
            agent=self.agent,
            date_creation__range=(month_start, month_end)
        )
        
        verifs_mois = VerificationCotisation.objects.filter(
            agent=self.agent,
            date_verification__range=(month_start, month_end)
        )
        
        return {
            'mensuel': {
                'bons_crees': bons_mois.count(),
                'verifications_effectuees': verifs_mois.count(),
                'montant_total_bons': bons_mois.aggregate(total=Sum('montant_max'))['total'] or 0,
                'moyenne_montant_bon': bons_mois.aggregate(moyenne=Avg('montant_max'))['moyenne'] or 0,
                'taux_utilisation_bons': self._calculate_taux_utilisation(bons_mois),
                'efficacite_verifications': self._calculate_efficacite_verifications(verifs_mois)
            }
        }
    
    def _get_alerts_and_recommendations(self):
        """Générer des alertes et recommandations"""
        alerts = []
        recommendations = []
        
        # Vérifier la limite quotidienne
        bons_du_jour = BonSoin.objects.filter(
            agent=self.agent,
            date_creation__date=self.today
        ).count()
        
        if bons_du_jour >= self.agent.limite_bons_quotidienne:
            alerts.append({
                'type': 'ALERTE',
                'message': f'Limite quotidienne atteinte ({bons_du_jour}/{self.agent.limite_bons_quotidienne})',
                'priorite': 'HAUTE'
            })
        elif bons_du_jour >= self.agent.limite_bons_quotidienne * 0.8:
            alerts.append({
                'type': 'ATTENTION',
                'message': f'Limite quotidienne proche ({bons_du_jour}/{self.agent.limite_bons_quotidienne})',
                'priorite': 'MOYENNE'
            })
        
        # Vérifier les bons expirés
        bons_expires = BonSoin.objects.filter(
            agent=self.agent,
            date_expiration__lt=timezone.now(),
            statut='en_attente'
        ).count()
        
        if bons_expires > 0:
            alerts.append({
                'type': 'ALERTE',
                'message': f'{bons_expires} bon(s) expiré(s) non utilisés',
                'priorite': 'MOYENNE'
            })
        
        # Recommandations basées sur les performances
        stats_semaine = self._get_weekly_stats()['hebdomadaire']
        if stats_semaine['bons_crees'] < 10:
            recommendations.append({
                'categorie': 'PRODUCTIVITE',
                'message': 'Augmenter le rythme de création de bons cette semaine',
                'action': 'Cibler 2-3 bons supplémentaires par jour'
            })
        
        return {
            'alertes': alerts,
            'recommandations': recommendations
        }
    
    def _get_bons_par_heure(self, start, end):
        """Analyser la répartition horaire des bons"""
        bons = BonSoin.objects.filter(
            agent=self.agent,
            date_creation__range=(start, end)
        ).extra({
            'heure': "EXTRACT(hour FROM date_creation)"
        }).values('heure').annotate(total=Count('id')).order_by('heure')
        
        return {f"{item['heure']}h": item['total'] for item in bons}
    
    def _get_jours_actifs_semaine(self, start, end):
        """Compter les jours d'activité dans la semaine"""
        jours_actifs = BonSoin.objects.filter(
            agent=self.agent,
            date_creation__range=(start, end)
        ).dates('date_creation', 'day').distinct().count()
        
        return jours_actifs
    
    def _calculate_tendance(self, queryset, field):
        """Calculer la tendance (croissance/décroissance)"""
        # Implémentation simplifiée - à améliorer
        return "STABLE"
    
    def _get_types_soins_populaires(self, queryset):
        """Obtenir les types de soins les plus populaires"""
        types = queryset.values('type_soin').annotate(
            total=Count('id'),
            montant_moyen=Avg('montant_max')
        ).order_by('-total')[:5]
        
        return list(types)
    
    def _calculate_success_rate(self, verifs_queryset):
        """Calculer le taux de succès des vérifications"""
        total = verifs_queryset.count()
        if total == 0:
            return 0
        
        succes = verifs_queryset.filter(statut_cotisation='a_jour').count()
        return round((succes / total) * 100, 1)
    
    def _calculate_taux_utilisation(self, bons_queryset):
        """Calculer le taux d'utilisation des bons"""
        total = bons_queryset.count()
        if total == 0:
            return 0
        
        utilises = bons_queryset.filter(statut='utilise').count()
        return round((utilises / total) * 100, 1)
    
    def _calculate_efficacite_verifications(self, verifs_queryset):
        """Calculer l'efficacité des vérifications"""
        total = verifs_queryset.count()
        if total == 0:
            return 0
        
        # Logique d'efficacité à définir selon les règles métier
        return 85.0  # Valeur exemple
    
    def generate_report(self, agent_id=None):
        """Générer un rapport complet"""
        stats = self.get_agent_stats(agent_id)
        
        if 'error' in stats:
            return stats
        
        # Formatage du rapport
        report = {
            'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'statistiques': stats,
            'resume': self._generate_summary(stats)
        }
        
        return report
    
    def _generate_summary(self, stats):
        """Générer un résumé exécutif"""
        quotidien = stats['quotidien']
        hebdomadaire = stats['hebdomadaire']
        mensuel = stats['mensuel']
        
        return {
            'performance_globale': self._evaluate_performance(quotidien, hebdomadaire, mensuel),
            'points_forts': self._identify_strengths(quotidien, hebdomadaire, mensuel),
            'points_amelioration': self._identify_improvements(quotidien, hebdomadaire, mensuel),
            'score_productivite': self._calculate_productivity_score(quotidien, hebdomadaire, mensuel)
        }
    
    def _evaluate_performance(self, quotidien, hebdomadaire, mensuel):
        """Évaluer la performance globale"""
        # Logique d'évaluation à adapter
        if quotidien['bons_crees'] >= 15 and mensuel['taux_utilisation_bons'] > 80:
            return "EXCELLENTE"
        elif quotidien['bons_crees'] >= 10 and mensuel['taux_utilisation_bons'] > 70:
            return "BONNE"
        else:
            return "SATISFAISANTE"
    
    def _identify_strengths(self, quotidien, hebdomadaire, mensuel):
        """Identifier les points forts"""
        strengths = []
        
        if quotidien['taux_success_verifications'] > 90:
            strengths.append("Taux de vérifications réussies élevé")
        
        if hebdomadaire['moyenne_quotidienne'] > 12:
            strengths.append("Productivité constante dans la création de bons")
        
        if mensuel['montant_total_bons'] > 500000:
            strengths.append("Gestion importante de montants de soins")
        
        return strengths
    
    def _identify_improvements(self, quotidien, hebdomadaire, mensuel):
        """Identifier les points d'amélioration"""
        improvements = []
        
        if quotidien['pourcentage_limite'] < 50:
            improvements.append("Utilisation partielle de la capacité de création de bons")
        
        if mensuel['taux_utilisation_bons'] < 70:
            improvements.append("Taux d'utilisation des bons à optimiser")
        
        return improvements
    
    def _calculate_productivity_score(self, quotidien, hebdomadaire, mensuel):
        """Calculer un score de productivité"""
        score = 0
        
        # Points pour les bons créés aujourd'hui
        score += min(quotidien['bons_crees'] * 2, 20)
        
        # Points pour la limite utilisée
        score += min(quotidien['pourcentage_limite'] / 5, 20)
        
        # Points pour les vérifications
        score += min(quotidien['verifications_effectuees'] * 3, 15)
        
        # Points pour le taux de succès
        score += min(quotidien['taux_success_verifications'] / 5, 20)
        
        # Points pour la productivité hebdomadaire
        score += min(hebdomadaire['moyenne_quotidienne'] * 2, 15)
        
        # Points pour le taux d'utilisation mensuel
        score += min(mensuel['taux_utilisation_bons'] / 5, 10)
        
        return min(round(score), 100)

def analyze_all_agents():
    """Analyser tous les agents actifs"""
    agents_actifs = Agent.objects.filter(est_actif=True)
    analyzer = DashboardAgentAnalyzer()
    
    rapports = {}
    for agent in agents_actifs:
        print(f"Analyse de l'agent: {agent.nom_complet()}")
        rapport = analyzer.generate_report(agent.id)
        rapports[agent.matricule] = rapport
    
    return rapports

def export_to_excel(rapports, filename="rapport_agents.xlsx"):
    """Exporter les rapports vers Excel"""
    data = []
    
    for matricule, rapport in rapports.items():
        stats = rapport['statistiques']
        data.append({
            'Matricule': matricule,
            'Nom': stats['agent']['nom_complet'],
            'Bons aujourd\'hui': stats['quotidien']['bons_crees'],
            'Vérifications aujourd\'hui': stats['quotidien']['verifications_effectuees'],
            'Bons semaine': stats['hebdomadaire']['bons_crees'],
            'Bons mois': stats['mensuel']['bons_crees'],
            'Taux utilisation': f"{stats['mensuel']['taux_utilisation_bons']}%",
            'Score productivité': rapport['resume']['score_productivite'],
            'Performance': rapport['resume']['performance_globale']
        })
    
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Rapport exporté vers {filename}")

if __name__ == "__main__":
    # Exemple d'utilisation
    if len(sys.argv) > 1:
        agent_id = int(sys.argv[1])
        analyzer = DashboardAgentAnalyzer(agent_id)
        rapport = analyzer.generate_report()
        
        # Affichage formaté
        import json
        print(json.dumps(rapport, indent=2, ensure_ascii=False))
    else:
        # Analyser tous les agents
        rapports = analyze_all_agents()
        export_to_excel(rapports)
        
        print(f"Analyse terminée pour {len(rapports)} agents")