# scripts/correction_donnees_corrige.py
import os
import django
import sys

# Détection automatique du projet
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)

# Chercher le projet
project_name = None
for item in os.listdir(current_dir):
    if os.path.isdir(os.path.join(current_dir, item)) and 'settings.py' in os.listdir(os.path.join(current_dir, item)):
        project_name = item
        break

if project_name:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
    print(f"🎯 Configuration avec projet: {project_name}")
else:
    print("❌ Impossible de détecter le projet Django")
    sys.exit(1)

django.setup()

from django.contrib.auth.models import User
from agents.models import Agent
from membres.models import Membre
from assureur.models import Assureur

def corriger_donnees():
    print("🔧 CORRECTION DES DONNÉES EXISTANTES")
    print("=" * 50)
    
    # 1. Vérifier les agents
    agents = Agent.objects.all()
    print(f"🎯 Agents trouvés: {agents.count()}")
    
    for agent in agents:
        nom_complet = agent.user.get_full_name()
        if not nom_complet.strip():
            agent.user.first_name = "Agent"
            agent.user.last_name = agent.matricule
            agent.user.save()
            print(f"✅ Agent corrigé: {agent.user.get_full_name()}")

    # 2. Vérifier les membres
    membres = Membre.objects.all()
    print(f"👤 Membres trouvés: {membres.count()}")
    
    for membre in membres:
        if not membre.prenom or not membre.nom:
            if hasattr(membre, 'user'):
                if not membre.prenom:
                    membre.prenom = membre.user.first_name or "Prénom"
                if not membre.nom:
                    membre.nom = membre.user.last_name or "Nom"
                membre.save()
                print(f"✅ Membre corrigé: {membre.prenom} {membre.nom}")

    # 3. Créer des données de test si nécessaire
    if membres.count() < 3:
        creer_donnees_test()
    
    print("\n✅ Correction des données terminée")

def creer_donnees_test():
    """Créer des données de test"""
    from datetime import date
    
    print("📝 Création de données de test...")
    
    # Créer un assureur de test si nécessaire
    assureur, created = Assureur.objects.get_or_create(
        numero_employe="ASSURTEST",
        defaults={
            'user': User.objects.create_user('assureur_test', 'assureur@test.com', 'test123',
                                           first_name="Assureur", last_name="Test"),
            'departement': "Test",
            'date_embauche': date.today()
        }
    )
    
    # Créer des membres de test
    membres_test = [
        {'prenom': 'Jean', 'nom': 'Dupont', 'telephone': '0612345678', 'numero_unique': 'MEM001'},
        {'prenom': 'Marie', 'nom': 'Martin', 'telephone': '0623456789', 'numero_unique': 'MEM002'},
        {'prenom': 'Pierre', 'nom': 'Durand', 'telephone': '0634567890', 'numero_unique': 'MEM003'},
    ]
    
    for data in membres_test:
        user, created = User.objects.get_or_create(
            username=f"{data['prenom'].lower()}.{data['nom'].lower()}",
            defaults={
                'first_name': data['prenom'],
                'last_name': data['nom'],
                'email': f"{data['prenom'].lower()}.{data['nom'].lower()}@test.com"
            }
        )
        if created:
            user.set_password('test123')
            user.save()
        
        membre, created = Membre.objects.get_or_create(
            user=user,
            defaults={
                'numero_unique': data['numero_unique'],
                'prenom': data['prenom'],
                'nom': data['nom'],
                'telephone': data['telephone'],
                'date_naissance': date(1990, 1, 1),
                'adresse': "123 Rue de Test",
                'statut': 'actif'
            }
        )
        
        if created:
            print(f"✅ Membre créé: {membre.prenom} {membre.nom}")

if __name__ == "__main__":
    corriger_donnees()