import os
import importlib
import django
import subprocess
from datetime import datetime
from pathlib import Path

# 🔧 Configuration de base
BASE_DIR = Path(__file__).resolve().parent
SETTINGS_PATH = BASE_DIR / "mutuelle_core" / "settings.py"
RAPPORT_PATH = BASE_DIR / "rapport_analyse.html"

def print_header():
    print("\n🔍 ANALYSE COMPLÈTE DU PROJET DJANGO MUTUELLE")
    print("=" * 70)

def check_django_settings():
    print(f"\n➡️ Vérification du fichier settings.py : {SETTINGS_PATH}")
    if SETTINGS_PATH.exists():
        print("✅ settings.py trouvé")
    else:
        print("❌ settings.py manquant")

def get_installed_apps():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    django.setup()
    from django.conf import settings
from django.utils import timezone
    return settings.INSTALLED_APPS

def check_apps(apps):
    print("\n➡️ Vérification des applications locales...")
    results = []
    for app in apps:
        if app.startswith("django.") or app.startswith("rest_framework") or "corsheaders" in app:
            continue
        app_path = BASE_DIR / app.replace(".", "/")
        if app_path.exists():
            results.append((app, "✅ OK"))
        else:
            results.append((app, "❌ Dossier manquant"))
    return results

def check_files(app_name):
    required_files = ["models.py", "views.py", "urls.py"]
    app_path = BASE_DIR / app_name.replace(".", "/")
    missing = [f for f in required_files if not (app_path / f).exists()]
    return missing

def check_imports(app_name):
    try:
        importlib.import_module(app_name)
        return "✅ Import OK"
    except Exception as e:
        return f"❌ Erreur import: {e}"

def check_migrations():
    print("\n➡️ Vérification des migrations...")
    result = subprocess.run(["python", "manage.py", "showmigrations"], capture_output=True, text=True)
    if " [ ] " in result.stdout:
        return "⚠️ Des migrations ne sont pas appliquées"
    else:
        return "✅ Toutes les migrations sont à jour"

def generate_html_report(app_results, migration_status):
    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Rapport d’analyse du projet Mutuelle</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f9f9f9; padding: 20px; }}
            h1 {{ color: #0a5275; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            th {{ background: #0a5275; color: white; }}
            tr:nth-child(even) {{ background: #f2f2f2; }}
            .ok {{ color: green; font-weight: bold; }}
            .warn {{ color: orange; font-weight: bold; }}
            .err {{ color: red; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>📊 Rapport d’analyse du projet Mutuelle</h1>
        <p>Généré le {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <h2>📁 Applications locales</h2>
        <table>
            <tr><th>Application</th><th>Statut</th><th>Fichiers manquants</th><th>Import</th></tr>
    """

    for app, status, missing, imp in app_results:
        html += f"<tr><td>{app}</td><td>{status}</td><td>{', '.join(missing) if missing else 'Aucun'}</td><td>{imp}</td></tr>"

    html += f"""
        </table>
        <h2>⚙️ Migrations</h2>
        <p>{migration_status}</p>
    </body>
    </html>
    """

    RAPPORT_PATH.write_text(html, encoding='utf-8')
    print(f"\n📄 Rapport HTML généré : {RAPPORT_PATH}")

def main():
    print_header()
    check_django_settings()

    try:
        apps = get_installed_apps()
    except Exception as e:
        print(f"❌ Erreur d’import des settings Django : {e}")
        return

    app_results = []
    for app in apps:
        if not app.startswith("django.") and "rest_framework" not in app:
            app_path = BASE_DIR / app.replace(".", "/")
            if app_path.exists():
                status = "✅ OK"
                missing_files = check_files(app)
                imp_status = check_imports(app)
            else:
                status = "❌ Dossier manquant"
                missing_files = []
                imp_status = "N/A"
            app_results.append((app, status, missing_files, imp_status))

    migration_status = check_migrations()
    generate_html_report(app_results, migration_status)

    print("\n🎯 Analyse terminée avec succès !")

if __name__ == "__main__":
    main()
