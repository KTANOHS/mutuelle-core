#!/bin/bash
# scripts/test_creation_bons_simple.sh

echo "🧪 SCRIPT DE TEST SIMPLIFIÉ - CRÉATION BONS DE SOIN"
echo "==================================================="

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️ $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️ $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# Vérification Django
log_info "Vérification environnement Django..."
python -c "import django; print('Django version:', django.get_version())" || {
    log_error "Django non configuré"
    exit 1
}
log_success "Environnement Django OK"

# Test des URLs de base
log_info "Test des URLs agents..."
python manage.py shell << EOF
from django.urls import reverse, NoReverseMatch

urls_a_tester = [
    'agents:dashboard',
    'agents:creer_bon_soin', 
    'agents:rechercher_membre',
]

for url_name in urls_a_tester:
    try:
        url = reverse(url_name)
        print(f"✅ {url_name} -> {url}")
    except NoReverseMatch as e:
        print(f"❌ {url_name} -> ERREUR: {e}")
EOF

# Test des modèles
log_info "Test des modèles..."
python manage.py shell << EOF
try:
    from agents.models import Agent, BonSoin
    from membres.models import Membre
    from django.contrib.auth.models import User
    
    print("✅ Modèles importés avec succès")
    
    # Test création données de test
    user_agent, created = User.objects.get_or_create(
        username='test_manual',
        defaults={'first_name': 'Test', 'last_name': 'Manual', 'email': 'test@manual.com'}
    )
    if created:
        user_agent.set_password('test123')
        user_agent.save()
        print("✅ Utilisateur de test créé")
    else:
        print("ℹ️ Utilisateur de test existe déjà")
        
    # Compter les agents
    nb_agents = Agent.objects.count()
    print(f"📊 Nombre d'agents en base: {nb_agents}")
    
    # Compter les membres  
    nb_membres = Membre.objects.count()
    print(f"📊 Nombre de membres en base: {nb_membres}")
    
    # Compter les bons
    nb_bons = BonSoin.objects.count()
    print(f"📊 Nombre de bons en base: {nb_bons}")
    
except Exception as e:
    print(f"❌ Erreur modèles: {e}")
EOF

# Test serveur de développement
log_info "Test du serveur de développement..."
timeout 5s python manage.py runserver --noreload 0.0.0.0:9999 &
SERVER_PID=$!
sleep 3

if ps -p $SERVER_PID > /dev/null; then
    log_success "Serveur Django démarre correctement"
    kill $SERVER_PID 2>/dev/null
else
    log_error "Le serveur Django ne démarre pas"
fi

# Test des vues avec requests
log_info "Test des vues avec client HTTP..."
python << EOF
import requests
import sys

base_url = "http://localhost:8000"
urls = [
    "/agents/",
    "/agents/creer-bon-soin/",
]

for url_path in urls:
    try:
        response = requests.get(f"{base_url}{url_path}", timeout=5)
        status = "✅" if response.status_code in [200, 302] else "❌"
        print(f"{status} {url_path} -> {response.status_code}")
    except Exception as e:
        print(f"❌ {url_path} -> Erreur: {e}")
EOF

# Test de création manuel
log_info "Test de création manuel de bon..."
python manage.py shell << EOF
from django.contrib.auth.models import User
from agents.models import Agent, BonSoin
from membres.models import Membre
from assureur.models import Assureur
from datetime import date

try:
    # Créer un assureur de test
    assureur, created = Assureur.objects.get_or_create(
        nom="Assureur Test Manuel",
        defaults={'code': 'TESTMANUEL', 'telephone': '0102030405'}
    )
    
    # Créer un agent de test
    user_agent, created = User.objects.get_or_create(
        username='agent_manuel',
        defaults={
            'first_name': 'Agent', 
            'last_name': 'Manuel',
            'email': 'agent@manuel.com'
        }
    )
    if created:
        user_agent.set_password('test123')
        user_agent.save()
    
    agent, created = Agent.objects.get_or_create(
        user=user_agent,
        defaults={
            'matricule': 'AGTMANUEL',
            'poste': 'Agent Manuel',
            'assureur': assureur,
            'date_embauche': date(2023, 1, 1)
        }
    )
    
    # Créer un membre de test
    user_membre, created = User.objects.get_or_create(
        username='membre_manuel',
        defaults={
            'first_name': 'Membre',
            'last_name': 'Manuel', 
            'email': 'membre@manuel.com'
        }
    )
    if created:
        user_membre.set_password('test123')
        user_membre.save()
    
    membre, created = Membre.objects.get_or_create(
        user=user_membre,
        defaults={
            'matricule': 'MEMMANUEL',
            'telephone': '0601020304',
            'assureur': assureur
        }
    )
    
    # Créer un bon de soin de test
    bon = BonSoin.objects.create(
        code="TESTMANUEL001",
        membre=membre,
        agent=agent,
        date_expiration=date(2024, 12, 31),
        montant_max=15000.00,
        motif_consultation="Test manuel de création",
        type_soin="consultation",
        statut='valide'
    )
    
    print(f"✅ Bon de soin créé avec succès:")
    print(f"   - Code: {bon.code}")
    print(f"   - Membre: {bon.membre.user.get_full_name()}")
    print(f"   - Agent: {bon.agent.user.get_full_name()}")
    print(f"   - Montant: {bon.montant_max} FCFA")
    print(f"   - Statut: {bon.get_statut_display()}")
    
except Exception as e:
    print(f"❌ Erreur lors de la création manuelle: {e}")
    import traceback
    traceback.print_exc()
EOF

echo ""
echo "🎯 SCÉNARIOS DE TEST À EXÉCUTER MANUELLEMENT:"
echo "=============================================="
echo "1.  Démarrer le serveur: python manage.py runserver"
echo "2.  Se connecter en tant qu'agent: http://localhost:8000/agents/"
echo "3.  Aller dans 'Créer un bon de soin'"
echo "4.  Rechercher un membre existant"
echo "5.  Remplir le formulaire et soumettre"
echo "6.  Vérifier la création dans l'historique"

echo ""
log_success "Tests terminés - Vérifiez les résultats ci-dessus"