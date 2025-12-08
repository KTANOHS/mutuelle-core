# corriger_redirections.py
import os
import re

def corriger_redirections_liste_messages():
    """Corriger toutes les redirections problématiques vers liste_messages"""
    
    fichiers_a_corriger = [
        'communication/views.py',
        'agents/views.py',
        'assureur/views.py'
    ]
    
    corrections = {
        # Anciennes redirections → Nouvelles redirections
        "redirect('communication:liste_messages')": "redirect('agents:liste_messages')",
        "redirect('liste_messages')": "redirect('agents:liste_messages')",
    }
    
    for fichier in fichiers_a_corriger:
        if os.path.exists(fichier):
            print(f"🔧 Correction de {fichier}...")
            
            with open(fichier, 'r') as f:
                contenu = f.read()
            
            # Compter les corrections
            corrections_appliquees = 0
            for ancien, nouveau in corrections.items():
                if ancien in contenu:
                    contenu = contenu.replace(ancien, nouveau)
                    corrections_appliquees += contenu.count(nouveau) - contenu.count(ancien)
            
            if corrections_appliquees > 0:
                with open(fichier, 'w') as f:
                    f.write(contenu)
                print(f"✅ {corrections_appliquees} correction(s) appliquée(s)")
            else:
                print("✅ Aucune correction nécessaire")
        else:
            print(f"⚠️ Fichier non trouvé: {fichier}")

if __name__ == "__main__":
    corriger_redirections_liste_messages()
    print("\n🎉 Toutes les redirections ont été corrigées !")