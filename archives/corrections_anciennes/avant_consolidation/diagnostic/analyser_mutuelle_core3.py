#!/usr/bin/env python3
"""
analyser_mutuelle_core3.py
Analyse avancée des modèles Django + détection relations + rapport HTML + Dot (Graphviz).

Place ce fichier à la racine du projet (même dossier que manage.py) et exécute :
    source venv/bin/activate
    python analyser_mutuelle_core3.py
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import importlib
import textwrap
import html
from collections import defaultdict

# --- Configuration ---
BASE_DIR = Path(__file__).resolve().parent
REPORT_HTML = BASE_DIR / "rapport_analyse3.html"
DOT_FILE = BASE_DIR / "mutuelle_models.dot"
SVG_FILE = BASE_DIR / "mutuelle_models.svg"
DJANGO_SETTINGS_MODULE = "mutuelle_core.settings"

# --- Setup Django environment ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
try:
    import django
from django.utils import timezone
    django.setup()
    from django.apps import apps as django_apps
    from django.db import models as dj_models
    from django.conf import settings
except Exception as e:
    print("❌ Impossible d'initialiser Django. Vérifie DJANGO_SETTINGS_MODULE et l'environnement virtuel.")
    print("Erreur:", e)
    sys.exit(1)


def safe_str(s):
    return html.escape(str(s))


def collect_models_info():
    """Collecte des informations sur tous les modèles installés."""
    model_infos = []
    relations = []  # tuples (from_model, to_model, relation_type, field_name)
    for model in django_apps.get_models():
        model_label = f"{model._meta.app_label}.{model.__name__}"
        fields_info = []
        for field in model._meta.get_fields():
            # On affiche les champs concrets (Field) et les relations
            f_info = {
                "name": field.name,
                "type": type(field).__name__,
                "is_relation": getattr(field, "is_relation", False),
                "nullable": getattr(field, "null", None),
                "blank": getattr(field, "blank", None),
                "unique": getattr(field, "unique", False),
                "has_default": getattr(field, "default", dj_models.fields.NOT_PROVIDED) is not dj_models.fields.NOT_PROVIDED,
                "related_model": None,
                "related_name": getattr(field, "related_name", None),
            }

            if getattr(field, "is_relation", False):
                rel = getattr(field, "related_model", None)
                if rel is not None:
                    f_info["related_model"] = f"{rel._meta.app_label}.{rel.__name__}"
                    # classify relation type
                    if isinstance(field, dj_models.ForeignKey):
                        rel_type = "FK"
                    elif isinstance(field, dj_models.OneToOneField):
                        rel_type = "O2O"
                    elif isinstance(field, dj_models.ManyToManyField):
                        rel_type = "M2M"
                    else:
                        rel_type = "Relation"
                    relations.append((model_label, f_info["related_model"], rel_type, field.name))
            # For reverse relations (ManyToOneRel, ManyToManyRel) include them too:
            fields_info.append(f_info)
        # extra metadata
        model_meta = {
            "label": model_label,
            "app_label": model._meta.app_label,
            "model_name": model.__name__,
            "db_table": model._meta.db_table,
            "fields": fields_info,
        }
        model_infos.append(model_meta)
    return model_infos, relations


def check_model_warnings(model_infos):
    """Détecte problèmes/anti-patterns simples : BooleanField null=True, missing related_name, nullable ForeignKey without on_delete?"""
    warnings = []
    for m in model_infos:
        for f in m["fields"]:
            # boolean null True
            if f["type"] in ("BooleanField", "NullBooleanField") and f["nullable"]:
                warnings.append((m["label"], f["name"], "BooleanField with null=True (prefer default False/True)"))
            # ForeignKey nullable check
            if f["type"] == "ForeignKey" and f["nullable"] and f["related_model"]:
                warnings.append((m["label"], f["name"], "ForeignKey allows null=True — confirm this is intended"))
            # ManyToMany without related_name (only flags if blank/related_name is None)
            if f["type"] == "ManyToManyField" and (not f["related_name"]):
                warnings.append((m["label"], f["name"], "ManyToManyField without related_name (may be okay)"))
    return warnings


def check_migrations_status():
    """Utilise manage.py makemigrations --check pour savoir s'il manque des migrations."""
    manage_py = BASE_DIR / "manage.py"
    if not manage_py.exists():
        return "❌ manage.py introuvable; impossible de vérifier les migrations."
    cmd = [sys.executable, str(manage_py), "makemigrations", "--check", "--dry-run"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=BASE_DIR)
        out = proc.stdout + proc.stderr
        if proc.returncode == 0:
            return "✅ Aucune modification de modèles détectée — migrations à jour."
        else:
            # makemigrations --check renvoie un code != 0 quand des changements sont détectés
            return f"⚠️ Des changements de modèles détectés — exécute `python manage.py makemigrations`.\n\nSortie:\n{out}"
    except Exception as e:
        return f"❌ Échec de la vérification des migrations: {e}"


