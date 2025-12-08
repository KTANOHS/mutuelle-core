# assureur/management/commands/inspect_assureur.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Inspecte les modèles pour l application assureur'

    def handle(self, *args, **options):
        exec(open('inspect_assureur_models.py').read())