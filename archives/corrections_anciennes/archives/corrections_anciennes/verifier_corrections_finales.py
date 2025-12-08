# verifier_corrections_finales.py
import os
import re

def verifier_corrections():
    print("🔍 VÉRIFICATION DES CORRECTIONS")
    print("=" * 50)
    
    problemes = []
    
    # Vérifier les fichiers pour les patterns problématiques
    fichiers = ['pharmacien/views.py', 'medecin/views.py', 'assureur/views.py', 'soins/views.py']
    
    for fichier in fichiers:
        if os.path.exists(fichier):
            with open(fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Vérifier les patterns problématiques
            if re.search(r'ordonnance\.medecin', contenu):
                problemes.append(f"{fichier}: contient 'ordonnance.medecin'")
            
            if re.search(r'\.filter\(medecin=', contenu):
                problemes.append(f"{fichier}: contient filtre sur 'medecin' dans Ordonnance")
            
            if re.search(r'date_emission', contenu):
                problemes.append(f"{fichier}: contient 'date_emission'")
    
    if problemes:
        print("🚨 PROBLÈMES DÉTECTÉS:")
        for probleme in problemes:
            print(f"  - {probleme}")
    else:
        print("✅ Aucun problème détecté!")

if __name__ == "__main__":
    verifier_corrections()