def generate_dot(relations):
    """Génère un fichier DOT décrivant les relations entre modèles."""
    dot_lines = [
        'digraph G {',
        '  rankdir=LR;',
        '  node [shape=record, fontsize=10];',
    ]
    models = set()
    for fr, to, rel_type, field_name in relations:
        models.add(fr)
        models.add(to)
    # create simple nodes
    for m in models:
        label = m.replace(".", "\\n")
        dot_lines.append(f'  "{m}" [label="{{{label}}}"];')
    # edges
    for fr, to, rel_type, field_name in relations:
        label = f"{rel_type}\\n{field_name}"
        style = 'solid'
        if rel_type == "M2M":
            style = 'dashed'
        dot_lines.append(f'  "{fr}" -> "{to}" [label="{label}", style="{style}"];')
    dot_lines.append("}")
    DOT_FILE.write_text("\n".join(dot_lines), encoding="utf-8")
    return DOT_FILE


def try_generate_svg(dot_path: Path, svg_path: Path):
    """Tente d'appeler graphviz 'dot' pour générer un svg depuis le dot."""
    try:
        res = subprocess.run(["dot", "-Tsvg", str(dot_path), "-o", str(svg_path)], capture_output=True, text=True)
        if res.returncode == 0 and svg_path.exists():
            return True, ""
        else:
            return False, (res.stdout + res.stderr).strip()
    except FileNotFoundError:
        return False, "Graphviz 'dot' non trouvé. Installe-le (ex: sudo apt install graphviz) pour générer le SVG."
    except Exception as e:
        return False, str(e)


