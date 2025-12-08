# create_members_simple.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre

# Désactiver temporairement les signaux si nécessaire
from django.db.models import signals
try:
    from assureur.models import creer_profil_assureur
    from medecin.models import creer_profil_medecin
    from pharmacien.models import creer_profil_pharmacien
    from django.contrib.auth.models import User
    
    # Désactiver les signaux
    signals.post_save.disconnect(creer_profil_assureur, sender=User)
    signals.post_save.disconnect(creer_profil_medecin, sender=User)
    signals.post_save.disconnect(creer_profil_pharmacien, sender=User)
    print("Signaux désactivés temporairement")
except ImportError:
    pass

# Vérifier et créer des membres
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
    try:
        membre = Membre.objects.create(**data)
        print(f"✓ Membre créé : {membre.nom} {membre.prenom}")
    except Exception as e:
        print(f"✗ Erreur création membre {data['nom']}: {e}")

print(f"\nTotal membres actifs : {Membre.objects.filter(statut='actif').count()}")