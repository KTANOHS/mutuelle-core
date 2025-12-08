# surveillance_auto.py
import schedule
import time
import smtplib
from email.mime.text import MimeText
from surveillance_sync import SurveillantSynchronisation

class SurveillanceAutomatisee:
    def __init__(self):
        self.surveillant = SurveillantSynchronisation()
    
    def surveillance_quotidienne(self):
        """Surveillance quotidienne automatique"""
        print(f"\n🔍 Surveillance quotidienne - {datetime.now()}")
        
        rapport = self.surveillant.verifier_synchronisation()
        
        # Vérifier si des alertes critiques
        alertes_critiques = [a for a in rapport['alertes'] if a['niveau'] == 'CRITIQUE']
        
        if alertes_critiques:
            print("🚨 Alertes critiques détectées - Notification envoyée")
            self.envoyer_alerte(alertes_critiques, rapport)
        
        self.surveillant.sauvegarder_rapport()
        self.surveillant.afficher_resume()
    
    def envoyer_alerte(self, alertes, rapport):
        """Envoie une alerte par email (à configurer)"""
        sujet = f"🔴 ALERTE Synchronisation - {len(alertes)} problème(s)"
        
        corps = f"""
        Problèmes de synchronisation détectés:
        
        {chr(10).join([f"• {a['message']}" for a in alertes])}
        
        Rapport complet: Vérifier les fichiers de surveillance.
        """
        
        print(f"📧 Alerte prête à envoyer: {sujet}")
        # Décommenter et configurer pour envoyer réellement
        # self._envoyer_email(sujet, corps)
    
    def demarrer_surveillance(self):
        """Démarre la surveillance planifiée"""
        print("🚀 Démarrage de la surveillance automatique...")
        
        # Planification
        schedule.every().day.at("08:00").do(self.surveillance_quotidienne)
        schedule.every().sunday.at("12:00").do(self.rapport_hebdomadaire)
        
        print("📅 Surveillance planifiée:")
        print("   • Quotidienne à 08:00")
        print("   • Hebdomadaire le dimanche à 12:00")
        print("   • Ctrl+C pour arrêter")
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    def rapport_hebdomadaire(self):
        """Rapport hebdomadaire détaillé"""
        print(f"\n📊 Rapport hebdomadaire - {datetime.now()}")

if __name__ == "__main__":
    surveillance = SurveillanceAutomatisee()
    
    # Test immédiat
    print("🧪 Test immédiat de la surveillance...")
    surveillance.surveillance_quotidienne()
    
    # Demander si on veut lancer la surveillance continue
    choix = input("\nDémarrer la surveillance continue? (O/N): ").strip().upper()
    if choix == 'O':
        surveillance.demarrer_surveillance()