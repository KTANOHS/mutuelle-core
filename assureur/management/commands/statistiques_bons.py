from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Count, Sum, Avg
from datetime import timedelta
from assureur.models import BonDeSoin

class Command(BaseCommand):
    help = 'Affiche les statistiques des bons de soin'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--periode',
            type=int,
            default=30,
            help='Période en jours pour les statistiques (défaut: 30)'
        )
        parser.add_argument(
            '--assureur',
            type=int,
            help='ID de l\'assureur pour filtrer les statistiques'
        )

    def handle(self, *args, **options):
        periode = options['periode']
        assureur_id = options['assureur']
        
        self.stdout.write(
            self.style.MIGRATE_HEADING(f"📊 Statistiques des bons - {periode} derniers jours")
        )
        
        # Filtre de base
        date_limite = timezone.now() - timedelta(days=periode)
        queryset = BonDeSoin.objects.filter(date_emission__gte=date_limite)
        
        if assureur_id:
            queryset = queryset.filter(assureur_id=assureur_id)
            self.stdout.write(f"Filtre: Assureur ID {assureur_id}")
        
        # Statistiques générales
        stats_generales = queryset.aggregate(
            total_bons=Count('id'),
            bons_utilises=Count('id', filter=models.Q(statut=BonDeSoin.StatutBon.UTILISE)),
            montant_total=Sum('montant'),
            montant_moyen=Avg('montant')
        )
        
        self.afficher_statistiques_generales(stats_generales)
        
        # Statistiques par type de soin
        self.afficher_statistiques_par_type(queryset)
        
        # Statistiques par statut
        self.afficher_statistiques_par_statut(queryset)

    def afficher_statistiques_generales(self, stats):
        """Affiche les statistiques générales"""
        self.stdout.write("\n" + "="*40)
        self.stdout.write(self.style.SUCCESS("📈 STATISTIQUES GÉNÉRALES"))
        self.stdout.write("="*40)
        
        self.stdout.write(f"• Total des bons: {stats['total_bons']}")
        self.stdout.write(f"• Bons utilisés: {stats['bons_utilises']}")
        self.stdout.write(f"• Montant total: {stats['montant_total'] or 0:.2f} €")
        self.stdout.write(f"• Montant moyen: {stats['montant_moyen'] or 0:.2f} €")
        
        if stats['total_bons'] > 0:
            taux_utilisation = (stats['bons_utilises'] / stats['total_bons']) * 100
            self.stdout.write(f"• Taux d'utilisation: {taux_utilisation:.1f}%")

    def afficher_statistiques_par_type(self, queryset):
        """Affiche les statistiques par type de soin"""
        self.stdout.write("\n" + self.style.SUCCESS("🏥 PAR TYPE DE SOIN"))
        
        stats_type = queryset.values('type_soin').annotate(
            count=Count('id'),
            montant_total=Sum('montant'),
            montant_moyen=Avg('montant')
        ).order_by('-count')
        
        for stat in stats_type:
            self.stdout.write(
                f"• {stat['type_soin']}: {stat['count']} bons "
                f"({stat['montant_total'] or 0:.2f} € total, "
                f"{stat['montant_moyen'] or 0:.2f} € moyen)"
            )

    def afficher_statistiques_par_statut(self, queryset):
        """Affiche les statistiques par statut"""
        self.stdout.write("\n" + self.style.SUCCESS("📋 PAR STATUT"))
        
        stats_statut = queryset.values('statut').annotate(
            count=Count('id'),
            montant_total=Sum('montant')
        ).order_by('-count')
        
        for stat in stats_statut:
            self.stdout.write(
                f"• {stat['statut']}: {stat['count']} bons "
                f"({stat['montant_total'] or 0:.2f} €)"
            )