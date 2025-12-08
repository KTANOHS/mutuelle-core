# scripts/correction_donnees.py
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User
from agents.models import Agent
from membres.models import Membre
from assureur.models import Assureur

def corriger_donnees():
    print("🔧 CORRECTION DES DONNÉES EXISTANTES")
    print("=" * 50)
    
    # 1. Corriger les utilisateurs sans noms
    users_sans_nom = User.objects.filter(first_name='', last_name='')
    print(f"👥 Utilisateurs sans nom: {users_sans_nom.count()}")
    
    for user in users_sans_nom:
        if 'agent' in user.username.lower():
            user.first_name = 'Agent'
            user.last_name = user.username.replace('agent', '').title()
        elif 'membre' in user.username.lower():
            user.first_name = 'Membre'
            user.last_name = user.username.replace('membre', '').title()
        else:
            user.first_name = 'Utilisateur'
            user.last_name = user.username.title()
        user.save()
        print(f"✅ {user.username} -> {user.get_full_name()}")
    
    # 2. Vérifier les agents
    agents = Agent.objects.all()
    print(f"\n🎯 Agents: {agents.count()}")
    for agent in agents:
        print(f"   - {agent.user.get_full_name()} ({agent.matricule})")
    
    # 3. Vérifier les membres
    membres = Membre.objects.all()
    print(f"\n👤 Membres: {membres.count()}")
    for membre in membres:
        nom_complet = f"{membre.prenom} {membre.nom}" if membre.prenom and membre.nom else membre.user.get_full_name()
        print(f"   - {nom_complet} ({membre.numero_unique})")
    
    # 4. Créer des données de test si nécessaire
    if membres.count() == 0:
        print("\n📝 Création de données de test...")
        creer_donnees_test()
    
    print("\n✅ Correction des données terminée")

def creer_donnees_test():
    """Créer des données de test pour les membres"""
    from datetime import date, timedelta
    
    # Créer des membres de test
    membres_test = [
        {'prenom': 'Jean', 'nom': 'Dupont', 'telephone': '0612345678'},
        {'prenom': 'Marie', 'nom': 'Martin', 'telephone': '0623456789'},
        {'prenom': 'Pierre', 'nom': 'Durand', 'telephone': '0634567890'},
        {'prenom': 'Sophie', 'nom': 'Leroy', 'telephone': '0645678901'},
    ]
    
    for i, data in enumerate(membres_test, 1):
        # Créer l'utilisateur
        user, created = User.objects.get_or_create(
            username=f"membre_test_{i}",
            defaults={
                'first_name': data['prenom'],
                'last_name': data['nom'],
                'email': f"{data['prenom'].lower()}.{data['nom'].lower()}@test.com"
            }
        )
        if created:
            user.set_password('test123')
            user.save()
        
        # Créer le membre
        membre, created = Membre.objects.get_or_create(
            user=user,
            defaults={
                'numero_unique': f"MEM{i:03d}",
                'prenom': data['prenom'],
                'nom': data['nom'],
                'telephone': data['telephone'],
                'date_naissance': date(1990, 1, 1),
                'adresse': f"{i} Rue de Test, Paris",
                'statut': 'actif'
            }
        )
        
        if created:
            print(f"✅ Membre créé: {membre.prenom} {membre.nom} ({membre.numero_unique})")

if __name__ == "__main__":
    corriger_donnees()