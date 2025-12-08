#!/usr/bin/env python3
"""
Nettoyage spécifique des templates agent
"""

from pathlib import Path
import shutil

class AgentTemplatesCleaner:
    def __init__(self, agents_dir="templates/agents"):
        self.agents_dir = Path(agents_dir)
        
    def clean_backup_files(self):
        """Nettoyer les fichiers de backup"""
        backup_patterns = [
            '*.backup*',
            '*backup*.html',
            '*consolidation_backup*'
        ]
        
        backup_files = []
        for pattern in backup_patterns:
            backup_files.extend(self.agents_dir.rglob(pattern))
        
        print(f"🗑️  Fichiers de backup trouvés: {len(backup_files)}")
        
        for file_path in backup_files:
            print(f"   📁 {file_path.relative_to(self.agents_dir.parent)}")
            file_path.unlink()
            
        return backup_files
    
    def consolidate_sidebars(self):
        """Consolider les sidebars dupliquées"""
        sidebar_files = list(self.agents_dir.rglob("*sidebar*agent*.html"))
        main_sidebar = self.agents_dir / "partials" / "_sidebar_agent.html"
        
        if main_sidebar.exists():
            # Garder seulement la sidebar principale
            for sidebar in sidebar_files:
                if sidebar != main_sidebar and 'backup' not in sidebar.name:
                    print(f"🔄 Consolidation: {sidebar.name} → {main_sidebar.name}")
                    # Option: copier le contenu de la version updated si elle est meilleure
                    if 'updated' in sidebar.name:
                        shutil.copy2(sidebar, main_sidebar)
                    sidebar.unlink()
    
    def check_template_dependencies(self):
        """Vérifier les dépendances entre templates agent"""
        dependencies = {}
        
        for file_path in self.agents_dir.rglob("*.html"):
            if file_path.name.endswith('.backup') or 'backup' in file_path.name:
                continue
                
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Trouver les includes vers d'autres templates agent
            includes = re.findall(r'\{%\s*include\s+[\'"]([^\'"]+)[\'"]\s*%\}', content)
            agent_includes = [inc for inc in includes if 'agent' in inc or 'partials' in inc]
            
            if agent_includes:
                dependencies[str(file_path.relative_to(self.agents_dir))] = agent_includes
        
        return dependencies

def main():
    cleaner = AgentTemplatesCleaner()
    
    print("🧹 NETTOYAGE DES TEMPLATES AGENT")
    print("=" * 50)
    
    # 1. Nettoyer les backups
    print("\n1. Nettoyage des fichiers de backup...")
    backups = cleaner.clean_backup_files()
    print(f"   ✅ {len(backups)} fichiers supprimés")
    
    # 2. Consolider les sidebars
    print("\n2. Consolidation des sidebars...")
    cleaner.consolidate_sidebars()
    
    # 3. Vérifier les dépendances
    print("\n3. Vérification des dépendances...")
    dependencies = cleaner.check_template_dependencies()
    
    if dependencies:
        print("   📋 Dépendances internes trouvées:")
        for template, deps in dependencies.items():
            print(f"      {template} → {', '.join(deps)}")
    else:
        print("   ✅ Aucune dépendance interne problématique")

if __name__ == "__main__":
    main()