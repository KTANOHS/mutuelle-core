# find_customloginview_usage.py
from pathlib import Path

def trouver_utilisation_customloginview():
    print("🔍 RECHERCHE DE L'UTILISATION DE CustomLoginView")
    print("=" * 60)
    
    project_path = Path(__file__).parent
    
    fichiers_concernes = []
    
    for py_file in project_path.rglob("*.py"):
        if 'venv' in str(py_file) or '__pycache__' in str(py_file):
            continue
            
        try:
            with open(py_file, 'r') as f:
                content = f.read()
            
            if 'CustomLoginView' in content:
                fichiers_concernes.append(py_file)
                print(f"📄 {py_file.relative_to(project_path)}")
                
                # Afficher le contexte
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'CustomLoginView' in line:
                        start = max(0, i-2)
                        end = min(len(lines), i+3)
                        print(f"   Lignes {start+1}-{end}:")
                        for j in range(start, end):
                            prefix = ">>> " if j == i else "    "
                            print(f"   {prefix}{lines[j]}")
                        print()
                        
        except Exception as e:
            print(f"❌ Erreur lecture {py_file}: {e}")
    
    print(f"\n📊 Total: {len(fichiers_concernes)} fichiers utilisent CustomLoginView")

if __name__ == "__main__":
    trouver_utilisation_customloginview()