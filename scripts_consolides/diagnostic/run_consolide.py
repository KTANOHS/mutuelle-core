"""
FICHIER CONSOLIDÉ: run
Catégorie: diagnostic
Fusion de 7 fichiers
Date de consolidation: 2025-12-06 13:55:44
"""

import sys
import os
from pathlib import Path

# =============================================================================
# FICHIERS D'ORIGINE CONSOLIDÉS
# =============================================================================

# ============================================================
# ORIGINE 1: run_diagnostic.sh (2025-12-02)
# ============================================================

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

# ============================================================
# ORIGINE 2: run_analyse_configuration3.py (2025-11-15)
# ============================================================

#!/usr/bin/env python3
# run_analyse_configuration2.py
import subprocess
import sys
import os

def executer_analyse():
    print("🚀 LANCEMENT DE L'ANALYSE DE CONFIGURATION...")
    print(f"📂 Répertoire: {os.getcwd()}")
    print("=" * 60)

    try:
        # Vérifier si le fichier d'analyse existe
        fichier_analyse = 'analyse_configuration_communication2.py'  # Assurez-vous que c'est le bon nom
        if not os.path.exists(fichier_analyse):
            print(f"❌ Fichier d'analyse non trouvé: {fichier_analyse}")
            return False

        # Exécuter l'analyse
        result = subprocess.run([
            sys.executable, fichier_analyse
        ], capture_output=True, text=True, cwd=os.getcwd())

        # Afficher la sortie standard
        if result.stdout:
            print(result.stdout)

        # Afficher les erreurs s'il y en a
        if result.stderr:
            print("=" * 60)
            print("ERREURS D'EXÉCUTION:")
            print("=" * 60)
            print(result.stderr)

        # Vérifier si l'analyse s'est bien passée
        if result.returncode == 0:
            print("✅ Analyse terminée avec succès")
        else:
            print(f"❌ Analyse terminée avec des erreurs (code: {result.returncode})")

        return result.returncode == 0

    except FileNotFoundError:
        print("❌ Erreur: Python ou le fichier d'analyse n'a pas été trouvé")
        return False
    except Exception as e:
        print(f"❌ Erreur d'exécution: {e}")
        return False

if __name__ == "__main__":
... (tronqué)

# ============================================================
# ORIGINE 3: run_analyse_configuration2.py (2025-11-15)
# ============================================================

#!/usr/bin/env python3
# run_analyse_configuration.py
import subprocess
import sys
import os

def executer_analyse():
    print("🚀 LANCEMENT DE L'ANALYSE DE CONFIGURATION...")
    print(f"📂 Répertoire: {os.getcwd()}")
    print("=" * 60)

    try:
        # Vérifier si le fichier d'analyse existe
        fichier_analyse = 'analyse_configuration_communication.py'
        if not os.path.exists(fichier_analyse):
            print(f"❌ Fichier d'analyse non trouvé: {fichier_analyse}")
            return False

        # Exécuter l'analyse
        result = subprocess.run([
            sys.executable, fichier_analyse
        ], capture_output=True, text=True, cwd=os.getcwd())

        # Afficher la sortie standard
        if result.stdout:
            print(result.stdout)

        # Afficher les erreurs s'il y en a
        if result.stderr:
            print("=" * 60)
            print("ERREURS D'EXÉCUTION:")
            print("=" * 60)
            print(result.stderr)

        # Vérifier si l'analyse s'est bien passée
        if result.returncode == 0:
            print("✅ Analyse terminée avec succès")
        else:
            print(f"❌ Analyse terminée avec des erreurs (code: {result.returncode})")

        return result.returncode == 0

    except FileNotFoundError:
        print("❌ Erreur: Python ou le fichier d'analyse n'a pas été trouvé")
        return False
    except Exception as e:
        print(f"❌ Erreur d'exécution: {e}")
        return False

if __name__ == "__main__":
... (tronqué)

# ============================================================
# ORIGINE 4: run_analyse_configuration1.py (2025-11-15)
# ============================================================

# run_analyse_configuration.py
#!/usr/bin/env python3
import subprocess
import sys
import os

def executer_analyse():
    print("🚀 LANCEMENT DE L'ANALYSE DE CONFIGURATION...")
    print(f"📂 Répertoire: {os.getcwd()}")

    try:
        result = subprocess.run([
            sys.executable, 'analyse_configuration_communication.py'
        ], capture_output=True, text=True, cwd=os.getcwd())

        print("=" * 60)
        print("RÉSULTAT DE L'ANALYSE:")
        print("=" * 60)
        print(result.stdout)

        if result.stderr:
            print("=" * 60)
            print("ERREURS:")
            print("=" * 60)
            print(result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Erreur d'exécution: {e}")
        return False

if __name__ == "__main__":
    succes = executer_analyse()
    sys.exit(0 if succes else 1)

# ============================================================
# ORIGINE 5: run_analyse_communication.py (2025-11-15)
# ============================================================

# run_analyse_communication.py
#!/usr/bin/env python3
import subprocess
import sys
import os

def executer_analyse():
    print("🚀 LANCEMENT DE L'ANALYSE DE COMMUNICATION...")
    print(f"📂 Répertoire: {os.getcwd()}")

    try:
        result = subprocess.run([
            sys.executable, 'analyse_communication.py'
        ], capture_output=True, text=True, cwd=os.getcwd())

        print("=" * 60)
        print("RÉSULTAT DE L'ANALYSE:")
        print("=" * 60)
        print(result.stdout)

        if result.stderr:
            print("=" * 60)
            print("ERREURS:")
            print("=" * 60)
            print(result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Erreur d'exécution: {e}")
        return False

if __name__ == "__main__":
    succes = executer_analyse()
    sys.exit(0 if succes else 1)

# ============================================================
# ORIGINE 6: run_diagnostic_complet.py (2025-11-15)
# ============================================================

# run_diagnostic_complet.py
#!/usr/bin/env python3
import subprocess
import sys
import os

def executer_diagnostic():
    print("🚀 LANCEMENT DU DIAGNOSTIC COMPLET...")
    print(f"📂 Répertoire: {os.getcwd()}")

    try:
        result = subprocess.run([
            sys.executable, 'diagnostic_final_complet.py'
        ], capture_output=True, text=True, cwd=os.getcwd())

        print("=" * 60)
        print("SORTIE DU DIAGNOSTIC:")
        print("=" * 60)
        print(result.stdout)

        if result.stderr:
            print("=" * 60)
            print("ERREURS D'EXÉCUTION:")
            print("=" * 60)
            print(result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Erreur d'exécution: {e}")
        return False

if __name__ == "__main__":
    succes = executer_diagnostic()
    sys.exit(0 if succes else 1)

# ============================================================
# ORIGINE 7: run_diagnostic.py (2025-11-15)
# ============================================================

# run_diagnostic.py
#!/usr/bin/env python3
"""
Script simplifié pour exécuter le diagnostic
"""

import subprocess
import sys

def run_diagnostic():
    print("🚀 Exécution du diagnostic des interactions...")

    try:
        # Exécuter le script de diagnostic
        result = subprocess.run([
            sys.executable, 'diagnostic_interactions.py'
        ], capture_output=True, text=True)

        print(result.stdout)

        if result.stderr:
            print("Erreurs:", result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        return False

if __name__ == "__main__":
    success = run_diagnostic()
    sys.exit(0 if success else 1)

