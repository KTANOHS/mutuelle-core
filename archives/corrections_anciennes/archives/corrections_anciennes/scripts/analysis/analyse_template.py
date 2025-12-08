#!/usr/bin/env python3
"""
Script d'analyse approfondie des templates Django
"""

from pathlib import Path
import os
import re
from collections import defaultdict

class TemplateAnalyzer:
    def __init__(self, project_root='.'):
        self.project_root = Path(project_root)
        self.results = {
            'template_dirs': [],
            'templates_count': 0,
            'templates_by_app': defaultdict(list),
            'templates_by_type': defaultdict(list),
            'extends_usage': defaultdict(list),
            'includes_usage': defaultdict(list),
            'blocks_defined': defaultdict(list),
            'missing_blocks': [],
            'template_issues': [],
            'static_usage': defaultdict(int),
            'url_usage': defaultdict(int)
        }
    
    def find_template_directories(self):
        """Recherche tous les répertoires de templates"""
        print("🔍 Recherche des répertoires de templates...")
        
        # Répertoires standards Django
        standard_dirs = [
            self.project_root / 'templates',
            *[self.project_root / app / 'templates' 
              for app in ['api', 'assureur', 'core', 'medecin', 'membres', 
                         'mutuelle_core', 'paiements', 'pharmacien', 'soins']]
        ]
        
        # Recherche également d'autres répertoires templates
        found_dirs = list(self.project_root.rglob('*templates*'))
        found_dirs = [d for d in found_dirs if d.is_dir()]
        
        all_dirs = list(set(standard_dirs + found_dirs))
        
        for template_dir in all_dirs:
            if template_dir.exists() and template_dir.is_dir():
                self.results['template_dirs'].append(str(template_dir.relative_to(self.project_root)))
        
        print(f"📁 Répertoires templates trouvés: {len(self.results['template_dirs'])}")
    
    def analyze_templates_structure(self):
        """Analyse la structure et le contenu des templates"""
        print("\n📊 Analyse de la structure des templates...")
        
        for template_dir_path in self.results['template_dirs']:
            template_dir = self.project_root / template_dir_path
            html_files = list(template_dir.rglob('*.html'))
            
            for html_file in html_files:
                self.analyze_single_template(html_file)
        
        self.results['templates_count'] = sum(len(templates) for templates in self.results['templates_by_app'].values())
    
    def analyze_single_template(self, template_path):
        """Analyse un template individuel"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = template_path.relative_to(self.project_root)
            
            # Déterminer l'application
            app_name = self._detect_app_name(template_path)
            self.results['templates_by_app'][app_name].append(str(relative_path))
            
            # Analyser le type de template
            template_type = self._detect_template_type(template_path, content)
            self.results['templates_by_type'][template_type].append(str(relative_path))
            
            # Analyser la syntaxe Django
            self._analyze_django_syntax(content, str(relative_path))
            
            # Analyser les dépendances
            self._analyze_template_dependencies(content, str(relative_path))
            
        except Exception as e:
            self.results['template_issues'].append({
                'file': str(relative_path),
                'issue': f"Erreur de lecture: {e}",
                'type': 'IO Error'
            })
    
    def _detect_app_name(self, template_path):
        """Détecte le nom de l'application associée au template"""
        path_parts = template_path.parts
        for i, part in enumerate(path_parts):
            if part in ['api', 'assureur', 'core', 'medecin', 'membres', 
                       'mutuelle_core', 'paiements', 'pharmacien', 'soins']:
                return part
        return 'global'
    
    def _detect_template_type(self, template_path, content):
        """Détecte le type de template"""
        filename = template_path.name.lower()
        
        if 'base' in filename:
            return 'base'
        elif 'partial' in filename or 'include' in filename or '_' in filename:
            return 'partial'
        elif any(x in filename for x in ['list', 'index', 'home']):
            return 'list'
        elif any(x in filename for x in ['detail', 'view', 'show']):
            return 'detail'
        elif any(x in filename for x in ['form', 'create', 'edit', 'update']):
            return 'form'
        elif 'email' in filename:
            return 'email'
        else:
            return 'other'
    
    def _analyze_django_syntax(self, content, template_path):
        """Analyse la syntaxe Django du template"""
        # Vérifier {% extends %}
        extends_match = re.search(r'{%\s*extends\s+[\'"]([^\'"]+)[\'"]\s*%}', content)
        if extends_match:
            base_template = extends_match.group(1)
            self.results['extends_usage'][template_path].append(base_template)
            
            # Vérifier si le template a des blocks
            if '{% block' not in content:
                self.results['missing_blocks'].append({
                    'template': template_path,
                    'base_template': base_template,
                    'issue': 'Template étend un base mais ne définit pas de blocks'
                })
        
        # Vérifier {% include %}
        includes = re.findall(r'{%\s*include\s+[\'"]([^\'"]+)[\'"]\s*%}', content)
        for included in includes:
            self.results['includes_usage'][template_path].append(included)
        
        # Vérifier les blocks définis
        blocks = re.findall(r'{%\s*block\s+(\w+)\s*%}', content)
        for block in blocks:
            self.results['blocks_defined'][template_path].append(block)
        
        # Vérifier l'usage des static files
        static_count = len(re.findall(r'{%\s*static\s+[\'"]([^\'"]+)[\'"]\s*%}', content))
        if static_count > 0:
            self.results['static_usage'][template_path] = static_count
        
        # Vérifier l'usage des URLs
        url_count = len(re.findall(r'{%\s*url\s+[\'"]([^\'"]+)[\'"]\s*%}', content))
        if url_count > 0:
            self.results['url_usage'][template_path] = url_count
        
        # Vérifier les erreurs potentielles
        self._check_template_issues(content, template_path)
    
    def _check_template_issues(self, content, template_path):
        """Détecte les problèmes potentiels dans le template"""
        issues = []
        
        # Vérifier les balises fermantes manquantes
        if content.count('{% block') != content.count('{% endblock %}'):
            issues.append("Nombre de blocks et endblocks ne correspond pas")
        
        # Vérifier les URLs absolues (potentiellement problématiques)
        absolute_urls = re.findall(r'href=["\'](https?://[^"\']+)["\']', content)
        if absolute_urls and 'localhost' not in str(absolute_urls):
            issues.append(f"URLs absolues détectées: {len(absolute_urls)}")
        
        # Vérifier le chargement des tags
        if '{% load' not in content and ('{% static' in content or '{% url' in content):
            issues.append("Tags Django utilisés mais pas de {% load %}")
        
        if issues:
            self.results['template_issues'].append({
                'file': template_path,
                'issues': issues,
                'type': 'Syntax Warning'
            })
    
    def _analyze_template_dependencies(self, content, template_path):
        """Analyse les dépendances entre templates"""
        # Cette méthode est déjà utilisée dans _analyze_django_syntax
        pass
    
    def generate_detailed_report(self):
        """Génère un rapport détaillé"""
        print("\n" + "="*80)
        print("📋 RAPPORT DÉTAILLÉ DES TEMPLATES")
        print("="*80)
        
        # Statistiques générales
        print(f"\n📊 STATISTIQUES GÉNÉRALES:")
        print(f"Total templates: {self.results['templates_count']}")
        print(f"Répertoires templates: {len(self.results['template_dirs'])}")
        
        # Templates par application
        print(f"\n📁 TEMPLATES PAR APPLICATION:")
        for app, templates in self.results['templates_by_app'].items():
            print(f"  {app}: {len(templates)} templates")
            if len(templates) <= 5:  # Afficher les noms si peu nombreux
                for template in templates:
                    print(f"    └─ {template}")
        
        # Templates par type
        print(f"\n🎯 TEMPLATES PAR TYPE:")
        for template_type, templates in self.results['templates_by_type'].items():
            print(f"  {template_type}: {len(templates)}")
        
        # Analyse des extends
        print(f"\n🔄 USAGE DES EXTENDS:")
        if self.results['extends_usage']:
            for template, bases in self.results['extends_usage'].items():
                print(f"  {template}")
                for base in bases:
                    print(f"    └─ étend: {base}")
        else:
            print("  Aucun usage de {% extends %} détecté")
        
        # Blocks manquants
        if self.results['missing_blocks']:
            print(f"\n⚠️  TEMPLATES SANS BLOCKS:")
            for issue in self.results['missing_blocks']:
                print(f"  {issue['template']}")
                print(f"    └─ Problème: {issue['issue']}")
        
        # Usage des static files
        if self.results['static_usage']:
            print(f"\n📦 USAGE DES FICHIERS STATIQUES:")
            templates_with_static = {k: v for k, v in self.results['static_usage'].items() if v > 0}
            for template, count in sorted(templates_with_static.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {template}: {count} références static")
        
        # Problèmes détectés
        if self.results['template_issues']:
            print(f"\n❌ PROBLÈMES DÉTECTÉS ({len(self.results['template_issues'])}):")
            for issue in self.results['template_issues'][:10]:
                print(f"  🔸 {issue['file']}")
                print(f"     Type: {issue['type']}")
                if 'issues' in issue:
                    for sub_issue in issue['issues']:
                        print(f"     - {sub_issue}")
                else:
                    print(f"     {issue['issue']}")
        
        # Recommandations
        self._generate_recommendations()
    
    def _generate_recommendations(self):
        """Génère des recommandations basées sur l'analyse"""
        print(f"\n💡 RECOMMANDATIONS:")
        
        recommendations = []
        
        # Vérifier l'organisation des templates
        if len(self.results['template_dirs']) > 3:
            recommendations.append("Trop de répertoires templates, envisager une consolidation")
        
        # Vérifier les templates sans extends
        total_templates = self.results['templates_count']
        templates_with_extends = len(self.results['extends_usage'])
        if templates_with_extends / total_templates < 0.5:
            recommendations.append("Peu de templates utilisent l'héritage, envisager plus de réutilisation")
        
        # Vérifier l'usage des partials
        partial_count = len(self.results['templates_by_type']['partial'])
        if partial_count == 0:
            recommendations.append("Aucun template partiel détecté, envisager de créer des includes")
        
        # Vérifier les problèmes de blocks
        if self.results['missing_blocks']:
            recommendations.append("Corriger les templates qui étendent mais n'ont pas de blocks")
        
        # Afficher les recommandations
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
        
        if not recommendations:
            print("  ✅ Structure des templates optimale!")
    
    def export_template_tree(self):
        """Exporte l'arborescence des templates"""
        print(f"\n🌳 ARBORESCENCE DES TEMPLATES:")
        for template_dir in self.results['template_dirs']:
            print(f"\n📁 {template_dir}/")
            dir_path = self.project_root / template_dir
            html_files = list(dir_path.rglob('*.html'))
            
            for html_file in html_files:
                relative_path = html_file.relative_to(self.project_root / template_dir)
                depth = len(relative_path.parts) - 1
                indent = "    " * depth + "└─ " if depth > 0 else "├─ "
                print(f"  {indent}{relative_path.name}")
    
    def run_complete_analysis(self):
        """Exécute l'analyse complète"""
        print("🚀 DÉMARRAGE DE L'ANALYSE DES TEMPLATES...")
        
        self.find_template_directories()
        self.analyze_templates_structure()
        self.generate_detailed_report()
        self.export_template_tree()

def main():
    """Fonction principale"""
    analyzer = TemplateAnalyzer()
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()