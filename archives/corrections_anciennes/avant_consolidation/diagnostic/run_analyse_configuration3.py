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
    succes = executer_analyse()
    sys.exit(0 if succes else 1)