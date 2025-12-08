# systeme_alertes_automatise_corrige.py
import os
import django
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Count

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import VerificationCotisation, Agent

class SystemeAlertes:
    def __init__(self):
        self.alertes_critiques = []
        self.alertes_attention = []
        self.alertes_info = []
    
    def scanner_anomalies(self):
        """Scan complet du système pour détecter les anomalies"""
        print("🔍 SCAN DES ANOMALIES EN COURS...")
        
        self._detecter_retards_severes()
        self._detecter_dettes_importantes()
        self._detecter_verifications_abandonnees()
        self._detecter_agents_inactifs()
        self._detecter_echeances_imminentes()
        
        return self.generer_rapport_alertes()
    
    def _detecter_retards_severes(self):
        """Détecte les retards de paiement sévères"""
        retards_severes = VerificationCotisation.objects.filter(
            jours_retard__gt=30,
            statut_cotisation__in=['en_retard', 'a_verifier']
        )
        
        for verification in retards_severes:
            self.alertes_critiques.append(
                f"🔴 RETARD SÉVÈRE - Membre {verification.membre.id}: "
                f"{verification.jours_retard} jours de retard "
                f"(Dette: {verification.montant_dette}€)"
            )
    
    def _detecter_dettes_importantes(self):
        """Détecte les dettes importantes"""
        dettes_importantes = VerificationCotisation.objects.filter(
            montant_dette__gt=1000
        )
        
        for verification in dettes_importantes:
            self.alertes_critiques.append(
                f"🔴 DETTE IMPORTANTE - Membre {verification.membre.id}: "
                f"{verification.montant_dette}€ de dette "
                f"(Agent: {verification.agent.matricule})"
            )
    
    def _detecter_verifications_abandonnees(self):
        """Détecte les vérifications non traitées depuis longtemps"""
        seuil_abandon = timezone.now() - timedelta(days=14)
        
        verifications_abandonnees = VerificationCotisation.objects.filter(
            date_verification__isnull=True,
            date_dernier_paiement__lt=seuil_abandon.date()
        )
        
        for verification in verifications_abandonnees:
            self.alertes_attention.append(
                f"🟡 VÉRIFICATION ABANDONNÉE - Membre {verification.membre.id}: "
                f"Non traitée depuis +14 jours (Agent: {verification.agent.matricule})"
            )
    
    def _detecter_agents_inactifs(self):
        """Détecte les agents inactifs"""
        agents_inactifs = Agent.objects.filter(
            est_actif=True
        ).annotate(
            verifications_completes=Count('verificationcotisation', 
                                       filter=Q(verificationcotisation__date_verification__isnull=False))
        ).filter(verifications_completes=0)
        
        for agent in agents_inactifs:
            self.alertes_attention.append(
                f"🟡 AGENT INACTIF - {agent.matricule}: "
                f"Aucune vérification complétée"
            )
    
    def _detecter_echeances_imminentes(self):
        """Détecte les échéances proches"""
        echeance_proche = timezone.now().date() + timedelta(days=3)
        
        echeances_imminentes = VerificationCotisation.objects.filter(
            prochaine_echeance__lte=echeance_proche,
            prochaine_echeance__gte=timezone.now().date()
        )
        
        for verification in echeances_imminentes:
            self.alertes_info.append(
                f"🔵 ÉCHÉANCE IMMINENTE - Membre {verification.membre.id}: "
                f"Échéance le {verification.prochaine_echeance} "
                f"(Agent: {verification.agent.matricule})"
            )
    
    def generer_rapport_alertes(self):
        """Génère un rapport structuré des alertes"""
        print("\n" + "=" * 80)
        print("🚨 RAPPORT D'ALERTES AUTOMATISÉ")
        print("=" * 80)
        
        if self.alertes_critiques:
            print("\n🔴 ALERTES CRITIQUES (Action immédiate requise):")
            for alerte in self.alertes_critiques:
                print(f"  • {alerte}")
        
        if self.alertes_attention:
            print("\n🟡 ALERTES ATTENTION (Surveillance requise):")
            for alerte in self.alertes_attention:
                print(f"  • {alerte}")
        
        if self.alertes_info:
            print("\n🔵 INFORMATIONS (Pour suivi):")
            for alerte in self.alertes_info:
                print(f"  • {alerte}")
        
        if not any([self.alertes_critiques, self.alertes_attention, self.alertes_info]):
            print("✅ Aucune alerte détectée - Système stable")
        
        total_alertes = len(self.alertes_critiques) + len(self.alertes_attention) + len(self.alertes_info)
        print(f"\n📊 TOTAL ALERTES: {total_alertes}")
        
        return total_alertes

# Exécution du système d'alertes
if __name__ == "__main__":
    systeme = SystemeAlertes()
    systeme.scanner_anomalies()