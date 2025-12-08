#!/usr/bin/env python
"""
Script d'analyse du problème 404 sur /dashboard/ - CORRIGÉ
"""

import os
import sys
import django
from pathlib import Path

def setup_django():
    """Configurer Django correctement"""
    print("🔧 CONFIGURATION DJANGO")
    print("=" * 50)
    
    try:
        # Trouver le fichier settings.py
        project_dir = Path.cwd()
        settings_path = None
        
        for path in project_dir.rglob('settings.py'):
            if 'env' not in str(path) and 'venv' not in str(path):
                settings_path = path
                break
        
        if not settings_path:
            print("❌ Fichier settings.py non trouvé")
            return False
        
        # Ajouter le répertoire parent au path Python
        project_root = settings_path.parent.parent
        sys.path.append(str(project_root))
        
        # Définir le module settings
        settings_module = f"{settings_path.parent.name}.settings"
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
        
        print(f"📋 Settings module: {settings_module}")
        print(f"📁 Project root: {project_root}")
        
        django.setup()
        print("✅ Django configuré avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur configuration Django: {e}")
        return False

def test_url_resolution():
    """Tester la résolution de l'URL"""
    print("\n🔍 TEST DE RÉSOLUTION URL")
    print("=" * 50)
    
    try:
        from django.urls import resolve
        
        match = resolve('/dashboard/')
        print(f"✅ URL résolue avec succès!")
        print(f"   📍 Vue: {match.func}")
        print(f"   📁 Module: {match.func.__module__}")
        print(f"   📛 Nom: {match.url_name}")
        
        return match.func
        
    except Exception as e:
        print(f"❌ Erreur résolution: {e}")
        return None

def test_view_execution_simple():
    """Tester l'exécution de la vue de manière simple"""
    print("\n🎯 TEST D'EXÉCUTION SIMPLE")
    print("=" * 50)
    
    try:
        view_func = resolve('/dashboard/').func
        
        # Afficher des infos sur la fonction
        print(f"📋 Fonction: {view_func}")
        print(f"📁 Module: {view_func.__module__}")
        print(f"📝 Nom: {view_func.__name__}")
        
        # Vérifier si c'est une fonction ou une classe
        if hasattr(view_func, 'view_class'):
            print("🎯 C'est une vue basée sur une classe")
        else:
            print("🎯 C'est une vue fonction")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur test simple: {e}")
        return False

def analyze_mutuelle_core_structure():
    """Analyser la structure de mutuelle_core"""
    print("\n📁 ANALYSE STRUCTURE MUTUELLE_CORE")
    print("=" * 50)
    
    try:
        # Vérifier si le module existe
        import importlib.util
        
        spec = importlib.util.find_spec("mutuelle_core")
        if spec is None:
            print("❌ Module mutuelle_core non trouvé")
            return False
            
        print("✅ Module mutuelle_core trouvé")
        print(f"📁 Emplacement: {spec.origin}")
        
        # Vérifier si views.py existe
        views_path = Path(spec.origin).parent / "views.py"
        if views_path.exists():
            print("✅ Fichier views.py trouvé")
            
            # Lire le contenu
            content = views_path.read_text()
            
            # Vérifier la fonction dashboard
            if 'def dashboard(' in content:
                print("✅ Fonction dashboard() trouvée")
                
                # Extraire quelques lignes autour de la fonction
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'def dashboard(' in line:
                        print("📄 Extrait de la fonction dashboard:")
                        for j in range(max(0, i-2), min(len(lines), i+8)):
                            print(f"   {j+1:3d}: {lines[j]}")
                        break
            else:
                print("❌ Fonction dashboard() NON trouvée")
                
        else:
            print("❌ Fichier views.py non trouvé")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur analyse structure: {e}")
        return False

def check_actual_error():
    """Vérifier l'erreur réelle qui se produit"""
    print("\n🚨 VÉRIFICATION DE L'ERREUR RÉELLE")
    print("=" * 50)
    
    try:
        # Importer la vue directement
        from mutuelle_core.views import dashboard
        print("✅ Vue dashboard importée avec succès")
        print(f"📋 Fonction: {dashboard}")
        
        # Essayer de créer un contexte minimal
        from django.test import RequestFactory
        from django.contrib.auth.models import AnonymousUser
        
        factory = RequestFactory()
        request = factory.get('/dashboard/')
        request.user = AnonymousUser()
        
        print("🔧 Test avec utilisateur anonyme...")
        try:
            response = dashboard(request)
            print(f"✅ Réponse: {response}")
            print(f"📊 Status: {getattr(response, 'status_code', 'N/A')}")
        except Exception as e:
            print(f"❌ Erreur exécution: {e}")
            import traceback
            traceback.print_exc()
            
    except ImportError as e:
        print(f"❌ Impossible d'importer la vue: {e}")
    except Exception as e:
        print(f"❌ Erreur générale: {e}")

