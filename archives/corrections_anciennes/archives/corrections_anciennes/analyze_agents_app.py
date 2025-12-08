#!/usr/bin/env python3
"""
ANALYSE COMPLÈTE DE L'APPLICATION AGENTS
"""

import os
import django
from pathlib import Path
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

BASE_DIR = Path(__file__).parent

class AgentsAppAnalyzer:
    def __init__(self):
        self.results = {
            'structure': {},
            'models': {},
            'views': {},
            'urls': {},
            'templates': {},
            'issues': []
        }
    
    def run_complete_analysis(self):
        """Exécute l'analyse complète de l'app agents"""
        
        print("🔍 ANALYSE COMPLÈTE DE L'APPLICATION AGENTS")
        print("=" * 60)
        
        self.analyze_structure()
        self.analyze_models()
        self.analyze_views()
        self.analyze_urls()
        self.analyze_templates()
        self.check_messaging_integration()
        
        self.generate_comprehensive_report()
    
    def analyze_structure(self):
        """Analyse la structure de l'application"""
        
        print("\n📁 ANALYSE DE LA STRUCTURE...")
        
        agents_dir = BASE_DIR / 'agents'
        
        if not agents_dir.exists():
            self.results['issues'].append("❌ DOSSIER AGENTS MANQUANT")
            return
        
        # Structure des fichiers
        structure = {}
        for item in agents_dir.rglob('*'):
            if item.is_file():
                rel_path = item.relative_to(agents_dir)
                folder = str(rel_path.parent)
                if folder == '.':
                    folder = 'root'
                
                if folder not in structure:
                    structure[folder] = []
                
                structure[folder].append({
                    'name': item.name,
                    'size': item.stat().st_size,
                    'lines': self.count_lines(item)
                })
        
        self.results['structure'] = structure
        
        # Afficher la structure
        for folder, files in structure.items():
            print(f"   📂 {folder}/")
            for file_info in files:
                print(f"      📄 {file_info['name']} ({file_info['lines']} lignes)")
    
    def count_lines(self, file_path):
        """Compte les lignes d'un fichier"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return len(f.readlines())
        except:
            return 0
    
    def analyze_models(self):
        """Analyse les modèles de l'app agents"""
        
        print("\n🗄️ ANALYSE DES MODÈLES...")
        
        models_file = BASE_DIR / 'agents' / 'models.py'
        
        if not models_file.exists():
            self.results['issues'].append("❌ models.py MANQUANT")
            return
        
        with open(models_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Compter les modèles
        model_count = len(re.findall(r'class (\w+)\(models\.Model\)', content))
        model_names = re.findall(r'class (\w+)\(models\.Model\)', content)
        
        self.results['models'] = {
            'count': model_count,
            'names': model_names,
            'file_size': len(content),
            'lines': content.count('\n') + 1
        }
        
        print(f"   📊 Modèles trouvés: {model_count}")
        for model in model_names:
            print(f"      🏷️  {model}")
        
        # Vérifier les relations utilisateur
        if 'User' in content or 'get_user_model' in content:
            print("   ✅ Relations utilisateur détectées")
        else:
            self.results['issues'].append("⚠️  Pas de relations utilisateur détectées")
    
    def analyze_views(self):
        """Analyse les vues de l'app agents"""
        
        print("\n👁️ ANALYSE DES VUES...")
        
        views_file = BASE_DIR / 'agents' / 'views.py'
        
        if not views_file.exists():
            self.results['issues'].append("❌ views.py MANQUANT")
            return
        
        with open(views_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Compter les vues
        function_views = len(re.findall(r'def (\w+)\(request', content))
        class_views = len(re.findall(r'class (\w+)\(.*View\)', content))
        total_views = function_views + class_views
        
        # Noms des vues
        function_names = re.findall(r'def (\w+)\(request', content)
        class_names = re.findall(r'class (\w+)\(.*View\)', content)
        
        self.results['views'] = {
            'total': total_views,
            'function_views': function_views,
            'class_views': class_views,
            'function_names': function_names,
            'class_names': class_names,
            'file_size': len(content),
            'lines': content.count('\n') + 1
        }
        
        print(f"   📊 Vues trouvées: {total_views} ({function_views} fonctions, {class_views} classes)")
        
        # Vues importantes à vérifier
        important_views = ['dashboard', 'liste_membres', 'creer_bon_soin']
        missing_views = [view for view in important_views if view not in content]
        
        if missing_views:
            for view in missing_views:
                self.results['issues'].append(f"⚠️  Vue importante manquante: {view}")
        
        # Vérifier les décorateurs de permission
        if '@login_required' in content or 'LoginRequiredMixin' in content:
            print("   ✅ Contrôle d'accès détecté")
        else:
            self.results['issues'].append("⚠️  Pas de contrôle d'accès détecté")
    
    def analyze_urls(self):
        """Analyse les URLs de l'app agents"""
        
        print("\n🔗 ANALYSE DES URLs...")
        
        urls_file = BASE_DIR / 'agents' / 'urls.py'
        
        if not urls_file.exists():
            self.results['issues'].append("❌ urls.py MANQUANT")
            return
        
        with open(urls_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraire les patterns d'URL
        url_patterns = re.findall(r"path\('([^']+)', [^,]+, name='([^']+)'\)", content)
        
        self.results['urls'] = {
            'patterns': url_patterns,
            'count': len(url_patterns),
            'file_size': len(content),
            'lines': content.count('\n') + 1
        }
        
        print(f"   📊 URLs configurées: {len(url_patterns)}")
        for pattern, name in url_patterns:
            print(f"      🌐 {pattern} → {name}")
        
        # URLs importantes à vérifier
        important_urls = ['dashboard', 'liste-membres', 'creer-bon-soin']
        missing_urls = [url for url in important_urls if not any(url in pattern for pattern, name in url_patterns)]
        
        if missing_urls:
            for url in missing_urls:
                self.results['issues'].append(f"⚠️  URL importante manquante: {url}")
    
    def analyze_templates(self):
        """Analyse les templates de l'app agents"""
        
        print("\n📄 ANALYSE DES TEMPLATES...")
        
        templates_dir = BASE_DIR / 'templates' / 'agents'
        
        if not templates_dir.exists():
            self.results['issues'].append("❌ DOSSIER TEMPLATES AGENTS MANQUANT")
            return
        
        templates = []
        for template_file in templates_dir.rglob('*.html'):
            rel_path = template_file.relative_to(templates_dir)
            
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            template_info = {
                'name': str(rel_path),
                'size': len(content),
                'lines': content.count('\n') + 1,
                'has_base_extend': '{% extends' in content,
                'has_static_load': '{% load static' in content,
                'has_messaging': 'messagerie' in content.lower() or 'communication' in content
            }
            
            templates.append(template_info)
        
        self.results['templates'] = templates
        
        print(f"   📊 Templates trouvés: {len(templates)}")
        for template in templates:
            status = "✅" if template['has_base_extend'] else "❌"
            messaging_status = "💬" if template['has_messaging'] else "🔇"
            print(f"      {status} {template['name']} ({template['lines']} lignes) {messaging_status}")
    
    def check_messaging_integration(self):
        """Vérifie l'intégration de la messagerie"""
        
        print("\n💬 VÉRIFICATION INTÉGRATION MESSAGERIE...")
        
        # Vérifier le dashboard
        dashboard_file = BASE_DIR / 'templates' / 'agents' / 'dashboard.html'
        if dashboard_file.exists():
            with open(dashboard_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'communication:messagerie_agent' in content:
                print("   ✅ Dashboard: Lien messagerie présent")
            else:
                self.results['issues'].append("❌ Dashboard: Lien messagerie ABSENT")
        
        # Vérifier les vues pour l'intégration messagerie
        views_file = BASE_DIR / 'agents' / 'views.py'
        if views_file.exists():
            with open(views_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'communication' in content or 'Message' in content:
                print("   ✅ Vues: Intégration messagerie détectée")
            else:
                self.results['issues'].append("⚠️  Vues: Pas d'intégration messagerie détectée")
    
    def generate_comprehensive_report(self):
        """Génère un rapport complet"""
        
        print("\n" + "=" * 80)
        print("📊 RAPPORT COMPLET - APPLICATION AGENTS")
        print("=" * 80)
        
        # Résumé statistique
        print(f"\n🎯 RÉSUMÉ STATISTIQUE:")
        print(f"   📁 Structure: {len(self.results['structure'])} dossiers")
        print(f"   🗄️  Modèles: {self.results['models'].get('count', 0)}")
        print(f"   👁️  Vues: {self.results['views'].get('total', 0)}")
        print(f"   🔗 URLs: {self.results['urls'].get('count', 0)}")
        print(f"   📄 Templates: {len(self.results['templates'])}")
        
        # Détails par section
        if self.results['models']:
            print(f"\n🗄️  MODÈLES:")
            for model in self.results['models'].get('names', []):
                print(f"   🏷️  {model}")
        
        if self.results['views']:
            print(f"\n👁️  VUES (Fonctions):")
            for view in self.results['views'].get('function_names', [])[:10]:
                print(f"   🔧 {view}()")
            
            print(f"\n👁️  VUES (Classes):")
            for view in self.results['views'].get('class_names', [])[:10]:
                print(f"   🏛️  {view}")
        
        if self.results['urls']:
            print(f"\n🔗 URLs:")
            for pattern, name in self.results['urls'].get('patterns', [])[:10]:
                print(f"   🌐 {name}: {pattern}")
        
        # Problèmes détectés
        if self.results['issues']:
            print(f"\n🚨 PROBLÈMES DÉTECTÉS ({len(self.results['issues'])}):")
            for issue in self.results['issues']:
                print(f"   {issue}")
        else:
            print(f"\n✅ AUCUN PROBLÈME CRITIQUE DÉTECTÉ")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS:")
        
        if any('MANQUANT' in issue for issue in self.results['issues']):
            print("   1. Complétez les fichiers manquants")
        
        if any('messagerie' in issue.lower() for issue in self.results['issues']):
            print("   2. Finalisez l'intégration de la messagerie")
        
        if len(self.results['templates']) < 5:
            print("   3. Développez davantage de templates")
        
        print(f"\n🔧 POUR AMÉLIORER L'APP AGENTS:")
        print("   1. Vérifiez les permissions et la sécurité")
        print("   2. Testez toutes les fonctionnalités")
        print("   3. Optimisez les performances")
        print("   4. Documentez le code")
        
        # Sauvegarde du rapport
        self.save_detailed_report()
    
    def save_detailed_report(self):
        """Sauvegarde un rapport détaillé"""
        
        report = f"""
# RAPPORT D'ANALYSE - APPLICATION AGENTS

## 📊 STATISTIQUES GÉNÉRALES

- **Modèles**: {self.results['models'].get('count', 0)}
- **Vues**: {self.results['views'].get('total', 0)} 
- **URLs**: {self.results['urls'].get('count', 0)}
- **Templates**: {len(self.results['templates'])}

## 🗄️ MODÈLES

{chr(10).join(f"- {model}" for model in self.results['models'].get('names', []))}

## 👁️ VUES

### Vues Fonctions
{chr(10).join(f"- {view}" for view in self.results['views'].get('function_names', []))}

### Vues Classes  
{chr(10).join(f"- {view}" for view in self.results['views'].get('class_names', []))}

## 🔗 URLs

{chr(10).join(f"- `{pattern}` → `{name}`" for pattern, name in self.results['urls'].get('patterns', []))}

## 📄 TEMPLATES

{chr(10).join(f"- `{t['name']}` ({t['lines']} lignes)" for t in self.results['templates'])}

## 🚨 PROBLÈMES

{chr(10).join(f"- {issue}" for issue in self.results['issues'])}

## 💡 RECOMMANDATIONS

1. Vérifiez l'intégration de la messagerie
2. Testez toutes les fonctionnalités
3. Assurez la sécurité des vues
4. Documentez le code
"""
        
        report_file = BASE_DIR / 'RAPPORT_ANALYSE_AGENTS.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📄 Rapport détaillé sauvegardé: {report_file}")

def main():
    analyzer = AgentsAppAnalyzer()
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()