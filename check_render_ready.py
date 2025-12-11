#!/usr/bin/env python
"""
VÉRIFICATION FINALE AVANT DÉPLOIEMENT RENDER
"""

import os
import sys
import subprocess
from pathlib import Path

def print_check(name, status, message=""):
    """Affiche une vérification"""
    icon = "✅" if status else "❌"
    print(f"{icon} {name}: {'PASS' if status else 'FAIL'} {message}")
    return status

def main():
    print("🔍 VÉRIFICATION ULTIME POUR RENDER")
    print("=" * 50)
    
    checks = []
    
    # 1. Fichiers essentiels
    essential_files = [
        "manage.py",
        "requirements.txt",
        "app.py",
        "start_render.sh",
        "render.yaml",
        "mutuelle_core/settings.py",
        "mutuelle_core/wsgi.py",
    ]
    
    for file in essential_files:
        exists = Path(file).exists()
        checks.append(print_check(f"Fichier {file}", exists))
    
    # 2. Vérifier app.py contient migrations
    if Path("app.py").exists():
        with open("app.py", 'r') as f:
            content = f.read()
            has_migrations = "apply_migrations" in content and "RENDER" in content
            checks.append(print_check("app.py migrations", has_migrations))
    
    # 3. Vérifier start_render.sh
    if Path("start_render.sh").exists():
        with open("start_render.sh", 'r') as f:
            content = f.read()
            has_gunicorn = "gunicorn app:application" in content
            has_migrate = "python manage.py migrate" in content
            checks.append(print_check("start_render.sh gunicorn", has_gunicorn))
            checks.append(print_check("start_render.sh migrate", has_migrate))
    
    # 4. Vérifier settings.py
    if Path("mutuelle_core/settings.py").exists():
        with open("mutuelle_core/settings.py", 'r') as f:
            content = f.read()
            has_onrender = ".onrender.com" in content
            has_render_check = "RENDER = os.environ.get" in content
            checks.append(print_check("settings.py .onrender.com", has_onrender))
            checks.append(print_check("settings.py RENDER check", has_render_check))
    
    # 5. Tester migrations
    try:
        result = subprocess.run(
            ["python", "manage.py", "migrate", "--noinput", "--check"],
            capture_output=True,
            text=True
        )
        migrations_ok = result.returncode == 0
        checks.append(print_check("Migrations test", migrations_ok))
    except Exception as e:
        checks.append(print_check("Migrations test", False, f"Erreur: {e}"))
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSULTAT FINAL:")
    print(f"   Total vérifications: {len(checks)}")
    print(f"   Vérifications passées: {sum(checks)}")
    print(f"   Vérifications échouées: {len(checks) - sum(checks)}")
    
    if all(checks):
        print("\n🎉 TOUT EST PRÊT POUR RENDER !")
        print("\nProchaines étapes:")
        print("1. git add .")
        print("2. git commit -m 'READY: Configuration ultime pour Render'")
        print("3. git push origin main")
        print("4. Render déploiera automatiquement")
        print("5. Surveillez les logs sur: https://dashboard.render.com")
        return True
    else:
        print("\n🚨 DES PROBLÈMES DOIVENT ÊTRE CORRIGÉS !")
        print("\nActions recommandées:")
        print("1. Vérifiez que tous les fichiers essentiels existent")
        print("2. Assurez-vous que app.py contient les migrations automatiques")
        print("3. Vérifiez que start_render.sh est correct")
        print("4. Vérifiez que settings.py contient .onrender.com")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)