# analyser_apps.py
import os
import sys
from pathlib import Path
import django
from django.apps import apps
from django.core.management import call_command

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

APPS_TO_ANALYSE = ['assureur', 'medecin']
RAPPORT_HTML = BASE_DIR / 'rapport_apps.html'
DOT_FILE = BASE_DIR / 'apps_models.dot'

def analyse_models(app_names):
    print("🔍 Analyse des modèles Django pour les apps:", ", ".join(app_names))
    
    total_models = 0
    total_relations = 0
    warnings = []

    with open(RAPPORT_HTML, 'w', encoding='utf-8') as f:
        f.write("<html><head><title>Rapport Analyse Apps</title></head><body>\n")
        f.write(f"<h1>Analyse Apps Django : {', '.join(app_names)}</h1>\n")
        f.write("<ul>\n")
        
        for app_label in app_names:
            try:
                app_config = apps.get_app_config(app_label)
            except LookupError:
                print(f"⚠️ App '{app_label}' non trouvée !")
                f.write(f"<li>⚠️ App '{app_label}' non trouvée</li>\n")
                continue

            f.write(f"<li><strong>{app_label}</strong>\n<ul>\n")
            for model in app_config.get_models():
                total_models += 1
                fields = model._meta.get_fields()
                relations = [f for f in fields if f.is_relation]
                total_relations += len(relations)
                
                f.write(f"<li>{model.__name__} ({len(relations)} relations)</li>\n")
                
                # Warnings simplifiés
                for field in fields:
                    if field.is_relation and not field.related_model:
                        warnings.append(f"{model.__name__}.{field.name} -> relation manquante")
            f.write("</ul></li>\n")
        
        f.write("</ul>\n")
        f.write(f"<p>Total modèles: {total_models}</p>\n")
        f.write(f"<p>Total relations: {total_relations}</p>\n")
        f.write(f"<p>Warnings détectés: {len(warnings)}</p>\n")
        if warnings:
            f.write("<ul>")
            for w in warnings:
                f.write(f"<li>{w}</li>")
            f.write("</ul>")
        f.write("</body></html>")

    print(f"✅ Rapport HTML généré : {RAPPORT_HTML}")

    # Génération DOT pour Graphviz
    try:
        from django_extensions.management.commands.graph_models import Command
        cmd = Command()
        cmd.handle(apps=app_names, output=str(DOT_FILE), verbose=True, group_models=True)
        print(f"✅ Fichier DOT généré : {DOT_FILE}")
        print("ℹ️ Pour générer un SVG : dot -Tsvg apps_models.dot -o apps_models.svg")
    except ImportError:
        print("⚠️ django-extensions non installé, impossible de générer DOT")
    except Exception as e:
        print(f"⚠️ Erreur génération DOT: {e}")


if __name__ == "__main__":
    analyse_models(APPS_TO_ANALYSE)
