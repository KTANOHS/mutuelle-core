#!/bin/bash
# scripts/lancement_test_corrige.sh

echo "🚀 LANCEMENT DES TESTS CORRIGÉS - CRÉATION BONS DE SOIN"
echo "======================================================"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}Étape 1: Détection du projet...${NC}"
python detect_project.py

echo -e "\n${BLUE}Étape 2: Correction des données existantes...${NC}"
python scripts/correction_donnees_corrige.py

echo -e "\n${BLUE}Étape 3: Test fonctionnel complet...${NC}"
python scripts/test_fonctionnel_bons_corrige.py

echo -e "\n${BLUE}Étape 4: Test unitaire Django...${NC}"
python manage.py test agents.tests.test_creation_bons

echo -e "\n${BLUE}Étape 5: Vérification finale...${NC}"
python manage.py shell << 'EOF'
from agents.models import BonSoin, Agent
from membres.models import Membre

print("📊 STATISTIQUES FINALES:")
print(f"   Agents: {Agent.objects.count()}")
print(f"   Membres: {Membre.objects.count()}") 
print(f"   Bons de soin: {BonSoin.objects.count()}")

if BonSoin.objects.exists():
    bon = BonSoin.objects.latest('date_creation')
    print(f"\n🎉 DERNIER BON CRÉÉ:")
    print(f"   Code: {bon.code}")
    print(f"   Membre: {getattr(bon.membre, 'prenom', 'N/A')} {getattr(bon.membre, 'nom', 'N/A')}")
    print(f"   Agent: {bon.agent.user.get_full_name()}")
    print(f"   Montant: {bon.montant_max} FCFA")
    print(f"   Statut: {bon.get_statut_display()}")
else:
    print("\n⚠️  AUCUN BON DE SOIN CRÉÉ")
    print("   Causes possibles:")
    print("   - Données de test manquantes")
    print("   - Problème de permissions")
    print("   - Erreur dans le processus de création")
EOF

echo -e "\n${GREEN}✅ TOUS LES TESTS SONT TERMINÉS${NC}"
echo ""
echo -e "${YELLOW}🎯 POUR TESTER MANUELLEMENT:${NC}"
echo "   python manage.py runserver"
echo "   http://localhost:8000/agents/creer-bon-soin/"
echo ""
echo -e "${YELLOW}🔧 SI DES PROBLÈMES PERSISTENT:${NC}"
echo "   1. Vérifiez que vous avez exécuté: python scripts/correction_donnees_corrige.py"
echo "   2. Assurez-vous qu'un agent et des membres existent"
echo "   3. Vérifiez les logs Django pour les erreurs"