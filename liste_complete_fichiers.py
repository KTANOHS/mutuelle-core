# liste_complete_fichiers.py
import os
from pathlib import Path

def list_all_files(start_path):
    """Liste récursivement tous les fichiers"""
    for root, dirs, files in os.walk(start_path):
        level = root.replace(str(start_path), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}📁 {os.path.basename(root)}/")
        
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if not file.startswith('.') and not file.endswith('.pyc'):
                print(f"{subindent}📄 {file}")

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    print("📂 STRUCTURE COMPLÈTE DU PROJET")
    list_all_files(BASE_DIR)