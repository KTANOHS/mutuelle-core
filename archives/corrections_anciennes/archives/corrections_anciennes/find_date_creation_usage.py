# find_date_creation_usage.py
import os
import re

def find_date_creation_usage():
    print("🔍 RECHERCHE DE 'date_creation' DANS LE CODE...")
    print("=" * 50)
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'date_creation' in content:
                            print(f"📁 {filepath}")
                            # Afficher les lignes concernées
                            lines = content.split('\n')
                            for i, line in enumerate(lines, 1):
                                if 'date_creation' in line:
                                    print(f"   Ligne {i}: {line.strip()}")
                except Exception as e:
                    print(f"❌ Erreur lecture {filepath}: {e}")

if __name__ == "__main__":
    find_date_creation_usage()