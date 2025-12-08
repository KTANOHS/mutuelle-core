# find_all_missing_views.py
import os
import sys
from pathlib import Path

def trouver_toutes_vues_manquantes():
    print("🔍 RECHERCHE DE TOUTES LES VUES MANQUANTES")
    print("=" * 60)
    
    project_path = Path(__file__).parent
    
    # 1. Analyser les URLs pour trouver toutes les vues référencées
    urls_path = project_path / "mutuelle_core" / "urls.py"
    print("1. 📋 VUES RÉFÉRENCÉES DANS LES URLs:")
    
    vues_referencees = set()
    
    if urls_path.exists():
        with open(urls_path, 'r') as f:
            urls_content = f.read()
        
        # Chercher les imports
        lines = urls_content.splitlines()
        for line in lines:
            if 'from' in line and 'import' in line and 'views' in line:
                # Extraire les noms des vues importées
                import_part = line.split('import')[-1].strip()
                vues_importees = [v.strip() for v in import_part.split(',')]
                for vue in vues_importees:
                    vues_referencees.add(vue)
                print(f"   📥 Importées: {', '.join(vues_importees)}")
        
        # Chercher les vues utilisées dans les paths
        for line in lines:
            if 'path(' in line and 'views.' in line:
                # Extraire le nom de la vue après views.
                if 'views.' in line:
                    vue_part = line.split('views.')[-1]
                    vue_name = vue_part.split(')')[0].split(',')[0].strip()
                    if vue_name and not vue_name.startswith('"') and not vue_name.startswith("'"):
                        vues_referencees.add(vue_name)
    
    # 2. Vérifier quelles vues existent dans views.py
    views_path = project_path / "mutuelle_core" / "views.py"
    print(f"\n2. 📄 VUES PRÉSENTES DANS views.py:")
    
    vues_existantes = set()
    
    if views_path.exists():
        with open(views_path, 'r') as f:
            views_content = f.read()
        
        # Chercher les définitions de fonctions
        lines = views_content.splitlines()
        for line in lines:
            if line.strip().startswith('def '):
                vue_name = line.split('def ')[1].split('(')[0].strip()
                vues_existantes.add(vue_name)
            elif line.strip().startswith('class '):
                vue_name = line.split('class ')[1].split('(')[0].split(':')[0].strip()
                vues_existantes.add(vue_name)
    
    print(f"   ✅ Existantes: {', '.join(sorted(vues_existantes))}")
    
    # 3. Identifier les vues manquantes
    vues_manquantes = vues_referencees - vues_existantes
    print(f"\n3. ❌ VUES MANQUANTES:")
    
    if vues_manquantes:
        for vue in sorted(vues_manquantes):
            print(f"   • {vue}")
    else:
        print("   ✅ Aucune vue manquante")
    
    return vues_manquantes

def analyser_autres_fichiers():
    print(f"\n4. 🔎 ANALYSE DES AUTRES FICHIERS:")
    print("=" * 40)
    
    project_path = Path(__file__).parent
    
    # Chercher d'autres références à des vues manquantes
    vues_trouvees = set()
    
    for py_file in project_path.rglob("*.py"):
        if 'venv' in str(py_file) or '__pycache__' in str(py_file) or 'test_' in str(py_file):
            continue
            
        try:
            with open(py_file, 'r') as f:
                content = f.read()
            
            # Chercher des références à des vues manquantes
            if 'redirect_to_user_dashboard' in content:
                vues_trouvees.add('redirect_to_user_dashboard')
                print(f"   📍 {py_file.relative_to(project_path)}")
                
        except Exception as e:
            if 'Is a directory' not in str(e):
                print(f"   ❌ Erreur lecture {py_file}: {e}")
    
    if vues_trouvees:
        print(f"   Vues référencées ailleurs: {', '.join(vues_trouvees)}")

if __name__ == "__main__":
    vues_manquantes = trouver_toutes_vues_manquantes()
    analyser_autres_fichiers()
    
    if vues_manquantes:
        print(f"\n🎯 EXÉCUTEZ: python fix_all_missing_views.py")