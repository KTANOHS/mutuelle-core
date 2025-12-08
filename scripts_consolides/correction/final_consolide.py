"""
FICHIER CONSOLIDÉ: final
Catégorie: correction
Fusion de 7 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: final_fix_permissions_corrected.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
"""
RÉSOLUTION DÉFINITIVE DES PERMISSIONS POUR GLORIA1
"""

import os
import sys
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import Permission, Group, ContentType
from django.contrib.auth import get_user_model
from django.db import transaction

def debug_permissions():
    """Debug complet des permissions"""
    print("🔍 DEBUG COMPLET DES PERMISSIONS")
    print("=" * 60)

    # 1. Cherche toutes les permissions avec 'ordonnance' dans le nom
    ordonnance_perms = Permission.objects.filter(codename__contains='ordonnance')
    print(f"Permissions avec 'ordonnance': {ordonnance_perms.count()}")

    for perm in ordonnance_perms:
        print(f"\n📋 {perm.codename}:")
        print(f"   ID: {perm.id}")
        print(f"   ContentType: {perm.content_type.app_label}.{perm.content_type.model}")
        print(f"   Nom: {perm.name}")

        # Cherche quels groupes ont cette permission
        groups = Group.objects.filter(permissions=perm)
        if groups.exists():
            print(f"   Groupes: {', '.join([g.name for g in groups])}")
        else:
            print(f"   ⚠ Aucun groupe")

    # 2. Vérifie le groupe Pharmacien
    print("\n" + "=" * 60)
    print("💊 GROUPE PHARMACIEN")
    print("=" * 60)

    try:
        group = Group.objects.get(name='Pharmacien')
        print(f"✅ Groupe Pharmacien trouvé")
        print(f"   ID: {group.id}")
        print(f"   Permissions: {group.permissions.count()}")

... (tronqué)

# ============================================================
# ORIGINE 2: final_fix_permissions.py (2025-12-02)
# ============================================================

#!/usr/bin/env python
"""
RÉSOLUTION DÉFINITIVE DES PERMISSIONS POUR GLORIA1
"""

import os
import sys
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import Permission, Group, ContentType
from django.contrib.auth import get_user_model
from django.db import transaction

def debug_permissions():
    """Debug complet des permissions"""
    print("🔍 DEBUG COMPLET DES PERMISSIONS")
    print("=" * 60)

    # 1. Cherche toutes les permissions avec 'ordonnance' dans le nom
    ordonnance_perms = Permission.objects.filter(codename__contains='ordonnance')
    print(f"Permissions avec 'ordonnance': {ordonnance_perms.count()}")

    for perm in ordonnance_perms:
        print(f"\n📋 {perm.codename}:")
        print(f"   ID: {perm.id}")
        print(f"   ContentType: {perm.content_type.app_label}.{perm.content_type.model}")
        print(f"   Nom: {perm.name}")

        # Cherche quels groupes ont cette permission
        groups = Group.objects.filter(permissions=perm)
        if groups.exists():
            print(f"   Groupes: {', '.join([g.name for g in groups])}")
        else:
            print(f"   ⚠ Aucun groupe")

    # 2. Vérifie le groupe Pharmacien
    print("\n" + "=" * 60)
    print("💊 GROUPE PHARMACIEN")
    print("=" * 60)

    try:
        group = Group.objects.get(name='Pharmacien')
        print(f"✅ Groupe Pharmacien trouvé")
        print(f"   ID: {group.id}")
        print(f"   Permissions: {group.permissions.count()}")

... (tronqué)

# ============================================================
# ORIGINE 3: final_ordonnance_fix.py (2025-11-30)
# ============================================================

# final_ordonnance_fix.py
import os
import django
from django.db import connection
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def fix_ordonnance_creation():
    """Corriger la création d'ordonnance avec le bon champ patient"""
    print("🔧 CORRECTION CRÉATION ORDONNANCE")
    print("=" * 50)

    try:
        from medecin.models import Ordonnance
        from membres.models import Membre
        from django.contrib.auth.models import User

        # Prendre un membre et un médecin existants
        membre = Membre.objects.first()
        medecin_user = User.objects.filter(groups__name='Médecins').first()

        if not medecin_user:
            print("❌ Aucun médecin trouvé dans le système")
            return

        print(f"👤 Membre: {membre}")
        print(f"👨‍⚕️ Médecin: {medecin_user.get_full_name()}")

        # Créer l'ordonnance avec patient_id au lieu de patient
        with connection.cursor() as cursor:
            # Insertion directe dans la table avec patient_id
            cursor.execute("""
                INSERT INTO medecin_ordonnance
                (numero, date_prescription, date_expiration, type_ordonnance,
                 diagnostic, medicaments, posologie, patient_id, medecin_id, statut)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                f"ORD-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                timezone.now().date(),
                timezone.now().date() + timezone.timedelta(days=30),
                "standard",
                "Test diagnostic - Partage médecin→pharmacien",
                "Paracétamol 500mg, Amoxicilline 1g",
                "1 comprimé 3 fois par jour pendant 7 jours",
                membre.id,  # patient_id
                medecin_user.id,  # medecin_id
                "validee"
            ])
... (tronqué)

# ============================================================
# ORIGINE 4: final_member_sync_fix.py (2025-11-30)
# ============================================================

# final_member_sync_fix.py
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def fix_all_sync_issues():
    """Correction définitive de tous les problèmes de synchronisation"""
    print("🔧 CORRECTION DÉFINITIVE SYNCHRONISATION")
    print("=" * 60)

    # 1. Vérifier l'état actuel
    print("\n📊 ÉTAT ACTUEL")
    print("-" * 40)

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM membres_membre")
        total_membres = cursor.fetchone()[0]
        print(f"👥 Membres totaux: {total_membres}")

        # Doublons
        cursor.execute("""
            SELECT prenom, nom, COUNT(*) as doublons
            FROM membres_membre
            GROUP BY prenom, nom
            HAVING COUNT(*) > 1
        """)
        doublons = cursor.fetchall()
        print(f"⚠️  Doublons détectés: {len(doublons)}")

    # 2. Résoudre le conflit de modèles
    print("\n🔗 RÉSOLUTION CONFLIT MODÈLES")
    print("-" * 40)
    print("💡 RECOMMANDATION: Supprimer assureur.Membre du modèle")
    print("   et utiliser uniquement membres.Membre comme source unique")

    # 3. Uniformiser les références
    print("\n🔄 UNIFORMISATION RÉFÉRENCES")
    print("-" * 40)

    # Vérifier les relations existantes
    relations = [
        ('assureur_cotisation', 'membre_id', '✅ OK'),
        ('agents_verificationcotisation', 'membre_id', '✅ OK'),
        ('medecin_consultation', 'membre_id', '⚠️  À vérifier'),
        ('soins_soin', 'patient_id', '❌ PROBLÈME: patient_id au lieu de membre_id'),
        ('soins_bondesoin', 'patient_id', '❌ PROBLÈME: patient_id au lieu de membre_id')
    ]
... (tronqué)

# ============================================================
# ORIGINE 5: final_notes_fix.py (2025-11-30)
# ============================================================

# final_notes_fix.py
import os
import django
from django.db import connection
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def create_cotisation_with_notes():
    """Créer une cotisation avec le champ notes obligatoire"""
    print("💰 CRÉATION COTISATION AVEC NOTES")
    print("=" * 50)

    try:
        with connection.cursor() as cursor:
            # SQL COMPLET avec tous les champs requis
            sql = """
                INSERT INTO assureur_cotisation
                (periode, type_cotisation, montant, montant_clinique, montant_pharmacie,
                 montant_charges_mutuelle, date_emission, date_echeance, statut, reference,
                 notes, membre_id, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            params = [
                '2025',                    # periode
                'STANDARD',                # type_cotisation
                5000.00,                   # montant
                2000.00,                   # montant_clinique
                2000.00,                   # montant_pharmacie
                1000.00,                   # montant_charges_mutuelle
                '2025-01-01',              # date_emission
                '2025-12-31',              # date_echeance
                'ACTIVE',                  # statut
                'FINAL-FIX-001',           # reference
                'Cotisation créée automatiquement',  # notes (OBLIGATOIRE!)
                1,                         # membre_id
                timezone.now().isoformat(), # created_at
                timezone.now().isoformat()  # updated_at
            ]

            cursor.execute(sql, params)
            print("✅ COTISATION CRÉÉE avec succès!")

    except Exception as e:
        print(f"❌ Erreur: {e}")

def create_multiple_with_notes():
    """Créer plusieurs cotisations avec notes"""
... (tronqué)

# ============================================================
# ORIGINE 6: final_nuclear_fix.py (2025-11-30)
# ============================================================

# final_nuclear_fix.py
import os
import django
from django.db import connection
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyze_conflict():
    """Analyser le conflit en détail"""
    print("🔍 ANALYSE DU CONFLIT DE MODÈLES")
    print("=" * 60)

    # Vérifier les tables SQL
    print("\n📊 TABLES EXISTANTES:")
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%cotisation%'")
        cotisation_tables = cursor.fetchall()
        print(f"   Tables cotisation: {[t[0] for t in cotisation_tables]}")

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%membre%'")
        membre_tables = cursor.fetchall()
        print(f"   Tables membre: {[t[0] for t in membre_tables]}")

def fix_model_conflict():
    """Corriger le conflit de modèles"""
    print("\n🔧 CORRECTION DU CONFLIT")
    print("=" * 60)

    # STRATÉGIE: Utiliser SEULEMENT membres.Membre et assureur.Cotisation

    print("🎯 STRATÉGIE:")
    print("   1. Utiliser membres.Membre comme modèle principal")
    print("   2. Utiliser assureur.Cotisation pour les cotisations")
    print("   3. Créer des relations directes entre les deux")

    # Vérifier la structure des tables
    with connection.cursor() as cursor:
        print("\n🔍 Structure table assureur_cotisation:")
        cursor.execute("PRAGMA table_info(assureur_cotisation)")
        for col in cursor.fetchall():
            print(f"   {col[1]} ({col[2]})")

def create_cotisations_correct():
    """Créer des cotisations avec la bonne relation"""
    print("\n💰 CRÉATION COTISATIONS CORRECTES")
    print("=" * 60)

    # 1. Obtenir les vrais IDs de membres depuis la table membres_membre
... (tronqué)

# ============================================================
# ORIGINE 7: final_fix_cotisations.py (2025-11-30)
# ============================================================

# final_fix_cotisations.py
import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def fix_all_issues():
    """Correction définitive de tous les problèmes"""
    print("🔧 CORRECTION DÉFINITIVE DES PROBLÈMES COTISATIONS")
    print("=" * 60)

    # 1. CORRECTION DU MODÈLE ASSUREUR
    fix_assureur_model()

    # 2. CRÉATION DES COTISATIONS
    create_cotisations_fixed()

    # 3. SYNCHRONISATION FINALE
    final_sync()

    # 4. VÉRIFICATION
    verify_fix()

def fix_assureur_model():
    """Corriger le problème de relation Assureur"""
    print("\n👤 CORRECTION RELATION ASSUREUR")
    print("-" * 40)

    from django.contrib.auth.models import User
    from assureur.models import Assureur

    try:
        # Vérifier/Créer l'utilisateur assureur
        user, created = User.objects.get_or_create(
            username='assureur_system',
            defaults={
                'first_name': 'Système',
                'last_name': 'Assureur',
                'email': 'assureur@mutuelle.local',
                'is_staff': True
            }
        )
        if created:
            user.set_password('assureur123')
            user.save()
            print("✅ Utilisateur assureur créé")
        else:
... (tronqué)

