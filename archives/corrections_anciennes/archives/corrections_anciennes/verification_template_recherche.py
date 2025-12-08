# verification_template_recherche.py
import os
from pathlib import Path

def verifier_template_recherche():
    print("📁 VÉRIFICATION DU TEMPLATE DE RECHERCHE")
    print("=" * 50)
    
    template_path = Path("/Users/koffitanohsoualiho/Documents/projet/templates/assureur/recherche_membre.html")
    
    if template_path.exists():
        print("✅ Template trouvé: templates/assureur/recherche_membre.html")
        
        # Lire le contenu pour vérification
        with open(template_path, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        # Vérifier les éléments importants
        if 'form' in contenu.lower() or 'search' in contenu.lower():
            print("   ✅ Le template contient des éléments de formulaire/recherche")
        else:
            print("   ⚠️  Le template peut ne pas contenir d'éléments de recherche")
        
        # Vérifier l'affichage des résultats
        if 'membres' in contenu or 'for' in contenu:
            print("   ✅ Le template semble prévu pour afficher les résultats")
        else:
            print("   ⚠️  Le template peut ne pas être configuré pour afficher les résultats")
            
    else:
        print("❌ Template non trouvé: templates/assureur/recherche_membre.html")
        print("   Création d'un template basique...")
        
        # Créer un template basique
        template_dir = template_path.parent
        template_dir.mkdir(parents=True, exist_ok=True)
        
        template_basique = '''<!DOCTYPE html>
<html>
<head>
    <title>Recherche de Membres</title>
</head>
<body>
    <h1>Recherche de Membres</h1>
    
    <form method="get" action=".">
        <input type="text" name="q" value="{{ query }}" placeholder="Rechercher un membre...">
        <button type="submit">Rechercher</button>
    </form>
    
    {% if query %}
        <h2>Résultats pour "{{ query }}"</h2>
        <p>{{ membres.count }} membre(s) trouvé(s)</p>
        
        {% if membres %}
            <ul>
            {% for membre in membres %}
                <li>
                    <strong>{{ membre.prenom }} {{ membre.nom }}</strong><br>
                    Numéro: {{ membre.numero_membre }}<br>
                    Email: {{ membre.email }}<br>
                    Téléphone: {{ membre.telephone }}
                </li>
            {% endfor %}
            </ul>
        {% else %}
            <p>Aucun membre trouvé.</p>
        {% endif %}
    {% else %}
        <p>Veuillez entrer un terme de recherche.</p>
    {% endif %}
</body>
</html>'''
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(template_basique)
        
        print("✅ Template basique créé")

if __name__ == "__main__":
    verifier_template_recherche()