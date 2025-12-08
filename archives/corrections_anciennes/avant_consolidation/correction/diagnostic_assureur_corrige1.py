#!/usr/bin/env python3
"""
Script de diagnostic corrigé pour l'application assureur
Utilise mutuelle_core.settings au lieu de core.settings
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    DJANGO_LOADED = True
    print("✅ Django chargé avec mutuelle_core.settings")
except Exception as e:
    print(f"⚠️  Django non chargé: {e}")
    print("🔄 Tentative avec core.settings...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
        django.setup()
        DJANGO_LOADED = True
        print("✅ Django chargé avec core.settings")
    except Exception as e2:
        print(f"❌ Django non chargé: {e2}")
        DJANGO_LOADED = False

BASE_DIR = Path(__file__).resolve().parent.parent

def verifier_installation_assureur():
    """Vérifie si l'app assureur est bien installée"""
    print("\n" + "="*80)
    print("VÉRIFICATION INSTALLATION ASSUREUR")
    print("="*80)
    
    if not DJANGO_LOADED:
        print("❌ Django non chargé - vérification impossible")
        return
    
    try:
        from django.apps import apps
        
        # Vérifier si l'app assureur est dans INSTALLED_APPS
        assureur_installe = apps.is_installed('assureur')
        
        if assureur_installe:
            print("✅ L'app 'assureur' est dans INSTALLED_APPS")
            
            # Vérifier les modèles
            try:
                from assureur import models
                model_count = len([m for m in dir(models) if m.endswith('_') and not m.startswith('_')])
                print(f"✅ Modèles trouvés: {model_count}")
                
                # Lister les modèles
                print("\n📋 Modèles de l'assureur:")
                for attr_name in dir(models):
                    attr = getattr(models, attr_name)
                    if hasattr(attr, '_meta') and hasattr(attr._meta, 'app_label'):
                        if attr._meta.app_label == 'assureur':
                            print(f"  - {attr.__name__}: {attr._meta.db_table}")
                
            except Exception as e:
                print(f"❌ Erreur import modèles: {e}")
        
        else:
            print("❌ L'app 'assureur' n'est pas dans INSTALLED_APPS")
            
            # Vérifier si elle existe physiquement
            assureur_dir = BASE_DIR / "assureur"
            if assureur_dir.exists():
                print("⚠️  L'app existe physiquement mais n'est pas dans INSTALLED_APPS")
                print("📌 Ajoutez 'assureur.apps.AssureurConfig' à INSTALLED_APPS dans settings.py")
            else:
                print("❌ L'app n'existe même pas physiquement")
    
    except Exception as e:
        print(f"❌ Erreur vérification installation: {e}")

