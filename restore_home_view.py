import re

views_path = 'mutuelle_core/views.py'

with open(views_path, 'r') as f:
    content = f.read()

# Nouvelle vue home qui utilise le template home.html
new_home = '''def home(request):
    """Page d'accueil principale"""
    from django.shortcuts import render
    try:
        return render(request, 'home.html')
    except Exception as e:
        # Fallback en cas d'erreur
        from django.http import HttpResponse
        return HttpResponse(f"""
        <html>
        <head><title>Erreur de chargement</title></head>
        <body>
            <h1>Erreur lors du chargement de la page</h1>
            <p>Détail : {str(e)}</p>
            <p><a href="/">Retour</a></p>
        </body>
        </html>
        """)'''

# Rechercher et remplacer la fonction home
# Pattern pour trouver la fonction home actuelle
pattern = r'def home\(request\):.*?return HttpResponse'

if re.search(pattern, content, re.DOTALL):
    content = re.sub(pattern, new_home, content, flags=re.DOTALL)
    with open(views_path, 'w') as f:
        f.write(content)
    print("✅ Vue home restaurée avec succès !")
else:
    print("⚠️  Impossible de trouver la fonction home actuelle")
    
# Vérification
print("\n📋 Vérification :")
with open(views_path, 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if 'def home' in line:
            print(f"Ligne {i+1}: {line.strip()}")
            # Afficher les 5 lignes suivantes
            for j in range(i+1, min(i+6, len(lines))):
                print(f"       {lines[j].rstrip()}")
            break
