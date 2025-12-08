# assureur/management/commands/init_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from assureur.models import Membre, Bon, Soin, Paiement

class Command(BaseCommand):
    help = 'Crée les groupes et permissions de base'

    def handle(self, *args, **options):
        # Groupe Assureur
        assureur_group, created = Group.objects.get_or_create(name='Assureur')
        if created:
            self.stdout.write(self.style.SUCCESS('Groupe Assureur créé'))
        
        # Groupe Membre
        membre_group, created = Group.objects.get_or_create(name='Membre')
        if created:
            self.stdout.write(self.style.SUCCESS('Groupe Membre créé'))
        
        # Groupe Medecin
        medecin_group, created = Group.objects.get_or_create(name='Medecin')
        if created:
            self.stdout.write(self.style.SUCCESS('Groupe Medecin créé'))
        
        # Groupe Pharmacien
        pharmacien_group, created = Group.objects.get_or_create(name='Pharmacien')
        if created:
            self.stdout.write(self.style.SUCCESS('Groupe Pharmacien créé'))

        self.stdout.write(self.style.SUCCESS('Groupes initialisés avec succès'))