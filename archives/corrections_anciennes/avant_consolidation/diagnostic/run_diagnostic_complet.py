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