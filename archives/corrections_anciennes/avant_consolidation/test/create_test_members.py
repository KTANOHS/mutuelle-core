# Créez ce script : create_test_members.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre
from django.contrib.auth.models import User

# Créer un utilisateur assureur pour les tests
user, created = User.objects.get_or_create(
    username='assureur_test',
    defaults={
        'email': 'assureur@test.com',
        'is_staff': True,
        'is_active': True
    }
)
if created:
    user.set_password('test123')
    user.save()

# Créer des membres actifs
membres_data = [
    {
        'nom': 'Dupont',
        'prenom': 'Jean',
        'numero_membre': 'MBR001',
        'statut': 'actif',
        'type_membre': 'standard',
        'email': 'jean.dupont@test.com',
        'telephone': '0123456789'
    },
    {
        'nom': 'Martin',
        'prenom': 'Marie',
        'numero_membre': 'MBR002',
        'statut': 'actif',
        'type_membre': 'premium',
        'email': 'marie.martin@test.com',
        'telephone': '0234567890'
    },
    {
        'nom': 'Bernard',
        'prenom': 'Pierre',
        'numero_membre': 'MBR003',
        'statut': 'actif',
        'type_membre': 'standard',
        'email': 'pierre.bernard@test.com',
        'telephone': '0345678901'
    }
]

for data in membres_data:
    membre, created = Membre.objects.get_or_create(
        numero_membre=data['numero_membre'],
        defaults=data
    )
    if created:
        print(f"Membre créé : {membre.nom} {membre.prenom}")
    else:
        print(f"Membre existant : {membre.nom} {membre.prenom}")

print(f"\nTotal membres actifs : {Membre.objects.filter(statut='actif').count()}")