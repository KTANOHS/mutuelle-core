#!/usr/bin/env python3
"""
SCRIPT DE VÉRIFICATION BASE DE DONNÉES
Vérifie l'état actuel de la base pour l'implémentation
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import connection
from membres.models import Membre
from django.contrib.auth.models import User, Group, Permission
from django.core.management import call_command

def verifier_base_donnees():
    """Vérifie l'état de la base de données"""
    print("🔍 VÉRIFICATION BASE DE DONNÉES")
    print("=" * 50)
    
    # 1. Vérifier les migrations
    print("\n1. 📦 ÉTAT DES MIGRATIONS")
    print("-" * 25)
    try:
        call_command('showmigrations', '--list')
        print("   ✅ Migrations vérifiées")
    except Exception as e:
        print(f"   ❌ Erreur migrations: {e}")
    
    # 2. Vérifier la connexion DB
    print("\n2. 🗄️ CONNEXION BASE DE DONNÉES")
    print("-" * 30)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"   ✅ Connecté à: {version[0]}")
    except Exception as e:
        print(f"   ❌ Erreur connexion DB: {e}")
    
    # 3. Compter les enregistrements
    print("\n3. 📊 STATISTIQUES DONNÉES")
    print("-" * 25)
    print(f"   👥 Utilisateurs: {User.objects.count()}")
    print(f"   👤 Membres: {Membre.objects.count()}")
    print(f"   👥 Groupes: {Group.objects.count()}")
    print(f"   🔐 Permissions: {Permission.objects.count()}")
    
    # 4. Vérifier les agents
    print("\n4. 👤 AGENTS EXISTANTS")
    print("-" * 20)
    try:
        from agents.models import Agent
        agents = Agent.objects.all()
        print(f"   Total agents: {agents.count()}")
        for agent in agents[:5]:  # Afficher les 5 premiers
            print(f"   📍 {agent.user.username} - {agent.user.get_full_name()}")
    except Exception as e:
        print(f"   ⚠️  Agents: {e}")

if __name__ == "__main__":
    verifier_base_donnees()