def generate_html_report(model_infos, relations, warnings, migration_status, svg_inlined=None):
    date_str = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    html_parts = []
    html_parts.append(f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8"/>
<title>Rapport d'analyse avancée - Mutuelle</title>
<style>
  body {{ font-family: Arial, sans-serif; padding: 20px; background: #f7fbfc; color: #0b2b36; }}
  h1 {{ color:#0a5275; }}
  table {{ width:100%; border-collapse: collapse; margin-bottom: 18px; }}
  th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
  th {{ background: #0a5275; color: #fff; }}
  tr:nth-child(even) {{ background:#f2f2f2; }}
  .ok {{ color:green; font-weight:bold; }}
  .warn {{ color:orange; font-weight:bold; }}
  .err {{ color:red; font-weight:bold; }}
  .mono {{ font-family: monospace; font-size: 0.9em; }}
  .small {{ font-size:0.9em; color:#555; }}
  .container {{ max-width:1200px; margin: 0 auto; }}
</style>
</head>
<body>
<div class="container">
<h1>📊 Rapport d'analyse avancée du projet Mutuelle</h1>
<p class="small">Généré le {date_str}</p>
<hr/>
<h2>✅ Résumé migrations</h2>
<p class="mono">{html.escape(migration_status)}</p>
<hr/>
<h2>📦 Modèles détectés</h2>
""")

    # models table summary
    for m in sorted(model_infos, key=lambda x: x["label"]):
        html_parts.append(f"<h3>{safe_str(m['label'])} <small>table: {safe_str(m['db_table'])}</small></h3>")
        html_parts.append("<table><tr><th>Champ</th><th>Type</th><th>nullable</th><th>blank</th><th>unique</th><th>default</th><th>related_model</th></tr>")
        for f in m["fields"]:
            html_parts.append("<tr>")
            html_parts.append(f"<td>{safe_str(f['name'])}</td>")
            html_parts.append(f"<td>{safe_str(f['type'])}</td>")
            html_parts.append(f"<td>{safe_str(f.get('nullable'))}</td>")
            html_parts.append(f"<td>{safe_str(f.get('blank'))}</td>")
            html_parts.append(f"<td>{safe_str(f.get('unique'))}</td>")
            html_parts.append(f"<td>{'Oui' if f.get('has_default') else 'Non'}</td>")
            html_parts.append(f"<td>{safe_str(f.get('related_model') or '')}</td>")
            html_parts.append("</tr>")
        html_parts.append("</table>")

    # warnings
    html_parts.append("<hr/><h2>⚠️ Warnings et bonnes pratiques</h2>")
    if warnings:
        html_parts.append("<table><tr><th>Model</th><th>Champ</th><th>Message</th></tr>")
        for mdl, fld, msg in warnings:
            html_parts.append(f"<tr><td>{safe_str(mdl)}</td><td>{safe_str(fld)}</td><td class='warn'>{safe_str(msg)}</td></tr>")
        html_parts.append("</table>")
    else:
        html_parts.append("<p class='ok'>Aucun warning détecté.</p>")

    # relations graph
    html_parts.append("<hr/><h2>🔗 Relations entre modèles</h2>")
    if svg_inlined:
        html_parts.append("<div><h3>Graphe des relations (SVG généré)</h3>")
        html_parts.append(svg_inlined)
        html_parts.append("</div>")
    else:
        html_parts.append("<p class='small'>SVG non disponible. Un fichier DOT a été créé :</p>")
        html_parts.append(f"<p class='mono'>{safe_str(str(DOT_FILE))}</p>")
        html_parts.append("<p class='small'>Pour générer un SVG localement : <code>dot -Tsvg mutuelle_models.dot -o mutuelle_models.svg</code></p>")

    html_parts.append("<hr/><p class='small'>Fin du rapport.</p></div></body></html>")

    REPORT_HTML.write_text("\n".join(html_parts), encoding="utf-8")
    return REPORT_HTML


def main():
    print("🔍 Analyse avancée des modèles Django (mutuelle_core)")
    print("=" * 70)

    print("➡️ Collecte des modèles...")
    model_infos, relations = collect_models_info()
    print(f"   {len(model_infos)} modèles trouvés, {len(relations)} relations détectées.")

    print("➡️ Détection des warnings...")
    warnings = check_model_warnings(model_infos)
    print(f"   {len(warnings)} warnings détectés.")

    print("➡️ Vérification des migrations (makemigrations --check)...")
    migration_status = check_migrations_status()

    print("➡️ Génération du fichier DOT des relations:", DOT_FILE)
    generate_dot(relations)

    print("➡️ Tentative de génération SVG via Graphviz (dot)...")
    ok_svg, svg_msg = try_generate_svg(DOT_FILE, SVG_FILE)
    svg_inlined = None
    if ok_svg:
        print("   ✅ SVG généré:", SVG_FILE)
        try:
            svg_text = SVG_FILE.read_text(encoding="utf-8")
            # inline svg for HTML report
            svg_inlined = svg_text
        except Exception:
            svg_inlined = None
    else:
        print("   ⚠️ SVG non généré:", svg_msg)

    print("➡️ Génération du rapport HTML:", REPORT_HTML)
    generate_html_report(model_infos, relations, warnings, migration_status, svg_inlined=svg_inlined)

    print("\n🎯 Rapport généré :", REPORT_HTML)
    if not ok_svg:
        print("ℹ️ Si tu veux le graph SVG, installe graphviz puis exécute:")
        print("    dot -Tsvg mutuelle_models.dot -o mutuelle_models.svg")
    print("Terminé.")

if __name__ == "__main__":
    main()
