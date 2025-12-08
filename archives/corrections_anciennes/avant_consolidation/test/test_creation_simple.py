import os
import django
import sys
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("🧪 TEST CRÉATION SIMPLIFIÉ")
print("==========================")

# Utiliser l'import direct comme dans le shell
try:
    # Ces imports fonctionnent dans le shell, utilisons la même méthode
    from django.apps import apps
    
    # Récupérer les modèles
    Membre = apps.get_model('member', 'Membre')
    BonDeSoin = apps.get_model('bon_soin', 'BonDeSoin')
    Agent = apps.get_model('agents', 'Agent')
    
    print("✅ Modèles chargés avec succès")
    
    # Compter les données
    print(f"📊 Membres: {Membre.objects.count()}")
    print(f"📊 Agents: {Agent.objects.count()}")
    print(f"📊 Bons de soin: {BonDeSoin.objects.count()}")
    
    # Créer un nouveau bon de soin
    membre = Membre.objects.first()
    agent = Agent.objects.first()
    
    print(f"👤 Membre: {membre.nom} {membre.prenom}")
    print(f"👨‍💼 Agent: {agent.nom_complet}")
    
    # Créer le bon
    bon = BonDeSoin.objects.create(
        membre=membre,
        agent_createur=agent,
        type_soin="Consultation générale",
        montant_total=15000.0,
        montant_remboursable=12000.0,
        date_soin=datetime.now().date(),
        statut="EN_ATTENTE",
        description="Test de création manuelle"
    )
    
    print(f"✅ BON CRÉÉ: {bon.numero_bon}")
    print(f"   Montant: {bon.montant_total} FCFA")
    print(f"   Statut: {bon.statut}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()