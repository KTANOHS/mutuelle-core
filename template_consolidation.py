#!/usr/bin/env python3
"""
Script de consolidation des templates dupliqués
"""

import shutil
from pathlib import Path

class TemplateConsolidator:
    def __init__(self, templates_dir="templates"):
        self.templates_dir = Path(templates_dir)
        
    def consolidate_dashboards(self):
        """Consolider les dashboards multiples"""
        dashboard_mapping = {
            # Core dashboards
            'core/dashboard_updated.html': 'core/dashboard.html',
            'core/generic_dashboard.html': 'core/dashboard.html',
            
            # Agent dashboards
            'agents/dashboard.html': 'core/dashboard.html',  # Utiliser le core
            
            # Membre dashboards  
            'membres/dashboard.html': 'core/dashboard.html',
            
            # Autres rôles peuvent garder leur dashboard spécifique
        }
        
        return self._apply_consolidation(dashboard_mapping)
    
    def consolidate_sidebars(self):
        """Consolider les sidebars"""
        sidebar_mapping = {
            # Sidebars agents
            'agents/partials/_sidebar_agent_updated.html': 'agents/partials/_sidebar_agent.html',
            'agents/partials/_sidebar_agent.html.backup.20251022_113509': 'agents/partials/_sidebar_agent.html',
            
            # Sidebars médecins
            'medecin/partials/_sidebar_updated.html': 'medecin/partials/_sidebar.html',
            'medecin/partials/_sidebar.html.backup.20251022_113509': 'medecin/partials/_sidebar.html',
            
            # Sidebars pharmaciens
            'pharmacien/_sidebar_pharmacien_updated.html': 'pharmacien/_sidebar_pharmacien.html',
            'pharmacien/_sidebar_pharmacien.html.backup.20251022_113509': 'pharmacien/_sidebar_pharmacien.html',
            'pharmacien/_sidebar_pharmacien.html.backup.20251022_160354': 'pharmacien/_sidebar_pharmacien.html',
        }
        
        return self._apply_consolidation(sidebar_mapping)
    
    def _apply_consolidation(self, mapping):
        """Appliquer le plan de consolidation"""
        results = []
        
        for source, target in mapping.items():
            source_path = self.templates_dir / source
            target_path = self.templates_dir / target
            
            if source_path.exists():
                # Sauvegarder avant remplacement
                backup_path = source_path.with_suffix('.html.consolidation_backup')
                shutil.copy2(source_path, backup_path)
                
                # Remplacer par la version cible
                if target_path.exists():
                    shutil.copy2(target_path, source_path)
                    results.append(f"✓ {source} → {target}")
                else:
                    results.append(f"✗ Cible non trouvée: {target}")
        
        return results

def create_standard_structure():
    """Créer la structure standardisée recommandée"""
    standard_dirs = [
        'templates/base',
        'templates/components/forms',
        'templates/components/cards', 
        'templates/components/tables',
        'templates/components/sidebars',
        'templates/pages/dashboard',
        'templates/pages/communication',
        'templates/pages/gestion'
    ]
    
    for dir_path in standard_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"📁 Créé: {dir_path}")

if __name__ == "__main__":
    print("🔄 Début de la consolidation...")
    
    # Créer la structure standard
    create_standard_structure()
    
    # Consolider les templates
    consolidator = TemplateConsolidator()
    
    print("\n📊 Consolidation des dashboards:")
    results = consolidator.consolidate_dashboards()
    for result in results:
        print(f"  {result}")
    
    print("\n🧭 Consolidation des sidebars:")
    results = consolidator.consolidate_sidebars()
    for result in results:
        print(f"  {result}")
    
    print("\n✅ Consolidation terminée!")