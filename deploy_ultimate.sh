#!/bin/bash
echo "🚀 DÉPLOIEMENT DE LA SOLUTION ULTIME"

echo "1. Vérification des fichiers..."
ls -la mutuelle_core/settings.py

echo -e "\n2. Ajout à git..."
git add .

echo -e "\n3. Commit..."
git commit -m "ULTIMATE FIX: CSRF configuration for Railway - $(date '+%Y-%m-%d %H:%M:%S')"

echo -e "\n4. Push sur Railway..."
echo "   Exécutez: git push railway main"
echo ""
echo "⏳ Attendez 2-3 minutes que Railway déploie"
echo ""
echo "5. Après déploiement, testez avec:"
echo "   python verify_ultimate_fix.py"
