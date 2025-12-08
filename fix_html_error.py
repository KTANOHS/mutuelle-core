# fix_html_error.py
import os

views_file = "/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30/mutuelle_core/views.py"

with open(views_file, 'r') as f:
    lines = f.readlines()

# Corriger la ligne 254
if len(lines) >= 254:
    lines[253] = '        """)\n'  # Ligne 254 corrigée
    
    # Sauvegarder
    with open(views_file, 'w') as f:
        f.writelines(lines)
    
    print("✅ Correction appliquée !")
    print("La ligne 254 a été changée de :")
    print('   """)(html)')
    print("à :")
    print('   """)')
else:
    print("❌ Le fichier n'a pas assez de lignes")