def analyser_urls_assureur():
    """Analyse les URLs de l'assureur"""
    print("\n" + "="*80)
    print("ANALYSE URLs ASSUREUR")
    print("="*80)
    
    urls_file = BASE_DIR / "assureur" / "urls.py"
    
    if urls_file.exists():
        try:
            with open(urls_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier la structure
            if 'urlpatterns' not in content:
                print("❌ 'urlpatterns' non défini dans urls.py")
                
                # Analyser le contenu pour voir ce qu'il y a
                lines = content.split('\n')
                print(f"\n📄 Contenu de urls.py ({len(lines)} lignes):")
                for i, line in enumerate(lines[:20]):  # Afficher les 20 premières lignes
                    print(f"  {i+1}: {line}")
                
                if len(lines) > 20:
                    print(f"  ... et {len(lines)-20} lignes supplémentaires")
                
                return
            
            # Extraire les URLs
            import re
            
            # Chercher les patterns path
            path_patterns = re.findall(r"path\s*\(\s*'([^']+)'", content)
            
            print(f"🔗 URLs définies: {len(path_patterns)}")
            for pattern in path_patterns:
                print(f"  - {pattern}")
            
            # Chercher le namespace (app_name)
            app_name_match = re.search(r"app_name\s*=\s*['\"]([^'\"]+)['\"]", content)
            if app_name_match:
                print(f"📌 Namespace: {app_name_match.group(1)}")
            else:
                print("⚠️  Namespace non défini (app_name manquant)")
        
        except Exception as e:
            print(f"❌ Erreur analyse URLs: {e}")
    else:
        print("❌ Fichier urls.py non trouvé")

def verifier_vues_assureur():
    """Vérifie les vues de l'assureur"""
    print("\n" + "="*80)
    print("VÉRIFICATION VUES ASSUREUR")
    print("="*80)
    
    if not DJANGO_LOADED:
        print("❌ Django non chargé - vérification impossible")
        return
    
    try:
        from assureur import views
        
        # Compter les fonctions de vue
        view_functions = []
        for attr_name in dir(views):
            attr = getattr(views, attr_name)
            if callable(attr) and not attr_name.startswith('_'):
                view_functions.append(attr_name)
        
        print(f"🔍 Fonctions de vue trouvées: {len(view_functions)}")
        
        # Afficher les principales vues
        vue_categories = {
            "Dashboard": ['dashboard_assureur'],
            "Membres": ['liste_membres', 'detail_membre', 'creer_membre', 'recherche_membre'],
            "Bons": ['liste_bons', 'detail_bon', 'creer_bon', 'valider_bon', 'rejeter_bon'],
            "Cotisations": ['liste_cotisations', 'generer_cotisations', 'preview_generation'],
            "Paiements": ['liste_paiements', 'creer_paiement', 'detail_paiement'],
            "Statistiques": ['statistiques_assureur', 'rapports', 'generer_rapport'],
            "API": ['api_statistiques', 'api_recherche_membre', 'api_creer_bon'],
            "Messagerie": ['messagerie_assureur', 'envoyer_message_assureur'],
        }
        
        for categorie, vues_attendues in vue_categories.items():
            vues_trouvees = [v for v in vues_attendues if v in view_functions]
            print(f"\n📁 {categorie}: {len(vues_trouvees)}/{len(vues_attendues)}")
            for vue in vues_trouvees:
                print(f"  ✅ {vue}")
            for vue in set(vues_attendues) - set(vues_trouvees):
                print(f"  ❌ {vue} (manquante)")
    
    except Exception as e:
        print(f"❌ Erreur vérification vues: {e}")

def verifier_templates_assureur():
    """Vérifie les templates de l'assureur"""
    print("\n" + "="*80)
    print("VÉRIFICATION TEMPLATES ASSUREUR")
    print("="*80)
    
    templates_dir = BASE_DIR / "templates" / "assureur"
    
    if templates_dir.exists():
        # Compter les templates
        templates = list(templates_dir.rglob("*.html"))
        
        print(f"🎨 Templates HTML trouvés: {len(templates)}")
        
        # Grouper par catégorie
        categories = {}
        for template in templates:
            rel_path = template.relative_to(templates_dir)
            parts = rel_path.parts
            
            if len(parts) > 1:
                categorie = parts[0]
            else:
                categorie = "racine"
            
            if categorie not in categories:
                categories[categorie] = []
            categories[categorie].append(rel_path)
        
        # Afficher par catégorie
        for categorie, fichiers in categories.items():
            print(f"\n📁 {categorie}: {len(fichiers)} fichier(s)")
            for fichier in sorted(fichiers):
                size_kb = (templates_dir / fichier).stat().st_size / 1024
                print(f"  - {fichier} ({size_kb:.1f} KB)")
        
        # Vérifier les templates essentiels
        templates_essentiels = [
            "dashboard.html",
            "liste_membres.html",
            "detail_membre.html",
            "creer_membre.html",
            "liste_cotisations.html",
            "generer_cotisations.html",
            "statistiques.html",
            "configuration.html",
            "acces_interdit.html"
        ]
        
        print("\n🔍 Vérification templates essentiels:")
        for template in templates_essentiels:
            template_path = templates_dir / template
            if template_path.exists():
                print(f"  ✅ {template}")
            else:
                print(f"  ❌ {template} (manquant)")
    
    else:
        print("❌ Dossier templates/assureur non trouvé")

def tester_acces_vues():
    """Teste l'accès aux vues principales"""
    print("\n" + "="*80)
    print("TEST ACCÈS VUES")
    print("="*80)
    
    if not DJANGO_LOADED:
        print("❌ Django non chargé - test impossible")
        return
    
    try:
        from django.test import Client
        from django.contrib.auth.models import User
        
        client = Client()
        
        # Créer un utilisateur de test
        test_user, created = User.objects.get_or_create(
            username='test_assureur',
            defaults={'email': 'test@assureur.local', 'password': 'testpass123'}
        )
        
        if created:
            print("✅ Utilisateur de test créé")
        else:
            print("✅ Utilisateur de test existant")
        
        # Essayer de se connecter
        login_success = client.login(username='test_assureur', password='testpass123')
        print(f"🔐 Login réussi: {login_success}")
        
        # Tester quelques URLs
        urls_a_tester = [
            '/assureur/dashboard/',
            '/assureur/membres/',
            '/assureur/cotisations/',
            '/assureur/statistiques/',
        ]
        
        print("\n🌐 Test des URLs:")
        for url in urls_a_tester:
            try:
                response = client.get(url, follow=True)
                print(f"  {url}: HTTP {response.status_code} ({'OK' if response.status_code == 200 else 'ERREUR'})")
            except Exception as e:
                print(f"  {url}: ❌ Exception: {e}")
    
    except Exception as e:
        print(f"❌ Erreur test accès: {e}")

def generer_rapport_final():
    """Génère un rapport final"""
    print("\n" + "="*80)
    print("RAPPORT FINAL - ÉTAT DE L'APPLICATION ASSUREUR")
    print("="*80)
    
    # État général
    print("\n📊 ÉTAT GÉNÉRAL:")
    print(f"  • Django chargé: {'✅' if DJANGO_LOADED else '❌'}")
    print(f"  • Application assureur: {BASE_DIR / 'assureur'}")
    print(f"  • Templates assureur: {BASE_DIR / 'templates' / 'assureur'}")
    
    # Vérifier les fichiers critiques
    fichiers_critiques = {
        'models.py': BASE_DIR / "assureur" / "models.py",
        'views.py': BASE_DIR / "assureur" / "views.py",
        'urls.py': BASE_DIR / "assureur" / "urls.py",
        'forms.py': BASE_DIR / "assureur" / "forms.py",
        'admin.py': BASE_DIR / "assureur" / "admin.py",
    }
    
    print("\n📁 FICHIERS CRITIQUES:")
    for nom, chemin in fichiers_critiques.items():
        if chemin.exists():
            size_kb = chemin.stat().st_size / 1024
            print(f"  ✅ {nom}: {size_kb:.1f} KB")
        else:
            print(f"  ❌ {nom}: MANQUANT")
    
    # Recommandations
    print("\n📌 RECOMMANDATIONS:")
    
    if DJANGO_LOADED:
        print("  1. ✅ Django est correctement chargé")
        print("  2. ✅ L'application assureur semble complète")
        print("  3. 📝 Vérifiez que 'assureur.apps.AssureurConfig' est dans INSTALLED_APPS")
    else:
        print("  1. ❌ Corrigez le chargement de Django")
        print("  2. 📝 Vérifiez que mutuelle_core.settings existe")
        print("  3. 📝 Vérifiez les imports dans vos fichiers Python")
    
    print("  4. 🚀 Testez avec: python manage.py runserver")
    print("  5. 🔍 Accédez à: http://localhost:8000/assureur/dashboard/")
    
    # Commandes à exécuter
    print("\n🔧 COMMANDES À EXÉCUTER:")
    print(f"  cd \"{BASE_DIR}\"")
    print("  python manage.py makemigrations assureur")
    print("  python manage.py migrate")
    print("  python manage.py createsuperuser")
    print("  python manage.py runserver")

def main():
    """Fonction principale"""
    print("\n" + "="*80)
    print("🚀 DIAGNOSTIC CORRIGÉ - APPLICATION ASSUREUR")
    print("="*80)
    
    # Exécuter toutes les vérifications
    verifier_installation_assureur()
    analyser_urls_assureur()
    verifier_vues_assureur()
    verifier_templates_assureur()
    tester_acces_vues()
    generer_rapport_final()
    
    print("\n" + "="*80)
    print("✅ DIAGNOSTIC TERMINÉ")
    print("="*80)
    print("\n💡 Prochaine étape: exécutez 'python manage.py runserver' et testez l'application.")

if __name__ == "__main__":
    main()