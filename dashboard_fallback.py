
# === FALLBACK SIMPLE POUR DASHBOARD ===
# À ajouter dans mutuelle_core/views.py

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_simple_fallback(request):
    """
    Version ultra-simplifiée du dashboard en fallback
    """
    try:
        # Essayer d'abord la version normale
        from . import get_user_primary_group, get_user_redirect_url
        user = request.user
        
        # Vérifier que l'utilisateur est bien en base
        if not user.id:
            return HttpResponse("""
            <h1>Erreur Utilisateur</h1>
            <p>L'utilisateur n'est pas correctement enregistré.</p>
            <p><a href="/logout/">Se reconnecter</a></p>
            """)
        
        group = get_user_primary_group(user)
        redirect_url = get_user_redirect_url(user)
        
        if redirect_url and redirect_url != '/dashboard/':
            from django.shortcuts import redirect
            return redirect(redirect_url)
            
    except Exception as e:
        # Fallback ultime
        pass
    
    # Dashboard simple
    return HttpResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tableau de Bord</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            .card {{ background: #f5f5f5; padding: 20px; margin: 10px 0; border-radius: 5px; }}
            .btn {{ display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 4px; margin: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 Tableau de Bord</h1>
            <div class="card">
                <h2>Bienvenue, {request.user.username} !</h2>
                <p>Groupe détecté: {getattr(locals().get('group', {}), 'group', 'Non détecté')}</p>
            </div>
            
            <h3>Accès rapide:</h3>
            <a class="btn" href="/agents/dashboard/">Espace Agent</a>
            <a class="btn" href="/assureur/dashboard/">Espace Assureur</a>
            <a class="btn" href="/medecin/dashboard/">Espace Médecin</a>
            <a class="btn" href="/pharmacien/dashboard/">Espace Pharmacien</a>
            <a class="btn" href="/membres/dashboard/">Espace Membre</a>
            
            <div style="margin-top: 30px;">
                <a href="/logout/">Déconnexion</a>
            </div>
        </div>
    </body>
    </html>
    """)

# Pour l'utiliser temporairement, dans urls.py :
# path('dashboard/', dashboard_simple_fallback, name='dashboard'),
