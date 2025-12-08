#!/usr/bin/env python
import os
import re

def trouver_references_message_interne():
    """Trouver toutes les références à Message dans le projet"""
    print("🔍 RECHERCHE DES RÉFÉRENCES À Message")
    print("=" * 60)
    
 fichiers_trouves = []
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if 'Message' in content:
                            fichiers_trouves.append(filepath)
                            print(f"❌ {filepath}")
                except Exception as e:
                    pass
    
    if fichiers_trouves:
        print(f"\n📊 {len(fichiers_trouves)} fichiers contiennent 'Message'")
        print("\n🚨 FICHIERS À CORRIGER :")
        for fichier in fichiers_trouves:
            print(f"   - {fichier}")
    else:
        print("✅ Aucune référence à 'Message' trouvée !")
    
    print("=" * 60)

if __name__ == "__main__":
    trouver_references_message_interne()