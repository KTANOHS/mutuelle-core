import re

# Lire le template
with open('templates/assureur/generer_cotisations.html', 'r') as f:
    content = f.read()

# Remplacer toutes les occurrences de preview_generation
# Pattern 1: JavaScript avec doubles quotes imbriquées
pattern1 = r"url:\s*'{% url \"preview_generation\" %}'"
replacement1 = "url: '{% url \"assureur:preview_generation\" %}'"

# Pattern 2: JavaScript avec simples quotes imbriquées  
pattern2 = r"url:\s*'{% url 'preview_generation' %}'"
replacement2 = "url: '{% url \"assureur:preview_generation\" %}'"

new_content = re.sub(pattern1, replacement1, content)
new_content = re.sub(pattern2, replacement2, new_content)

# Écrire le fichier corrigé
with open('templates/assureur/generer_cotisations.html', 'w') as f:
    f.write(new_content)

print("Template corrigé !")
