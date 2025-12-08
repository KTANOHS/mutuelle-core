# verifier_urls_medecin.py
import os

def verifier_urls_medecin():
    """Vérifier le contenu actuel de medecin/urls.py"""
    print("CONTENU ACTUEL DE MEDECIN/URLS.PY")
    print("=" * 50)
    
    urls_path = 'medecin/urls.py'
    
    if os.path.exists(urls_path):
        with open(urls_path, 'r') as f:
            lignes = f.readlines()
        
        print("Lignes problématiques trouvées:")
        print("-" * 30)
        
        problemes = []
        for i, ligne in enumerate(lignes, 1):
            if 'views.,' in ligne or 'views.historique,' in ligne:
                problemes.append((i, ligne.strip()))
                print(f"Ligne {i}: {ligne.strip()}")
        
        if not problemes:
            print("✓ Aucun problème détecté")
        else:
            print(f"\n✗ {len(problemes)} problème(s) détecté(s)")
    else:
        print("✗ Fichier non trouvé")

if __name__ == "__main__":
    verifier_urls_medecin()