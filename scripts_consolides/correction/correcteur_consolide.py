"""
FICHIER CONSOLIDÉ: correcteur
Catégorie: correction
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
# ORIGINE 1: correcteur_problemes_diagnostic.py (2025-11-28)
# ============================================================

# correcteur_problemes_diagnostic.py

import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

def creer_groupes_manquants():
    """Crée les groupes manquants identifiés par le diagnostic"""
    print("🔧 CRÉATION DES GROUPES MANQUANTS")
    print("=" * 50)

    groupes_a_creer = ['Médecins', 'Pharmaciens', 'Membres']

    for nom_groupe in groupes_a_creer:
        groupe, created = Group.objects.get_or_create(name=nom_groupe)
        if created:
            print(f"✅ Groupe '{nom_groupe}' créé")
        else:
            print(f"✅ Groupe '{nom_groupe}' existe déjà")

def creer_profils_agents():
    """Crée les profils Agent pour les utilisateurs existants"""
    print("\n🔧 CRÉATION DES PROFILS AGENTS")
    print("=" * 50)

    try:
        from agents.models import Agent

        # Compter les utilisateurs dans le groupe Agents sans profil
        users_agents = User.objects.filter(groups__name='Agents')
        agents_sans_profil = []

        for user in users_agents:
            try:
                Agent.objects.get(user=user)
            except Agent.DoesNotExist:
                agents_sans_profil.append(user)

        print(f"👥 Utilisateurs Agents sans profil: {len(agents_sans_profil)}")

        # Créer les profils manquants
... (tronqué)

# ============================================================
# ORIGINE 2: correcteur_sync_corrige.py (2025-11-27)
# ============================================================

# correcteur_sync_corrige.py
import os
import sys
import django
from pathlib import Path
from django.db import transaction

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from django.contrib.auth.models import User
from membres.models import Membre
from django.db.models import Q

print("🔧 CORRECTEUR DE SYNCHRONISATION - VERSION CORRIGÉE")
print("=" * 50)

class CorrecteurSynchronisationCorrige:
    def __init__(self, mode_test=True):
        self.mode_test = mode_test
        self.actions = []
        self.corrections_appliquees = 0

    def corriger_tous_problemes(self):
        """Corrige tous les problèmes identifiés - Version corrigée"""
        print("🎯 CORRECTION DES PROBLÈMES DE SYNCHRO...")

        try:
            # MODIFICATION : Pas de bloc atomic en mode test
            if self.mode_test:
                print("⚠️  MODE TEST - Simulations seulement")
                self._corriger_membres_sans_user()
                self._corriger_numeros_uniques()
                self._synchroniser_utilisateurs_membres()
            else:
                # MODIFICATION : Atomic seulement en mode réel
                with transaction.atomic():
                    self._corriger_membres_sans_user()
                    self._corriger_numeros_uniques()
                    self._synchroniser_utilisateurs_membres()

            # Résumé
            self._afficher_resume()

        except Exception as e:
            print(f"❌ Erreur lors des corrections: {e}")

... (tronqué)

# ============================================================
# ORIGINE 3: correcteur_sync_urgence.py (2025-11-27)
# ============================================================

# correcteur_sync_urgence.py
import os
import sys
import django
from pathlib import Path
from django.db import transaction

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from django.contrib.auth.models import User
from membres.models import Membre
from django.db.models import Q

print("🔧 CORRECTEUR DE SYNCHRONISATION URGENCE")
print("=" * 50)

class CorrecteurSynchronisation:
    def __init__(self, mode_test=True):
        self.mode_test = mode_test
        self.actions = []
        self.corrections_appliquees = 0

    def corriger_tous_problemes(self):
        """Corrige tous les problèmes identifiés"""
        print("🎯 CORRECTION DES PROBLÈMES DE SYNCHRO...")

        try:
            with transaction.atomic():
                if self.mode_test:
                    transaction.set_rollback(True)
                    print("⚠️  MODE TEST - Aucune modification en base")

                # 1. Corriger les membres sans user
                self._corriger_membres_sans_user()

                # 2. Vérifier et corriger les numéros uniques
                self._corriger_numeros_uniques()

                # 3. Synchroniser utilisateurs-membres
                self._synchroniser_utilisateurs_membres()

                # Résumé
                self._afficher_resume()

        except Exception as e:
            print(f"❌ Erreur lors des corrections: {e}")
... (tronqué)

# ============================================================
# ORIGINE 4: correcteur_formulaire_urgence.py (2025-11-16)
# ============================================================

# correcteur_formulaire_urgence.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def correcteur_formulaire_urgence():
    """Correcteur d'urgence pour forcer la méthode save() corrigée"""
    print("=== CORRECTEUR URGENCE FORMULAIRE ===")

    # Réimporter le formulaire pour forcer la mise à jour
    import importlib
    import communication.forms
    importlib.reload(communication.forms)

    from communication.forms import MessageForm
    from django.contrib.auth import get_user_model

    User = get_user_model()

    # Forcer la méthode save corrigée
    def save_corrigee(self, commit=True):
        from communication.utils import get_or_create_conversation
        from communication.models import PieceJointe

        print("🔧 Utilisation de save() corrigée")

        # Appeler la méthode save originale mais sans commit
        message = super(MessageForm, self).save(commit=False)

        # Assigner l'expéditeur
        if hasattr(self, 'expediteur') and self.expediteur:
            message.expediteur = self.expediteur
            print(f"✅ Expéditeur assigné: {self.expediteur.username}")

        # Créer automatiquement une conversation
        if hasattr(message, 'expediteur') and hasattr(message, 'destinataire'):
            if message.expediteur and message.destinataire:
                conversation = get_or_create_conversation(message.expediteur, message.destinataire)
                message.conversation = conversation
                print(f"✅ Conversation assignée: {conversation.id}")
            else:
                print("❌ Expéditeur ou destinataire manquant")
        else:
            print("❌ Champs expediteur/destinataire manquants dans le modèle")

        if commit:
            try:
... (tronqué)

