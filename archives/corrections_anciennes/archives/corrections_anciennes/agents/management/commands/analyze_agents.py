# agents/management/commands/analyze_agents.py
from django.core.management.base import BaseCommand
from agents.analysis_script import analyze_all_agents, export_to_excel

class Command(BaseCommand):
    help = 'Analyser les performances des agents et générer un rapport'
    
    def add_arguments(self, parser):
        parser.add_argument('--export', type=str, help='Nom du fichier Excel pour l\'export')
    
    def handle(self, *args, **options):
        self.stdout.write('🚀 Analyse des performances des agents...')
        
        rapports = analyze_all_agents()
        
        if options['export']:
            export_to_excel(rapports, options['export'])
            self.stdout.write(
                self.style.SUCCESS(f'✅ Rapport exporté vers {options["export"]}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'✅ Analyse terminée pour {len(rapports)} agents')
            )