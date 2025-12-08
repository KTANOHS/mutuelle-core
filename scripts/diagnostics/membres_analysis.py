# membres_analysis.py
import os
import django
from datetime import datetime, timedelta
import json
from django.db.models import Count, Sum, Avg, Q, F, Value
from django.db.models.functions import TruncMonth, TruncWeek, Concat, ExtractYear

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre, HistoriqueValidationDocument
from soins.models import Soin, BonDeSoin
from medecin.models import Consultation, Ordonnance
from django.contrib.auth.models import User
from django.utils import timezone
import time

class MembresAnalytics:
    """
    Classe complète d'analyse des données membres - VERSION SANS PANDAS
    """
    
    def __init__(self, membre_id=None):
        self.membre_id = membre_id
        self.membre = None
        self.data_loaded = False
        
        if membre_id:
            self.load_membre_data()
    
    def load_membre_data(self):
        """Charger les données du membre"""
        try:
            self.membre = Membre.objects.get(id=self.membre_id)
            self.data_loaded = True
            print(f"✅ Données chargées pour {self.membre.nom_complet}")
        except Membre.DoesNotExist:
            print(f"❌ Membre avec ID {self.membre_id} non trouvé")
            return False
        return True
    
    def get_membre_stats_overview(self, periode_jours=365):
        """
        Statistiques générales du membre
        """
        if not self.data_loaded:
            return None
        
        date_debut = timezone.now() - timedelta(days=periode_jours)
        
        stats = {
            # Soins et consultations
            'soins_total': Soin.objects.filter(patient=self.membre.user).count(),
            'soins_periode': Soin.objects.filter(
                patient=self.membre.user,
                date_realisation__gte=date_debut
            ).count(),
            'consultations_total': Consultation.objects.filter(membre=self.membre).count(),
            'ordonnances_total': Ordonnance.objects.filter(patient=self.membre).count(),
            
            # Bons de soin
            'bons_soin_total': BonDeSoin.objects.filter(patient=self.membre).count(),
            'bons_soin_valides': BonDeSoin.objects.filter(
                patient=self.membre,
                statut='VALIDE'
            ).count(),
            'bons_soin_attente': BonDeSoin.objects.filter(
                patient=self.membre,
                statut='EN_ATTENTE'
            ).count(),
            
            # Coûts et remboursements
            'cout_total_soins': Soin.objects.filter(
                patient=self.membre.user,
                statut='valide'
            ).aggregate(total=Sum('cout_reel'))['total'] or 0,
            
            'montant_bons_valides': BonDeSoin.objects.filter(
                patient=self.membre,
                statut='VALIDE'
            ).aggregate(total=Sum('montant'))['total'] or 0,
            
            # Informations membre
            'jours_inscription': (timezone.now().date() - self.membre.date_inscription).days,
            'jours_derniere_cotisation': (
                (timezone.now().date() - self.membre.date_derniere_cotisation).days 
                if self.membre.date_derniere_cotisation else 0
            ),
            'est_en_retard': self.membre.statut == Membre.StatutMembre.EN_RETARD,
        }
        
        return stats
    
    def get_soins_timeseries(self, periode='mois', nb_periodes=12):
        """
        Série temporelle des soins du membre
        """
        if not self.data_loaded:
            return None
        
        if periode == 'mois':
            trunc_func = TruncMonth('date_realisation')
        elif periode == 'semaine':
            trunc_func = TruncWeek('date_realisation')
        else:
            trunc_func = TruncMonth('date_realisation')
        
        timeseries = (
            Soin.objects
            .filter(patient=self.membre.user)
            .annotate(period=trunc_func)
            .values('period')
            .annotate(
                total=Count('id'),
                cout_total=Sum('cout_reel'),
                cout_moyen=Avg('cout_reel')
            )
            .order_by('period')
        )
        
        return list(timeseries)
    
    def get_type_soins_analysis(self):
        """
        Analyse des soins par type
        """
        if not self.data_loaded:
            return None
        
        analysis = (
            Soin.objects
            .filter(patient=self.membre.user)
            .values('type_soin__nom')
            .annotate(
                total=Count('id'),
                cout_total=Sum('cout_reel'),
                cout_moyen=Avg('cout_reel')
            )
            .order_by('-total')
        )
        
        return list(analysis)
    
    def get_medecins_frequents(self, top_n=5):
        """
        Médecins les plus fréquentés par le membre
        """
        if not self.data_loaded:
            return None
        
        medecins = (
            Consultation.objects
            .filter(membre=self.membre)
            .values('medecin__nom_complet', 'medecin__specialite__nom')
            .annotate(
                consultations=Count('id'),
                derniere_consultation=Max('date_consultation')
            )
            .order_by('-consultations')[:top_n]
        )
        
        return list(medecins)
    
    def get_alertes_et_recommandations(self):
        """
        Génère des alertes et recommandations personnalisées
        """
        if not self.data_loaded:
            return None
        
        alertes = []
        recommandations = []
        stats = self.get_membre_stats_overview(365)
        
        # Alertes
        if stats['est_en_retard']:
            alertes.append({
                'type': 'danger',
                'titre': 'Cotisation en retard',
                'message': f"Votre cotisation est en retard de {stats['jours_derniere_cotisation'] - 365} jours",
                'action': 'Payer maintenant'
            })
        
        if stats['jours_derniere_cotisation'] > 300:
            alertes.append({
                'type': 'warning',
                'titre': 'Cotisation bientôt due',
                'message': f"Votre cotisation arrive à expiration dans {365 - stats['jours_derniere_cotisation']} jours",
                'action': 'Renouveler'
            })
        
        if stats['soins_periode'] == 0:
            recommandations.append({
                'type': 'info',
                'titre': 'Bilan de santé recommandé',
                'message': 'Vous n\'avez pas effectué de consultation depuis 1 an',
                'action': 'Prendre rendez-vous'
            })
        
        # Recommandations basées sur l'historique
        if stats['ordonnances_total'] > 5:
            recommandations.append({
                'type': 'success',
                'titre': 'Suivi médical régulier',
                'message': 'Votre suivi médical est régulier, continuez !',
                'action': 'Voir l\'historique'
            })
        
        return {
            'alertes': alertes,
            'recommandations': recommandations
        }
    
    def generate_health_report(self):
        """
        Génère un rapport de santé personnalisé
        """
        if not self.data_loaded:
            return None
        
        stats = self.get_membre_stats_overview()
        soins_par_type = self.get_type_soins_analysis()
        medecins_frequents = self.get_medecins_frequents()
        alertes_recommandations = self.get_alertes_et_recommandations()
        
        report = {
            'informations_membre': {
                'nom_complet': self.membre.nom_complet,
                'numero_unique': self.membre.numero_unique,
                'date_inscription': self.membre.date_inscription,
                'statut': self.membre.get_statut_display(),
                'categorie': self.membre.get_categorie_display(),
                'age': self.calculer_age() if self.membre.date_naissance else 'Non spécifié'
            },
            'statistiques_globales': stats,
            'analyse_soins': {
                'par_type': soins_par_type,
                'medecins_frequents': medecins_frequents,
                'frequence_mensuelle': self.calculer_frequence_mensuelle()
            },
            'aspects_financiers': {
                'cout_moyen_soin': stats['cout_total_soins'] / stats['soins_total'] if stats['soins_total'] > 0 else 0,
                'economies_estimees': stats['montant_bons_valides'],
                'taux_utilisation': (stats['soins_periode'] / 12) * 100  # Soins par mois sur un an
            },
            'alertes_recommandations': alertes_recommandations,
            'score_sante': self.calculer_score_sante(),
            'date_generation': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return report
    
    def calculer_age(self):
        """Calcule l'âge du membre"""
        if not self.membre.date_naissance:
            return None
        aujourdhui = timezone.now().date()
        return aujourdhui.year - self.membre.date_naissance.year - (
            (aujourdhui.month, aujourdhui.day) < 
            (self.membre.date_naissance.month, self.membre.date_naissance.day)
        )
    
    def calculer_frequence_mensuelle(self):
        """Calcule la fréquence mensuelle des soins"""
        if not self.data_loaded:
            return 0
        
        jours_inscription = (timezone.now().date() - self.membre.date_inscription).days
        mois_inscription = max(jours_inscription / 30.44, 1)  # Éviter la division par zéro
        
        stats = self.get_membre_stats_overview()
        return stats['soins_total'] / mois_inscription
    
    def calculer_score_sante(self):
        """
        Calcule un score de santé basé sur l'activité médicale
        """
        if not self.data_loaded:
            return 0
        
        stats = self.get_membre_stats_overview(365)
        
        # Facteurs positifs
        facteurs_positifs = 0
        if stats['soins_periode'] > 0:  # Suivi médical régulier
            facteurs_positifs += 1
        if stats['ordonnances_total'] > 0:  # Traitements suivis
            facteurs_positifs += 1
        if not stats['est_en_retard']:  # Cotisation à jour
            facteurs_positifs += 1
        
        # Facteurs négatifs
        facteurs_negatifs = 0
        if stats['soins_periode'] > 12:  # Trop de soins peut indiquer des problèmes
            facteurs_negatifs += 1
        
        score_base = 50  # Score de base
        score = score_base + (facteurs_positifs * 10) - (facteurs_negatifs * 5)
        
        return min(100, max(0, score))

class AnalyseComportementMembres:
    """
    Analyse du comportement et des patterns des membres
    """
    
    def __init__(self):
        self.today = timezone.now().date()
    
    def get_membres_par_tranche_age(self):
        """Répartition des membres par tranche d'âge"""
        tranches = [
            ('0-18', 0, 18),
            ('19-30', 19, 30),
            ('31-45', 31, 45),
            ('46-60', 46, 60),
            ('61+', 61, 150)
        ]
        
        resultats = []
        for nom, age_min, age_max in tranches:
            count = Membre.objects.filter(
                date_naissance__isnull=False
            ).annotate(
                age=ExtractYear(self.today) - ExtractYear('date_naissance')
            ).filter(
                age__gte=age_min,
                age__lte=age_max
            ).count()
            
            resultats.append({
                'tranche': nom,
                'nombre': count
            })
        
        return resultats
    
    def get_activite_mensuelle(self, annee=None):
        """Activité mensuelle des membres"""
        if not annee:
            annee = self.today.year
        
        activite = (
            Soin.objects
            .filter(date_realisation__year=annee)
            .annotate(mois=TruncMonth('date_realisation'))
            .values('mois')
            .annotate(
                soins_total=Count('id'),
                membres_uniques=Count('patient', distinct=True),
                cout_total=Sum('cout_reel')
            )
            .order_by('mois')
        )
        
        return list(activite)
    
    def get_membres_plus_actifs(self, limit=10, periode_jours=365):
        """Membres les plus actifs médicalement"""
        date_limite = self.today - timedelta(days=periode_jours)
        
        membres_actifs = (
            Soin.objects
            .filter(date_realisation__gte=date_limite)
            .values('patient__membre__id', 'patient__membre__nom', 'patient__membre__prenom')
            .annotate(
                nom_complet=Concat('patient__membre__nom', Value(' '), 'patient__membre__prenom'),
                soins_count=Count('id'),
                cout_total=Sum('cout_reel'),
                derniere_activite=Max('date_realisation')
            )
            .order_by('-soins_count')[:limit]
        )
        
        return list(membres_actifs)
    
    def get_taux_renouvellement(self):
        """Taux de renouvellement des cotisations"""
        total_membres = Membre.objects.count()
        membres_a_jour = Membre.objects.filter(
            statut=Membre.StatutMembre.ACTIF
        ).count()
        
        if total_membres > 0:
            taux_renouvellement = (membres_a_jour / total_membres) * 100
        else:
            taux_renouvellement = 0
        
        return {
            'total_membres': total_membres,
            'membres_a_jour': membres_a_jour,
            'taux_renouvellement': taux_renouvellement,
            'membres_en_retard': total_membres - membres_a_jour
        }

# ==============================================================================
# MONITEUR TEMPS RÉEL POUR MEMBRES
# ==============================================================================

class RealTimeMembreMonitor:
    """
    Moniteur en temps réel pour l'activité des membres
    """
    
    def __init__(self, membre_id):
        self.membre_id = membre_id
        try:
            self.membre = Membre.objects.get(id=membre_id)
            self.last_check = timezone.now()
        except Membre.DoesNotExist:
            raise ValueError(f"Membre avec ID {membre_id} non trouvé")
    
    def get_recent_activity(self, minutes=60):
        """Obtenir l'activité récente du membre"""
        since_time = timezone.now() - timedelta(minutes=minutes)
        
        activity = {
            'nouvelles_consultations': Consultation.objects.filter(
                membre=self.membre,
                date_creation__gte=since_time
            ).count(),
            
            'nouveaux_soins': Soin.objects.filter(
                patient=self.membre.user,
                date_creation__gte=since_time
            ).count(),
            
            'nouveaux_bons_soin': BonDeSoin.objects.filter(
                patient=self.membre,
                date_creation__gte=since_time
            ).count(),
            
            'bons_attente_validation': BonDeSoin.objects.filter(
                patient=self.membre,
                statut='EN_ATTENTE'
            ).count(),
            
            'consultations_aujourdhui': Consultation.objects.filter(
                membre=self.membre,
                date_consultation__date=timezone.now().date()
            ).count()
        }
        
        return activity
    
    def get_alertes_urgentes(self):
        """Obtenir les alertes urgentes pour le membre"""
        alertes = []
        
        # Bons en attente depuis plus de 48h
        bons_attente_longue = BonDeSoin.objects.filter(
            patient=self.membre,
            statut='EN_ATTENTE',
            date_creation__lt=timezone.now() - timedelta(hours=48)
        ).count()
        
        if bons_attente_longue > 0:
            alertes.append(f"🚨 {bons_attente_longue} bons en attente depuis plus de 48h")
        
        # Cotisation en retard
        if self.membre.statut == Membre.StatutMembre.EN_RETARD:
            jours_retard = (timezone.now().date() - self.membre.date_derniere_cotisation).days - 365
            alertes.append(f"💰 Cotisation en retard de {jours_retard} jours")
        
        return alertes
    
    def afficher_tableau_bord(self, activity, alertes):
        """Afficher un tableau de bord formaté"""
        print(f"\n{'='*60}")
        print(f"👤 TABLEAU DE BORD - {self.membre.nom_complet}")
        print(f"⏰ {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"{'='*60}")
        
        print(f"\n📊 ACTIVITÉ RÉCENTE (60 min):")
        print(f"   🩺 Nouvelles consultations: {activity['nouvelles_consultations']}")
        print(f"   💊 Nouveaux soins: {activity['nouveaux_soins']}")
        print(f"   📋 Nouveaux bons de soin: {activity['nouveaux_bons_soin']}")
        print(f"   ⏳ Bons en attente: {activity['bons_attente_validation']}")
        print(f"   📅 Consultations aujourd'hui: {activity['consultations_aujourdhui']}")
        
        # Score de santé
        analyzer = MembresAnalytics(self.membre_id)
        score = analyzer.calculer_score_sante()
        print(f"\n🏥 SCORE DE SANTÉ: {score}/100")
        
        if alertes:
            print(f"\n🚨 ALERTES:")
            for alerte in alertes:
                print(f"   {alerte}")
        else:
            print(f"\n✅ Aucune alerte urgente")
        
        print(f"{'='*60}")
    
    def start_monitoring(self, interval_minutes=5):
        """Démarrer le monitoring en temps réel"""
        print(f"🔍 Monitoring de {self.membre.nom_complet}")
        print(f"📡 Intervalle: {interval_minutes} minutes (Ctrl+C pour arrêter)")
        
        try:
            compteur = 0
            while True:
                compteur += 1
                print(f"\n🔄 Mise à jour #{compteur}")
                
                # Récupérer les données
                activity = self.get_recent_activity()
                alertes = self.get_alertes_urgentes()
                
                # Afficher le tableau de bord
                self.afficher_tableau_bord(activity, alertes)
                
                # Attendre avant la prochaine mise à jour
                print(f"\n⏳ Prochaine mise à jour dans {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print(f"\n🛑 Monitoring arrêté à {timezone.now().strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"\n❌ Erreur: {e}")

# ==============================================================================
# FONCTIONS UTILITAIRES
# ==============================================================================

def analyser_membre_specifique(membre_id):
    """Analyser un membre spécifique"""
    analyzer = MembresAnalytics(membre_id)
    if analyzer.data_loaded:
        report = analyzer.generate_health_report()
        print(f"\n📊 RAPPORT POUR {report['informations_membre']['nom_complet']}")
        print(f"📅 Membre depuis: {report['informations_membre']['date_inscription']}")
        print(f"🏥 Score santé: {report['score_sante']}/100")
        print(f"💰 Coût total soins: {report['statistiques_globales']['cout_total_soins']:.2f} €")
        print(f"📋 Bons validés: {report['statistiques_globales']['bons_soin_valides']}")
        
        # Soins par type
        soins_par_type = report['analyse_soins']['par_type']
        if soins_par_type:
            print(f"\n🏥 SOINS PAR TYPE:")
            for soin in soins_par_type[:5]:  # Top 5
                print(f"   • {soin['type_soin__nom']}: {soin['total']} soins")
        
        # Alertes
        alertes = report['alertes_recommandations']['alertes']
        if alertes:
            print(f"\n🚨 ALERTES:")
            for alerte in alertes:
                print(f"   • {alerte['titre']}: {alerte['message']}")
        
        # Recommandations
        recommandations = report['alertes_recommandations']['recommandations']
        if recommandations:
            print(f"\n💡 RECOMMANDATIONS:")
            for reco in recommandations:
                print(f"   • {reco['titre']}: {reco['message']}")
    else:
        print("❌ Membre non trouvé")

def analyser_comportement_global():
    """Analyse comportementale de tous les membres"""
    analyse_comportement = AnalyseComportementMembres()
    
    print(f"\n📈 ANALYSE COMPORTEMENTALE GLOBALE")
    
    # Tranches d'âge
    tranches = analyse_comportement.get_membres_par_tranche_age()
    print(f"\n📊 RÉPARTITION PAR ÂGE:")
    for tranche in tranches:
        print(f"   {tranche['tranche']} ans: {tranche['nombre']} membres")
    
    # Taux de renouvellement
    taux = analyse_comportement.get_taux_renouvellement()
    print(f"\n💰 TAUX DE RENOUVELLEMENT: {taux['taux_renouvellement']:.1f}%")
    print(f"   Membres à jour: {taux['membres_a_jour']}")
    print(f"   Membres en retard: {taux['membres_en_retard']}")
    
    # Membres les plus actifs
    membres_actifs = analyse_comportement.get_membres_plus_actifs(5)
    print(f"\n🏆 TOP 5 MEMBRES ACTIFS:")
    for i, membre in enumerate(membres_actifs, 1):
        print(f"   {i}. {membre['nom_complet']}: {membre['soins_count']} soins")

def lister_tous_membres():
    """Lister tous les membres avec leurs IDs"""
    membres = Membre.objects.all().order_by('nom', 'prenom')
    
    print(f"\n👥 LISTE DES MEMBRES ({membres.count()}):")
    for membre in membres:
        soins_count = Soin.objects.filter(patient=membre.user).count()
        consultations_count = Consultation.objects.filter(membre=membre).count()
        print(f"   • {membre.nom_complet}")
        print(f"     📞 {membre.telephone or 'Non défini'}")
        print(f"     📧 {membre.email}")
        print(f"     📊 {soins_count} soins, {consultations_count} consultations")
        print(f"     🆔 ID: {membre.id}")
        print()

def menu_interactif():
    """Menu interactif pour l'analyse des membres"""
    while True:
        print(f"\n{'='*50}")
        print("👥 MENU PRINCIPAL - ANALYSE MEMBRES")
        print(f"{'='*50}")
        print("1. 📋 Lister tous les membres")
        print("2. 🔍 Analyser un membre spécifique")
        print("3. 📈 Analyse comportementale globale")
        print("4. 🔄 Monitoring temps réel")
        print("5. 🚪 Quitter")
        
        choix = input("\nVotre choix (1-5): ").strip()
        
        if choix == '1':
            lister_tous_membres()
                
        elif choix == '2':
            membre_id = input("ID du membre à analyser: ").strip()
            if membre_id.isdigit():
                analyser_membre_specifique(int(membre_id))
            else:
                print("❌ ID invalide")
                
        elif choix == '3':
            analyser_comportement_global()
            
        elif choix == '4':
            membre_id = input("ID du membre à monitorer: ").strip()
            if membre_id.isdigit():
                try:
                    monitor = RealTimeMembreMonitor(int(membre_id))
                    interval = input("Intervalle en minutes (défaut: 5): ").strip()
                    interval_minutes = int(interval) if interval.isdigit() else 5
                    monitor.start_monitoring(interval_minutes)
                except Exception as e:
                    print(f"❌ Erreur: {e}")
            else:
                print("❌ ID invalide")
                
        elif choix == '5':
            print("👋 Au revoir!")
            break
        else:
            print("❌ Choix invalide")

# ==============================================================================
# EXÉCUTION PRINCIPALE
# ==============================================================================

if __name__ == "__main__":
    print("🚀 SCRIPT D'ANALYSE DES MEMBRES")
    print("=" * 50)
    print("📋 Ce script analyse l'activité des membres")
    print("⚠️  Assurez-vous que Django est correctement configuré")
    print("=" * 50)
    
    # Menu interactif
    menu_interactif()