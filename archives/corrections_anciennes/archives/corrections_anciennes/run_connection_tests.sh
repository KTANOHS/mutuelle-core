#!/bin/bash

echo "🔐 LANCEMENT DES TESTS DE CONNEXION UTILISATEURS"
echo "================================================"

# Active l'environnement virtuel
source venv/bin/activate

# Exécute les tests
python test_user_connections.py

echo ""
echo "================================================"
echo "✅ TESTS TERMINÉS"
echo ""
echo "💡 Conseil: Vous pouvez maintenant tester manuellement avec les identifiants fournis"