"""
core/views.py - Views de l'application "core"
Pages statiques: about, contact, politique, etc.
"""

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db import connection
from datetime import datetime
import os

# === IMPORT CONDITIONNEL DE PSUTIL ===
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None

# === PAGES STATIQUES ===

def home(request):
    """
    Page d'accueil publique
    """
    context = {
        'page_title': 'Accueil - Mutuelle de Santé',
        'description': 'Plateforme de gestion de mutuelle de santé',
        'show_login': True,
        'is_home': True,
    }
    
    # Si l'utilisateur est déjà connecté, on pourrait le rediriger
    if request.user.is_authenticated:
        context['user'] = request.user
        context['user_groups'] = list(request.user.groups.values_list('name', flat=True))
    
    # Essayer d'abord le template de l'app core
    try:
        return render(request, 'core/home.html', context)
    except:
        # Fallback vers template racine
        return render(request, 'home.html', context)

def about(request):
    """
    Page À propos
    """
    context = {
        'page_title': 'À propos de nous',
        'description': 'Découvrez notre mission et notre équipe',
        'is_about': True,
    }
    return render(request, 'core/about.html', context)

def contact(request):
    """
    Page de contact
    """
    context = {
        'page_title': 'Contactez-nous',
        'description': 'Prenez contact avec notre équipe',
        'is_contact': True,
    }
    return render(request, 'core/contact.html', context)

def privacy_policy(request):
    """
    Politique de confidentialité
    """
    context = {
        'page_title': 'Politique de confidentialité',
        'description': 'Comment nous protégeons vos données',
        'is_privacy': True,
    }
    return render(request, 'core/privacy_policy.html', context)

def terms_of_service(request):
    """
    Conditions d'utilisation
    """
    context = {
        'page_title': 'Conditions d\'utilisation',
        'description': 'Règles d\'utilisation de la plateforme',
        'is_terms': True,
    }
    return render(request, 'core/terms_of_service.html', context)

def services(request):
    """
    Nos services
    """
    context = {
        'page_title': 'Nos services',
        'description': 'Découvrez nos services',
        'is_services': True,
    }
    return render(request, 'core/services.html', context)

def faq(request):
    """
    Foire aux questions
    """
    context = {
        'page_title': 'FAQ - Questions fréquentes',
        'description': 'Trouvez des réponses à vos questions',
        'is_faq': True,
    }
    return render(request, 'core/faq.html', context)

# === PAGES D'INFORMATION ===

def how_it_works(request):
    """
    Comment ça marche
    """
    context = {
        'page_title': 'Comment ça marche',
        'description': 'Guide d\'utilisation de la plateforme',
        'is_guide': True,
    }
    return render(request, 'core/how_it_works.html', context)

def pricing(request):
    """
    Tarifs
    """
    context = {
        'page_title': 'Tarifs',
        'description': 'Nos offres et tarifs',
        'is_pricing': True,
    }
    return render(request, 'core/pricing.html', context)

# === VUES UTILITAIRES ===

def maintenance(request):
    """
    Page de maintenance
    """
    context = {
        'page_title': 'Maintenance en cours',
        'description': 'Le site est temporairement indisponible',
        'is_maintenance': True,
    }
    return render(request, 'core/maintenance.html', context, status=503)

def coming_soon(request):
    """
    Page "Bientôt disponible"
    """
    context = {
        'page_title': 'Bientôt disponible',
        'description': 'Cette fonctionnalité arrive bientôt',
        'is_coming_soon': True,
    }
    return render(request, 'core/coming_soon.html', context)

def site_status(request):
    """
    Status du site (similaire à health check mais plus orienté utilisateur)
    """
    context = {
        'page_title': 'État du service',
        'description': 'Vérifiez l\'état de notre plateforme',
        'is_status': True,
    }
    return render(request, 'core/site_status.html', context)

# === VUE POUR LES TEMPLATES MANQUANTS ===

