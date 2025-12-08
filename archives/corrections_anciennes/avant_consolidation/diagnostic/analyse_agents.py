#!/usr/bin/env python3
"""
Script d'analyse approfondie de l'application Agents
"""

import os
import sys
import ast
import inspect
from pathlib import Path
from datetime import datetime
import django
from django.conf import settings

# Configuration Django
sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

# Import des modèles après configuration Django
from django.apps import apps
from django.db import models
from django.core.management import call_command
from io import StringIO

class AgentsAnalyzer:
    def __init__(self):
        self.project_path = Path(__file__).resolve().parent
        self.agents_path = self.project_path / 'agents'
        self.results = {
            'critical': [],
            'errors': [],
            'warnings': [],
            'info': [],
            'success': []
        }
    
    def log(self, level, message):
        """Journalise un message avec niveau"""
        self.results[level].append(message)
        print(f"{self.get_emoji(level)} {message}")
    
    def get_emoji(self, level):
        """Retourne l'emoji correspondant au niveau"""
        emojis = {
            'critical': '🚨',
            'errors': '❌',
            'warnings': '⚠️',
            'info': 'ℹ️',
            'success': '✅'
        }
        return emojis.get(level, '🔍')
    
    def analyze_structure(self):
        """Analyse la structure de l'application agents"""
        self.log('info', "Analyse de la structure de l'application...")
        
        required_files = [
            '__init__.py',
            'admin.py',
            'apps.py',
            'models.py',
            'views.py',
            'urls.py',
            'forms.py'
        ]
        
        for file in required_files:
            file_path = self.agents_path / file
            if file_path.exists():
                self.log('success', f"{file} - Présent")
            else:
                self.log('warnings', f"{file} - Manquant")
        
        # Dossiers templates
        templates_dir = self.project_path / 'templates' / 'agents'
        if templates_dir.exists():
            templates = list(templates_dir.glob('*.html'))
            self.log('success', f"Templates: {len(templates)} fichiers trouvés")
            
            # Templates critiques
            critical_templates = [
                'base_agent.html',
                'dashboard.html',
                'creer_bon_soin.html',
                'creer_membre.html',
                'liste_membres.html',
                'historique_bons.html'
            ]
            
            for template in critical_templates:
                if (templates_dir / template).exists():
                    self.log('success', f"  Template {template} - Présent")
                else:
                    self.log('warnings', f"  Template {template} - Manquant")
        else:
            self.log('errors', "Dossier templates/agents introuvable")
    
    def analyze_models(self):
        """Analyse les modèles de l'application agents"""
        self.log('info', "Analyse des modèles...")
        
        try:
            models_file = self.agents_path / 'models.py'
            if models_file.exists():
                with open(models_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Vérifier la présence de classes de modèles
                model_classes = []
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        for base in node.bases:
                            if isinstance(base, ast.Name) and base.id == 'Model':
                                model_classes.append(node.name)
                                self.log('success', f"Modèle détecté: {node.name}")
                
                if not model_classes:
                    self.log('warnings', "Aucun modèle Django détecté dans models.py")
                
                # Vérifier les champs communs
                if 'Agent' in content or 'agent' in content.lower():
                    self.log('info', "Modèle Agent référencé")
                else:
                    self.log('warnings', "Modèle Agent non détecté")
                    
            else:
                self.log('errors', "Fichier models.py introuvable")
                
        except Exception as e:
            self.log('errors', f"Erreur analyse modèles: {e}")
    
    def analyze_views(self):
        """Analyse les vues de l'application agents"""
        self.log('info', "Analyse des vues...")
        
        views_file = self.agents_path / 'views.py'
        if not views_file.exists():
            self.log('errors', "Fichier views.py introuvable")
            return
        
        try:
            with open(views_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les vues critiques
            critical_views = [
                'dashboard',
                'creer_bon_soin',
                'creer_membre',
                'liste_membres',
                'historique_bons'
            ]
            
            for view in critical_views:
                if f'def {view}' in content:
                    self.log('success', f"Vue {view} - Présente")
                else:
                    self.log('warnings', f"Vue {view} - Manquante")
            
            # Vérifier les décorateurs de sécurité
            if '@login_required' in content:
                self.log('success', "Décorateur login_required détecté")
            else:
                self.log('warnings', "Décorateur login_required manquant")
            
            # Vérifier les imports importants
            required_imports = [
                'render',
                'login_required',
                'HttpResponse'
            ]
            
            for imp in required_imports:
                if imp in content:
                    self.log('success', f"Import {imp} - Présent")
                else:
                    self.log('info', f"Import {imp} - Non détecté")
                    
        except Exception as e:
            self.log('errors', f"Erreur analyse vues: {e}")
    
    def analyze_urls(self):
        """Analyse la configuration des URLs"""
        self.log('info', "Analyse des URLs...")
        
        # URLs de l'application
        agents_urls = self.agents_path / 'urls.py'
        if agents_urls.exists():
            with open(agents_urls, 'r') as f:
                content = f.read()
            
            # Vérifier les patterns d'URL critiques
            url_patterns = [
                'dashboard',
                'creer-bon-soin',
                'creer-membre',
                'liste-membres'
            ]
            
            for pattern in url_patterns:
                if pattern in content:
                    self.log('success', f"URL {pattern} - Configurée")
                else:
                    self.log('warnings', f"URL {pattern} - Non configurée")
            
            # Vérifier app_name
            if 'app_name' in content:
                self.log('success', "app_name configuré")
            else:
                self.log('warnings', "app_name non configuré")
                
        else:
            self.log('errors', "Fichier urls.py introuvable")
        
        # Vérifier l'inclusion dans les URLs principales
        main_urls = self.project_path / 'mutuelle_core' / 'urls.py'
        if main_urls.exists():
            with open(main_urls, 'r') as f:
                content = f.read()
            
            if 'agents.urls' in content:
                self.log('success', "Application incluse dans URLs principales")
            else:
                self.log('critical', "Application NON incluse dans URLs principales")
    
    def analyze_admin(self):
        """Analyse la configuration admin"""
        self.log('info', "Analyse de l'interface admin...")
        
        admin_file = self.agents_path / 'admin.py'
        if admin_file.exists():
            with open(admin_file, 'r') as f:
                content = f.read()
            
            if 'admin.site.register' in content or 'ModelAdmin' in content:
                self.log('success', "Modèles enregistrés dans l'admin")
            else:
                self.log('info', "Aucun modèle enregistré dans l'admin")
        else:
            self.log('warnings', "Fichier admin.py introuvable")
    
    def analyze_forms(self):
        """Analyse des formulaires"""
        self.log('info', "Analyse des formulaires...")
        
        forms_file = self.agents_path / 'forms.py'
        if forms_file.exists():
            with open(forms_file, 'r') as f:
                content = f.read()
            
            if 'forms.Form' in content or 'forms.ModelForm' in content:
                self.log('success', "Formulaires détectés")
            else:
                self.log('warnings', "Aucun formulaire détecté")
        else:
            self.log('info', "Fichier forms.py introuvable (optionnel)")
    
    def analyze_settings_integration(self):
        """Analyse l'intégration dans les settings"""
        self.log('info', "Analyse de l'intégration...")
        
        # Vérifier dans INSTALLED_APPS
        if 'agents' in settings.INSTALLED_APPS:
            self.log('success', "Application dans INSTALLED_APPS")
        else:
            self.log('critical', "Application ABSENTE de INSTALLED_APPS")
        
        # Vérifier la configuration agents
        mutuelle_config = getattr(settings, 'MUTUELLE_CONFIG', {})
        if 'LIMITE_BONS_QUOTIDIENNE' in mutuelle_config:
            self.log('success', "Configuration agents détectée")
        else:
            self.log('warnings', "Configuration agents non spécifique")
    
    def analyze_database(self):
        """Analyse l'état de la base de données"""
        self.log('info', "Analyse de la base de données...")
        
        try:
            # Vérifier les migrations
            output = StringIO()
            call_command('showmigrations', 'agents', stdout=output)
            output.seek(0)
            migrations_output = output.read()
            
            applied = migrations_output.count('[X]')
            pending = migrations_output.count('[ ]')
            
            self.log('info', f"Migrations agents: {applied} appliquées, {pending} en attente")
            
            if pending > 0:
                self.log('warnings', f"{pending} migration(s) en attente")
            else:
                self.log('success', "Toutes les migrations sont appliquées")
                
        except Exception as e:
            self.log('errors', f"Erreur vérification migrations: {e}")
    
    def analyze_permissions(self):
        """Analyse le système de permissions"""
        self.log('info', "Analyse des permissions...")
        
        # Vérifier les modèles de permission
        models_file = self.agents_path / 'models.py'
        if models_file.exists():
            with open(models_file, 'r') as f:
                content = f.read()
            
            if 'Permission' in content or 'permission' in content.lower():
                self.log('success', "Système de permissions détecté")
            else:
                self.log('info', "Aucun système de permission spécifique détecté")
    
    def analyze_templates_content(self):
        """Analyse le contenu des templates critiques"""
        self.log('info', "Analyse du contenu des templates...")
        
        templates_dir = self.project_path / 'templates' / 'agents'
        
        # Vérifier le template de base
        base_template = templates_dir / 'base_agent.html'
        if base_template.exists():
            with open(base_template, 'r') as f:
                content = f.read()
            
            # Vérifications importantes
            checks = [
                ('{% block content %}', 'Structure de bloc content'),
                ('{% extends %}', 'Héritage de template'),
                ('{% include %}', 'Inclusions de templates'),
                ('{{ user }}', 'Utilisation de user'),
                ('{% url %}', 'Tags URL')
            ]
            
            for check, description in checks:
                if check in content:
                    self.log('success', f"Template: {description} - Présent")
                else:
                    self.log('info', f"Template: {description} - Non détecté")
        else:
            self.log('warnings', "Template base_agent.html introuvable")
    
    def generate_report(self):
        """Génère un rapport complet"""
        print("\n" + "="*80)
        print("📊 RAPPORT D'ANALYSE COMPLET - APPLICATION AGENTS")
        print("="*80)
        
        # Statistiques
        total_critical = len(self.results['critical'])
        total_errors = len(self.results['errors'])
        total_warnings = len(self.results['warnings'])
        total_success = len(self.results['success'])
        
        print(f"\n📈 STATISTIQUES:")
        print(f"   🚨 Critique: {total_critical}")
        print(f"   ❌ Erreurs: {total_errors}")
        print(f"   ⚠️  Avertissements: {total_warnings}")
        print(f"   ✅ Succès: {total_success}")
        
        # Affichage par catégorie
        for level in ['critical', 'errors', 'warnings', 'success', 'info']:
            items = self.results[level]
            if items:
                print(f"\n{self.get_emoji(level)} {level.upper()} ({len(items)}):")
                for item in items:
                    print(f"   • {item}")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS:")
        
        if total_critical > 0:
            print("   🚨 CORRIGER EN PRIORITÉ les points critiques")
        if total_errors > 0:
            print("   ❌ Résoudre les erreurs avant déploiement")
        if total_warnings > 0:
            print("   ⚠️  Examiner les avertissements pour optimisation")
        
        if total_critical == 0 and total_errors == 0:
            if total_warnings == 0:
                print("   🎉 Application parfaitement configurée !")
            else:
                print("   ✅ Application fonctionnelle - optimisations possibles")
        
        print("\n" + "="*80)
        
        return total_critical == 0 and total_errors == 0

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DE L'ANALYSE DE L'APPLICATION AGENTS")
    print("=" * 60)
    
    analyzer = AgentsAnalyzer()
    
    # Exécution des analyses
    analyzer.analyze_structure()
    analyzer.analyze_models()
    analyzer.analyze_views()
    analyzer.analyze_urls()
    analyzer.analyze_admin()
    analyzer.analyze_forms()
    analyzer.analyze_settings_integration()
    analyzer.analyze_database()
    analyzer.analyze_permissions()
    analyzer.analyze_templates_content()
    
    # Génération du rapport
    success = analyzer.generate_report()
    
    if success:
        print("\n🎉 L'application agents est PRÊTE pour l'utilisation !")
    else:
        print("\n❌ Des corrections sont nécessaires avant utilisation.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)