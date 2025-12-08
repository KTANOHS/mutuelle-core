# Créer un script de correction d'urgence
#!/usr/bin/env python3
"""
CORRECTION URGENCE ADMIN.PY
Supprime les modèles manquants des imports
"""

from pathlib import Path

def corriger_admin_urgence():
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
        return
    
    # Sauvegarder le backup
    backup_file = communication_path / 'admin_backup_urgence.py'
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(contenu)
    print(f"✅ Backup sauvegardé: {backup_file.name}")
    
    # Écrire le fichier corrigé
    with open(admin_file, 'w', encoding='utf-8') as f:
        f.write(contenu)
    
    print("✅ admin.py corrigé avec succès!")
    
    # Tester la correction
    try:
        from communication.admin import *
        print("✅ Test d'import réussi!")
    except ImportError as e:
        print(f"❌ Erreur après correction: {e}")

if __name__ == '__main__':
    print("🚀 CORRECTION URGENCE ADMIN.PY")
    print("=" * 35)
    corriger_admin_urgence()


