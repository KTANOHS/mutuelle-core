#!/usr/bin/env python
"""
DIAGNOSTIC RAPIDE RENDER
À exécuter sur votre machine locale avant déploiement
"""

import sys
import os
from pathlib import Path

def check_file(file_path, required=True):
    """Vérifie si un fichier existe"""
    exists = Path(file_path).exists()
    status = "✅" if exists else "❌"
    print(f"{status} {file_path}")
    
    if not exists and required:
        print(f"   ⚠️  FICHIER REQUIS MANQUANT!")
        return False
    return True

def main():
    print("🔍 DIAGNOSTIC RAPIDE POUR RENDER")
    print("=" * 50)
    
    # Fichiers essentiels
    print("\n📁 FICHIERS ESSENTIELS:")
    essential_files = [
        "manage.py",
        "requirements.txt",
        "app.py",
        "mutuelle_core/wsgi.py",
        "mutuelle_core/settings.py",
        "Procfile" if Path("Procfile").exists() else None,
        "render.yaml" if Path("render.yaml").exists() else None,
        "runtime.txt" if Path("runtime.txt").exists() else None,
    ]
    
    all_ok = True
    for file in filter(None, essential_files):
        if not check_file(file):
            all_ok = False
    
    # Vérifier les dossiers
    print("\n📁 DOSSIERS:")
    directories = [
        "static",
        "staticfiles",
        "mutuelle_core",
    ]
    
    for directory in directories:
        exists = Path(directory).exists()
        status = "✅" if exists else "⚠️"
        print(f"{status} {directory}/")
    
    # Vérifier les dépendances critiques
    print("\n📦 DÉPENDANCES CRITIQUES (requirements.txt):")
    critical_deps = ["Django", "gunicorn", "whitenoise", "psycopg2-binary"]
    
    if Path("requirements.txt").exists():
        with open("requirements.txt", 'r') as f:
            content = f.read()
        
        for dep in critical_deps:
            if dep.lower() in content.lower():
                print(f"✅ {dep}")
            else:
                print(f"❌ {dep} (MANQUANT)")
                all_ok = False
    else:
        print("❌ requirements.txt non trouvé")
        all_ok = False
    
    # Vérifier la configuration Django basique
    print("\n⚙️  CONFIGURATION DJANGO:")
    try:
        sys.path.append(os.getcwd())
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        
        import django
        django.setup()
        
        from django.conf import settings
        
        checks = [
            ("DEBUG", settings.DEBUG, "Devrait être False en production"),
            ("ALLOWED_HOSTS", settings.ALLOWED_HOSTS, "Doit contenir .onrender.com"),
            ("STATIC_ROOT", settings.STATIC_ROOT, "Doit être défini"),
            ("SECRET_KEY", settings.SECRET_KEY, "Ne doit pas être la valeur par défaut"),
        ]
        
        for name, value, comment in checks:
            if name == "DEBUG":
                ok = not value
            elif name == "ALLOWED_HOSTS":
                ok = any('.onrender.com' in host for host in value) or len(value) == 0 or '*' in value
            elif name == "STATIC_ROOT":
                ok = bool(value)
            elif name == "SECRET_KEY":
                ok = value and 'django-insecure-' not in value
            else:
                ok = bool(value)
            
            status = "✅" if ok else "❌"
            print(f"{status} {name}: {value}")
            if not ok:
                print(f"   💡 {comment}")
                all_ok = False
                
    except Exception as e:
        print(f"❌ Impossible de charger Django: {e}")
        all_ok = False
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 50)
    
    if all_ok:
        print("🎉 VOTRE APPLICATION EST PRÊTE POUR RENDER!")
        print("\nProchaines étapes:")
        print("1. git add .")
        print("2. git commit -m 'Prêt pour déploiement'")
        print("3. git push origin main")
        print("4. Render déploiera automatiquement")
    else:
        print("🚨 DES PROBLÈMES ONT ÉTÉ IDENTIFIÉS")
        print("\nActions recommandées:")
        print("1. Corrigez les fichiers manquants")
        print("2. Vérifiez requirements.txt")
        print("3. Vérifiez la configuration Django")
        print("4. Exécutez à nouveau ce diagnostic")
        
        # Générer un fichier de correction
        with open("render_fixes.txt", "w") as f:
            f.write("Problèmes identifiés:\n")
            f.write("1. Vérifiez que tous les fichiers essentiels existent\n")
            f.write("2. Assurez-vous que requirements.txt contient:\n")
            f.write("   Django>=4.0\n   gunicorn\n   whitenoise\n   psycopg2-binary\n")
            f.write("3. Dans settings.py, assurez-vous que:\n")
            f.write("   DEBUG = False\n   ALLOWED_HOSTS = ['*'] ou contient .onrender.com\n")
            f.write("   STATIC_ROOT est défini\n   SECRET_KEY est définie\n")
        
        print(f"\n📝 Liste des corrections dans: render_fixes.txt")

if __name__ == "__main__":
    main()