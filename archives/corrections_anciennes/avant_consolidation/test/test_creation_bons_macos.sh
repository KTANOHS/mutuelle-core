#!/bin/bash
# scripts/test_creation_bons_macos.sh

echo "🧪 SCRIPT DE TEST macOS - CRÉATION BONS DE SOIN"
echo "================================================"

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

# Diagnostic des modèles
log_info "Diagnostic des modèles..."
python diagnostic_models.py

# Test des URLs
log_info "Test des URLs..."
python manage.py shell << 'EOF'
from django.urls import reverse, NoReverseMatch

urls_a_tester = [
    'agents:dashboard',
    'agents:creer_bon_soin',
    'agents:rechercher_membre',
    'agents:details_membre',
]

print("🔗 Test des URLs agents:")
for url_name in urls_a_tester:
    try:
        url = reverse(url_name)
        print(f"   ✅ {url_name} -> {url}")
    except NoReverseMatch as e:
        print(f"   ❌ {url_name} -> Non trouvée: {e}")

# Test données existantes
from django.contrib.auth.models import User
from agents.models import Agent, BonSoin
from membres.models import Membre

print("\n📊 Données existantes:")
print(f"   Utilisateurs: {User.objects.count()}")
print(f"   Agents: {Agent.objects.count()}")
print(f"   Membres: {Membre.objects.count()}")
print(f"   Bons de soin: {BonSoin.objects.count()}")

if Agent.objects.exists():
    agent = Agent.objects.first()
    print(f"\n👤 Premier agent: {agent.user.get_full_name()} ({agent.matricule})")
    
if Membre.objects.exists():
    membre = Membre.objects.first()
    print(f"👤 Premier membre: {membre.user.get_full_name()} ({membre.matricule})")
EOF

# Test création simple
log_info "Test création simple..."
python manage.py shell << 'EOF'
from django.contrib.auth.models import User
from agents.models import Agent, BonSoin
from membres.models import Membre

try:
    # Vérifier s'il y a des agents et membres
    if Agent.objects.count() > 0 and Membre.objects.count() > 0:
        agent = Agent.objects.first()
        membre = Membre.objects.first()
        
        print(f"🎯 Test avec agent: {agent.user.get_full_name()}")
        print(f"🎯 Test avec membre: {membre.user.get_full_name()}")
        
        # Vérifier si l'agent peut créer un bon
        peut_creer = agent.peut_creer_bon()
        print(f"📝 Agent peut créer un bon: {peut_creer}")
        
        # Compter les bons existants
        bons_count = BonSoin.objects.count()
        print(f"📦 Bons existants: {bons_count}")
        
    else:
        print("❌ Pas assez de données pour tester")
        
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
EOF

# Test API recherche
log_info "Test API recherche..."
python manage.py shell << 'EOF'
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

client = Client()

# Créer un utilisateur de test
user, created = User.objects.get_or_create(
    username='api_tester',
    defaults={'email': 'api@test.com'}
)
if created:
    user.set_password('test123')
    user.save()

client.force_login(user)

# Tester l'API de recherche
response = client.get(reverse('agents:rechercher_membre') + '?q=test')
print(f"🔍 API Recherche - Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"   Succès: {data.get('success', 'N/A')}")
    print(f"   Résultats: {len(data.get('results', []))}")
    print(f"   Erreur: {data.get('error', 'Aucune')}")
else:
    print(f"   ❌ Erreur HTTP: {response.status_code}")
EOF

echo ""
echo "🎯 PROCHAINES ÉTAPES:"
echo "===================="
echo "1. Démarrer le serveur: python manage.py runserver"
echo "2. Se connecter à: http://localhost:8000/agents/"
echo "3. Tester manuellement la création de bons"
echo ""
echo "🔧 CORRECTIONS NÉCESSAIRES:"
echo "==========================="
echo "- Vérifier le modèle Assureur (champ 'nom' manquant)"
echo "- Créer des données de test si nécessaire"
echo "- Tester avec un agent existant"

log_success "Diagnostic terminé"