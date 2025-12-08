# fix_redirect_complete.py
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

django.setup()

print("🔧 CORRECTION COMPLÈTE DE LA REDIRECTION")
print("="*50)

# 1. Vérifier et corriger core/utils.py
print("\n1. Correction de core/utils.py...")
core_utils_path = BASE_DIR / "core" / "utils.py"

if core_utils_path.exists():
    with open(core_utils_path, 'r') as f:
        content = f.read()
    
    # Vérifier si la fonction retourne /assureur/dashboard/
    if 'return \'/assureur/dashboard/\'' in content:
        content = content.replace('return \'/assureur/dashboard/\'', 'return \'/assureur/\'')
        with open(core_utils_path, 'w') as f:
            f.write(content)
        print("✅ core/utils.py corrigé (retourne '/assureur/')")
    elif 'return "/assureur/dashboard/"' in content:
        content = content.replace('return "/assureur/dashboard/"', 'return "/assureur/"')
        with open(core_utils_path, 'w') as f:
            f.write(content)
        print("✅ core/utils.py corrigé (retourne '/assureur/')")
    else:
        print("ℹ️  La fonction get_user_redirect_url ne retourne pas '/assureur/dashboard/'")
else:
    print("❌ core/utils.py non trouvé")

# 2. Vérifier et corriger assureur/urls.py
print("\n2. Correction de assureur/urls.py...")
urls_path = BASE_DIR / "assureur" / "urls.py"

if urls_path.exists():
    with open(urls_path, 'r') as f:
        content = f.read()
    
    # Vérifier si l'import views_correction existe
    if 'from . import views_correction' not in content:
        # Ajouter après les autres imports
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'from . import views' in line:
                lines.insert(i + 1, 'from . import views_correction')
                break
        content = '\n'.join(lines)
        print("✅ Import de views_correction ajouté")
    
    # Vérifier si l'URL dashboard/ existe
    if 'path(\'dashboard/\',' not in content and "path('dashboard/", not in content:
        # Trouver le bon endroit pour l'insérer (après l'URL principale)
        lines = content.split('\n')
        inserted = False
        for i, line in enumerate(lines):
            if 'path(\'\',' in line or "path(''," in line:
                if 'views.dashboard_assureur' in line:
                    # Insérer après cette ligne
                    lines.insert(i + 1, "    path('dashboard/', views_correction.redirect_to_dashboard, name='dashboard_redirect'),")
                    inserted = True
                    break
        
        if not inserted:
            # Sinon, ajouter à la fin de urlpatterns
            for i, line in enumerate(lines):
                if ']' in line and '#' not in line:
                    lines.insert(i, "    path('dashboard/', views_correction.redirect_to_dashboard, name='dashboard_redirect'),")
                    inserted = True
                    break
        
        if inserted:
            content = '\n'.join(lines)
            print("✅ URL dashboard/ ajoutée à urlpatterns")
        else:
            print("❌ Impossible de trouver où ajouter l'URL")
    else:
        print("ℹ️  L'URL dashboard/ existe déjà")
    
    # Écrire les modifications
    with open(urls_path, 'w') as f:
        f.write(content)
else:
    print("❌ assureur/urls.py non trouvé")

# 3. Vérifier que views_correction.py existe
print("\n3. Vérification de views_correction.py...")
views_correction_path = BASE_DIR / "assureur" / "views_correction.py"
if views_correction_path.exists():
    print("✅ views_correction.py existe")
else:
    # Créer le fichier
    with open(views_correction_path, 'w') as f:
        f.write('''"""
Vues de correction pour les redirections
"""

from django.shortcuts import redirect

def redirect_to_dashboard(request):
    """Redirige vers le vrai dashboard assureur"""
    return redirect('assureur:dashboard')
''')
    print("✅ views_correction.py créé")

print("\n" + "="*50)
print("🎯 CORRECTIONS TERMINÉES !")
print("\n📋 RÉCAPITULATIF DES CORRECTIONS :")
print("1. core/utils.py : Modifié pour retourner '/assureur/' au lieu de '/assureur/dashboard/'")
print("2. assureur/urls.py : URL '/assureur/dashboard/' ajoutée avec redirection")
print("3. assureur/views_correction.py : Vérifié/créé")
print("\n🚀 Pour tester :")
print("1. Redémarrez le serveur : python manage.py runserver")
print("2. Connectez-vous avec l'utilisateur DOUA")
print("3. Vous serez redirigé vers /assureur/")
print("4. L'URL /assureur/dashboard/ fonctionnera aussi")