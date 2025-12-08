# verifier_agent_structure.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Agent

def analyser_structure_agent():
    print("🔍 ANALYSE COMPLÈTE DU MODÈLE AGENT")
    print("=" * 60)
    
    agents = Agent.objects.all()
    print(f"Nombre total d'agents: {agents.count()}")
    
    if agents.exists():
        print("\n📋 DÉTAIL DES AGENTS:")
        for agent in agents:
            print(f"\n👨‍💼 Agent ID: {agent.id}")
            
            # Attributs de base
            print(f"   - Type: {type(agent)}")
            print(f"   - PK: {agent.pk}")
            
            # Vérifier tous les attributs non privés
            attributs = [attr for attr in dir(agent) if not attr.startswith('_')]
            print(f"   - Attributs disponibles ({len(attributs)}):")
            
            # Afficher les attributs importants
            for attr in ['id', 'user', 'nom', 'prenom', 'assureur', 'email', 'telephone']:
                if hasattr(agent, attr):
                    value = getattr(agent, attr)
                    print(f"      * {attr}: {value}")
                else:
                    print(f"      * {attr}: ❌ NON DISPONIBLE")
            
            # Vérifier les méthodes spéciales
            if hasattr(agent, '__str__'):
                print(f"   - __str__: {str(agent)}")
            
            # Vérifier les relations
            if hasattr(agent, 'user') and agent.user:
                print(f"   - User associé: {agent.user.username} ({agent.user.get_full_name()})")
            
            if hasattr(agent, 'assureur') and agent.assureur:
                print(f"   - Assureur: {agent.assureur.nom}")
            else:
                print(f"   - Assureur: ❌ NON ASSOCIÉ")
    
    else:
        print("❌ Aucun agent trouvé dans la base de données")

def verifier_relations_agent():
    print("\n🔗 VÉRIFICATION DES RELATIONS AGENT")
    print("=" * 60)
    
    try:
        from django.db import models
        agent_model = Agent
        
        print("📋 Relations du modèle Agent:")
        for field in agent_model._meta.get_fields():
            if field.is_relation:
                print(f"   - {field.name}: {field.related_model.__name__} ({field.get_internal_type()})")
                
    except Exception as e:
        print(f"❌ Erreur analyse relations: {e}")

def suggestions_correction():
    print("\n💡 SUGGESTIONS DE CORRECTION")
    print("=" * 60)
    
    suggestions = [
        "1. Vérifier si le modèle Agent a un champ 'nom'",
        "2. Si non, utiliser user.first_name et user.last_name",
        "3. Ou ajouter les champs manquants au modèle Agent",
        "4. Créer une propriété @property pour le nom complet",
        "5. Mettre à jour les vues pour utiliser les bons attributs"
    ]
    
    for suggestion in suggestions:
        print(f"• {suggestion}")

if __name__ == "__main__":
    analyser_structure_agent()
    verifier_relations_agent()
    suggestions_correction()