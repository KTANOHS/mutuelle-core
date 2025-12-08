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