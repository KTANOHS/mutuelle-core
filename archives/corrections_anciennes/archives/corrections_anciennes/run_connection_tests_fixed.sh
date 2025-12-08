#!/bin/bash

echo "🔐 LANCEMENT DES TESTS DE CONNEXION UTILISATEURS - CORRIGÉ"
echo "========================================================"

# Active l'environnement virtuel
source venv/bin/activate

# Exécute les tests corrigés
python test_user_connections_fixed.py

echo ""
echo "========================================================"
echo "✅ TESTS TERMINÉS"
echo ""
echo "💡 Conseil: Vous pouvez maintenant tester manuellement avec les identifiants fournis"