#!/usr/bin/env python3
"""
Script pour gérer les templates dupliqués
"""

from pathlib import Path

class DuplicateManager:
    def __init__(self, templates_dir="templates"):
        self.templates_dir = Path(templates_dir)
        
    def analyze_duplicates(self):
        """Analyser les doublons et suggérer des actions"""
        duplicates_plan = {
            'keep_one_remove_others': {
                'home.html': {
                    'keep': 'core/home.html',
                    'remove': ['home.html']
                },
                'dashboard.html': {
                    'keep': 'core/dashboard_unified.html',
                    'remove': [
                        'dashboard.html',
                        'core/dashboard.html', 
                        'soins/dashboard.html',
                        'medecin/dashboard.html',
                        'agents/dashboard.html',
                        'membres/dashboard.html',
                        'assureur/dashboard.html',
                        'pharmacien/dashboard.html'
                    ]
                }
            },
            'role_specific': {
                'liste_soins': {
                    'assureur': 'assureur/liste_soins.html',
                    'soins': 'soins/liste_soins.html'
                },
                'liste_ordonnances': {
                    'medecin': 'medecin/liste_ordonnances.html',
                    'pharmacien': 'pharmacien/liste_ordonnances.html'
                }
            },
            'consolidate_partials': {
                '_stats_cards': 'components/stats_cards.html',
                '_sidebar': 'components/sidebars/role_sidebar.html'
            }
        }
        
        return duplicates_plan
    
    def generate_migration_guide(self):
        """Générer un guide de migration pour l'équipe"""
        guide = "# 📋 GUIDE DE MIGRATION DES TEMPLATES\n\n"
        guide += "## 🎯 Actions Prioritaires\n\n"
        guide += "### 1. Dashboard Unifié\n"
        guide += "- Utiliser `core/dashboard_unified.html` comme base\n"
        guide += "- Adapter le contenu par rôle avec `{% block dashboard_content %}`\n\n"
        guide += "### 2. Structure des Composants\n"
        guide += "```\n"
        guide += "templates/\n"
        guide += "├── components/\n"
        guide += "│   ├── stats_cards.html          # Cartes stats unifiées\n"
        guide += "│   ├── sidebars/\n"
        guide += "│   │   ├── agent_sidebar.html\n"
        guide += "│   │   ├── assureur_sidebar.html\n"
        guide += "│   │   └── role_sidebar.html     # Base pour sidebars\n"
        guide += "│   └── forms/                    # Formulaires communs\n"
        guide += "```\n\n"
        guide += "### 3. Gestion des Rôles\n"
        guide += "- **Assureur** : Garder `assureur/liste_soins.html` \n"
        guide += "- **Soins** : Garder `soins/liste_soins.html`\n"
        guide += "- **Médecin/Pharmacien** : Garder leurs versions spécifiques\n\n"
        guide += "### 4. Templates d'Email\n"
        guide += "- Déplacés vers `templates/emails/`\n"
        guide += "- Structure corrigée\n"
        
        return guide

def main():
    manager = DuplicateManager()
    
    print("🔍 Analyse des doublons...")
    plan = manager.analyze_duplicates()
    
    print("\n📊 Plan de consolidation:")
    for category, items in plan.items():
        print(f"\n{category.upper()}:")
        for key, value in items.items():
            if 'remove' in value:
                print(f"  📁 {key}: {len(value.get('remove', []))} à consolider")
            else:
                print(f"  📁 {key}: spécifique au rôle")
    
    print("\n📖 Guide de migration généré:")
    print(manager.generate_migration_guide())

if __name__ == "__main__":
    main()