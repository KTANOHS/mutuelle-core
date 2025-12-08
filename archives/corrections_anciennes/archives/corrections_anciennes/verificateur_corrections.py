# verificateur_corrections.py
import os
import re
from pathlib import Path

def verifier_fichiers(projet_path):
    """Vérifie que les corrections ont été appliquées"""
    projet = Path(projet_path)
    problemes = []
    
    # Patterns à vérifier
    patterns_problematiques = [
        r"{%\s*url\s+['\"]creer_bon['\"]",
        r"reverse\(['\"]creer_bon['\"]",
        r'href=[\"']/bons/creer/[\"']'
    ]
    
    print("🔍 VÉRIFICATION DES CORRECTIONS DANS LES FICHIERS")
    print("=" * 60)
    
    # Vérifier les templates
    templates_path = projet / 'templates'
    if not templates_path.exists():
        templates_path = projet / 'assureur' / 'templates'
    
    for fichier in templates_path.rglob('*.html'):
        verifier_fichier(fichier, patterns_problematiques, problemes)
    
    # Vérifier les vues Python
    vues_path = projet / 'assureur'
    for fichier in vues_path.rglob('*.py'):
        verifier_fichier(fichier, patterns_problematiques, problemes)
    
    if problemes:
        print(f"\n❌ {len(problemes)} PROBLÈMES DÉTECTÉS:")
        for fichier, ligne, pattern in problemes:
            print(f"   📄 {fichier}")
            print(f"      Ligne: {ligne.strip()}")
            print(f"      Pattern: {pattern}")
    else:
        print(f"\n✅ AUCUN PROBLÈME DÉTECTÉ - Toutes les corrections sont appliquées!")

def verifier_fichier(fichier, patterns, problemes):
    """Vérifie un fichier spécifique"""
    try:
        with open(fichier, 'r', encoding='utf-8') as f:
            lignes = f.readlines()
    except:
        return
    
    for num_ligne, ligne in enumerate(lignes, 1):
        for pattern in patterns:
            if re.search(pattern, ligne):
                problemes.append((fichier, num_ligne, pattern))

if __name__ == "__main__":
    verifier_fichiers("/Users/koffitanohsoualiho/Documents/projet")