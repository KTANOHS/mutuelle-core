# check_invalid_filters_verbose.py
import os
import django
import re
from django.apps import apps
from django.db.models import Model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mutuelle_core.settings")
django.setup()

# Expressions à détecter dans le code
FILTER_PATTERNS = [
    r"\.filter\(([^)]*)\)",
    r"\.exclude\(([^)]*)\)",
    r"\.get\(([^)]*)\)",
]

def extract_keywords(expr):
    """Extrait les clés utilisées dans les filtres Django"""
    expr = expr.strip()
    if not expr:
        return []
    parts = re.split(r"[, ]+", expr)
    keys = []
    for p in parts:
        if '=' in p:
            k = p.split('=')[0]
            if '__' in k:
                keys.append(k.split('__')[0])
            else:
                keys.append(k)
    return keys

def get_model_fields(model):
    """Retourne la liste des champs valides pour un modèle Django"""
    return [f.name for f in model._meta.get_fields()]

def find_model_for_keyword(keyword):
    """Cherche tous les modèles qui contiennent ce champ"""
    matching_models = []
    for model in apps.get_models():
        if keyword in get_model_fields(model):
            matching_models.append(model.__name__)
    return matching_models

def analyze_file(filepath):
    """Analyse un fichier Python pour détecter les filtres ORM potentiellement invalides"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for pattern in FILTER_PATTERNS:
        for match in re.finditer(pattern, content):
            expr = match.group(1)
            keywords = extract_keywords(expr)
            if keywords:
                print(f"\n📄 {filepath}")
                print(f"🔍 Requête détectée : .filter({expr})")
                for key in keywords:
                    models_found = find_model_for_keyword(key)
                    if models_found:
                        print(f"   ✅ Champ '{key}' existe dans le(s) modèle(s) : {', '.join(models_found)}")
                    else:
                        print(f"   ⚠️ Champ '{key}' n’existe dans aucun modèle connu")

def run_scan():
    print("🔎 Scan du projet Django pour détecter les filtres ORM invalides (version verbose)...\n")
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py") and not file.startswith("migrations"):
                analyze_file(os.path.join(root, file))
    print("\n✅ Scan terminé !")

if __name__ == "__main__":
    run_scan()
