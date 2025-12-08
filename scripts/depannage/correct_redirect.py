# correct_redirect.py
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

django.setup()

print("🔧 CORRECTION DE LA REDIRECTION ASSUREUR")
print("="*50)

# 1. Ajouter l'URL dashboard/ dans assureur/urls.py
urls_file = BASE_DIR / "assureur" / "urls.py"

with open(urls_file, 'r') as f:
    content = f.read()

# Vérifier si l'URL dashboard/ existe déjà
if "path('dashboard/'," not in content:
    # Ajouter l'import si nécessaire
    if "from . import views_correction" not in content:
        # Ajouter après les autres imports
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "from . import views" in line:
                lines.insert(i+1, "from . import views_correction")
                break
        
        content = '\n'.join(lines)
    
    # Ajouter l'URL dans urlpatterns
    if "path('dashboard/', views_correction.redirect_to_dashboard, name='dashboard_redirect')," not in content:
        # Chercher où ajouter (juste après le dashboard principal)
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "path('', views.dashboard_assureur, name='dashboard')," in line:
                lines.insert(i+1, "    path('dashboard/', views_correction.redirect_to_dashboard, name='dashboard_redirect'),")
                break
        
        content = '\n'.join(lines)
    
    with open(urls_file, 'w') as f:
        f.write(content)
    
    print("✅ URLs corrigées dans assureur/urls.py")

# 2. Créer le fichier views_correction.py
views_correction_file = BASE_DIR / "assureur" / "views_correction.py"
if not views_correction_file.exists():
    with open(views_correction_file, 'w') as f:
        f.write('''"""
Vues de correction pour les redirections
"""

from django.shortcuts import redirect

def redirect_to_dashboard(request):
    """Redirige vers le vrai dashboard assureur"""
    return redirect('assureur:dashboard')
''')
    print("✅ Fichier views_correction.py créé")

# 3. Vérifier la fonction get_user_redirect_url
print("\n📋 Recherche de la fonction de redirection...")

# Chercher dans core/utils.py
core_utils = BASE_DIR / "core" / "utils.py"
if core_utils.exists():
    with open(core_utils, 'r') as f:
        utils_content = f.read()
    
    if 'def get_user_redirect_url' in utils_content:
        print("✅ Fonction get_user_redirect_url trouvée dans core/utils.py")
        
        # Vérifier ce qu'elle retourne pour les assureurs
        if 'assureur/dashboard' in utils_content:
            print("⚠️  La fonction retourne peut-être '/assureur/dashboard/'")
            print("   Elle devrait retourner '/assureur/'")
    else:
        print("ℹ️  Fonction get_user_redirect_url non trouvée dans core/utils.py")

print("\n🎯 CORRECTIONS APPLIQUÉES !")
print("\nRedémarrez le serveur :")
print("  python manage.py runserver")
print("\nTestez l'accès :")
print("  1. Connectez-vous avec l'utilisateur DOUA")
print("  2. Vous devriez être redirigé vers /assureur/")
print("  3. L'URL /assureur/dashboard/ devrait aussi fonctionner")