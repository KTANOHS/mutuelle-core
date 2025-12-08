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