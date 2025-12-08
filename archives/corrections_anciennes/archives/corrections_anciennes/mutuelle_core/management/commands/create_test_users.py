"""
Commandes de gestion pour créer des utilisateurs de test
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from membres.models import Membre, Assureur, Medecin, Pharmacien

class Command(BaseCommand):
    help = 'Crée des utilisateurs de test pour tous les rôles'

    def handle(self, *args, **options):
        # Créer les groupes s'ils n'existent pas
        groups = ['Assureur', 'Medecin', 'Pharmacien', 'Membre']
        for group_name in groups:
            Group.objects.get_or_create(name=group_name)

        # Utilisateur assureur
        assureur, created = User.objects.get_or_create(
            username='assureur_test',
            defaults={'email': 'assureur@test.com', 'is_staff': True}
        )
        if created:
            assureur.set_password('test123')
            assureur.save()
            assureur.groups.add(Group.objects.get(name='Assureur'))
            Assureur.objects.create(user=assureur, nom="Assureur Test")
            self.stdout.write(self.style.SUCCESS('Assureur créé'))

        # Utilisateur médecin
        medecin, created = User.objects.get_or_create(
            username='medecin_test',
            defaults={'email': 'medecin@test.com'}
        )
        if created:
            medecin.set_password('test123')
            medecin.save()
            medecin.groups.add(Group.objects.get(name='Medecin'))
            Medecin.objects.create(user=medecin, nom="Medecin Test")
            self.stdout.write(self.style.SUCCESS('Médecin créé'))

        # Utilisateur pharmacien
        pharmacien, created = User.objects.get_or_create(
            username='pharmacien_test',
            defaults={'email': 'pharmacien@test.com'}
        )
        if created:
            pharmacien.set_password('test123')
            pharmacien.save()
            pharmacien.groups.add(Group.objects.get(name='Pharmacien'))
            Pharmacien.objects.create(user=pharmacien, nom="Pharmacien Test")
            self.stdout.write(self.style.SUCCESS('Pharmacien créé'))

        # Utilisateur membre
        membre, created = User.objects.get_or_create(
            username='membre_test',
            defaults={'email': 'membre@test.com'}
        )
        if created:
            membre.set_password('test123')
            membre.save()
            membre.groups.add(Group.objects.get(name='Membre'))
            Membre.objects.create(
                user=membre,
                nom="Membre",
                prenom="Test",
                email="membre@test.com",
                telephone="0123456789"
            )
            self.stdout.write(self.style.SUCCESS('Membre créé'))

        self.stdout.write(self.style.SUCCESS('Tous les utilisateurs de test ont été créés'))