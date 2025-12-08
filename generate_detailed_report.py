#!/usr/bin/env python3
"""
Script d'analyse du projet Django - Version corrigée
Reconnaît la structure existante des templates
"""

import os
import sys
import ast
import re
from pathlib import Path
from datetime import datetime

class AccurateProjectAnalyzer:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.analysis_results = {
            'errors': [],
            'warnings': [],
            'info': [],
            'success': []
        }
    
    def analyze_templates_structure(self):
        """Analyse précise de la structure des templates"""
        print("🔍 Analyse de la structure des templates...")
        
        templates_dir = self.project_path / 'templates'
        
        if not templates_dir.exists():
            self.analysis_results['errors'].append("❌ Dossier templates introuvable")
            return
        
        # Vérification des templates agents
        agents_templates = templates_dir / 'agents'
        if agents_templates.exists():
            agent_files = list(agents_templates.glob('*.html'))
            self.analysis_results['success'].append(f"✅ Templates agents: {len(agent_files)} fichiers trouvés")
            
            # Fichiers critiques pour agents
            critical_templates = [
                'base_agent.html',
                'dashboard.html', 
                'creer_bon_soin.html',
                'creer_membre.html',
                'liste_membres.html'
            ]
            
            for template in critical_templates:
                if (agents_templates / template).exists():
                    self.analysis_results['success'].append(f"  ✅ {template}")
                else:
                    self.analysis_results['warnings'].append(f"  ⚠️  {template} manquant")
        else:
            self.analysis_results['errors'].append("❌ Dossier templates/agents introuvable")
        
        # Analyse globale des templates par application
        app_folders = [
            'agents', 'assureur', 'communication', 'core', 'inscription',
            'medecin', 'membres', 'pharmacien', 'registration', 'soins'
        ]
        
        for app in app_folders:
            app_dir = templates_dir / app
            if app_dir.exists():
                html_files = list(app_dir.rglob('*.html'))
                self.analysis_results['info'].append(f"📁 {app}: {len(html_files)} templates")
            else:
                self.analysis_results['warnings'].append(f"⚠️  Dossier templates/{app} manquant")
    
    def analyze_settings_configuration(self):
        """Analyse la configuration depuis le fichier settings.py"""
        print("🔍 Analyse de la configuration...")
        
        settings_file = self.project_path / 'mutuelle_core' / 'settings.py'
        
        if not settings_file.exists():
            self.analysis_results['errors'].append("❌ Fichier settings.py introuvable")
            return
        
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérification de la configuration des templates
            if 'os.path.join(BASE_DIR, \'templates\')' in content:
                self.analysis_results['success'].append("✅ Configuration templates correcte")
            else:
                self.analysis_results['warnings'].append("⚠️ Configuration templates non standard")
            
            # Vérification applications installées
            installed_apps_match = re.search(r'INSTALLED_APPS\s*=\s*\[(.*?)\]', content, re.DOTALL)
            if installed_apps_match:
                apps_content = installed_apps_match.group(1)
                required_apps = ['agents', 'membres', 'communication', 'core']
                
                for app in required_apps:
                    if f"'{app}'" in apps_content or f'"{app}"' in apps_content:
                        self.analysis_results['success'].append(f"✅ Application installée: {app}")
                    else:
                        self.analysis_results['errors'].append(f"❌ Application manquante: {app}")
            
            # Vérification configuration agents
            if 'agents.context_processors.agent_context' in content:
                self.analysis_results['success'].append("✅ Context processor agents configuré")
            else:
                self.analysis_results['warnings'].append("⚠️ Context processor agents non configuré")
                
        except Exception as e:
            self.analysis_results['errors'].append(f"❌ Erreur analyse settings: {e}")
    
    def analyze_agents_application(self):
        """Analyse spécifique de l'application agents"""
        print("🔍 Analyse de l'application agents...")
        
        agents_app = self.project_path / 'agents'
        
        if not agents_app.exists():
            self.analysis_results['errors'].append("❌ Application agents introuvable")
            return
        
        # Fichiers requis pour agents
        required_files = [
            'models.py',
            'views.py', 
            'urls.py',
            'admin.py'
        ]
        
        for file in required_files:
            if (agents_app / file).exists():
                self.analysis_results['success'].append(f"✅ Fichier agents/{file} présent")
            else:
                self.analysis_results['warnings'].append(f"⚠️ Fichier agents/{file} manquant")
        
        # Vérification des vues agents
        views_file = agents_app / 'views.py'
        if views_file.exists():
            try:
                with open(views_file, 'r') as f:
                    views_content = f.read()
                
                if 'def dashboard' in views_content:
                    self.analysis_results['success'].append("✅ Vue dashboard agents présente")
                else:
                    self.analysis_results['warnings'].append("⚠️ Vue dashboard agents manquante")
                    
            except Exception as e:
                self.analysis_results['warnings'].append(f"⚠️ Impossible de lire agents/views.py: {e}")
    
    def check_urls_configuration(self):
        """Vérifie la configuration des URLs"""
        print("🔍 Analyse des URLs...")
        
        # URLs principal
        root_urls = self.project_path / 'mutuelle_core' / 'urls.py'
        if root_urls.exists():
            try:
                with open(root_urls, 'r') as f:
                    urls_content = f.read()
                
                if 'agents.urls' in urls_content:
                    self.analysis_results['success'].append("✅ URLs agents inclus dans URLs principal")
                else:
                    self.analysis_results['warnings'].append("⚠️ URLs agents non inclus dans URLs principal")
                    
            except Exception as e:
                self.analysis_results['warnings'].append(f"⚠️ Erreur lecture URLs principal: {e}")
        
        # URLs agents
        agents_urls = self.project_path / 'agents' / 'urls.py'
        if agents_urls.exists():
            self.analysis_results['success'].append("✅ Fichier agents/urls.py présent")
        else:
            self.analysis_results['errors'].append("❌ Fichier agents/urls.py manquant")
    
    def analyze_static_files(self):
        """Analyse les fichiers statiques"""
        print("🔍 Analyse des fichiers statiques...")
        
        static_dir = self.project_path / 'static'
        if static_dir.exists():
            # Compter les fichiers par type
            css_files = list(static_dir.rglob("*.css"))
            js_files = list(static_dir.rglob("*.js"))
            image_files = list(static_dir.rglob("*.jpg")) + list(static_dir.rglob("*.png"))
            
            self.analysis_results['info'].append(f"📊 Fichiers statiques: {len(css_files)} CSS, {len(js_files)} JS, {len(image_files)} images")
        else:
            self.analysis_results['warnings'].append("⚠️ Dossier static introuvable")
    
    def check_dependencies(self):
        """Vérifie les dépendances installées"""
        print("🔍 Vérification des dépendances...")
        
        try:
            import django
            self.analysis_results['success'].append(f"✅ Django {django.__version__} installé")
        except ImportError:
            self.analysis_results['errors'].append("❌ Django non installé")
        
        # Vérification d'autres packages importants
        packages = [
            ('djangorestframework', 'DRF'),
            ('corsheaders', 'CORS Headers'),
            ('crispy_forms', 'Crispy Forms'),
            ('channels', 'Channels'),
        ]
        
        for package, name in packages:
            try:
                __import__(package)
                self.analysis_results['success'].append(f"✅ {name} installé")
            except ImportError:
                self.analysis_results['warnings'].append(f"⚠️ {name} non installé")
    
    def generate_detailed_report(self):
        """Génère un rapport détaillé"""
        print("\n" + "="*80)
        print("📊 RAPPORT D'ANALYSE DÉTAILLÉ - PROJET MUTUELLE")
        print("="*80)
        
        # Résumé par catégorie
        categories = ['success', 'info', 'warnings', 'errors']
        emojis = ['✅', 'ℹ️', '⚠️', '❌']
        
        for i, category in enumerate(categories):
            items = self.analysis_results[category]
            if items:
                print(f"\n{emojis[i]} {category.upper()} ({len(items)}):")
                for item in items[:10]:  # Limite à 10 items par catégorie
                    print(f"   {item}")
                if len(items) > 10:
                    print(f"   ... et {len(items) - 10} autres")
        
        # Recommandations finales
        total_errors = len(self.analysis_results['errors'])
        total_warnings = len(self.analysis_results['warnings'])
        
        print(f"\n💡 RECOMMANDATIONS FINALES:")
        
        if total_errors == 0 and total_warnings == 0:
            print("   🎉 Projet parfaitement configuré !")
            print("   → Vous pouvez démarrer le développement")
        elif total_errors == 0:
            print("   ✅ Projet fonctionnel avec quelques améliorations possibles")
            print("   → Examinez les avertissements pour optimiser")
        else:
            print("   ❌ Corrections nécessaires avant démarrage")
            print("   → Priorisez la résolution des erreurs")
        
        print("\n" + "="*80)
        
        return total_errors == 0

def main():
    """Fonction principale"""
    project_path = Path(__file__).resolve().parent
    
    print("🚀 DÉMARRAGE DE L'ANALYSE PRÉCISE DU PROJET")
    print(f"📁 Répertoire: {project_path}")
    print()
    
    analyzer = AccurateProjectAnalyzer(project_path)
    
    # Exécution des analyses
    analyzer.analyze_templates_structure()
    analyzer.analyze_settings_configuration()
    analyzer.analyze_agents_application()
    analyzer.check_urls_configuration()
    analyzer.analyze_static_files()
    analyzer.check_dependencies()
    
    # Rapport
    success = analyzer.generate_detailed_report()
    
    if success:
        print("\n🎉 ANALYSE TERMINÉE - PROJET PRÊT !")
        print("\n🚀 PROCHAINES ÉTAPES:")
        print("   1. python manage.py makemigrations")
        print("   2. python manage.py migrate")
        print("   3. python manage.py createsuperuser")
        print("   4. python manage.py runserver")
        print("   5. Accéder à: http://localhost:8000/agents/")
    else:
        print("\n❌ PROBLEMES DÉTECTÉS - CORRIGEZ LES ERREURS AVANT DE CONTINUER")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)