#!/bin/bash
# scripts/lancement_test_final.sh

echo "🚀 LANCEMENT DES TESTS FINAUX - CRÉATION BONS DE SOIN"
echo "===================================================="

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Étape 1: Correction des données existantes...${NC}"
python scripts/correction_donnees.py

echo -e "\n${BLUE}Étape 2: Test fonctionnel complet...${NC}"
python scripts/test_fonctionnel_bons.py

echo -e "\n${BLUE}Étape 3: Test unitaire Django...${NC}"
python manage.py test agents.tests.test_creation_bons

echo -e "\n${BLUE}Étape 4: Vérification finale...${NC}"
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
    print(f"   Membre: {bon.membre.prenom} {bon.membre.nom}")
    print(f"   Montant: {bon.montant_max} FCFA")
    print(f"   Statut: {bon.get_statut_display()}")
else:
    print("\n⚠️  AUCUN BON DE SOIN CRÉÉ")
    print("   Le système nécessite des données de test valides")
EOF

echo -e "\n${GREEN}✅ TOUS LES TESTS SONT TERMINÉS${NC}"
echo ""
echo "🎯 POUR TESTER MANUELLEMENT:"
echo "   python manage.py runserver"
echo "   http://localhost:8000/agents/creer-bon-soin/"
echo ""
echo "🔧 SI DES PROBLÈMES PERSISTENT:"
echo "   1. Vérifier que vous avez des membres dans la base"
echo "   2. Vérifier qu'un agent est connecté"
echo "   3. Tester avec différents termes de recherche"