# assureur/diagnostic_complet.py
import os
import django
import sys

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.template.loader import get_template
from django.urls import resolve, Resolver404
from django.conf import settings

def diagnostic_complet():
    print("=" * 60)
    print("🔍 DIAGNOSTIC COMPLET DU DASHBOARD ASSUREUR")
    print("=" * 60)
    
    # 1. Vérifier le template
    print("\n1. 📄 TEMPLATE DASHBOARD:")
    try:
        template = get_template('assureur/dashboard.html')
        print(f"   ✅ Template trouvé: {template.origin.name}")
        print(f"   📍 Chemin physique: {template.origin.loadname}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 2. Vérifier les URLs
    print("\n2. 🌐 URLs ASSUREUR:")
    urls_assureur = [
        '/assureur/dashboard/',
        '/assureur-dashboard/',
        '/assureur/',
    ]
    
    for url in urls_assureur:
        try:
            match = resolve(url)
            print(f"   {url} → {match.view_name} ({match.func.__module__}.{match.func.__name__})")
        except Resolver404:
            print(f"   {url} → ❌ NON TROUVÉ")
    
    # 3. Vérifier la structure des templates
    print("\n3. 📁 STRUCTURE DES TEMPLATES:")
    template_dirs = settings.TEMPLATES[0]['DIRS']
    for dir in template_dirs:
        if os.path.exists(dir):
            print(f"   📂 {dir}")
            assureur_path = os.path.join(dir, 'assureur')
            if os.path.exists(assureur_path):
                for file in os.listdir(assureur_path):
                    print(f"     📄 {file}")
    
    # 4. Vérifier l'app assureur
    print("\n4. 📦 APP ASSUREUR:")
    from django.apps import apps
    try:
        assureur_config = apps.get_app_config('assureur')
        print(f"   ✅ App trouvée: {assureur_config.path}")
        templates_path = os.path.join(assureur_config.path, 'templates', 'assureur')
        if os.path.exists(templates_path):
            print(f"   📁 Templates app: {templates_path}")
            for file in os.listdir(templates_path):
                print(f"     📄 {file}")
    except Exception as e:
        print(f"   ❌ Erreur app: {e}")

if __name__ == "__main__":
    diagnostic_complet()