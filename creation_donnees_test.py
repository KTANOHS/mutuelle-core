# creation_donnees_test.py
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from membres.models import Membre
from soins.models import BonDeSoin
from medecin.models import Ordonnance
from agents.models import Agent

def creer_donnees_test():
    print("🧪 CRÉATION DES DONNÉES DE TEST...")
    
    # Récupérer les groupes
    try:
        groupe_medecins = Group.objects.get(name='Médecins')
        groupe_agents = Group.objects.get(name='Agents')
    except Group.DoesNotExist:
        print("❌ Groupes non trouvés")
        return
    
    # Créer un médecin de test
    medecin_user, created = User.objects.get_or_create(
        username='dr_test',
        defaults={'email': 'dr@test.com', 'first_name': 'Docteur', 'last_name': 'Test'}
    )
    if created:
        medecin_user.set_password('test123')
        medecin_user.save()
        medecin_user.groups.add(groupe_medecins)
    
    # Créer un agent de test
    agent_user, created = User.objects.get_or_create(
        username='agent_complet',
        defaults={'email': 'agent@test.com', 'first_name': 'Agent', 'last_name': 'Complet'}
    )
    if created:
        agent_user.set_password('test123')
        agent_user.save()
        agent_user.groups.add(groupe_agents)
        
        # Créer le profil Agent
        Agent.objects.create(
            user=agent_user,
            numero_agent='AGT0001',
            actif=True
        )
    
    # Créer quelques bons de soin
    membre_test = Membre.objects.first()
    if membre_test:
        bon = BonDeSoin.objects.create(
            numero_bon='BS001',
            membre=membre_test,
            medecin_prescripteur="Dr. Test",
            date_prescription=datetime.now().date(),
            description="Consultation de test"
        )
        print(f"✅ Bon de soin créé: {bon.numero_bon}")
    
    # Créer une ordonnance
    ordonnance = Ordonnance.objects.create(
        numero_ordonnance='ORD001',
        medecin_prescripteur="Dr. Test", 
        patient=membre_test,
        date_prescription=datetime.now().date(),
        medicaments="Paracétamol 500mg - 1 comprimé 3 fois par jour"
    )
    print(f"✅ Ordonnance créée: {ordonnance.numero_ordonnance}")
    
    print("✅ DONNÉES DE TEST CRÉÉES AVEC SUCCÈS")

if __name__ == "__main__":
    creer_donnees_test()