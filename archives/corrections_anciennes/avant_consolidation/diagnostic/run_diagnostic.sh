#!/bin/bash
echo "🚀 Lancement du diagnostic communication..."
echo "=========================================="

# Activer l'environnement virtuel si nécessaire
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Environnement virtuel activé"
fi

# Exécuter le diagnostic
python diagnostic_communication.py

# Sauvegarder les résultats dans un fichier
python diagnostic_communication.py > diagnostic_results.txt
echo "📄 Résultats sauvegardés dans diagnostic_results.txt"

echo "✅ Diagnostic terminé !"
