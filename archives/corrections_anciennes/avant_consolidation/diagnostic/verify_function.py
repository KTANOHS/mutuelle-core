# verify_function.py
import os
import sys

# Lire le fichier views.py pour vérifier si la fonction existe
views_path = "agents/views.py"

try:
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "def verifier_statut_cotisation_simple" in content:
        print("✅ SUCCÈS : La fonction verifier_statut_cotisation_simple EST dans le fichier")
        
        # Vérifier l'ordre des fonctions
        pos_simple = content.find("def verifier_statut_cotisation_simple")
        pos_simplifiee = content.find("def verifier_cotisation_membre_simplifiee")
        
        if pos_simple < pos_simplifiee:
            print("✅ ORDRE CORRECT : simple AVANT simplifiee")
        else:
            print("❌ ORDRE INCORRECT : simple APRÈS simplifiee")
            
    else:
        print("❌ ÉCHEC : La fonction verifier_statut_cotisation_simple N'EST PAS dans le fichier")
        print("💡 Vous devez l'ajouter manuellement")
        
except FileNotFoundError:
    print(f"❌ Fichier {views_path} non trouvé")
except Exception as e:
    print(f"❌ Erreur: {e}")