# Créer la version corrigée

#!/usr/bin/env python3
"""
CORRECTION FINALE ADMIN.PY
Supprime les modèles manquants des imports
"""

from pathlib import Path

def corriger_admin_final():
    communication_path = Path('communication')
    admin_file = communication_path / 'admin.py'
    
    if not admin_file.exists():
        print("❌ admin.py non trouvé")
        return
    
    # Lire le contenu actuel
    with open(admin_file, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # Modèles qui existent réellement (basé sur l'analyse)
    modeles_existants = ['Message', 'Conversation', 'PieceJointe', 'Notification']
    
    # Remplacer la ligne d'import
    ancienne_ligne = "from .models import Message, Conversation, PieceJointe, Notification, GroupeCommunication, MessageGroupe"
    nouvelle_ligne = f"from .models import {', '.join(modeles_existants)}"
    
    if ancienne_ligne in contenu:
        contenu = contenu.replace(ancienne_ligne, nouvelle_ligne)
        print(f"✅ Ligne d'import corrigée:")
        print(f"   AVANT: {ancienne_ligne}")
        print(f"   APRÈS: {nouvelle_ligne}")
    else:
        print("❌ Ligne d'import non trouvée dans le format attendu")
        # Essayer un autre format
        autres_formats = [
            "from .models import Message, PieceJointe, Notification, GroupeCommunication, MessageGroupe",
            "from .models import Message, Conversation, PieceJointe, Notification"
        ]
        for format_ in autres_formats:
            if format_ in contenu:
                contenu = contenu.replace(format_, nouvelle_ligne)
                print(f"✅ Format alternatif corrigé: {format_}")
                break
        else:
            print("❌ Aucun format d'import reconnu")
            return
    
    # Sauvegarder le backup
    backup_file = communication_path / 'admin_backup_final.py'
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(contenu)
    print(f"✅ Backup sauvegardé: {backup_file.name}")
    
    # Écrire le fichier corrigé
    with open(admin_file, 'w', encoding='utf-8') as f:
        f.write(contenu)
    
    print("✅ admin.py corrigé avec succès!")

if __name__ == '__main__':
    print("🚀 CORRECTION FINALE ADMIN.PY")
    print("=" * 35)
    corriger_admin_final()
    
    # Tester séparément
    print("\n🔍 TEST DE LA CORRECTION...")
    try:
        exec(open('communication/admin.py').read())
        print("✅ Test d'import réussi!")
    except Exception as e:
        print(f"❌ Erreur après correction: {e}")


