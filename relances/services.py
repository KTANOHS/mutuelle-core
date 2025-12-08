from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from membres.models import Membre
from agents.models import VerificationCotisation
from relances.models import TemplateRelance, RelanceProgrammee

class ServiceRelances:
    def __init__(self):
        self.seuils = {
            'premier_rappel': 7,
            'relance_urgente': 15,
            'suspension_imminente': 30
        }
    
    def identifier_membres_a_relancer(self):
        """Identifie les membres nécessitant une relance"""
        membres_relance = []
        
        # Premier rappel - 7 jours de retard
        seuil_premier = timezone.now().date() - timedelta(days=self.seuils['premier_rappel'])
        membres_premier = Membre.objects.filter(
            verificationcotisation__prochaine_echeance__lte=seuil_premier,
            verificationcotisation__jours_retard__gte=self.seuils['premier_rappel'],
            verificationcotisation__statut_cotisation='a_verifier'
        ).distinct()
        
        for membre in membres_premier:
            membres_relance.append((membre, 'premier_rappel'))
        
        # Relances urgentes - 15+ jours de retard
        membres_urgent = Membre.objects.filter(
            verificationcotisation__jours_retard__gte=self.seuils['relance_urgente']
        ).distinct()
        
        for membre in membres_urgent:
            membres_relance.append((membre, 'relance_urgente'))
        
        return membres_relance
    
    def creer_relance_programmee(self, membre, type_relance):
        """Crée une relance programmée"""
        template = TemplateRelance.objects.filter(
            type_relance=type_relance
        ).first()
        
        if template:
            RelanceProgrammee.objects.create(
                membre=membre,
                template=template,
                date_programmation=timezone.now(),
                statut='programmee'
            )
            return True
        return False

def planifier_relances_automatiques():
    """Fonction utilitaire pour planifier les relances"""
    service = ServiceRelances()
    membres_a_relancer = service.identifier_membres_a_relancer()
    
    for membre, type_relance in membres_a_relancer:
        service.creer_relance_programmee(membre, type_relance)
    
    return len(membres_a_relancer)
