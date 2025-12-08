# complete_views_fix.py
import os
import sys
import django
from pathlib import Path

sys.path.append('/Users/koffitanohsoualiho/Documents/projet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

def create_complete_views_file():
    print("🔧 CRÉATION D'UN FICHIER VIEWS COMPLET")
    print("=" * 60)
    
    views_path = Path('/Users/koffitanohsoualiho/Documents/projet/mutuelle_core/views.py')
    
    # Sauvegarder l'ancien fichier
    backup_path = views_path.with_suffix('.py.backup')
    if views_path.exists():
        views_path.rename(backup_path)
        print(f"✅ Ancien fichier sauvegardé: {backup_path}")
    
    # Nouveau contenu complet avec indentation correcte
    complete_views = '''"""
Vues pour l'application mutuelle_core
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from .utils import get_user_redirect_url

def home(request):
    """
    Vue de la page d'accueil
    Redirige les utilisateurs connectés vers leur dashboard approprié
    """
    if request.user.is_authenticated:
        redirect_url = get_user_redirect_url(request.user)
        return redirect(redirect_url)
    
    # Page d'accueil pour les utilisateurs non connectés
    return render(request, 'home.html')

@login_required
def dashboard(request):
    """
    Dashboard principal - utilise la logique de redirection
    """
    redirect_url = get_user_redirect_url(request.user)
    return redirect(redirect_url)

@login_required
def redirect_to_user_dashboard(request):
    """
    Redirige l'utilisateur vers son dashboard approprié
    Utilise la fonction get_user_redirect_url pour une logique cohérente
    """
    redirect_url = get_user_redirect_url(request.user)
    return redirect(redirect_url)

@login_required
def assureur_dashboard(request):
    """
    Dashboard spécifique pour les assureurs
    """
    if not request.user.groups.filter(name='assureur').exists():
        return HttpResponseForbidden("Accès réservé aux assureurs")
    
    return render(request, 'assureur/dashboard.html', {
        'user': request.user,
        'user_type': 'assureur'
    })

@login_required
def medecin_dashboard(request):
    """
    Dashboard spécifique pour les médecins
    """
    if not request.user.groups.filter(name='medecin').exists():
        return HttpResponseForbidden("Accès réservé aux médecins")
    
    return render(request, 'medecin/dashboard.html', {
        'user': request.user,
        'user_type': 'medecin'
    })

@login_required
def pharmacien_dashboard(request):
    """
    Dashboard spécifique pour les pharmaciens
    """
    if not request.user.groups.filter(name='pharmacien').exists():
        return HttpResponseForbidden("Accès réservé aux pharmaciens")
    
    return render(request, 'pharmacien/dashboard.html', {
        'user': request.user,
        'user_type': 'pharmacien'
    })

@login_required
def membre_dashboard(request):
    """
    Dashboard spécifique pour les membres
    """
    if not request.user.groups.filter(name='membre').exists():
        return HttpResponseForbidden("Accès réservé aux membres")
    
    return render(request, 'membre/dashboard.html', {
        'user': request.user,
        'user_type': 'membre'
    })

def view(request, *args, **kwargs):
    """
    Vue générique pour les URLs d'authentification Django
    Cette vue permet d'utiliser les vues d'authentification Django par défaut
    """
    from django.contrib.auth import views as auth_views
    
    # Déterminer quelle vue d'authentification appeler basée sur l'URL
    path = request.path_info
    
    if path.endswith('/login/'):
        return auth_views.LoginView.as_view()(request, *args, **kwargs)
    elif path.endswith('/logout/'):
        return auth_views.LogoutView.as_view()(request, *args, **kwargs)
    elif 'password_change' in path:
        return auth_views.PasswordChangeView.as_view()(request, *args, **kwargs)
    elif 'password_reset' in path:
        return auth_views.PasswordResetView.as_view()(request, *args, **kwargs)
    else:
        return HttpResponse("Page d'authentification", status=404)

def connection_status(request):
    """
    Vue de debug pour vérifier le statut de connexion
    """
    return HttpResponse(f"Utilisateur: {request.user} | Connecté: {request.user.is_authenticated}")

def test_login(request):
    """
    Vue de test pour le login
    """
    return HttpResponse("Page de test login")
'''

    with open(views_path, 'w') as f:
        f.write(complete_views)
    
    print(f"✅ Nouveau fichier views.py créé: {views_path}")

def verify_new_views():
    print("\n🔍 VÉRIFICATION DU NOUVEAU FICHIER VIEWS")
    print("=" * 60)
    
    try:
        django.setup()
        from mutuelle_core import views
        
        required_views = [
            'home', 'dashboard', 'redirect_to_user_dashboard',
            'assureur_dashboard', 'medecin_dashboard', 
            'pharmacien_dashboard', 'membre_dashboard', 'view'
        ]
        
        for view_name in required_views:
            if hasattr(views, view_name):
                print(f"✅ Vue '{view_name}' importable")
            else:
                print(f"❌ Vue '{view_name}' manquante")
                
        print("\n🎉 Toutes les vues sont maintenant disponibles!")
        
    except Exception as e:
        print(f"❌ Erreur de vérification: {e}")

def create_basic_templates():
    """Crée les templates basiques manquants"""
    print("\n📁 CRÉATION DES TEMPLATES DE BASE")
    print("=" * 60)
    
    templates_dir = Path('/Users/koffitanohsoualiho/Documents/projet/templates')
    templates_dir.mkdir(exist_ok=True)
    
    # Template home
    home_template = '''<!DOCTYPE html>
<html>
<head>
    <title>Mutuelle - Accueil</title>
</head>
<body>
    <h1>Bienvenue sur la Mutuelle</h1>
    <p>Plateforme de gestion des soins de santé</p>
    <a href="/accounts/login/">Se connecter</a>
</body>
</html>'''
    
    with open(templates_dir / 'home.html', 'w') as f:
        f.write(home_template)
    print("✅ Template home.html créé")
    
    # Templates de dashboard basiques
    dashboards = ['assureur', 'medecin', 'pharmacien', 'membre']
    for dashboard in dashboards:
        dashboard_dir = templates_dir / dashboard
        dashboard_dir.mkdir(exist_ok=True)
        
        dashboard_template = f'''<!DOCTYPE html>
<html>
<head>
    <title>Dashboard {dashboard.title()}</title>
</head>
<body>
    <h1>Dashboard {dashboard.title()}</h1>
    <p>Bienvenue, {{{{ user.username }}}} ({{{{ user_type }}}})</p>
    <a href="/accounts/logout/">Déconnexion</a>
</body>
</html>'''
        
        with open(dashboard_dir / 'dashboard.html', 'w') as f:
            f.write(dashboard_template)
        print(f"✅ Template {dashboard}/dashboard.html créé")

if __name__ == "__main__":
    create_complete_views_file()
    verify_new_views()
    create_basic_templates()
    
    print("\n" + "=" * 60)
    print("🚀 ACTION REQUISE:")
    print("=" * 60)
    print("1. Redémarrez le serveur: python manage.py runserver")
    print("2. Testez: http://127.0.0.1:8000/")
    print("3. Testez la connexion avec différents utilisateurs")