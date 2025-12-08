# Vérifier le problème dans models.py


# Corriger l'erreur de syntaxe

#!/usr/bin/env python3
"""
CORRECTION ERREUR SYNTAXE MODELS.PY
"""

from pathlib import Path

def corriger_syntaxe():
    communication_path = Path('communication')
    models_file = communication_path / 'models.py'
    
    if not models_file.exists():
        print("❌ models.py non trouvé")
        return
    
    # Lire le contenu
    with open(models_file, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # Corriger l'erreur de syntaxe - ajouter une ligne vide avant class Meta
    contenu_corrige = contenu.replace(
        "return self.type_fichier in ['PDF', 'IMAGE']class Meta:",
        "return self.type_fichier in ['PDF', 'IMAGE']\n\n    class Meta:"
    )
    
    if contenu_corrige != contenu:
        # Sauvegarder backup
        backup_file = communication_path / 'models_backup_syntaxe.py'
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(contenu)
        
        # Écrire la version corrigée
        with open(models_file, 'w', encoding='utf-8') as f:
            f.write(contenu_corrige)
        
        print("✅ Erreur de syntaxe corrigée!")
        print("📝 Correction: Ajout d'une ligne vide avant 'class Meta:'")
    else:
        print("✅ Aucune erreur de syntaxe détectée")

if __name__ == '__main__':
    print("🚀 CORRECTION ERREUR SYNTAXE MODELS.PY")
    print("=" * 45)
    corriger_syntaxe()

