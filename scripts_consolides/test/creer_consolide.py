"""
FICHIER CONSOLIDÉ: creer
Catégorie: test
Fusion de 5 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: creer_donnees_test_complet.py (2025-12-01)
# ============================================================

#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from communication.models import Conversation, Notification, Message
from pharmacien.models import Pharmacien
from medecin.models import Medecin
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

def creer_donnees_test_complet():
    User = get_user_model()

    print("🚀 CRÉATION DE DONNÉES DE TEST COMPLÈTES")
    print("=" * 60)

    # 1. Trouver ou créer GLORIA1 (pharmacien)
    try:
        gloria = User.objects.get(username='GLORIA1')
        print(f"✅ GLORIA1 trouvée (ID: {gloria.id})")
    except User.DoesNotExist:
        print("❌ GLORIA1 non trouvée, création...")
        gloria = User.objects.create_user(
            username='GLORIA1',
            email='gloria@pharmacie.com',
            password='pharmacien123'
        )
        gloria.save()
        print(f"👤 GLORIA1 créée (ID: {gloria.id})")

    # 2. Créer/s'assurer que GLORIA1 est pharmacien
    pharmacien, created = Pharmacien.objects.get_or_create(
        user=gloria,
        defaults={
            'nom_complet': 'Gloria Pharmacien',
            'telephone': '0123456789',
            'pharmacie_nom': 'Pharmacie Centrale'
        }
    )
    if created:
        print(f"🏥 Pharmacien créé: {pharmacien.nom_complet}")
    else:
        print(f"🏥 Pharmacien existant: {pharmacien.nom_complet}")

    # 3. Créer des médecins de test pour les conversations
    medecins_users = []
... (tronqué)

# ============================================================
# ORIGINE 2: creer_conversations_test1.py (2025-11-16)
# ============================================================

# creer_conversations_test.py
import os
import django
import sys

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from communication.models import Conversation, Message
from django.contrib.auth import get_user_model
from django.utils import timezone

def creer_conversations_test():
    print("🚀 CRÉATION DE CONVERSATIONS DE TEST")
    print("=" * 50)

    User = get_user_model()

    try:
        # Récupérer les utilisateurs existants
        test_agent = User.objects.get(username='test_agent')
        test_assureur = User.objects.get(username='test_assureur')
        test_medecin = User.objects.get(username='test_medecin')

        print("✅ Utilisateurs trouvés:")
        print(f"   • Agent: {test_agent}")
        print(f"   • Assureur: {test_assureur}")
        print(f"   • Médecin: {test_medecin}")

    except User.DoesNotExist as e:
        print(f"❌ Utilisateurs de test non trouvés: {e}")
        print("   Création d'utilisateurs de test...")
        return

    # Créer une conversation entre agent et assureur
    try:
        conv1 = Conversation.objects.create()
        conv1.participants.add(test_agent, test_assureur)
        conv1.save()

        # Créer des messages de test
        Message.objects.create(
            expediteur=test_agent,
            destinataire=test_assureur,
            conversation=conv1,
            titre="Demande d'information",
            contenu="Bonjour, je souhaite avoir des informations sur la couverture des soins.",
            est_lu=False
        )
... (tronqué)

# ============================================================
# ORIGINE 3: creer_conversations_test.py (2025-11-16)
# ============================================================

# creer_conversations_test.py
import os
import django
import sys

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from communication.models import Conversation, Message
from django.contrib.auth import get_user_model
from django.utils import timezone

def creer_conversations_test():
    print("🚀 CRÉATION DE CONVERSATIONS DE TEST")
    print("=" * 50)

    User = get_user_model()

    # Récupérer les utilisateurs existants
    try:
        test_agent = User.objects.get(username='test_agent')
        test_assureur = User.objects.get(username='test_assureur')
        test_medecin = User.objects.get(username='test_medecin')

        print("✅ Utilisateurs trouvés:")
        print(f"   • Agent: {test_agent}")
        print(f"   • Assureur: {test_assureur}")
        print(f"   • Médecin: {test_medecin}")

    except User.DoesNotExist:
        print("❌ Utilisateurs de test non trouvés")
        return

    # Créer une conversation entre agent et assureur
    conv1, created1 = Conversation.objects.get_or_create()
    if created1:
        conv1.participants.add(test_agent, test_assureur)
        conv1.save()

        # Créer des messages de test
        Message.objects.create(
            expediteur=test_agent,
            destinataire=test_assureur,
            conversation=conv1,
            titre="Demande d'information",
            contenu="Bonjour, je souhaite avoir des informations sur la couverture des soins.",
            est_lu=False
        )

... (tronqué)

# ============================================================
# ORIGINE 4: creer_donnees_test2.py (2025-11-15)
# ============================================================

# creer_donnees_test.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from membres.models import Membre
from assureur.models import Assureur
from django.utils import timezone

def creer_donnees_test():
    print("🧪 CRÉATION DE DONNÉES DE TEST")
    print("-" * 40)

    User = get_user_model()

    # Créer un assureur de test
    try:
        # Créer l'utilisateur
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
            print("✅ Utilisateur assureur_test créé")
        else:
            print("✅ Utilisateur assureur_test existe déjà")

        # Créer le profil assureur
        assureur, created = Assureur.objects.get_or_create(
            user=user,
            defaults={
                'nom': 'Assureur Test',
                'email': 'assureur@test.com',
                'telephone': '+2250102030405'
            }
        )
        if created:
            print("✅ Profil Assureur créé")
        else:
            print("✅ Profil Assureur existe déjà")

... (tronqué)

# ============================================================
# ORIGINE 5: creer_donnees_test1.py (2025-11-15)
# ============================================================

import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from membres.models import Membre
from medecin.models import Medecin, Consultation, SpecialiteMedicale, EtablissementMedical
from agents.models import BonSoin
from django.utils import timezone

def creer_donnees_test():
    print("🔧 Création des données de test...")

    # 1. Créer ou récupérer le groupe médecin
    groupe_medecin, created = Group.objects.get_or_create(name='medecin')

    # 2. Créer un utilisateur médecin de test (s'il n'existe pas)
    try:
        user_medecin = User.objects.get(username='test_medecin')
        print("✅ Médecin test existant trouvé")
    except User.DoesNotExist:
        user_medecin = User.objects.create_user(
            username='test_medecin',
            password='test123',
            first_name='Jean',
            last_name='Dupont',
            email='jean.dupont@clinique.com'
        )
        user_medecin.groups.add(groupe_medecin)
        user_medecin.save()
        print("✅ Médecin test créé")

    # 3. Créer le profil médecin
    try:
        medecin = Medecin.objects.get(user=user_medecin)
        print("✅ Profil médecin existant trouvé")
    except Medecin.DoesNotExist:
        # Créer spécialité et établissement par défaut
        specialite, _ = SpecialiteMedicale.objects.get_or_create(
            nom='Médecine Générale',
            defaults={'description': 'Médecine générale et soins primaires'}
        )

        etablissement, _ = EtablissementMedical.objects.get_or_create(
            nom='Clinique du Lac',
            defaults={
                'type_etablissement': 'CLINIQUE',
... (tronqué)