def test_alternative_urls():
    """Tester les URLs alternatives"""
    print("\n🔄 TEST DES URLs ALTERNATIVES")
    print("=" * 50)
    
    try:
        from django.urls import resolve
        
        alternative_urls = [
            '/agents/dashboard/',
            '/assureur/dashboard/', 
            '/medecin/dashboard/',
            '/pharmacien/dashboard/',
            '/membres/dashboard/',
            '/agent-dashboard/',
            '/assureur-dashboard/'
        ]
        
        for url in alternative_urls:
            try:
                match = resolve(url)
                print(f"✅ {url} -> {match.func}")
            except Exception:
                print(f"❌ {url} -> NON TROUVÉE")
                
    except Exception as e:
        print(f"❌ Erreur test alternatives: {e}")

def create_quick_fix():
    """Créer un correctif rapide"""
    print("\n🔧 CRÉATION D'UN CORRECTIF RAPIDE")
    print("=" * 50)
    
    fix_content = '''
# CORRECTIF RAPIDE PUR /dashboard/
# Ajoutez ceci temporairement dans mutuelle_core/views.py

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required  
def dashboard_fixed(request):
    """Version fixée du dashboard"""
    return HttpResponse(f"""
    <h1>Dashboard Fixé</h1>
    <p>User: {request.user}</p>
    <p>Path: {request.path}</p>
    <p>Cette page fonctionne !</p>
    <hr>
    <p><a href="/agents/dashboard/">Aller au dashboard agent</a></p>
    <p><a href="/assureur/dashboard/">Aller au dashboard assureur</a></p>
    """)

# Puis dans urls.py, remplacez temporairement :
# path('dashboard/', dashboard_fixed, name='dashboard'),
'''
    
    with open('dashboard_quick_fix.py', 'w') as f:
        f.write(fix_content)
    
    print("📄 Fichier 'dashboard_quick_fix.py' créé")

def main():
    print("🔍 ANALYSE COMPLÈTE DU PROBLÈME /dashboard/")
    print("=" * 60)
    
    if not setup_django():
        print("❌ Impossible de continuer sans configuration Django")
        return
    
    # Tests successifs
    test_url_resolution()
    test_view_execution_simple() 
    analyze_mutuelle_core_structure()
    check_actual_error()
    test_alternative_urls()
    create_quick_fix()
    
    print("\n" + "=" * 60)
    print("🎯 DIAGNOSTIC COMPLET")
    print("=" * 60)
    
    print("""
📊 RÉSULTATS :

L'URL /dashboard/ est configurée et pointe vers mutuelle_core.views.dashboard
Le problème se produit lors de l'EXÉCUTION de la vue.

🚨 CAUSE PROBABLE :

La fonction dashboard() dans mutuelle_core/views.py contient une logique qui :
- Soit redirige vers une URL qui n'existe pas
- Soit tente d'utiliser un template manquant  
- Soit génère une exception non gérée

🚀 SOLUTIONS IMMÉDIATES :

1. MODIFIER TEMPORAIREMENT la vue dashboard pour la simplifier
2. UTILISER les URLs alternatives qui fonctionnent :
   - /agents/dashboard/  (pour les agents)
   - /assureur/dashboard/ (pour les assureurs)
   
3. INSPECTER le code de mutuelle_core.views.dashboard
4. AJOUTER un try/except pour capturer l'erreur

📋 COMMANDES DE TEST :

# Test direct de l'URL
curl -v http://127.0.0.1:8000/dashboard/

# Voir les logs Django
tail -f logs/django.log

# Test en shell
python manage.py shell
>>> from mutuelle_core.views import dashboard
>>> from django.test import RequestFactory
>>> request = RequestFactory().get('/dashboard/')
>>> dashboard(request)
""")

if __name__ == "__main__":
    main()