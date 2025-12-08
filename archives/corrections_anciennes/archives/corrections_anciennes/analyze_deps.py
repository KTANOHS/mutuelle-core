
import ast
import os
from collections import defaultdict

def get_imports(filepath):
    """Extrait tous les imports d'un fichier Python"""
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=filepath)
        except:
            return set()
    
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
    return imports

# Packages à ignorer (standards Python)
STD_PACKAGES = {
    'os', 'sys', 'json', 'datetime', 'time', 're', 'math', 'decimal',
    'logging', 'collections', 'itertools', 'functools', 'pathlib'
}

external_deps = set()

for root, dirs, files in os.walk('.'):
    # Ignorer certains dossiers
    if any(x in root for x in ['__pycache__', 'migrations', 'venv', '.git']):
        continue
        
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            imports = get_imports(filepath)
            external_deps.update(imports - STD_PACKAGES)

print("=== DÉPENDANCES DÉTECTÉES ===")
for dep in sorted(external_deps):
    if not dep.startswith('_'):
        print(f"pip install {dep}")

print(f"\nTotal: {len(external_deps)} dépendances détectées")
