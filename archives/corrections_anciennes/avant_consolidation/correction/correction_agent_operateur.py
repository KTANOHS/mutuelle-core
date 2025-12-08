import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User
from agents.models import Agent
from assureur.models import Assureur

def corriger_agent_operateur():
    """Corriger l'association de l'utilisateur agent_operateur avec un Agent"""
    print("🔧 CORRECTION AGENT OPERATEUR")
    print("=============================")
    
    try:
        # 1. Récupérer l'utilisateur
        user = User.objects.get(username='agent_operateur')
        print(f"👤 Utilisateur trouvé: {user.username}")
        
        # 2. Vérifier s'il a déjà un agent
        try:
            agent_existant = Agent.objects.get(user=user)
            print(f"✅ Agent déjà associé: {agent_existant}")
            return True
        except Agent.DoesNotExist:
            print("⚠️  Aucun agent associé - création en cours...")
        
        # 3. Récupérer un assureur pour l'agent
        try:
            assureur = Assureur.objects.first()
            print(f"🏥 Assureur utilisé: {assureur}")
        except:
            assureur = None
            print("⚠️  Aucun assureur trouvé")
        
        # 4. Créer l'agent
        agent = Agent.objects.create(
            user=user,
            matricule="AGENT-OPERATEUR",
            poste="Agent opérateur",
            assureur=assureur,
            date_embauche="2025-01-01",
            est_actif=True,
            limite_bons_quotidienne=100,
            telephone="+225 01 02 03 04 05",
            email_professionnel="agent_operateur@mutuelle.ci"
        )
        
        print(f"✅ AGENT CRÉÉ AVEC SUCCÈS!")
        print(f"   Matricule: {agent.matricule}")
        print(f"   Poste: {agent.poste}")
        print(f"   Est actif: {agent.est_actif}")
        
        return True
        
    except User.DoesNotExist:
        print("❌ Utilisateur 'agent_operateur' non trouvé")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = corriger_agent_operateur()
    
    if success:
        print("\n🎉 AGENT OPERATEUR CORRIGÉ!")
        print("🔁 Redémarrez le serveur pour appliquer les changements")
    else:
        print("\n⚠️  CORRECTION ÉCHOUÉE")