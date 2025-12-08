#!/bin/bash
# scripts/test_creation_bons.sh

echo "🧪 SCRIPT DE TEST MANUEL - CRÉATION BONS DE SOIN"
echo "================================================"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
log_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifier que Django est configuré
log_info "Vérification de l'environnement Django..."
python -c "import django; print('Django version:', django.get_version())" || {
    log_error "Django n'est pas correctement configuré"
    exit 1
}

log_success "Environnement Django vérifié"

# Lancer les tests automatiques
log_info "Lancement des tests automatiques..."
python manage.py test agents.tests.test_creation_bons || {
    log_error "Les tests automatiques ont échoué"
    exit 1
}

log_success "Tests automatiques terminés avec succès"

echo ""
echo "🔍 TESTS MANUELS - CRÉATION DE BONS DE SOIN"
echo "==========================================="

# URL de base
BASE_URL="http://localhost:8000"

log_info "1. Test d'accès sans authentification"
curl -s "$BASE_URL/agents/creer-bon-soin/" | grep -q "connexion" && log_success "Redirection vers login fonctionne" || log_error "Problème avec la redirection"

log_info "2. Test de création d'utilisateur de test"
python manage.py shell << EOF
from django.contrib.auth.models import User
from membres.models import Membre
from agents.models import Agent
from assureur.models import Assureur

# Créer un utilisateur agent
user_agent, created = User.objects.get_or_create(
    username='test_agent',
    defaults={
        'first_name': 'Test',
        'last_name': 'Agent',
        'email': 'test@agent.com',
        'is_staff': True
    }
)
if created:
    user_agent.set_password('test123')
    user_agent.save()
    print("✅ Utilisateur agent créé")
else:
    print("ℹ️ Utilisateur agent existe déjà")

# Créer un assureur
assureur, created = Assureur.objects.get_or_create(
    nom="Assureur Test",
    defaults={
        'code': 'TEST',
        'telephone': '0123456789',
        'email': 'test@assureur.com'
    }
)

# Créer l'agent
agent, created = Agent.objects.get_or_create(
    user=user_agent,
    defaults={
        'matricule': 'TESTAGT',
        'poste': 'Agent Test',
        'assureur': assureur,
        'date_embauche': '2023-01-01',
        'est_actif': True
    }
)

# Créer un membre
user_membre, created = User.objects.get_or_create(
    username='test_membre',
    defaults={
        'first_name': 'Jean',
        'last_name': 'Test',
        'email': 'jean@test.com'
    }
)
if created:
    user_membre.set_password('test123')
    user_membre.save()

membre, created = Membre.objects.get_or_create(
    user=user_membre,
    defaults={
        'matricule': 'TESTMEM',
        'telephone': '0612345678',
        'assureur': assureur,
        'est_actif': True
    }
)

print("✅ Configuration des données de test terminée")
print("👤 Agent: test_agent / test123")
print("👤 Membre: test_membre / test123")
EOF

log_info "3. Test de l'API de recherche"
curl -s "$BASE_URL/agents/rechercher-membre/?q=Jean" | python -m json.tool && log_success "API recherche fonctionnelle" || log_error "Problème avec l'API recherche"

log_info "4. Test de création de bon via API"
# Note: Vous devrez d'abord vous authentifier et récupérer le CSRF token
# Ceci est un exemple conceptuel

log_info "5. Vérification des statistiques"
python manage.py shell << EOF
from agents.models import BonSoin, Agent
from django.utils import timezone

today = timezone.now().date()
agent = Agent.objects.get(matricule='TESTAGT')
bons_aujourdhui = BonSoin.objects.filter(agent=agent, date_creation__date=today).count()

print(f"📊 Statistiques du jour:")
print(f"   - Agent: {agent.user.get_full_name()}")
print(f"   - Bons créés aujourd'hui: {bons_aujourdhui}")
print(f"   - Limite quotidienne: {agent.limite_bons_quotidienne}")
print(f"   - Peut créer un bon: {agent.peut_creer_bon()}")
EOF

echo ""
echo "🎯 SCÉNARIOS DE TEST À EXÉCUTER MANUELLEMENT"
echo "============================================"

echo "1.  Connexion en tant qu'agent (test_agent / test123)"
echo "2.  Accéder à: $BASE_URL/agents/creer-bon-soin/"
echo "3.  Rechercher un membre par nom 'Jean'"
echo "4.  Sélectionner le membre dans les résultats"
echo "5.  Remplir le formulaire de création de bon:"
echo "    - Type de soin: Consultation médicale"
echo "    - Montant: 15000"
echo "    - Symptômes: Fièvre et toux"
echo "    - Diagnostic: Infection respiratoire"
echo "6.  Soumettre le formulaire"
echo "7.  Vérifier la redirection vers la page de confirmation"
echo "8.  Vérifier que le bon apparaît dans l'historique"

echo ""
log_success "Script de test terminé"
echo "📝 Consultez les logs ci-dessus pour les résultats détaillés"