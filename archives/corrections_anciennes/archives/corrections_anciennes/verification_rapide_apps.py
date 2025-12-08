#!/usr/bin/env python
"""
VÉRIFICATION RAPIDE - AGENTS & COMMUNICATION
Vérification express de l'état des applications
"""

import os
import sys
from pathlib import Path

def verifier_structure_app(nom_app):
    """Vérification rapide de la structure d'une application"""
    print(f"\n🔍 VÉRIFICATION {nom_app.upper()}")
    print("-" * 30)
    
    chemin_app = Path(nom_app)
    if not chemin_app.exists():
        print(f"❌ Dossier {nom_app} non trouvé")
        return False
    
    fichiers_requis = ['models.py', 'views.py', 'urls.py', 'admin.py', 'apps.py']
    tous_ok = True
    
    for fichier in fichiers_requis:
        if (chemin_app / fichier).exists():
            print(f"✅ {fichier}")
        else:
            print(f"❌ {fichier}")
            tous_ok = False
    
    # Vérifier les migrations
    migrations_dir = chemin_app / 'migrations'
    if migrations_dir.exists():
        migrations = list(migrations_dir.glob('0*.py'))
        print(f"📦 Migrations: {len(migrations)} fichiers")
    else:
        print("❌ Dossier migrations manquant")
        tous_ok = False
    
    # Vérifier les templates
    templates_dir = chemin_app / 'templates' / nom_app
    if templates_dir.exists():
        templates = list(templates_dir.glob('*.html'))
        print(f"🎨 Templates: {len(templates)} fichiers")
    else:
        print("⚠️  Dossier templates manquant")
    
    return tous_ok

def verifier_imports():
    """Vérification des imports"""
    print(f"\n📥 TEST DES IMPORTS")
    print("-" * 30)
    
    modules_a_tester = [
        'agents.models',
        'agents.views', 
        'agents.admin',
        'agents.urls',
        'communication.models',
        'communication.views',
        'communication.admin',
        'communication.urls'
    ]
    
    succes = 0
    echecs = 0
    
    for module in modules_a_tester:
        try:
            __import__(module)
            print(f"✅ {module}")
            succes += 1
        except ImportError as e:
            print(f"❌ {module}: {e}")
            echecs += 1
        except Exception as e:
            print(f"⚠️  {module}: {e}")
            echecs += 1
    
    print(f"\n📊 RÉSULTAT: {succes}✅ / {echecs}❌")
    return echecs == 0

def verifier_settings():
    """Vérification rapide des settings"""
    print(f"\n⚙️  VÉRIFICATION SETTINGS")
    print("-" * 30)
    
    try:
        # Essayer d'importer settings
        from django.conf import settings
        
        apps_requises = ['agents', 'communication', 'channels']
        apps_trouvees = [app for app in apps_requises if app in settings.INSTALLED_APPS]
        
        print(f"📋 Applications dans INSTALLED_APPS:")
        for app in apps_requises:
            if app in settings.INSTALLED_APPS:
                print(f"   ✅ {app}")
            else:
                print(f"   ❌ {app}")
        
        print(f"\n🔌 Configuration Channels:")
        asgi_app = getattr(settings, 'ASGI_APPLICATION', None)
        print(f"   • ASGI_APPLICATION: {'✅' if asgi_app else '❌'}")
        
        return len(apps_trouvees) == len(apps_requises)
        
    except Exception as e:
        print(f"❌ Impossible de vérifier settings: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 VÉRIFICATION RAPIDE - AGENTS & COMMUNICATION")
    print("=" * 50)
    
    # Vérifier structure
    agents_ok = verifier_structure_app('agents')
    communication_ok = verifier_structure_app('communication')
    
    # Vérifier imports
    imports_ok = verifier_imports()
    
    # Vérifier settings
    settings_ok = verifier_settings()
    
    # Résumé final
    print(f"\n🎯 RÉSUMÉ FINAL")
    print("=" * 30)
    print(f"📁 Structure agents: {'✅' if agents_ok else '❌'}")
    print(f"📁 Structure communication: {'✅' if communication_ok else '❌'}")
    print(f"📥 Imports: {'✅' if imports_ok else '❌'}")
    print(f"⚙️  Settings: {'✅' if settings_ok else '❌'}")
    
    if all([agents_ok, communication_ok, imports_ok, settings_ok]):
        print(f"\n🎉 TOUT EST OK! Les applications sont prêtes.")
    else:
        print(f"\n⚠️  Des problèmes ont été détectés. Vérifiez les points en erreur.")

if __name__ == "__main__":
    # Ajouter le chemin du projet
    sys.path.append(str(Path(__file__).parent))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    
    try:
        import django
        django.setup()
    except:
        print("⚠️  Django non configuré - vérification limitée")
    
    main()