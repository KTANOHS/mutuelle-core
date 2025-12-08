#!/bin/bash
# automation_surveillance_macos.sh
# Script d'automatisation pour macOS - Surveillance Mutuelle Core

SCRIPT_DIR="/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/projet 21.49.30"
VENV_PYTHON="/Users/koffitanohsoualiho/Documents/projet/venv/bin/python"
LOG_DIR="/tmp/mutuelle_logs"

mkdir -p "$LOG_DIR"

echo "🤖 Démarrage automatique surveillance - $(date)"

# Surveillance quotidienne (8h00)
if [ "$1" = "quotidien" ] || [ -z "$1" ]; then
    echo "🔍 Surveillance quotidienne..."
    "$VENV_PYTHON" "$SCRIPT_DIR/surveillance_simple.py" --mode auto >> "$LOG_DIR/surveillance_quotidienne.log" 2>&1
fi

# Diagnostic hebdomadaire (lundi 9h00)
if [ "$1" = "hebdomadaire" ] || [ -z "$1" ]; then
    echo "📊 Diagnostic hebdomadaire..."
    "$VENV_PYTHON" "$SCRIPT_DIR/surveillance_hebdomadaire.py" >> "$LOG_DIR/diagnostic_hebdo.log" 2>&1
fi

# Rapport mensuel (1er du mois)
if [ "$1" = "mensuel" ] || [ -z "$1" ]; then
    echo "📈 Rapport mensuel..."
    "$VENV_PYTHON" "$SCRIPT_DIR/rapport_performance_mensuel.py" >> "$LOG_DIR/rapport_mensuel.log" 2>&1
fi

echo "✅ Automatisation terminée - $(date)"
