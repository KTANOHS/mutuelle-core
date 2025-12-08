# create_members_final.py
import os
import django
from datetime import datetime, date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur.models import Membre
import inspect

# Créer des membres avec tous les champs obligatoires
membres_data = [
    {
        'nom': 'Dupont',
        'prenom': 'Jean',
        'numero_membre': 'MBR001',
        'date_naissance': date(1980, 1, 1),  # Champ obligatoire !
        'email': 'jean.dupont@test.com',
        'telephone': '0123456789',
        'adresse': '123 Rue Test, Ville',
        'statut': 'actif',
        'type_contrat': 'standard',
        'numero_contrat': 'CONTRAT001',
        'date_adhesion': date(2024, 1, 1),
        'date_effet': date(2024, 1, 1),
        'date_expiration': date(2025, 1, 1),
        'taux_couverture': 80.00
    },
    {
        'nom': 'Martin',
        'prenom': 'Marie', 
        'numero_membre': 'MBR002',
        'date_naissance': date(1985, 5, 15),
        'email': 'marie.martin@test.com',
        'telephone': '0234567890',
        'adresse': '456 Avenue Test, Ville',
        'statut': 'actif',
        'type_contrat': 'premium',
        'numero_contrat': 'CONTRAT002',
        'date_adhesion': date(2024, 2, 1),
        'date_effet': date(2024, 2, 1),
        'date_expiration': date(2025, 2, 1),
        'taux_couverture': 90.00
    },
    {
        'nom': 'Bernard',
        'prenom': 'Pierre',
        'numero_membre': 'MBR003',
        'date_naissance': date(1990, 10, 30),
        'email': 'pierre.bernard@test.com',
        'telephone': '0345678901',
        'adresse': '789 Boulevard Test, Ville',
        'statut': 'actif',
        'type_contrat': 'standard',
        'numero_contrat': 'CONTRAT003',
        'date_adhesion': date(2024, 3, 1),
        'date_effet': date(2024, 3, 1),
        'date_expiration': date(2025, 3, 1),
        'taux_couverture': 80.00
    }
]

print("=== CRÉATION DES MEMBRES AVEC TOUS LES CHAMPS OBLIGATOIRES ===")

for data in membres_data:
    try:
        # Vérifier si le numéro de membre existe déjà
        if Membre.objects.filter(numero_membre=data['numero_membre']).exists():
            print(f"⚠ Membre {data['numero_membre']} existe déjà - mise à jour")
            membre = Membre.objects.get(numero_membre=data['numero_membre'])
            for key, value in data.items():
                setattr(membre, key, value)
            membre.save()
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

# Afficher les membres créés
print("\n=== LISTE DES MEMBRES ===")
for m in Membre.objects.all():
    print(f"  - {m.nom} {m.prenom} ({m.numero_membre}) - {m.statut} - Né le: {m.date_naissance}")