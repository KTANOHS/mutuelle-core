from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from assureur.models import BonDeSoin, HistoriqueActionAssureur
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Nettoie les bons de soin expirés et met à jour leur statut'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--jours-avant',
            type=int,
            default=0,
            help='Nombre de jours avant expiration pour le nettoyage (défaut: 0 - déjà expirés)'
        )
        parser.add_argument(
            '--simulation',
            action='store_true',
            help='Mode simulation - affiche ce qui serait fait sans modifier la base'
        )

    def handle(self, *args, **options):
        jours_avant = options['jours_avant']
        simulation = options['simulation']
        
        self.stdout.write(
            self.style.MIGRATE_HEADING(
                f"🚀 Début du nettoyage des bons expirés..."
            )
        )
        
        # Construction de la requête
        date_reference = timezone.now()
        if jours_avant > 0:
            date_reference += timedelta(days=jours_avant)
            self.stdout.write(
                self.style.WARNING(
                    f"Recherche des bons expirant dans {jours_avant} jour(s) ou déjà expirés"
                )
            )
        
        # Query pour trouver les bons à nettoyer
        queryset = BonDeSoin.objects.filter(
            statut=BonDeSoin.StatutBon.EMIS,
            date_expiration__lt=date_reference
        )
        
        bons_a_nettoyer = queryset.select_related('membre', 'assureur')
        count_total = bons_a_nettoyer.count()
        
        if count_total == 0:
            self.stdout.write(
                self.style.SUCCESS("✅ Aucun bon à nettoyer trouvé.")
            )
            return
        
        if simulation:
            self.afficher_simulation(bons_a_nettoyer)
            return
        
        # Exécution réelle du nettoyage
        self.effectuer_nettoyage(bons_a_nettoyer)

    def afficher_simulation(self, bons):
        """Affiche ce qui serait fait en mode simulation"""
        self.stdout.write(
            self.style.WARNING("🔍 MODE SIMULATION - Aucune modification ne sera effectuée")
        )
        
        for bon in bons:
            jours_restants = (bon.date_expiration - timezone.now()).days
            statut_jours = "EXPIRÉ" if jours_restants < 0 else f"expire dans {jours_restants} jour(s)"
            
            self.stdout.write(
                f"• {bon.numero_bon} - {bon.membre.nom_complet} - "
                f"{bon.get_type_soin_display()} - {statut_jours}"
            )
        
        self.stdout.write(
            self.style.WARNING(
                f"\n💡 {bons.count()} bon(s) seraient marqués comme expirés"
            )
        )

    def effectuer_nettoyage(self, bons):
        """Effectue le nettoyage réel des bons"""
        succes = 0
        erreurs = 0
        
        with transaction.atomic():
            for bon in bons:
                try:
                    ancien_statut = bon.statut
                    bon.statut = BonDeSoin.StatutBon.EXPIRE
                    bon.observations = (
                        f"🔴 Bon automatiquement expiré le {timezone.now().strftime('%d/%m/%Y %H:%M')}\n"
                        f"{bon.observations}"
                    )
                    bon.save()
                    
                    # Logger l'action dans l'historique
                    HistoriqueActionAssureur.logger_action(
                        assureur=bon.assureur,
                        type_action=HistoriqueActionAssureur.TypeAction.ANNULATION_BON,
                        description=f"Bon {bon.numero_bon} automatiquement expiré",
                        bon=bon,
                        donnees={
                            'ancien_statut': ancien_statut,
                            'automatique': True
                        }
                    )
                    
                    succes += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✅ {bon.numero_bon} - Marqué comme expiré"
                        )
                    )
                    
                except Exception as e:
                    erreurs += 1
                    logger.error(f"Erreur nettoyage bon {bon.numero_bon}: {e}")
                    self.stdout.write(
                        self.style.ERROR(
                            f"❌ {bon.numero_bon} - Erreur: {e}"
                        )
                    )
        
        # Rapport final
        self.stdout.write("\n" + "="*50)
        self.stdout.write(
            self.style.SUCCESS(
                f"🎉 Nettoyage terminé: {succes} bon(s) expiré(s) avec succès"
            )
        )
        if erreurs > 0:
            self.stdout.write(
                self.style.ERROR(
                    f"⚠️  {erreurs} erreur(s) pendant le nettoyage"
                )
            )