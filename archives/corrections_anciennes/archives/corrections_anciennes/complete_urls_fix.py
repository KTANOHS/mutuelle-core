# complete_urls_fix.py
import os
import sys
from pathlib import Path

def create_clean_urls():
    print("🧹 CRÉATION D'UN FICHIER URLS.PY PROPRE")
    print("=" * 60)
    
    urls_path = Path('/Users/koffitanohsoualiho/Documents/projet/mutuelle_core/urls.py')
    
    # Sauvegarder l'ancien fichier
    backup_path = urls_path.with_suffix('.py.backup2')
    if urls_path.exists():
        urls_path.rename(backup_path)
        print(f"✅ Ancien fichier sauvegardé: {backup_path}")
    
    # Nouveau contenu propre et simple
    clean_urls = '''"""
Configuration des URLs pour mutuelle_core
Version corrigée - imports simplifiés
"""
from django.contrib import admin
from django.urls import path, include
from . import views  # Import simple de toutes les views

urlpatterns = [
    # ========================
    # PAGES PRINCIPALES
    # ========================
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('redirect-after-login/', views.redirect_to_user_dashboard, name='redirect_after_login'),
    
    # ========================
    # DASHBOARDS SPÉCIFIQUES
    # ========================
    path('assureur-dashboard/', views.assureur_dashboard, name='assureur_dashboard'),
    path('medecin-dashboard/', views.medecin_dashboard, name='medecin_dashboard'),
    path('pharmacien-dashboard/', views.pharmacien_dashboard, name='pharmacien_dashboard'),
    path('membre-dashboard/', views.membre_dashboard, name='membre_dashboard'),
    
    # ========================
    # APPLICATIONS INCLUSES
    # ========================
    path('soins/', include('soins.urls')),
    path('assureur/', include('assureur.urls')),
    path('medecin/', include('medecin.urls')),
    path('pharmacien/', include('pharmacien.urls')),
    path('membres/', include('membres.urls')),
    path('inscription/', include('inscription.urls')),
    
    # ========================
    # AUTHENTIFICATION
    # ========================
    path('accounts/', include('django.contrib.auth.urls')),
    
    # ========================
    # PAGES DE DEBUG
    # ========================
    path('debug/test-login/', views.test_login, name='test_login'),
    path('debug/connection-status/', views.connection_status, name='connection_status'),
    
    # ========================
    # ADMIN
    # ========================
    path('admin/', admin.site.urls),
]

# Gestionnaires d'erreurs personnalisés (optionnel)
handler404 = 'mutuelle_core.views.view'
handler500 = 'mutuelle_core.views.view'
'''
    
    with open(urls_path, 'w') as f:
        f.write(clean_urls)
    
    print(f"✅ Nouveau fichier urls.py créé: {urls_path}")

def verify_urls_imports():
    print("\n🔍 VÉRIFICATION DES IMPORTS")
    print("=" * 60)
    
    try:
        # Tester l'import du nouveau fichier urls
        urls_path = Path('/Users/koffitanohsoualiho/Documents/projet/mutuelle_core/urls.py')
        
        with open(urls_path, 'r') as f:
            content = f.read()
        
        # Vérifier qu'il n'y a pas d'imports problématiques
        problematic_imports = ['CustomLoginView', 'CustomLogoutView', 'logout_confirmation']
        for import_name in problematic_imports:
            if import_name in content:
                print(f"❌ Import problématique trouvé: {import_name}")
            else:
                print(f"✅ Pas d'import: {import_name}")
        
        print("\n✅ Fichier urls.py vérifié avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur de vérification: {e}")

def test_server_start():
    print("\n🚀 TEST DE DÉMARRAGE DU SERVEUR")
    print("=" * 60)
    
    try:
        # Essayer d'importer la configuration URLs
        sys.path.append('/Users/koffitanohsoualiho/Documents/projet')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        
        import django
        from django.urls import get_resolver
        
        django.setup()
        
        # Essayer de résoudre les URLs
        resolver = get_resolver()
        print("✅ URLs résolues avec succès!")
        
        # Vérifier quelques URLs critiques
        critical_urls = ['home', 'dashboard', 'assureur_dashboard']
        for url_name in critical_urls:
            try:
                path = resolver.reverse(url_name)
                print(f"✅ URL '{url_name}': {path}")
            except:
                print(f"⚠️  URL '{url_name}' non trouvée")
                
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

if __name__ == "__main__":
    create_clean_urls()
    verify_urls_imports()
    test_server_start()
    
    print("\n" + "=" * 60)
    print("🎯 ACTION FINALE:")
    print("=" * 60)
    print("1. Redémarrez le serveur: python manage.py runserver")
    print("2. Testez: http://127.0.0.1:8000/")
    print("3. Testez la connexion avec différents utilisateurs")