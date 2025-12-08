import os
import django
import sys
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("🧪 TEST CRÉATION CORRIGÉ")
print("========================")

try:
    # IMPORTS CORRIGÉS
    from membres.models import Membre
    from soins.models import BonDeSoin
    from agents.models import Agent
    
    print("✅ Modèles chargés avec succès")
    
    # Compter les données
    print(f"📊 Membres: {Membre.objects.count()}")
    print(f"📊 Agents: {Agent.objects.count()}")
    print(f"📊 Bons de soin: {BonDeSoin.objects.count()}")
    
    # Sélectionner un membre et un agent
    membre = Membre.objects.first()
    agent = Agent.objects.first()
    
    print(f"👤 Membre: {membre.nom} {membre.prenom} (ID: {membre.id})")
    print(f"👨‍💼 Agent: {agent.matricule} - {agent}")
    
    # Vérifier les champs disponibles pour BonDeSoin
    print(f"\n🔍 CHAMPS BonDeSoin:")
    bon_exemple = BonDeSoin.objects.first()
    if bon_exemple:
        for field in bon_exemple._meta.fields:
            print(f"  - {field.name}")
    
    # Créer un nouveau bon de soin
    print(f"\n🔄 CRÉATION D'UN NOUVEAU BON...")
    
    bon = BonDeSoin.objects.create(
        membre=membre,
        agent_createur=agent,
        type_soin="Consultation générale",
        montant_total=15000.0,
        montant_remboursable=12000.0,
        date_soin=datetime.now().date(),
        statut="EN_ATTENTE",
        description="Test de création via script corrigé"
    )
    
    print(f"✅ BON DE SOIN CRÉÉ AVEC SUCCÈS!")
    print(f"   Numéro: {bon.numero_bon}")
    print(f"   Membre: {bon.membre.nom_complet}")
    print(f"   Agent: {bon.agent_createur}")
    print(f"   Montant: {bon.montant_total} FCFA")
    print(f"   Statut: {bon.statut}")
    
    # Vérification finale
    print(f"\n📊 VÉRIFICATION FINALE:")
    print(f"   Bons de soin en base: {BonDeSoin.objects.count()}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()