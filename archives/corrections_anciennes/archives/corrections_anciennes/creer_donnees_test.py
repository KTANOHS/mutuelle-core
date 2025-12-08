# creer_donnees_test.py
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from membres.models import Membre, Cotisation  # Adaptez selon vos modèles
from agents.models import Agent

def creer_donnees_test():
    print("🎲 CRÉATION DONNÉES DE TEST")
    print("===========================")
    
    User = get_user_model()
    
    # Créer quelques membres de test
    membres_data = [
        {
            'numero_secu': '123456789012345',
            'nom': 'Dupont',
            'prenom': 'Marie',
            'date_naissance': timezone.now().date().replace(year=1985),
            'adresse': '123 Rue Test, Ville',
            'telephone': '+2250100000001',
            'est_actif': True
        },
        {
            'numero_secu': '123456789012346', 
            'nom': 'Martin',
            'prenom': 'Pierre',
            'date_naissance': timezone.now().date().replace(year=1978),
            'adresse': '456 Avenue Test, Ville',
            'telephone': '+2250100000002',
            'est_actif': True
        }
    ]
    
    for data in membres_data:
        membre, created = Membre.objects.get_or_create(
            numero_secu=data['numero_secu'],
            defaults=data
        )
        if created:
            print(f"✅ Membre créé: {membre.prenom} {membre.nom}")
        else:
            print(f"ℹ️  Membre existe déjà: {membre.prenom} {membre.nom}")
    
    print(f"📊 Total membres: {Membre.objects.count()}")
    
    # Vérifier l'agent
    agent = Agent.objects.filter(user__username='agent_test').first()
    if agent:
        print(f"👨‍⚕️ Agent de test: {agent.user.get_full_name()} ({agent.matricule})")
    
    print("\n🎯 DONNÉES DE TEST PRÊTES !")

if __name__ == "__main__":
    creer_donnees_test()