# medecin_realtime_monitor_corrige.py
import time
from datetime import datetime, timedelta
import django
import os
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from medecin.models import Consultation, Ordonnance, Medecin
from soins.models import BonDeSoin
from django.db.models import Sum

class RealTimeMedecinMonitor:
    """
    Moniteur en temps réel pour les activités des médecins - VERSION CORRIGÉE
    """
    
    def __init__(self, medecin_id):
        self.medecin_id = medecin_id
        try:
            self.medecin = Medecin.objects.get(id=medecin_id)
            self.last_check = timezone.now()
        except Medecin.DoesNotExist:
            raise ValueError(f"Médecin avec ID {medecin_id} non trouvé")
    
    def get_recent_activity(self, minutes=60):
        """Obtenir l'activité récente - CORRIGÉ"""
        since_time = timezone.now() - timedelta(minutes=minutes)
        aujourdhui = timezone.now().date()
        
        activity = {
            'nouvelles_consultations': Consultation.objects.filter(
                medecin=self.medecin,
                date_creation__gte=since_time
            ).count(),
            
            'nouvelles_ordonnances': Ordonnance.objects.filter(
                medecin=self.medecin.user,
                date_creation__gte=since_time
            ).count(),
            
            'nouveaux_bons_soin': BonDeSoin.objects.filter(
                medecin=self.medecin.user,
                date_creation__gte=since_time
            ).count(),
            
            'bons_attente_validation': BonDeSoin.objects.filter(
                medecin=self.medecin.user,
                statut='EN_ATTENTE'
            ).count(),
            
            # CORRECTION : Utiliser __range pour la date du jour
            'consultations_aujourdhui': Consultation.objects.filter(
                medecin=self.medecin,
                date_consultation__range=[aujourdhui, aujourdhui + timedelta(days=1)]
            ).count(),
            
            'consultations_en_cours': Consultation.objects.filter(
                medecin=self.medecin,
                statut='EN_COURS'
            ).count(),
            
            'ordonnances_urgentes': Ordonnance.objects.filter(
                medecin=self.medecin.user,
                est_urgent=True,
                date_creation__gte=since_time
            ).count()
        }
        
        return activity
    
    def get_alertes_urgentes(self):
        """Obtenir les alertes urgentes"""
        alertes = []
        
        # Bons en attente depuis plus de 24h
        bons_attente_longue = BonDeSoin.objects.filter(
            medecin=self.medecin.user,
            statut='EN_ATTENTE',
            date_creation__lt=timezone.now() - timedelta(hours=24)
        ).count()
        
        if bons_attente_longue > 0:
            alertes.append(f"🚨 {bons_attente_longue} bons en attente depuis plus de 24h")
        
        # Consultations en retard
        consultations_retard = Consultation.objects.filter(
            medecin=self.medecin,
            statut='PLANIFIEE',
            date_consultation__lt=timezone.now()
        ).count()
        
        if consultations_retard > 0:
            alertes.append(f"⏰ {consultations_retard} consultations en retard")
        
        return alertes
    
    def get_performance_metrics(self):
        """Métriques de performance"""
        aujourdhui = timezone.now().date()
        debut_semaine = aujourdhui - timedelta(days=aujourdhui.weekday())
        debut_mois = aujourdhui.replace(day=1)
        
        metrics = {
            'semaine_consultations': Consultation.objects.filter(
                medecin=self.medecin,
                date_consultation__gte=debut_semaine
            ).count(),
            
            'mois_consultations': Consultation.objects.filter(
                medecin=self.medecin,
                date_consultation__gte=debut_mois
            ).count(),
            
            'taux_validation_bons': self.calculer_taux_validation(),
            
            'revenus_estimes_semaine': self.estimer_revenus_semaine()
        }
        
        return metrics
    
    def calculer_taux_validation(self):
        """Calculer le taux de validation des bons de soin"""
        total_bons = BonDeSoin.objects.filter(medecin=self.medecin.user).count()
        bons_valides = BonDeSoin.objects.filter(
            medecin=self.medecin.user, 
            statut='VALIDE'
        ).count()
        
        if total_bons > 0:
            return (bons_valides / total_bons) * 100
        return 0
    
    def estimer_revenus_semaine(self):
        """Estimer les revenus de la semaine"""
        debut_semaine = timezone.now().date() - timedelta(days=timezone.now().date().weekday())
        
        consultations_semaine = Consultation.objects.filter(
            medecin=self.medecin,
            date_consultation__gte=debut_semaine,
            statut='TERMINEE'
        ).count()
        
        revenus_consultations = consultations_semaine * (self.medecin.tarif_consultation or 0)
        
        revenus_bons = BonDeSoin.objects.filter(
            medecin=self.medecin.user,
            statut='VALIDE',
            date_validation__gte=debut_semaine
        ).aggregate(total=Sum('montant'))['total'] or 0
        
        return revenus_consultations + revenus_bons
    
    def afficher_tableau_bord(self, activity, metrics, alertes):
        """Afficher un tableau de bord formaté"""
        print(f"\n{'='*60}")
        print(f"🏥 TABLEAU DE BORD - Dr {self.medecin.nom_complet}")
        print(f"⏰ {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"{'='*60}")
        
        print(f"\n📊 ACTIVITÉ RÉCENTE (60 min):")
        print(f"   🩺 Nouvelles consultations: {activity['nouvelles_consultations']}")
        print(f"   📝 Nouvelles ordonnances: {activity['nouvelles_ordonnances']}")
        print(f"   💊 Nouvelles ordonnances urgentes: {activity['ordonnances_urgentes']}")
        print(f"   📋 Nouveaux bons de soin: {activity['nouveaux_bons_soin']}")
        print(f"   ⏳ Bons en attente: {activity['bons_attente_validation']}")
        print(f"   🔄 Consultations en cours: {activity['consultations_en_cours']}")
        print(f"   📅 Consultations aujourd'hui: {activity['consultations_aujourdhui']}")
        
        print(f"\n📈 PERFORMANCE:")
        print(f"   🗓️  Consultations cette semaine: {metrics['semaine_consultations']}")
        print(f"   📅 Consultations ce mois: {metrics['mois_consultations']}")
        print(f"   ✅ Taux validation bons: {metrics['taux_validation_bons']:.1f}%")
        print(f"   💰 Revenus estimés semaine: {metrics['revenus_estimes_semaine']:.2f} €")
        
        if alertes:
            print(f"\n🚨 ALERTES:")
            for alerte in alertes:
                print(f"   {alerte}")
        else:
            print(f"\n✅ Aucune alerte")
        
        print(f"{'='*60}")
    
    def start_monitoring(self, interval_minutes=5):
        """Démarrer le monitoring en temps réel - CORRIGÉ"""
        print(f"🔍 Monitoring du Dr {self.medecin.nom_complet}")
        print(f"📡 Intervalle: {interval_minutes} minutes (Ctrl+C pour arrêter)")
        
        try:
            while True:
                # Récupérer les données
                activity = self.get_recent_activity()
                metrics = self.get_performance_metrics()
                alertes = self.get_alertes_urgentes()
                
                # Afficher le tableau de bord
                self.afficher_tableau_bord(activity, metrics, alertes)
                
                # Attendre avant la prochaine mise à jour
                print(f"\n⏳ Prochaine mise à jour dans {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print(f"\n🛑 Monitoring arrêté à {timezone.now().strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"\n❌ Erreur: {e}")

# ==============================================================================
# SCRIPT D'ANALYSE CORRIGÉ
# ==============================================================================

class MedecinAnalyticsCorrige:
    """
    Classe d'analyse des données médecins - VERSION CORRIGÉE
    """
    
    def __init__(self, medecin_id=None):
        self.medecin_id = medecin_id
        self.medecin = None
        self.data_loaded = False
        
        if medecin_id:
            self.load_medecin_data()
    
    def load_medecin_data(self):
        """Charger les données du médecin"""
        try:
            self.medecin = Medecin.objects.get(id=self.medecin_id)
            self.data_loaded = True
            print(f"✅ Données chargées pour le Dr {self.medecin.nom_complet}")
        except Medecin.DoesNotExist:
            print(f"❌ Médecin avec ID {self.medecin_id} non trouvé")
            return False
        return True
    
    def get_medecin_stats_overview(self, periode_jours=30):
        """Statistiques générales du médecin - CORRIGÉ"""
        if not self.data_loaded:
            return None
        
        date_debut = timezone.now() - timedelta(days=periode_jours)
        aujourdhui = timezone.now().date()
        
        stats = {
            # Consultations
            'consultations_total': Consultation.objects.filter(
                medecin=self.medecin
            ).count(),
            
            'consultations_periode': Consultation.objects.filter(
                medecin=self.medecin,
                date_consultation__gte=date_debut
            ).count(),
            
            'consultations_aujourdhui': Consultation.objects.filter(
                medecin=self.medecin,
                date_consultation__range=[aujourdhui, aujourdhui + timedelta(days=1)]
            ).count(),
            
            'consultations_planifiees': Consultation.objects.filter(
                medecin=self.medecin,
                statut='PLANIFIEE'
            ).count(),
            
            'consultations_terminees': Consultation.objects.filter(
                medecin=self.medecin,
                statut='TERMINEE'
            ).count(),
            
            # Bons de soin
            'bons_soin_total': BonDeSoin.objects.filter(
                medecin=self.medecin.user
            ).count(),
            
            'bons_soin_valides': BonDeSoin.objects.filter(
                medecin=self.medecin.user,
                statut='VALIDE'
            ).count(),
            
            'bons_soin_attente': BonDeSoin.objects.filter(
                medecin=self.medecin.user,
                statut='EN_ATTENTE'
            ).count(),
            
            # Ordonnances
            'ordonnances_total': Ordonnance.objects.filter(
                medecin=self.medecin.user
            ).count(),
            
            'ordonnances_urgentes': Ordonnance.objects.filter(
                medecin=self.medecin.user,
                est_urgent=True
            ).count(),
            
            # Revenus estimés
            'revenus_consultations': Consultation.objects.filter(
                medecin=self.medecin,
                statut='TERMINEE'
            ).count() * (self.medecin.tarif_consultation or 0),
            
            'revenus_bons_soin': BonDeSoin.objects.filter(
                medecin=self.medecin.user,
                statut='VALIDE'
            ).aggregate(total=Sum('montant'))['total'] or 0,
        }
        
        stats['revenus_totaux'] = stats['revenus_consultations'] + stats['revenus_bons_soin']
        
        return stats
    
    def generate_quick_report(self):
        """Générer un rapport rapide"""
        if not self.data_loaded:
            return None
        
        stats = self.get_medecin_stats_overview()
        
        print(f"\n{'='*50}")
        print(f"📋 RAPPORT RAPIDE - Dr {self.medecin.nom_complet}")
        print(f"{'='*50}")
        
        print(f"\n🎯 ACTIVITÉ GLOBALE:")
        print(f"   • Consultations totales: {stats['consultations_total']}")
        print(f"   • Bons de soin validés: {stats['bons_soin_valides']}")
        print(f"   • Ordonnances prescrites: {stats['ordonnances_total']}")
        
        print(f"\n📅 AUJOURD'HUI:")
        print(f"   • Consultations: {stats['consultations_aujourdhui']}")
        print(f"   • Bons en attente: {stats['bons_soin_attente']}")
        
        print(f"\n💰 ASPECTS FINANCIERS:")
        print(f"   • Revenus totaux: {stats['revenus_totaux']:.2f} €")
        print(f"   • Dont consultations: {stats['revenus_consultations']:.2f} €")
        print(f"   • Dont bons de soin: {stats['revenus_bons_soin']:.2f} €")
        
        print(f"\n⚡ PERFORMANCE:")
        taux_validation = (stats['bons_soin_valides'] / stats['bons_soin_total'] * 100) if stats['bons_soin_total'] > 0 else 0
        print(f"   • Taux validation bons: {taux_validation:.1f}%")
        print(f"   • Ordonnances urgentes: {stats['ordonnances_urgentes']}")
        
        print(f"{'='*50}")
        
        return stats

# ==============================================================================
# FONCTIONS UTILITAIRES CORRIGÉES
# ==============================================================================

def lister_medecins_actifs():
    """Lister tous les médecins - CORRIGÉ avec les champs réels"""
    # Utiliser 'actif' au lieu de 'est_actif' qui n'existe pas
    medecins = Medecin.objects.filter(actif=True)
    
    print(f"\n🏥 MÉDECINS ACTIFS ({medecins.count()}):")
    for medecin in medecins:
        consultations_count = Consultation.objects.filter(medecin=medecin).count()
        print(f"   • {medecin.nom_complet} - {consultations_count} consultations - ID: {medecin.id}")
    
    # Si aucun médecin actif, lister tous les médecins
    if medecins.count() == 0:
        print("\nℹ️  Aucun médecin marqué comme 'actif', affichage de tous les médecins:")
        tous_medecins = Medecin.objects.all()
        for medecin in tous_medecins:
            consultations_count = Consultation.objects.filter(medecin=medecin).count()
            statut = "✅ Actif" if medecin.actif else "❌ Inactif"
            print(f"   • {medecin.nom_complet} - {consultations_count} consultations - {statut} - ID: {medecin.id}")
    
    return medecins

def tester_moniteur(medecin_id):
    """Tester le moniteur avec un médecin spécifique"""
    try:
        monitor = RealTimeMedecinMonitor(medecin_id)
        print("✅ Moniteur initialisé avec succès")
        
        # Test rapide
        activity = monitor.get_recent_activity()
        print("📊 Test activité récente:")
        for key, value in activity.items():
            print(f"   {key}: {value}")
        
        return monitor
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        return None

def analyser_medecin(medecin_id):
    """Analyser un médecin spécifique"""
    analyzer = MedecinAnalyticsCorrige(medecin_id)
    if analyzer.data_loaded:
        return analyzer.generate_quick_report()
    return None

def menu_principal():
    """Menu interactif principal"""
    while True:
        print(f"\n{'='*50}")
        print("🏥 MENU PRINCIPAL - ANALYSE MÉDECINS")
        print(f"{'='*50}")
        print("1. 📋 Lister tous les médecins")
        print("2. 🔍 Analyser un médecin spécifique")
        print("3. 🔄 Démarrer le monitoring temps réel")
        print("4. 🚪 Quitter")
        
        choix = input("\nVotre choix (1-4): ").strip()
        
        if choix == '1':
            lister_medecins_actifs()
            
        elif choix == '2':
            medecin_id = input("ID du médecin à analyser: ").strip()
            if medecin_id.isdigit():
                analyser_medecin(int(medecin_id))
            else:
                print("❌ ID invalide")
                
        elif choix == '3':
            medecin_id = input("ID du médecin à monitorer: ").strip()
            if medecin_id.isdigit():
                try:
                    monitor = RealTimeMedecinMonitor(int(medecin_id))
                    interval = input("Intervalle en minutes (défaut: 5): ").strip()
                    interval_minutes = int(interval) if interval.isdigit() else 5
                    monitor.start_monitoring(interval_minutes)
                except Exception as e:
                    print(f"❌ Erreur: {e}")
            else:
                print("❌ ID invalide")
                
        elif choix == '4':
            print("👋 Au revoir!")
            break
        else:
            print("❌ Choix invalide")

# ==============================================================================
# EXÉCUTION PRINCIPALE CORRIGÉE
# ==============================================================================

if __name__ == "__main__":
    print("🚀 MONITEUR MÉDECIN - VERSION CORRIGÉE")
    print("=" * 50)
    
    # Option 1: Menu interactif
    menu_principal()
    
    # Option 2: Exécution automatique (décommentez si voulu)
    """
    print("\n🎯 EXÉCUTION AUTOMATIQUE")
    
    # Lister les médecins
    medecins = lister_medecins_actifs()
    
    if medecins.exists():
        # Prendre le premier médecin
        premier_medecin = medecins.first()
        medecin_id = premier_medecin.id
        
        print(f"\n📊 Analyse du Dr {premier_medecin.nom_complet} (ID: {medecin_id})")
        
        # Rapport rapide
        analyser_medecin(medecin_id)
        
        # Test du moniteur (court)
        print(f"\n🔍 Test du moniteur (30 secondes)...")
        monitor = tester_moniteur(medecin_id)
        if monitor:
            time.sleep(30)  # Test court de 30 secondes
    else:
        print("❌ Aucun médecin trouvé dans la base de données")
    """