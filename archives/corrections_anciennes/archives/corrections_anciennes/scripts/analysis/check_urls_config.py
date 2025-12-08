#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC DES URLs DJANGO
Vérifie la configuration des URLs et identifie les problèmes de redirection
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
from django.urls import get_resolver, URLPattern, URLResolver
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def check_urls_configuration():
    """Vérifie la configuration complète des URLs"""
    print("=" * 80)
    print("🔍 DIAGNOSTIC COMPLET DE LA CONFIGURATION DES URLs")
    print("=" * 80)
    
    # 1. Vérification des paramètres dans settings.py
    check_settings_config()
    
    # 2. Analyse de la structure des URLs
    check_urls_structure()
    
    # 3. Vérification des URLs d'authentification
    check_auth_urls()
    
    # 4. Détection des boucles potentielles
    check_redirect_loops()
    
    # 5. Vérification des templates
    check_templates_existence()

def check_settings_config():
    """Vérifie la configuration dans settings.py"""
    print("\n📋 1. VÉRIFICATION DES PARAMÈTRES SETTINGS.PY")
    print("-" * 50)
    
    auth_settings = {
        'LOGIN_REDIRECT_URL': getattr(settings, 'LOGIN_REDIRECT_URL', None),
        'LOGIN_URL': getattr(settings, 'LOGIN_URL', None),
        'LOGOUT_REDIRECT_URL': getattr(settings, 'LOGOUT_REDIRECT_URL', None),
        'DEBUG': getattr(settings, 'DEBUG', False),
    }
    
    for key, value in auth_settings.items():
        status = "✅" if value else "❌"
        print(f"{status} {key}: {value}")
        
        # Vérifications spécifiques
        if key == 'LOGIN_REDIRECT_URL' and value == '/redirect-after-login/':
            print("   ⚠️  Attention: URL absolue utilisée, vérifiez qu'elle n'existe pas en double")
        
        if key == 'DEBUG' and value:
            print("   ℹ️  Mode DEBUG activé - vérifiez SESSION_COOKIE_SECURE")

def check_urls_structure():
    """Analyse la structure hiérarchique des URLs"""
    print("\n🌐 2. STRUCTURE DES URLs")
    print("-" * 50)
    
    resolver = get_resolver()
    urls_list = []
    
    def extract_urls(urlpatterns, prefix='', depth=0):
        for pattern in urlpatterns:
            if isinstance(pattern, URLPattern):
                urls_list.append({
                    'pattern': str(pattern.pattern),
                    'name': pattern.name,
                    'prefix': prefix,
                    'depth': depth
                })
            elif isinstance(pattern, URLResolver):
                new_prefix = f"{prefix}{pattern.pattern}"
                extract_urls(pattern.url_patterns, new_prefix, depth + 1)
    
    extract_urls(resolver.url_patterns)
    
    # Afficher les URLs importantes
    auth_urls = [url for url in urls_list if 'account' in url['prefix'].lower() or 'login' in str(url['pattern']).lower()]
    
    print("📎 URLs d'authentification trouvées:")
    for url in auth_urls:
        status = "✅" if url['name'] else "⚠️"
        print(f"   {status} {url['prefix']}{url['pattern']} -> name: '{url['name']}'")
    
    # Vérifier les doublons
    patterns = [f"{url['prefix']}{url['pattern']}" for url in urls_list]
    duplicates = set([p for p in patterns if patterns.count(p) > 1])
    
    if duplicates:
        print("\n❌ DOUBLONS D'URLs DÉTECTÉS:")
        for dup in duplicates:
            print(f"   ⚠️  {dup}")
    else:
        print("✅ Aucun doublon d'URL détecté")

def check_auth_urls():
    """Vérifie spécifiquement les URLs d'authentification"""
    print("\n🔐 3. VÉRIFICATION DES URLs D'AUTHENTIFICATION")
    print("-" * 50)
    
    # URLs critiques à vérifier
    critical_urls = {
        'login': 'Connexion',
        'logout': 'Déconnexion', 
        'password_change': 'Changement mot de passe',
        'password_reset': 'Réinitialisation mot de passe'
    }
    
    resolver = get_resolver()
    
    for url_name, description in critical_urls.items():
        try:
            reverse_url = django.urls.reverse(url_name)
            print(f"✅ {description}: {url_name} -> {reverse_url}")
        except django.urls.NoReverseMatch:
            print(f"❌ {description}: URL '{url_name}' non trouvée")

def check_redirect_loops():
    """Détecte les boucles de redirection potentielles"""
    print("\n🔄 4. DÉTECTION DES BOUCLES DE REDIRECTION")
    print("-" * 50)
    
    # Vérifier la cohérence des redirections
    login_redirect = getattr(settings, 'LOGIN_REDIRECT_URL', '')
    logout_redirect = getattr(settings, 'LOGOUT_REDIRECT_URL', '')
    login_url = getattr(settings, 'LOGIN_URL', '')
    
    # Vérifier les boucles évidentes
    if login_redirect == login_url:
        print(f"❌ BOUCLE: LOGIN_REDIRECT_URL == LOGIN_URL ({login_redirect})")
    
    if logout_redirect == login_url:
        print(f"❌ BOUCLE: LOGOUT_REDIRECT_URL == LOGIN_URL ({logout_redirect})")
    
    # Vérifier la redirection après login
    if login_redirect:
        try:
            redirect_url = django.urls.reverse(login_redirect) if '/' not in login_redirect else login_redirect
            print(f"ℹ️  Après login: redirection vers {redirect_url}")
        except:
            print(f"⚠️  URL de redirection après login non résolvable: {login_redirect}")

def check_templates_existence():
    """Vérifie l'existence des templates critiques"""
    print("\n📄 5. VÉRIFICATION DES TEMPLATES")
    print("-" * 50)
    
    critical_templates = [
        'registration/login.html',
        'registration/logout.html', 
        'registration/password_change_form.html',
        'base.html',
        'home.html',
        'dashboard.html'
    ]
    
    template_dirs = getattr(settings, 'TEMPLATES', [{}])[0].get('DIRS', [])
    
    for template in critical_templates:
        found = False
        for template_dir in template_dirs:
            template_path = os.path.join(template_dir, template)
            if os.path.exists(template_path):
                found = True
                break
        
        status = "✅" if found else "❌"
        print(f"{status} {template}")

def generate_recommendations():
    """Génère des recommandations basées sur l'analyse"""
    print("\n💡 6. RECOMMANDATIONS")
    print("-" * 50)
    
    recommendations = [
        "✅ Utilisez des noms d'URLs dans LOGIN_REDIRECT_URL au lieu de chemins absolus",
        "✅ Vérifiez que redirect_after_login ne redirige pas vers /accounts/login/",
        "✅ Assurez-vous que tous les templates d'authentification existent",
        "✅ Testez la connexion avec un utilisateur ayant un profil complet",
        "✅ Activez SESSION_COOKIE_SECURE=False en développement",
        "✅ Vérifiez les middlewares d'authentification dans settings.py"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")

if __name__ == "__main__":
    check_urls_configuration()
    generate_recommendations()
    print("\n" + "=" * 80)
    print("🎯 DIAGNOSTIC TERMINÉ - Suivez les recommandations ci-dessus")
    print("=" * 80)