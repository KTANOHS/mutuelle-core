# ajouter_koffitanoh_agent_final.py
import os
import sys
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

django.setup()

from django.contrib.auth.models import User
from agents.models import Agent

def ajouter_koffitanoh_comme_agent():
    print("👤 AJOUT DE KOFFITANOH COMME AGENT (STRUCTURE CORRECTE)")
    print("=" * 60)
    
    try:
        # Récupérer l'utilisateur koffitanoh
        user = User.objects.get(username='koffitanoh')
        print(f"✅ Utilisateur trouvé: {user.username} (superutilisateur: {user.is_superuser})")
        
        # Vérifier s'il existe déjà comme agent
        try:
            agent_existant = Agent.objects.get(user=user)
            print(f"✅ Déjà agent: ID {agent_existant.id}")
            print(f"   - Matricule: {agent_existant.matricule}")
            print(f"   - Poste: {agent_existant.poste}")
            print(f"   - Actif: {agent_existant.est_actif}")
            return agent_existant
        except Agent.DoesNotExist:
            print("❌ koffitanoh n'est pas encore agent - Création en cours...")
            
            # Créer l'agent avec la structure correcte
            nouvel_agent = Agent.objects.create(
                user=user,
                matricule="AGENT-001",  # Champ REQUIS
                poste="Superviseur",    # Champ REQUIS  
                date_embauche=date.today(),  # Champ REQUIS
                est_actif=True,         # Champ REQUIS
                limite_bons_quotidienne=50,  # Champ REQUIS
                telephone="+225 07 00 00 00 00",  # Optionnel
                email_professionnel=user.email or "koffitanoh@example.com"  # Optionnel
            )
            
            print(f"✅ KOFFITANOH MAINTENANT AGENT!")
            print(f"   - ID Agent: {nouvel_agent.id}")
            print(f"   - Matricule: {nouvel_agent.matricule}")
            print(f"   - Poste: {nouvel_agent.poste}")
            print(f"   - Date embauche: {nouvel_agent.date_embauche}")
            print(f"   - Actif: {nouvel_agent.est_actif}")
            print(f"   - Limite bons: {nouvel_agent.limite_bons_quotidienne}")
            
            return nouvel_agent
            
    except User.DoesNotExist:
        print("❌ Utilisateur 'koffitanoh' non trouvé")
        return None
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return None

if __name__ == "__main__":
    agent = ajouter_koffitanoh_comme_agent()
    
    if agent:
        print("\n🎉 koffitanoh peut maintenant créer des bons de soin!")
        print("Testez avec: python test_permissions.py")
    else:
        print("\n❌ Échec de l'ajout")