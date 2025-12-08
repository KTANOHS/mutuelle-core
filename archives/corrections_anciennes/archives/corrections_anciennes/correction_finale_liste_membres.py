# correction_finale_liste_membres.py
import re

def corriger_liste_membres():
    fichier_path = "/Users/koffitanohsoualiho/Documents/projet/templates/assureur/liste_membres.html"
    
    print(f"🔧 Correction de: {fichier_path}")
    
    with open(fichier_path, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # Rechercher la ligne problématique spécifique
    ligne_problematique = r'<a href="{% url \'creer_bon\' %}\?membre_id=\{\{ membre\.id \}\}"'
    
    if re.search(ligne_problematique, contenu):
        print("✅ Ligne problématique trouvée!")
        
        # Correction 1: Remplacer l'URL sans namespace
        nouveau_contenu = re.sub(
            r'<a href="{% url \'creer_bon\' %}\?membre_id=\{\{ membre\.id \}\}"',
            r'<a href="{% url \'assureur:creer_bon\' membre.id %}"',
            contenu
        )
        
        # Sauvegarder
        with open(fichier_path, 'w', encoding='utf-8') as f:
            f.write(nouveau_contenu)
        
        print("✅ Correction appliquée!")
        
        # Vérifier la correction
        with open(fichier_path, 'r', encoding='utf-8') as f:
            contenu_corrige = f.read()
            if '{% url \'assureur:creer_bon\' membre.id %}' in contenu_corrige:
                print("✅ Vérification: La correction a été appliquée avec succès!")
            else:
                print("❌ Vérification: La correction n'a pas fonctionné")
    else:
        print("ℹ️  La ligne problématique n'a pas été trouvée")
        print("Recherche d'autres patterns...")
        
        # Chercher d'autres variations
        patterns = [
            r"{%\s*url\s+['\"]creer_bon['\"]",
            r"creer_bon.*membre_id",
        ]
        
        for pattern in patterns:
            if re.search(pattern, contenu):
                print(f"❌ Pattern trouvé: {pattern}")
                print("Le fichier nécessite une correction manuelle")

if __name__ == "__main__":
    corriger_liste_membres()