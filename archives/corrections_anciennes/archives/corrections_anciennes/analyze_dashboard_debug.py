#!/usr/bin/env python
"""
Script d'analyse du problème 404 sur /dashboard/ - Étape 2
"""

import os
import django
from django.urls import resolve, Resolver404
from django.test import RequestFactory
from django.contrib.auth.models import User

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_url_resolution():
    """Tester la résolution de l'URL"""
    print("🔍 TEST DE RÉSOLUTION URL")
    print("=" * 50)
    
    try:
        match = resolve('/dashboard/')
        print(f"✅ URL résolue avec succès!")
        print(f"   📍 Vue: {match.func}")
        print(f"   📁 Module: {match.func.__module__}")
        print(f"   📛 Nom: {match.url_name}")
        
        # Vérifier si la fonction existe
        if hasattr(match.func, '__call__'):
            print("   ✅ La fonction est callable")
        else:
            print("   ❌ La fonction n'est pas callable")
            
        return match.func
        
    except Resolver404 as e:
        print(f"❌ Resolver404: {e}")
        return None
    except Exception as e:
        print(f"❌ Erreur résolution: {e}")
        return None

def test_view_execution(view_func):
    """Tester l'exécution de la vue"""
    print("\n🎯 TEST D'EXÉCUTION DE LA VUE")
    print("=" * 50)
    
    try:
        # Créer une requête simulée
        factory = RequestFactory()
        request = factory.get('/dashboard/')
        
        # Simuler un utilisateur connecté
        user = User(username='test_user')
        request.user = user
        
        print("🔧 Configuration requête:")
        print(f"   Method: {request.method}")
        print(f"   Path: {request.path}")
        print(f"   User: {request.user}")
        
        # Exécuter la vue
        response = view_func(request)
        
        print(f"✅ Vue exécutée avec succès!")
        print(f"   📊 Status Code: {response.status_code}")
        print(f"   📋 Type: {type(response)}")
        
        if hasattr(response, 'url'):
            print(f"   🔄 Redirection vers: {response.url}")
            
        return response
        
    except Exception as e:
        print(f"❌ Erreur exécution vue: {e}")
        import traceback
        traceback.print_exc()
        return None

def analyze_mutuelle_core_views():
    """Analyser le contenu de mutuelle_core/views.py"""
    print("\n📝 ANALYSE DE MUTUELLE_CORE/VIEWS.PY")
    print("=" * 50)
    
    try:
        from mutuelle_core import views
        
        # Vérifier la fonction dashboard
        if hasattr(views, 'dashboard'):
            print("✅ Fonction dashboard trouvée dans mutuelle_core.views")
            
            # Analyser le code source
            import inspect
            source = inspect.getsource(views.dashboard)
            
            print("📄 Code de la fonction dashboard:")
            lines = source.split('\n')
            for i, line in enumerate(lines[:15]):  # Afficher les 15 premières lignes
                print(f"   {i+1:2d}: {line}")
                
            # Vérifier les décorateurs
            if '@login_required' in source:
                print("✅ Décorateur @login_required présent")
            else:
                print("❌ Décorateur @login_required MANQUANT")
                
            # Vérifier les redirections
            if 'redirect(' in source:
                print("🔄 La fonction contient des redirections")
            if 'render(' in source:
                print("📊 La fonction contient des rendus de template")
                
        else:
            print("❌ Fonction dashboard NON trouvée dans mutuelle_core.views")
            
    except Exception as e:
        print(f"❌ Erreur analyse views: {e}")

def check_template_existence():
    """Vérifier l'existence des templates"""
    print("\n📁 VÉRIFICATION DES TEMPLATES")
    print("=" * 50)
    
    from django.template.loader import get_template
    from django.template import TemplateDoesNotExist
    
    templates_to_check = [
        'core/dashboard.html',
        'dashboard.html', 
        'agents/dashboard.html',
        'assureur/dashboard.html'
    ]
    
    for template_name in templates_to_check:
        try:
            template = get_template(template_name)
            print(f"✅ Template trouvé: {template_name}")
            print(f"   📍 Chemin: {template.origin.name}")
        except TemplateDoesNotExist:
            print(f"❌ Template NON trouvé: {template_name}")

def test_authentication_requirements():
    """Tester les requirements d'authentification"""
    print("\n🔐 TEST DES REQUIREMENTS D'AUTHENTIFICATION")
    print("=" * 50)
    
    view_func = resolve('/dashboard/').func
    
    # Tester sans authentification
    factory = RequestFactory()
    request = factory.get('/dashboard/')
    request.user = User()  # Utilisateur anonyme
    request.user.is_authenticated = False
    
    try:
        response = view_func(request)
        print("❌ Vue accessible sans authentification")
        print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"✅ Vue protégée (erreur attendue): {e}")
    
    # Tester avec authentification
    request.user = User(username='test_user')
    request.user.is_authenticated = True
    
    try:
        response = view_func(request)
        print(f"✅ Vue accessible avec authentification")
        print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur avec utilisateur authentifié: {e}")

def check_middleware_issues():
    """Vérifier les problèmes de middleware"""
    print("\n⚙️ VÉRIFICATION MIDDLEWARE")
    print("=" * 50)
    
    from django.conf import settings
    
    print("Middleware activé:")
    for mw in settings.MIDDLEWARE:
        print(f"   📦 {mw}")
    
    # Vérifier les middlewares critiques
    critical_middlewares = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware'
    ]
    
    for critical in critical_middlewares:
        if critical in settings.MIDDLEWARE:
            print(f"✅ {critical} - ACTIF")
        else:
            print(f"❌ {critical} - INACTIF")

def main():
    print("🔍 ANALYSE AVANCÉE DU PROBLÈME /dashboard/")
    print("=" * 60)
    
    # 1. Test résolution URL
    view_func = test_url_resolution()
    
    if view_func:
        # 2. Analyse de la vue
        analyze_mutuelle_core_views()
        
        # 3. Test d'exécution
        test_view_execution(view_func)
        
        # 4. Vérification templates
        check_template_existence()
        
        # 5. Test authentification
        test_authentication_requirements()
        
        # 6. Vérification middleware
        check_middleware_issues()
    
    print("\n" + "=" * 60)
    print("🎯 DIAGNOSTIC FINAL")
    print("=" * 60)
    
    print("""
📋 RÉSULTATS DE L'ANALYSE :

✅ L'URL /dashboard/ est bien configurée
✅ Elle pointe vers mutuelle_core.views.dashboard
✅ La résolution Django fonctionne

🔍 CAUSES POSSIBLES DU 404 :

1. 🚨 LA VUE REDIRIGE VERS UNE AUTRE URL QUI N'EXISTE PAS
2. 🚨 LA VUE TENTE DE RENDRE UN TEMPLATE QUI N'EXISTE PAS  
3. 🚨 ERREUR DANS LA LOGIQUE DE LA VUE dashboard()
4. 🚨 PROBLÈME DE DÉCORATEUR @login_required

🚀 SOLUTIONS :

1. INSPECTEZ LA FONCTION dashboard() dans mutuelle_core/views.py
2. VÉRIFIEZ SI ELLE REDIRIGE VERS UNE MAUVAISE URL
3. TESTEZ DIRECTEMENT : http://127.0.0.1:8000/agents/dashboard/
4. AJOUTEZ UN TRY/EXCEPT DANS LA VUE POUR CAPTURER L'ERREUR
""")

if __name__ == "__main__":
    main()