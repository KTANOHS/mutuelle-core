import os
import re

def corriger_fichiers():
    corrections = [
        # Fichiers Python
        {
            'fichier': 'assureur/services.py',
            'remplacements': [
                (r"Soin\.objects\.filter\(membre=", "Soin.objects.filter(patient="),
                (r"BonDeSoin\.objects\.filter\(membre=", "BonDeSoin.objects.filter(patient="),
            ]
        },
        {
            'fichier': 'membres/views.py', 
            'remplacements': [
                (r"Soin\.objects\.filter\(membre=", "Soin.objects.filter(patient="),
                (r"soins_query = Soin\.objects\.filter\(membre=", "soins_query = Soin.objects.filter(patient="),
            ]
        }
    ]
    
    for correction in corrections:
        if os.path.exists(correction['fichier']):
            with open(correction['fichier'], 'r') as f:
                contenu = f.read()
            
            for pattern, replacement in correction['remplacements']:
                contenu = re.sub(pattern, replacement, contenu)
            
            with open(correction['fichier'], 'w') as f:
                f.write(contenu)
            print(f"✅ {correction['fichier']} corrigé")

if __name__ == "__main__":
    corriger_fichiers()
    print("🔧 Corrections appliquées avec succès!")