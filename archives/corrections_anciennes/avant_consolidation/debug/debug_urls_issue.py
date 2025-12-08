#!/usr/bin/env python
import os
import sys
import django
from django.urls import reverse, NoReverseMatch

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django configuré avec succès")
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def debug_urls():
    """Déboguer les URLs manquantes"""
    
    print("🔍 DÉBOGAGE DES URLs MANQUANTES")
    print("=" * 50)
    
    # URLs à vérifier
    urls_to_check = [
        'agents:creer_bon_soin_membre',
        'agents:confirmation_bon_soin'
    ]
    
    for url_name in urls_to_check:
        try:
            # Essayer avec des arguments
            if 'membre_id' in url_name:
                url = reverse(url_name, args=[1])
            elif 'bon_id' in url_name:
                url = reverse(url_name, args=[1])
            else:
                url = reverse(url_name)
            
            print(f"✅ {url_name:45} -> {url}")
            
        except NoReverseMatch as e:
            print(f"❌ {url_name:45} -> NON TROUVÉE: {e}")
            
        except Exception as e:
            print(f"⚠️  {url_name:45} -> ERREUR: {e}")

def check_urls_file():
    """Vérifier le contenu du fichier agents/urls.py"""
    
    print("\n📁 VÉRIFICATION DU FICHIER agents/urls.py")
    print("=" * 50)
    
    file_path = 'agents/urls.py'
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Vérifier la présence des URLs problématiques
        target_patterns = [
            "name='creer_bon_soin_membre'",
            "name='confirmation_bon_soin'",
            "creer-bon-soin/<int:membre_id>/",
            "confirmation-bon-soin/<int:bon_id>/"
        ]
        
        for pattern in target_patterns:
            if pattern in content:
                print(f"✅ '{pattern}' trouvé dans le fichier")
            else:
                print(f"❌ '{pattern}' NON trouvé dans le fichier")
        
        # Vérifier la structure générale
        if 'urlpatterns = [' in content:
            print("✅ Structure urlpatterns trouvée")
        else:
            print("❌ Structure urlpatterns manquante")
            
        if 'app_name = ' in content:
            print("✅ app_name défini")
        else:
            print("❌ app_name non défini")
            
    except Exception as e:
        print(f"❌ Erreur lecture fichier: {e}")

def check_views_exist():
    """Vérifier que les vues existent"""
    
    print("\n👁️ VÉRIFICATION DES VUES DANS agents/views.py")
    print("=" * 50)
    
    file_path = 'agents/views.py'
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        views_to_check = [
            'def creer_bon_soin_membre(',
            'def confirmation_bon_soin('
        ]
        
        for view in views_to_check:
            if view in content:
                print(f"✅ {view} trouvée")
            else:
                print(f"❌ {view} NON trouvée")
                
    except Exception as e:
        print(f"❌ Erreur lecture views.py: {e}")

def check_urls_module():
    """Vérifier que le module URLs peut être importé"""
    
    print("\n🔄 TEST D'IMPORT DU MODULE URLs")
    print("=" * 50)
    
    try:
        from agents import urls as agents_urls
        print("✅ Module agents.urls importé avec succès")
        
        # Compter le nombre d'URLs
        url_count = len(agents_urls.urlpatterns)
        print(f"✅ {url_count} URLs trouvées dans le module")
        
        # Lister toutes les URLs
        print("\n📋 LISTE DE TOUTES LES URLs:")
        for pattern in agents_urls.urlpatterns:
            print(f"   - {pattern.name} -> {pattern.pattern}")
            
    except Exception as e:
        print(f"❌ Erreur import agents.urls: {e}")

if __name__ == "__main__":
    print("🎯 DÉBOGAGE COMPLET DES URLs AGENTS")
    print("=" * 60)
    
    debug_urls()
    check_urls_file()
    check_views_exist()
    check_urls_module()
    
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ DU DÉBOGAGE TERMINÉ")