#!/usr/bin/env python3
"""
CORRECTION RAPIDE NameError: 'GroupeCommunication' is not defined
"""

from pathlib import Path

def correction_rapide():
    print("🔧 CORRECTION RAPIDE NameError")
    print("=" * 35)
    
    communication_path = Path('communication')
    admin_file = communication_path / 'admin.py'
    
    if not admin_file.exists():
        print("❌ admin.py non trouvé")
        return
    
    # Lire le contenu actuel
    with open(admin_file, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # Import correct
    import_correct = "from .models import Message, Conversation, PieceJointe, Notification, GroupeCommunication, MessageGroupe"
    
    # Remplacer l'import
    import_trouve = False
    lignes = contenu.split('\n')
    nouvelles_lignes = []
    
    for ligne in lignes:
        if ligne.strip().startswith('from .models import'):
            nouvelles_lignes.append(import_correct)
            import_trouve = True
            print(f"✅ Import corrigé: {import_correct}")
        else:
            nouvelles_lignes.append(ligne)
    
    if import_trouve:
        # Sauvegarder backup
        backup_file = communication_path / 'admin_backup_rapide.py'
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(contenu)
        
        # Écrire la version corrigée
        with open(admin_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(nouvelles_lignes))
        
        print(f"✅ admin.py corrigé avec succès")
        print(f"📦 Backup: {backup_file.name}")
        
        # Vérification
        try:
            exec(open(admin_file).read())
            print("✅ Vérification: admin.py fonctionne correctement")
        except Exception as e:
            print(f"❌ Erreur après correction: {e}")
    else:
        print("❌ Aucun import trouvé à corriger")

if __name__ == '__main__':
    correction_rapide()