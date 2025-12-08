# recherche_manuelle.py
import re
from pathlib import Path

def rechercher_urls_problematiques():
    """Recherche manuelle des URLs problématiques"""
    projet_path = Path("/Users/koffitanohsoualiho/Documents/projet")
    
    print("🔍 RECHERCHE MANUELLE DES URLs PROBLÉMATIQUES")
    print("=" * 60)
    
    patterns = [
        r"creer_bon",
        r"/bons/creer/",
        r"creer-bon",
    ]
    
    fichiers_trouves = []
    
    # Rechercher dans tous les fichiers
    for fichier in projet_path.rglob('*'):
        if fichier.is_file() and fichier.suffix.lower() in ['.html', '.htm', '.py', '.txt']:
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                
                for pattern in patterns:
                    if re.search(pattern, contenu):
                        # Compter les occurrences
                        occurrences = len(re.findall(pattern, contenu))
                        fichiers_trouves.append((fichier, pattern, occurrences))
                        print(f"📄 {fichier}")
                        print(f"   Pattern: '{pattern}' -> {occurrences} occurrence(s)")
                        
                        # Afficher les lignes concernées
                        lignes = contenu.split('\n')
                        for i, ligne in enumerate(lignes, 1):
                            if re.search(pattern, ligne):
                                print(f"      Ligne {i}: {ligne.strip()}")
                        
                        print()
                        break
                        
            except Exception as e:
                continue
    
    return fichiers_trouves

if __name__ == "__main__":
    resultats = rechercher_urls_problematiques()
    print(f"🎯 TOTAL: {len(resultats)} fichier(s) avec URLs problématiques")