"""
FICHIER CONSOLIDÉ: create
Catégorie: test
Fusion de 4 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: create_simple_test_data.py (2025-12-05)
# ============================================================


import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()

from django.contrib.auth.models import User, Group
from membres.models import Membre
from assureur.models import Bon, ConfigurationAssurance, Paiement
from django.utils import timezone
from datetime import timedelta
import random

print("=== CRÉATION DE DONNÉES DE TEST SIMPLES ===")

# 1. Vérifier que DOUA est dans le bon groupe
doua = User.objects.get(username='DOUA')
assureur_group = Group.objects.get(name='Assureur')
print(f"✓ DOUA dans groupe: {assureur_group.name}")

# 2. Créer quelques membres
membres_data = [
    {'nom': 'KOUADIO', 'prenom': 'Jean', 'matricule': 'MEM001', 'telephone': '07000001'},
    {'nom': 'KONE', 'prenom': 'Marie', 'matricule': 'MEM002', 'telephone': '07000002'},
    {'nom': 'DIAKITE', 'prenom': 'Paul', 'matricule': 'MEM003', 'telephone': '07000003'},
]

for data in membres_data:
    membre, created = Membre.objects.get_or_create(
        matricule=data['matricule'],
        defaults={
            'nom': data['nom'],
            'prenom': data['prenom'],
            'telephone': data['telephone'],
            'date_inscription': timezone.now() - timedelta(days=random.randint(30, 365)),
            'statut': 'actif',
            'email': f"{data['prenom'].lower()}.{data['nom'].lower()}@example.com",
        }
    )
    if created:
        print(f"✓ Membre créé: {membre.nom_complet}")

# 3. Créer quelques bons de soin
membres = Membre.objects.all()
types_soin = ['consultation', 'hospitalisation', 'pharmacie']
statuts = ['en_attente', 'valide', 'rejete']

for i in range(5):
    bon = Bon.objects.create(
        numero=f"BS{2024}{i+1:04d}",
... (tronqué)

# ============================================================
# ORIGINE 2: create_test_data1.py (2025-12-05)
# ============================================================


import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()

from django.contrib.auth.models import User, Group
from membres.models import Membre
from assureur.models import Bon, ConfigurationAssurance, Paiement
from django.utils import timezone
from datetime import timedelta
import random

print("=== CRÉATION DE DONNÉES DE TEST SIMPLES ===")

# 1. Vérifier que DOUA est dans le bon groupe
doua = User.objects.get(username='DOUA')
assureur_group = Group.objects.get(name='Assureur')
print(f"✓ DOUA dans groupe: {assureur_group.name}")

# 2. Créer quelques membres
membres_data = [
    {'nom': 'KOUADIO', 'prenom': 'Jean', 'matricule': 'MEM001', 'telephone': '07000001'},
    {'nom': 'KONE', 'prenom': 'Marie', 'matricule': 'MEM002', 'telephone': '07000002'},
    {'nom': 'DIAKITE', 'prenom': 'Paul', 'matricule': 'MEM003', 'telephone': '07000003'},
]

for data in membres_data:
    membre, created = Membre.objects.get_or_create(
        matricule=data['matricule'],
        defaults={
            'nom': data['nom'],
            'prenom': data['prenom'],
            'telephone': data['telephone'],
            'date_inscription': timezone.now() - timedelta(days=random.randint(30, 365)),
            'statut': 'actif',
            'email': f"{data['prenom'].lower()}.{data['nom'].lower()}@example.com",
        }
    )
    if created:
        print(f"✓ Membre créé: {membre.nom_complet}")

# 3. Créer quelques bons de soin
membres = Membre.objects.all()
types_soin = ['consultation', 'hospitalisation', 'pharmacie']
statuts = ['en_attente', 'valide', 'rejete']

for i in range(5):
    bon = Bon.objects.create(
        numero=f"BS{2024}{i+1:04d}",
... (tronqué)

# ============================================================
# ORIGINE 3: create_test_data.py (2025-12-04)
# ============================================================

# Créez un fichier create_test_data.py
import os
import django
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from soins.models import Soin
from django.contrib.auth.models import User

# Créer des soins de test pour chaque membre
def create_test_soins():
    membres = Membre.objects.all()[:5]  # Les 5 premiers membres

    for membre in membres:
        # Créer plusieurs soins par membre
        soin1 = Soin.objects.create(
            patient=membre,
            type_soin='Consultation générale',
            date_soin='2023-12-01',
            cout_reel=5000.00,
            statut='valide',
            created_by=User.objects.first()
        )
        print(f"✅ Soin créé: {soin1.id} - {soin1.type_soin} pour {membre.prenom} {membre.nom}")

        soin2 = Soin.objects.create(
            patient=membre,
            type_soin='Analyse sanguine',
            date_soin='2023-12-10',
            cout_reel=15000.00,
            statut='valide',
            created_by=User.objects.first()
        )
        print(f"✅ Soin créé: {soin2.id} - {soin2.type_soin} pour {membre.prenom} {membre.nom}")

if __name__ == "__main__":
    create_test_soins()

# ============================================================
# ORIGINE 4: create_test_members.py (2025-12-03)
# ============================================================

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
... (tronqué)

