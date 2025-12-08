# Script pour analyser tous les imports

import os
import re

external_packages = set()

# Packages Django standards qu'on peut ignorerpip install openpyxl
django_std = {'django', 'os', 'sys', 'datetime', 'time', 'json', 'decimal', 'logging'}

for root, dirs, files in os.walk('.'):
    if '__pycache__' in root or 'migrations' in root or 'venv' in root:
        continue
        
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Trouver les imports
                    imports = re.findall(r'^(?:import|from)\s+([a-zA-Z0-9_\.]+)', content, re.MULTILINE)
                    
                    for imp in imports:
                        # Nettoyer le nom du package
                        pkg = imp.split('.')[0]
                        if pkg and pkg not in django_std and not pkg.startswith('_'):
                            external_packages.add(pkg)
                            
            except Exception as e:
                print(f"Erreur lecture {filepath}: {e}")

print("Packages externes détectés:")
for pkg in sorted(external_packages):
    print(f"- {pkg}")


