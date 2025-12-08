# find_fix_ordonnance.py
import os
import re

def find_and_fix_ordonnance():
    """Trouve et corrige les références à liste_ordonnance"""
    
    print("🔍 RECHERCHE DE 'liste_ordonnance' DANS LES TEMPLATES")
    print("=" * 60)
    
    templates_dir = 'templates'
    problem_files = []
    
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Chercher liste_ordonnance
                    if 'liste_ordonnance' in content:
                        problem_files.append(file_path)
                        print(f"❌ PROBLEME dans: {file_path}")
                        
                        # Afficher le contexte
                        lines = content.split('\n')
                        for i, line in enumerate(lines, 1):
                            if 'liste_ordonnance' in line:
                                print(f"   Ligne {i}: {line.strip()}")
                
                except Exception as e:
                    print(f"⚠️  Erreur lecture {file_path}: {e}")
    
    if problem_files:
        print(f"\n🚨 {len(problem_files)} FICHIERS AVEC LE PROBLÈME:")
        for file in problem_files:
            print(f"   - {file}")
        
        print(f"\n💡 CORRECTION AUTOMATIQUE...")
        fix_ordonnance_references(problem_files)
    else:
        print("✅ Aucun problème trouvé!")

def fix_ordonnance_references(problem_files):
    """Corrige automatiquement les références"""
    
    for file_path in problem_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remplacer liste_ordonnance par pharmacien:liste_ordonnances_attente
            new_content = content.replace(
                "{% url 'liste_ordonnance' %}",
                "{% url 'pharmacien:liste_ordonnances_attente' %}"
            )
            
            new_content = new_content.replace(
                "{% url 'pharmacien:liste_ordonnance' %}",
                "{% url 'pharmacien:liste_ordonnances_attente' %}"
            )
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ CORRIGÉ: {file_path}")
            else:
                print(f"ℹ️  Aucune correction nécessaire: {file_path}")
                
        except Exception as e:
            print(f"❌ Erreur correction {file_path}: {e}")

if __name__ == "__main__":
    find_and_fix_ordonnance()