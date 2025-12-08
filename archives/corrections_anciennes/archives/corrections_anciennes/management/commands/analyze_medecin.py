from django.core.management.base import BaseCommand
from analysis_medecin import MedecinAnalyzer

class Command(BaseCommand):
    help = 'Analyse la conformité de l\'application medecin'
    
    def handle(self, *args, **options):
        analyzer = MedecinAnalyzer()
        analyzer.analyze_all()