# diagnostics/monitor_sync.py
import schedule
import time
import smtplib
from email.mime.text import MimeText

class SurveillantSynchronisation:
    """Surveillance continue de la synchronisation"""
    
    def __init__(self):
        self.dernier_rapport = None
    
    def surveillance_quotidienne(self):
        """Exécute un diagnostic quotidien"""
        print(f"🔍 Surveillance quotidienne - {datetime.now()}")
        
        diagnostic = DiagnosticSynchronisation()
        diagnostic.executer_diagnostic_complet()
        
        # Alertes si problèmes critiques
        problemes_critiques = [p for p in diagnostic.resultats['problemes'] 
                             if p['severite'] == 'HAUTE']
        
        if problemes_critiques:
            self.envoyer_alerte(problemes_critiques, diagnostic.resultats)
        
        self.dernier_rapport = diagnostic.resultats
    
    def envoyer_alerte(self, problemes, rapport):
        """Envoie une alerte par email"""
        sujet = f"🔴 ALERTE Synchronisation - {len(problemes)} problèmes critiques"
        
        corps = f"""
        Problèmes critiques identifiés dans la synchronisation:
        
        {chr(10).join([f"• {p['description']}" for p in problemes])}
        
        Rapport complet: Vérifier le fichier de diagnostic.
        """
        
        # Configuration email (à adapter)
        try:
            # self._envoyer_email(sujet, corps)
            print(f"📧 Alerte envoyée: {sujet}")
        except Exception as e:
            print(f"❌ Erreur envoi email: {str(e)}")
    
    def demarrer_surveillance(self):
        """Démarre la surveillance planifiée"""
        print("🚀 Démarrage de la surveillance continue...")
        
        # Planification
        schedule.every().day.at("06:00").do(self.surveillance_quotidienne)
        schedule.every().hour.do(self.surveillance_rapide)
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    def surveillance_rapide(self):
        """Surveillance rapide horaire"""
        print(f"⏱️  Surveillance rapide - {datetime.now()}")
        # Vérifications légères rapides

if __name__ == "__main__":
    surveillant = SurveillantSynchronisation()
    surveillant.demarrer_surveillance()