# management/commands/diagnostic_sync.py
from django.core.management.base import BaseCommand
from diagnostics.sync_diagnostic import DiagnosticSynchronisation

class Command(BaseCommand):
    help = 'Exécute le diagnostic de synchronisation des données'
    
    def add_arguments(self, parser):
        parser.add_argument('--correct', action='store_true', help='Applique les corrections')
    
    def handle(self, *args, **options):
        diagnostic = DiagnosticSynchronisation()
        diagnostic.executer_diagnostic_complet()
        
        if options['correct']:
            from diagnostics.correcteur_sync import CorrecteurSynchronisation
            correcteur = CorrecteurSynchronisation(mode_test=False)
            correcteur.corriger_problemes(diagnostic.resultats)