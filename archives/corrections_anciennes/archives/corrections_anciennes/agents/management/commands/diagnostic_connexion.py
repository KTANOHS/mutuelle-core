# management/commands/diagnostic_connexion.py
from django.core.management.base import BaseCommand
from diagnostic_connexion import DiagnosticConnexion

class Command(BaseCommand):
    help = 'Diagnostic complet du processus de connexion des acteurs'
    
    def handle(self, *args, **options):
        diagnostic = DiagnosticConnexion()
        diagnostic.executer_diagnostic_complet()