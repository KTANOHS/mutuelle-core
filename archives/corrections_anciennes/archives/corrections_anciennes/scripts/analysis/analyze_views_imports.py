#!/usr/bin/env python3
"""
Analyse les imports et dépendances des views
"""

import os
import ast
import importlib.util
from pathlib import Path

class ViewsImportAnalyzer:
    """Analyse les imports des modules de views"""
    
    def __init__(self, project_root='.'):
        self.project_root = Path(project_root)
        self.imports_data = {}
    
    def analyze_views_imports(self):
        """Analyse tous les imports des fichiers de views"""
        print("🔍 ANALYSE DES IMPORTS DES VIEWS")
        print("=" * 50)
        
        # Trouver tous les fichiers views.py
        views_files = list(self.project_root.rglob('views.py'))
        print(f"📁 Fichiers views.py trouvés: {len(views_files)}")
        
        for views_file in views_files:
            print(f"\n📄 Analyse de: {views_file.relative_to(self.project_root)}")
            self.analyze_file_imports(views_file)
    
    def analyze_file_imports(self, file_path):
        """Analyse les imports d'un fichier spécifique"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            imports = {
                'standard_imports': [],
                'django_imports': [],
                'internal_imports': [],
                'third_party_imports': []
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        import_name = alias.name
                        self._categorize_import(import_name, imports)
                
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for alias in node.names:
                        import_name = f"{module}.{alias.name}" if module else alias.name
                        self._categorize_import(import_name, imports)
            
            # Afficher les résultats
            self._display_imports(imports)
            
        except Exception as e:
            print(f"❌ Erreur analyse {file_path}: {e}")
    
    def _categorize_import(self, import_name, imports):
        """Catégorise un import"""
        if import_name.startswith('django.'):
            imports['django_imports'].append(import_name)
        elif any(import_name.startswith(pkg) for pkg in ['os', 'sys', 'json', 'datetime']):
            imports['standard_imports'].append(import_name)
        elif '.' not in import_name or import_name.startswith('.'):
            imports['internal_imports'].append(import_name)
        else:
            imports['third_party_imports'].append(import_name)
    
    def _display_imports(self, imports):
        """Affiche les imports catégorisés"""
        categories = [
            ('📚 Standards', 'standard_imports'),
            ('🎯 Django', 'django_imports'),
            ('🏠 Internes', 'internal_imports'),
            ('📦 Tierces', 'third_party_imports')
        ]
        
        for label, key in categories:
            items = imports[key]
            if items:
                print(f"   {label}: {len(items)} imports")
                for item in sorted(items)[:5]:  # Afficher les 5 premiers
                    print(f"      📌 {item}")
                if len(items) > 5:
                    print(f"      ... et {len(items) - 5} autres")

def main():
    """Fonction principale"""
    analyzer = ViewsImportAnalyzer()
    analyzer.analyze_views_imports()

if __name__ == "__main__":
    main()