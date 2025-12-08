# medecin_realtime_monitor.py
import time
from datetime import datetime, timedelta
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from medecin.models import Consultation, Ordonnance, Medecin
from soins.models import BonDeSoin
from django.utils import timezone

class RealTimeMedecinMonitor:
    """
    Moniteur en temps réel pour les activités des médecins
    """
    
    def __init__(self, medecin_id):
        self.medecin_id = medecin_id
        self.medecin = Medecin.objects.get(id=medecin_id)
        self.last_check = timezone.now()
    
    def get_recent_activity(self, minutes=60):
        """Obtenir l'activité récente"""
        since_time = timezone.now() - timedelta(minutes=minutes)
        
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
            
            'consultations_aujourdhui': Consultation.objects.filter(
                medecin=self.medecin,
                date_consultation__date=timezone.now().date()
            ).count()
        }
        
        return activity
    
    def start_monitoring(self, interval_minutes=5):
        """Démarrer le monitoring en temps réel"""
        print(f"🔍 Monitoring du Dr {self.medecin.nom_complet} (Ctrl+C pour arrêter)")
        
        try:
            while True:
                activity = self.get_recent_activity()
                
                print(f"\n⏰ {timezone.now().strftime('%H:%M:%S')} - Activité récente:")
                print(f"   Nouvelles consultations: {activity['nouvelles_consultations']}")
                print(f"   Nouvelles ordonnances: {activity['nouvelles_ordonnances']}")
                print(f"   Nouveaux bons de soin: {activity['nouveaux_bons_soin']}")
                print(f"   Bons en attente: {activity['bons_attente_validation']}")
                print(f"   Consultations aujourd'hui: {activity['consultations_aujourdhui']}")
                
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring arrêté")

# Utilisation
if __name__ == "__main__":
    # Démarrer le monitoring pour un médecin
    monitor = RealTimeMedecinMonitor(medecin_id=1)
    monitor.start_monitoring(interval_minutes=5)