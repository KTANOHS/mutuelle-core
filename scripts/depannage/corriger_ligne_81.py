#!/usr/bin/env python3
"""
CORRECTION URGENTE - Ligne 81 du template
"""

import os
import re

def corriger_ligne_81():
    """Correction spécifique de la ligne problématique"""
    
    template_path = 'templates/agents/dashboard.html'
    
    if not os.path.exists(template_path):
        print("❌ Template non trouvé")
        return False
    
    # Lire le contenu
    with open(template_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Chercher et corriger la ligne 81 (index 80 en Python)
    if len(lines) > 80:
        old_line = lines[80].strip()
        print(f"🔍 Ligne 81 actuelle: {old_line}")
        
        # Vérifier si c'est la ligne problématique
        if 'stats.membres_a_jour' in old_line and 'stats.membres_actifs' in old_line:
            # Remplacer par la version corrigée
            lines[80] = '                                {{ stats.pourcentage_conformite|floatformat:0 }}%\n'
            
            # Sauvegarder
            with open(template_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            print("✅ Ligne 81 CORRIGÉE !")
            print("📝 Nouvelle ligne: {{ stats.pourcentage_conformite|floatformat:0 }}%")
            return True
        else:
            print("❌ Ligne 81 ne contient pas l'erreur attendue")
            return False
    else:
        print("❌ Le template a moins de 81 lignes")
        return False

def verifier_correction():
    """Vérifier que la correction a fonctionné"""
    
    template_path = 'templates/agents/dashboard.html'
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier que l'ancienne syntaxe n'existe plus
    ancienne_syntaxe = r'\(\s*\(\s*stats\.membres_a_jour\s*/\s*stats\.membres_actifs\s*\)\s*\*\s*100\s*\)\s*\|\s*floatformat:0'
    
    if re.search(ancienne_syntaxe, content):
        print("🚨 ERREUR: L'ancienne syntaxe est toujours présente !")
        return False
    else:
        print("✅ SUCCÈS: L'ancienne syntaxe a été supprimée")
        
        # Vérifier que la nouvelle syntaxe existe
        if 'stats.pourcentage_conformite' in content:
            print("✅ SUCCÈS: La nouvelle syntaxe est présente")
            return True
        else:
            print("❌ ERREUR: La nouvelle syntaxe n'est pas présente")
            return False

def vider_cache():
    """Vider le cache Django"""
    print("\n🗑️  VIDAGE DU CACHE...")
    
    cache_dirs = ['__pycache__', 'agents/__pycache__']
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            os.system(f'rm -rf {cache_dir}')
            print(f"✅ Cache supprimé: {cache_dir}")
    
    # Supprimer les fichiers .pyc
    os.system('find . -name "*.pyc" -delete')
    print("✅ Fichiers .pyc supprimés")

if __name__ == "__main__":
    print("🛠️  CORRECTION URGENTE - Ligne 81")
    print("=" * 50)
    
    if corriger_ligne_81():
        print("\n🔍 VÉRIFICATION DE LA CORRECTION...")
        if verifier_correction():
            vider_cache()
            print("\n🎉 CORRECTION RÉUSSIE !")
            print("💡 Redémarrez votre serveur: python manage.py runserver")
        else:
            print("\n❌ La vérification a échoué")
    else:
        print("\n❌ La correction a échoué")