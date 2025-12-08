# corriger_agents_urgence.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.db import connection

def corriger_agents():
    print("🚨 CORRECTION URGENTE DES AGENTS 🚨")
    print("="*50)
    
    try:
        from agents.models import Agent
        
        # 1. Vérifier/Créer le groupe AGENT (majuscules)
        print("\n1. 📋 GROUPES:")
        groupe_agent_maj, _ = Group.objects.get_or_create(name='AGENT')
        print(f"   ✅ Groupe AGENT (majuscules) créé/trouvé")
        
        groupe_agent_min, _ = Group.objects.get_or_create(name='Agent')
        print(f"   ✅ Groupe Agent (minuscule) existe aussi")
        
        # 2. Récupérer l'utilisateur ORNELLA
        print("\n2. 👤 UTILISATEUR ORNELLA:")
        try:
            user_ornella = User.objects.get(username='ORNELLA')
            print(f"   ✅ Utilisateur trouvé (ID: {user_ornella.id})")
            
            # S'assurer qu'il est dans le groupe AGENT (majuscules)
            if not user_ornella.groups.filter(name='AGENT').exists():
                user_ornella.groups.add(groupe_agent_maj)
                print("   ✅ ORNELLA ajoutée au groupe AGENT")
                
            # Vérifier les groupes actuels
            groupes = [g.name for g in user_ornella.groups.all()]
            print(f"   📋 Groupes actuels: {', '.join(groupes)}")
                
        except User.DoesNotExist:
            print("   ❌ Utilisateur ORNELLA non trouvé")
            return
        
        # 3. Créer l'agent pour ORNELLA
        print("\n3. 🏢 CRÉATION AGENT ORNELLA:")
        try:
            # Vérifier si l'agent existe déjà
            agent = Agent.objects.get(user=user_ornella)
            print(f"   ✅ Agent existe déjà (ID: {agent.pk})")
            print(f"   📊 Matricule: {agent.matricule}")
            print(f"   📊 Poste: {agent.poste}")
            print(f"   📊 Est actif: {agent.est_actif}")
            
        except Agent.DoesNotExist:
            print("   ⚠️ Agent non trouvé, création en cours...")
            
            # Créer l'agent avec les champs du modèle
            agent = Agent.objects.create(
                user=user_ornella,
                matricule='AG001',
                poste='Agent commercial',
                est_actif=True,
                limite_bons_quotidienne=10,
                telephone='',
                email_professionnel=''
            )
            print(f"   ✅ Agent créé avec succès!")
            print(f"   📋 ID: {agent.pk}")
            print(f"   📋 Matricule: {agent.matricule}")
            print(f"   📋 Poste: {agent.poste}")
        
        # 4. Vérifier la structure de la table
        print("\n4. 🗄️ STRUCTURE DE LA TABLE:")
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(agents_agent)")
            colonnes = cursor.fetchall()
            print(f"   📊 Nombre de colonnes: {len(colonnes)}")
            for col in colonnes[:5]:  # Afficher les 5 premières
                print(f"   - {col[1]} ({col[2]})")
        
        # 5. Statistiques finales
        print("\n5. 📈 STATISTIQUES FINALES:")
        print(f"   👥 Total agents: {Agent.objects.count()}")
        print(f"   👤 Agents actifs: {Agent.objects.filter(est_actif=True).count()}")
        
        print("\n✅ CORRECTION TERMINÉE AVEC SUCCÈS!")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    corriger_agents()