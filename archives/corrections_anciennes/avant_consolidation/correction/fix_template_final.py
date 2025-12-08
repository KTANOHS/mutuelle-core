# fix_template_final.py
import re

# Lire le template
with open('templates/assureur/generer_cotisations.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("=== CORRECTION DU TEMPLATE ===")

# Vérifier si l'URL incorrecte existe encore
if '{% url "preview_generation" %}' in content:
    print("⚠ URL incorrecte trouvée : {% url \"preview_generation\" %}")
    # Remplacer par la version corrigée
    content = content.replace(
        '{% url "preview_generation" %}',
        '{% url "assureur:preview_generation" %}'
    )
    print("✓ Corrigé en : {% url \"assureur:preview_generation\" %}")

if "url: '{% url \"preview_generation\" %}'" in content:
    print("⚠ URL JavaScript incorrecte trouvée")
    # Remplacer la ligne JavaScript spécifique
    content = content.replace(
        "url: '{% url \"preview_generation\" %}'",
        "url: '{% url \"assureur:preview_generation\" %}'"
    )
    print("✓ Ligne JavaScript corrigée")

# Écrire le fichier corrigé
with open('templates/assureur/generer_cotisations.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n=== VÉRIFICATION FINALE ===")

# Vérifier qu'il n'y a plus d'erreurs
with open('templates/assureur/generer_cotisations.html', 'r', encoding='utf-8') as f:
    content = f.read()
    
if 'preview_generation' in content:
    # Trouver les lignes avec preview_generation
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if 'preview_generation' in line and 'assureur:preview_generation' not in line:
            print(f"⚠ Ligne {i}: {line.strip()}")
        elif 'assureur:preview_generation' in line:
            print(f"✓ Ligne {i}: Correcte")

print("\nCorrection terminée !")