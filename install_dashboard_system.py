# install_dashboard_system.py
from pathlib import Path

def installer_systeme_dashboard():
    print("🚀 INSTALLATION COMPLÈTE DU SYSTÈME DASHBOARD")
    print("=" * 60)
    
    project_path = Path(__file__).parent
    
    # 1. Créer/Mettre à jour le fichier views.py
    views_path = project_path / "mutuelle_core" / "views.py"
    
    print("📝 Mise à jour de mutuelle_core/views.py...")
    
    nouveau_contenu = '''from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

# === FONCTIONS UTILITAIRES (à ajouter si core.utils n'existe pas) ===

def get_user_primary_group(user):
    """
    Retourne le groupe principal de l'utilisateur
    Version de secours si core.utils n'existe pas
    """
    try:
        groups = user.groups.all()
        if groups.exists():
            return groups.first().name
        return None
    except Exception:
        return None

def get_user_redirect_url(user):
    """
    Retourne l'URL de redirection selon le groupe
    Version de secours si core.utils n'existe pas
    """
    group = get_user_primary_group(user)
    if group == 'assureur':
        return '/assureur/'
    elif group == 'medecin':
        return '/medecin/dashboard/'
    elif group == 'pharmacien':
        return '/pharmacien/dashboard/'
    elif group == 'membre':
        return '/membres/dashboard/'
    else:
        return '/'

# === VUES PRINCIPALES ===

@login_required
def dashboard(request):
    """
    Point d'entrée principal du dashboard
    Redirige vers le bon dashboard selon le groupe
    """
    try:
        # Vérifier si on est déjà sur une page de dashboard
        current_path = request.path
        dashboard_paths = [
            '/dashboard/', '/assureur/', '/assureur/dashboard/', 
            '/medecin/', '/medecin/dashboard/', 
            '/pharmacien/', '/pharmacien/dashboard/',
            '/membres/', '/membres/dashboard/', '/admin/'
        ]
        
        if any(current_path.startswith(path) for path in dashboard_paths):
            # Ne pas rediriger si déjà sur un dashboard
            group = get_user_primary_group(request.user)
            # Afficher le dashboard approprié
            return render_dashboard_for_group(request, group)
        
        # Redirection normale
        redirect_url = get_user_redirect_url(request.user)
        return redirect(redirect_url)
        
    except Exception as e:
        # Fallback sécurisé
        print(f"Erreur redirection dashboard: {e}")
        return render_default_dashboard(request)

def render_dashboard_for_group(request, group):
    """Affiche le dashboard approprié selon le groupe"""
    user = request.user
    
    if group == 'assureur':
        return render(request, "assureur/dashboard.html", {
            "user": user,
            "primary_group": group
        })
    elif group == 'medecin':
        return render(request, "medecin/dashboard.html", {
            "user": user,
            "primary_group": group
        })
    elif group == 'pharmacien':
        return render(request, "pharmacien/dashboard.html", {
            "user": user,
            "primary_group": group
        })
    elif group == 'membre':
        return render(request, "membres/dashboard.html", {
            "user": user,
            "primary_group": group
        })
    else:
        # Fallback pour utilisateurs sans groupe ou groupe inconnu
        return render_default_dashboard(request)

def render_default_dashboard(request):
    """
    Dashboard par défaut pour utilisateurs sans groupe spécifique
    """
    user = request.user
    primary_group = get_user_primary_group(user)
    
    context = {
        "user": user,
        "primary_group": primary_group,
        "user_groups": list(user.groups.values_list('name', flat=True))
    }
    
    # Essayer d'abord le template dans core/, sinon le template racine
    try:
        return render(request, "core/dashboard.html", context)
    except:
        try:
            return render(request, "dashboard.html", context)
        except:
            # Fallback ultime - page simple
            from django.http import HttpResponse
            return HttpResponse(f"""
                <h1>Tableau de Bord</h1>
                <p>Utilisateur: {user.username}</p>
                <p>Groupes: {', '.join(context['user_groups']) if context['user_groups'] else 'Aucun'}</p>
                <p><a href="/">Retour à l'accueil</a></p>
            """)

# === ANCIENNE VUE (À SUPPRIMER PROGRESSIVEMENT) ===

@login_required
def old_default_dashboard(request):
    """
    Ancienne vue - à supprimer progressivement
    Redirige vers la nouvelle vue dashboard
    """
    return redirect('dashboard')

# === VUE DE SECOURS SI LES IMPORTS core.utils ÉCHOUENT ===

try:
    from core.utils import get_user_redirect_url, get_user_primary_group
    # Si l'import réussit, utiliser les fonctions de core.utils
except ImportError:
    # Si core.utils n'existe pas, utiliser nos fonctions de secours
    print("⚠️  core.utils non trouvé - utilisation des fonctions de secours")
    pass
'''

    # Sauvegarder le nouveau contenu
    with open(views_path, 'w') as f:
        f.write(nouveau_contenu)
    
    print("✅ mutuelle_core/views.py mis à jour")
    
    # 2. Vérifier/Mettre à jour les URLs
    urls_path = project_path / "mutuelle_core" / "urls.py"
    print(f"\n🔗 Vérification des URLs...")
    
    if urls_path.exists():
        with open(urls_path, 'r') as f:
            urls_content = f.read()
        
        # Vérifier si l'URL dashboard est configurée
        if "path('dashboard/', views.dashboard, name='dashboard')" not in urls_content:
            print("⚠️  URL dashboard non configurée - ajout manuel nécessaire")
            print("   Ajoutez dans mutuelle_core/urls.py:")
            print("   path('dashboard/', views.dashboard, name='dashboard')")
        else:
            print("✅ URL dashboard correctement configurée")
    
    # 3. Vérifier le template
    template_path = project_path / "templates" / "core" / "dashboard.html"
    print(f"\n📁 Vérification du template...")
    
    if template_path.exists():
        print("✅ Template core/dashboard.html présent")
    else:
        print("❌ Template core/dashboard.html manquant")
        print("   Assurez-vous d'avoir renommé home.html en dashboard.html")
    
    print(f"\n🎉 INSTALLATION TERMINÉE!")
    print("Redémarrez le serveur: python manage.py runserver")

if __name__ == "__main__":
    installer_systeme_dashboard()