def placeholder(request, template_name):
    """
    Vue générique pour les templates manquants
    """
    context = {
        'page_title': template_name.replace('_', ' ').title(),
        'template_name': template_name,
        'is_placeholder': True,
    }
    
    # Essayer le template spécifié
    try:
        return render(request, f'core/{template_name}.html', context)
    except:
        # Fallback vers un template générique
        try:
            return render(request, 'core/placeholder.html', context)
        except:
            # Template générique HTML direct
            return HttpResponse(f"""
                <!DOCTYPE html>
                <html lang="fr">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>{context['page_title']} - Mutuelle de Santé</title>
                    <style>
                        body {{
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                            margin: 0;
                            padding: 0;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            min-height: 100vh;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        }}
                        .container {{
                            background: white;
                            padding: 40px;
                            border-radius: 12px;
                            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                            text-align: center;
                            max-width: 600px;
                            width: 90%;
                        }}
                        h1 {{
                            color: #333;
                            margin-bottom: 20px;
                            font-size: 2.5rem;
                        }}
                        p {{
                            color: #666;
                            line-height: 1.8;
                            margin-bottom: 30px;
                            font-size: 1.1rem;
                        }}
                        .code {{
                            background: #f8f9fa;
                            padding: 15px;
                            border-radius: 8px;
                            border-left: 4px solid #667eea;
                            margin: 20px 0;
                            font-family: 'Courier New', monospace;
                            text-align: left;
                        }}
                        .btn {{
                            display: inline-block;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            padding: 12px 30px;
                            border-radius: 30px;
                            text-decoration: none;
                            font-weight: 600;
                            margin: 10px;
                            transition: transform 0.3s;
                        }}
                        .btn:hover {{
                            transform: translateY(-3px);
                            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
                        }}
                        .btn-secondary {{
                            background: #6c757d;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>{context['page_title']}</h1>
                        <p>Cette page est en cours de développement et sera bientôt disponible avec tout son contenu.</p>
                        
                        <div class="code">
                            <strong>Template demandé :</strong> {template_name}.html<br>
                            <strong>URL :</strong> {request.path}
                        </div>
                        
                        <p>En attendant, vous pouvez retourner à l'accueil ou explorer d'autres sections du site.</p>
                        
                        <div>
                            <a href="/" class="btn">🏠 Retour à l'accueil</a>
                            <a href="/about/" class="btn">ℹ️ À propos</a>
                            <a href="/contact/" class="btn-secondary">📞 Contact</a>
                        </div>
                        
                        <p style="margin-top: 30px; font-size: 0.9rem; color: #999;">
                            Mutuelle de Santé © {datetime.now().year}
                        </p>
                    </div>
                </body>
                </html>
            """)

# === VUES D'API UTILITAIRES ===

def api_health_check(request):
    """
    API Health check (similaire à celle du projet mais pour core)
    """
    status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'core-app',
        'version': '1.0.0',
    }
    
    # Vérifier la base de données
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            status['database'] = 'connected'
    except Exception as e:
        status['database'] = 'error'
        status['database_error'] = str(e)[:100]
        status['status'] = 'unhealthy'
    
    http_status = 200 if status['status'] == 'healthy' else 503
    return JsonResponse(status, status=http_status)

def api_system_info(request):
    """
    Informations système (version simplifiée)
    """
    info = {
        'timestamp': datetime.now().isoformat(),
        'django_version': '5.2.6',
        'python_version': '3.11.10',
        'environment': os.environ.get('ENVIRONMENT', 'development'),
        'debug': os.environ.get('DEBUG', 'False'),
    }
    
    return JsonResponse(info)

# === VUES D'ERREUR POUR L'APPLICATION CORE ===

def error_404(request, exception=None):
    """
    Page 404 pour l'application core
    """
    context = {
        'page_title': '404 - Page non trouvée',
        'error_code': 404,
        'error_message': 'La page que vous recherchez n\'existe pas.',
        'is_error': True,
    }
    return render(request, 'core/error_404.html', context, status=404)

def error_500(request):
    """
    Page 500 pour l'application core
    """
    context = {
        'page_title': '500 - Erreur serveur',
        'error_code': 500,
        'error_message': 'Une erreur interne s\'est produite.',
        'is_error': True,
    }
    return render(request, 'core/error_500.html', context, status=500)

# === VUE DE TEST ===

@login_required
def test_view(request):
    """
    Vue de test pour vérifier l'authentification et les permissions
    """
    user = request.user
    context = {
        'page_title': 'Vue de test',
        'user': user,
        'user_groups': list(user.groups.values_list('name', flat=True)),
        'is_superuser': user.is_superuser,
        'is_authenticated': user.is_authenticated,
        'is_test': True,
    }
    return render(request, 'core/test.html', context)

# === VUE POUR LE SITEMAP XML (OPTIONNELLE) ===

def sitemap_xml(request):
    """
    Génère un sitemap XML simple
    """
    urls = [
        {'loc': '/', 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': '/about/', 'priority': '0.8', 'changefreq': 'monthly'},
        {'loc': '/contact/', 'priority': '0.8', 'changefreq': 'monthly'},
        {'loc': '/services/', 'priority': '0.7', 'changefreq': 'monthly'},
        {'loc': '/faq/', 'priority': '0.6', 'changefreq': 'monthly'},
        {'loc': '/privacy-policy/', 'priority': '0.5', 'changefreq': 'yearly'},
        {'loc': '/terms-of-service/', 'priority': '0.5', 'changefreq': 'yearly'},
    ]
    
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        xml_content += f'  <url>\n'
        xml_content += f'    <loc>https://example.com{url["loc"]}</loc>\n'
        xml_content += f'    <priority>{url["priority"]}</priority>\n'
        xml_content += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml_content += f'  </url>\n'
    
    xml_content += '</urlset>'
    
    return HttpResponse(xml_content, content_type='application/xml')