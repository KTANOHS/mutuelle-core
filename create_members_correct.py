# create_members_correct.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre
import inspect

# Vérifier les champs disponibles du modèle Membre
print("=== CHAMPS DISPONIBLES DANS LE MODÈLE MEMBRE ===")
for field in Membre._meta.fields:
    print(f"  - {field.name} ({field.get_internal_type()})")

# Créer des membres avec les champs corrects
membres_data = [
    {
        'nom': 'Dupont',
        'prenom': 'Jean',
        'numero_membre': 'MBR001',
        'statut': 'actif',
        'email': 'jean.dupont@test.com',
        'telephone': '0123456789',
        'adresse': '123 Rue Test, Ville'
    },
    {
        'nom': 'Martin',
        'prenom': 'Marie', 
        'numero_membre': 'MBR002',
        'statut': 'actif',
        'email': 'marie.martin@test.com',
        'telephone': '0234567890',
        'adresse': '456 Avenue Test, Ville'
    },
    {
        'nom': 'Bernard',
        'prenom': 'Pierre',
        'numero_membre': 'MBR003',
        'statut': 'actif',
        'email': 'pierre.bernard@test.com',
        'telephone': '0345678901',
        'adresse': '789 Boulevard Test, Ville'
    }
]

print("\n=== CRÉATION DES MEMBRES ===")
for data in membres_data:
    try:
        # Vérifier si le numéro de membre existe déjà
        if Membre.objects.filter(numero_membre=data['numero_membre']).exists():
            print(f"⚠ Membre {data['numero_membre']} existe déjà")
        else:
            membre = Membre(**data)
            membre.save()
            print(f"✓ Membre créé : {membre.nom} {membre.prenom} ({membre.numero_membre})")
    except Exception as e:
        print(f"✗ Erreur création membre {data['nom']}: {e}")
        import traceback
        traceback.print_exc()

print(f"\n=== RÉSUMÉ ===")
print(f"Total membres : {Membre.objects.count()}")
print(f"Membres actifs : {Membre.objects.filter(statut='actif').count()}")