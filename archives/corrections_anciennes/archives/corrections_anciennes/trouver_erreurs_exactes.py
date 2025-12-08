# trouver_erreurs_exactes.py
import re

def trouver_erreurs_exactes():
    """Trouve les lignes exactes avec des erreurs dans soins/views.py"""
    
    with open('soins/views.py', 'r', encoding='utf-8') as f:
        lignes = f.readlines()
    
    print("🔍 RECHERCHE DES ERREURS EXACTES DANS SOINS/VIEWS.PY")
    print("=" * 50)
    
    problemes = []
    
    for numero, ligne in enumerate(lignes, 1):
        if re.search(r'\.filter\(medecin=', ligne):
            problemes.append((numero, "Filtre sur 'medecin'", ligne.strip()))
        
        if re.search(r'ordonnance\.medecin', ligne):
            problemes.append((numero, "Référence à 'ordonnance.medecin'", ligne.strip()))
        
        if re.search(r'date_emission', ligne):
            problemes.append((numero, "Champ 'date_emission'", ligne.strip()))
    
    if problemes:
        print("🚨 LIGNES PROBLÉMATIQUES TROUVÉES:")
        for numero, type_erreur, ligne in problemes:
            print(f"\nLigne {numero}: {type_erreur}")
            print(f"   → {ligne}")
    else:
        print("✅ Aucune erreur trouvée!")

if __name__ == "__main__":
    trouver_erreurs_exactes()