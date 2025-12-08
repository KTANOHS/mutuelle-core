# quick_diagnostic.py
import os
import sys
from pathlib import Path

print("🔍 DIAGNOSTIC RAPIDE")
print("=" * 50)

proj_dir = Path.cwd()
print(f"Projet: {proj_dir.name}")
print(f"Chemin: {proj_dir}")

# Vérifier la structure
print("\n📁 STRUCTURE:")
for item in proj_dir.iterdir():
    if item.is_dir():
        print(f"  📂 {item.name}/")
    else:
        print(f"  📄 {item.name}")

# Vérifier mutuelle_core
print("\n📦 MUTUELLE_CORE:")
core_dir = proj_dir / "mutuelle_core"
if core_dir.exists():
    for item in core_dir.iterdir():
        if item.name.endswith('.py'):
            status = "✅" if item.exists() else "❌"
            print(f"  {status} {item.name}")
            
    # Vérifier le problème spécifique
    init_file = core_dir / "__init__.py"
    if init_file.exists():
        with open(init_file, 'r') as f:
            content = f.read()
            if "from .production import" in content:
                prod_file = core_dir / "production.py"
                if not prod_file.exists():
                    print("\n🚨 PROBLÈME DÉTECTÉ:")
                    print(f"  {init_file.name} importe production.py mais il n'existe pas!")
                    print("\n📋 FICHIERS DISPONIBLES:")
                    for f in core_dir.glob("*.py"):
                        if "prod" in f.name.lower() or "production" in f.name.lower():
                            print(f"  • {f.name}")

print("\n💡 SOLUTION:")
print("  Option 1: mv mutuelle_core/settings_prod.py mutuelle_core/production.py")
print("  Option 2: Modifier mutuelle_core/__init__.py pour utiliser settings_prod.py")
print("  Option 3: Créer mutuelle_core/production.py qui importe settings_prod.py")