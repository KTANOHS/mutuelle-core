# affecter_verifications_final_corrige.py
import os
import django
import random
from django.utils import timezone
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from agents.models import Agent, VerificationCotisation
from django.contrib.auth.models import User
from assureur.models import Assureur

def creer_agents_avec_structure_correcte():
    """Crée des agents avec la structure identifiée"""
    print("🆕 CRÉATION D'AGENTS AVEC STRUCTURE CORRECTE...")
    
    if Agent.objects.count() > 0:
        print("✅ Agents déjà existants")
        return True
    
    # Récupérer un assureur existant ou en créer un
    assureur = Assureur.objects.first()
    if not assureur:
        print("❌ Aucun assureur existant - création nécessaire")
        return False
    
    # Récupérer ou créer un rôle agent
    try:
        from agents.models import RoleAgent
        role_agent = RoleAgent.objects.first()
        if not role_agent:
            role_agent = RoleAgent.objects.create(nom="Agent Validation", permissions="verifier_cotisations")
    except:
        role_agent = None
    
    # Créer les users et agents
    agents_data = [
        {"username": "agent_validation1", "email": "agent1@system.com", "matricule": "AG001", "poste": "Agent Validation"},
        {"username": "agent_validation2", "email": "agent2@system.com", "matricule": "AG002", "poste": "Agent Validation"}, 
        {"username": "agent_validation3", "email": "agent3@system.com", "matricule": "AG003", "poste": "Agent Validation"},
    ]
    
    agents_crees = 0
    for data in agents_data:
        try:
            # Créer le user
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    'email': data["email"],
                    'is_staff': True,
                    'is_active': True
                }
            )
            
            # Créer l'agent avec tous les champs requis
            agent = Agent.objects.create(
                user=user,
                matricule=data["matricule"],
                poste=data["poste"],
                assureur=assureur,
                role=role_agent,
                date_embauche=date.today(),
                est_actif=True,
                limite_bons_quotidienne=20,
                telephone="+1234567890",
                email_professionnel=data["email"]
            )
            agents_crees += 1
            print(f"✅ Agent créé: {agent.matricule} - {agent.poste}")
            
        except Exception as e:
            print(f"❌ Erreur création agent {data['username']}: {e}")
    
    return agents_crees > 0

def affecter_verifications_completes():
    print("🔄 AFFECTATION COMPLÈTE DES VÉRIFICATIONS...")
    
    # 1. Créer les agents si nécessaire
    if not creer_agents_avec_structure_correcte():
        print("❌ Impossible de créer des agents")
        return
    
    # 2. Récupérer les agents actifs
    agents = list(Agent.objects.filter(est_actif=True))
    print(f"👨‍💼 Agents actifs disponibles: {len(agents)}")
    
    if not agents:
        print("❌ Aucun agent actif disponible")
        return
    
    # 3. Trouver les membres sans vérification
    membres_sans_verif = []
    for membre in Membre.objects.all():
        if not VerificationCotisation.objects.filter(membre=membre).exists():
            membres_sans_verif.append(membre)
    
    print(f"📊 {len(membres_sans_verif)} membres sans vérification")
    
    if not membres_sans_verif:
        print("✅ Tous les membres ont déjà une vérification!")
        return
    
    # 4. Créer les vérifications avec tous les champs
    verifications_creees = 0
    for membre in membres_sans_verif:
        agent = random.choice(agents)
        
        try:
            # Calculer des dates réalistes
            aujourd_hui = timezone.now()
            dernier_paiement = aujourd_hui - timedelta(days=random.randint(0, 30))
            prochaine_echeance = aujourd_hui + timedelta(days=random.randint(1, 90))
            
            # Créer la vérification complète
            verification = VerificationCotisation.objects.create(
                agent=agent,
                membre=membre,
                date_verification=None,  # Pas encore vérifié
                statut_cotisation='a_verifier',  # ou 'en_attente', 'valide'
                date_dernier_paiement=dernier_paiement.date(),
                montant_dernier_paiement=random.uniform(50, 200),
                prochaine_echeance=prochaine_echeance.date(),
                jours_retard=random.randint(0, 15),
                montant_dette=random.uniform(0, 100),
                observations="Assignation automatique - vérification requise",
                notifier_membre=False
            )
            verifications_creees += 1
            print(f"✅ Vérification {verifications_creees}: Membre {membre.id} → Agent {agent.matricule}")
            
        except Exception as e:
            print(f"❌ Erreur pour membre {membre.id}: {e}")
    
    print(f"\n🎯 RÉSULTAT FINAL: {verifications_creees} vérifications créées!")
    print(f"👥 Membres restants sans vérification: {len(membres_sans_verif) - verifications_creees}")

if __name__ == "__main__":
    affecter_verifications_completes()