#!/usr/bin/env python3
"""
Script d'analyse des templates Django pour l'application pharmacien
Vérifie la cohérence, les URLs, les variables de contexte et les erreurs potentielles
"""

import os
import re
from pathlib import Path

class TemplateAnalyzer:
    def __init__(self, templates_dir):
        self.templates_dir = Path(templates_dir)
        self.issues = []
        self.templates_data = {}
        
    def analyze_all_templates(self):
        """Analyse tous les templates du dossier pharmacien"""
        print("🔍 Analyse des templates pharmacien...")
        print(f"📁 Dossier: {self.templates_dir}")
        print("-" * 60)
        
        # Liste tous les fichiers HTML
        template_files = list(self.templates_dir.glob("*.html"))
        
        for template_file in template_files:
            print(f"\n📄 Analyse de: {template_file.name}")
            self.analyze_template(template_file)
        
        self.generate_report()
    
    def analyze_template(self, template_file):
        """Analyse un template spécifique"""
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            issues = []
            
            # 1. Vérifier les extends
            extends_issues = self.check_extends(content, template_file.name)
            issues.extend(extends_issues)
            
            # 2. Vérifier les URLs
            url_issues = self.check_urls(content, template_file.name)
            issues.extend(url_issues)
            
            # 3. Vérifier les variables de contexte
            context_issues = self.check_context_variables(content, template_file.name)
            issues.extend(context_issues)
            
            # 4. Vérifier les blocs
            block_issues = self.check_blocks(content, template_file.name)
            issues.extend(block_issues)
            
            # 5. Vérifier les includes
            include_issues = self.check_includes(content, template_file.name)
            issues.extend(include_issues)
            
            # Stocker les données
            self.templates_data[template_file.name] = {
                'content': content,
                'issues': issues,
                'extends': self.get_extends(content),
                'urls': self.get_all_urls(content),
                'blocks': self.get_blocks(content),
                'includes': self.get_includes(content)
            }
            
            # Afficher les résultats pour ce template
            if issues:
                for issue in issues:
                    print(f"   ⚠️  {issue}")
            else:
                print("   ✅ Aucun problème détecté")
                
        except Exception as e:
            error_msg = f"❌ Erreur lors de la lecture: {e}"
            print(f"   {error_msg}")
            self.issues.append(f"{template_file.name}: {error_msg}")
    
    def check_extends(self, content, template_name):
        """Vérifie les déclarations extends"""
        issues = []
        extends_match = re.search(r'{% extends [\'"]([^\'"]+)[\'"] %}', content)
        
        if extends_match:
            base_template = extends_match.group(1)
            if not self.template_exists(base_template):
                issues.append(f"Template étendu manquant: '{base_template}'")
            
            # Vérifier la cohérence des extends
            if template_name == "base_pharmacien.html" and extends_match:
                issues.append("base_pharmacien.html ne devrait pas étendre un autre template")
        
        return issues
    
    def check_urls(self, content, template_name):
        """Vérifie les URLs Django"""
        issues = []
        url_pattern = r'{% url [\'"]([^\'":]+):?([^\'"]*)[\'"] ?([^%]*)%}'
        matches = re.findall(url_pattern, content)
        
        for match in matches:
            url_name = match[0]
            namespace = match[1] if match[1] else 'pas de namespace'
            args = match[2]
            
            # Vérifications spécifiques
            if not url_name:
                issues.append(f"URL sans nom: {match}")
            
            # Vérifier les URLs problématiques
            if "valider_ordonnance" in url_name and not args.strip():
                issues.append(f"URL '{url_name}' sans argument - risque d'erreur NoReverseMatch")
        
        return issues
    
    def check_context_variables(self, content, template_name):
        """Vérifie les variables de contexte potentiellement problématiques"""
        issues = []
        
        # Variables qui pourraient causer des erreurs
        risky_variables = [
            r'{{\s*ordonnance\.id\s*}}',
            r'{{\s*ordonnance\.\w+\s*}}',
            r'{{\s*user\.groups\.all\.0\.name\s*}}',
            r'{{\s*request\.resolver_match\.url_name\s*}}'
        ]
        
        for pattern in risky_variables:
            matches = re.findall(pattern, content)
            for match in matches:
                issues.append(f"Variable potentiellement risquée: {match}")
        
        return issues
    
    def check_blocks(self, content, template_name):
        """Vérifie la cohérence des blocs"""
        issues = []
        
        # Trouver tous les blocs
        block_pattern = r'{% block (\w+) %}'
        blocks = re.findall(block_pattern, content)
        endblock_pattern = r'{% endblock(?: (\w+))? %}'
        endblocks = re.findall(endblock_pattern, content)
        
        # Vérifier la correspondance des blocs
        if len(blocks) != len(endblocks):
            issues.append(f"Nombre de blocs ({len(blocks)}) et endblocks ({len(endblocks)}) différent")
        
        # Vérifier les blocs manquants dans base_pharmacien.html
        if template_name == "base_pharmacien.html":
            required_blocks = ['title', 'content', 'extra_css', 'extra_js']
            missing_blocks = [block for block in required_blocks if block not in blocks]
            if missing_blocks:
                issues.append(f"Blocs requis manquants: {missing_blocks}")
        
        return issues
    
    def check_includes(self, content, template_name):
        """Vérifie les inclusions de templates"""
        issues = []
        include_pattern = r'{% include [\'"]([^\'"]+)[\'"] %}'
        includes = re.findall(include_pattern, content)
        
        for include in includes:
            if not self.template_exists(include):
                issues.append(f"Inclusion manquante: '{include}'")
        
        return issues
    
    def template_exists(self, template_path):
        """Vérifie si un template existe"""
        # Vérifier dans le même dossier
        if not '/' in template_path:
            return (self.templates_dir / template_path).exists()
        
        # Vérifier les chemins relatifs
        full_path = self.templates_dir.parent / template_path
        return full_path.exists()
    
    def get_extends(self, content):
        """Récupère le template étendu"""
        match = re.search(r'{% extends [\'"]([^\'"]+)[\'"] %}', content)
        return match.group(1) if match else None
    
    def get_all_urls(self, content):
        """Récupère toutes les URLs"""
        url_pattern = r'{% url [\'"]([^\'":]+):?([^\'"]*)[\'"] ?([^%]*)%}'
        return re.findall(url_pattern, content)
    
    def get_blocks(self, content):
        """Récupère tous les blocs"""
        block_pattern = r'{% block (\w+) %}'
        return re.findall(block_pattern, content)
    
    def get_includes(self, content):
        """Récupère toutes les inclusions"""
        include_pattern = r'{% include [\'"]([^\'"]+)[\'"] %}'
        return re.findall(include_pattern, content)
    
    def generate_report(self):
        """Génère un rapport complet"""
        print("\n" + "=" * 60)
        print("📊 RAPPORT D'ANALYSE COMPLET")
        print("=" * 60)
        
        # Statistiques générales
        total_templates = len(self.templates_data)
        total_issues = sum(len(data['issues']) for data in self.templates_data.values())
        
        print(f"\n📈 Statistiques:")
        print(f"   Templates analysés: {total_templates}")
        print(f"   Problèmes détectés: {total_issues}")
        
        # Templates avec problèmes
        problematic_templates = {name: data for name, data in self.templates_data.items() if data['issues']}
        
        if problematic_templates:
            print(f"\n🚨 Templates avec problèmes:")
            for name, data in problematic_templates.items():
                print(f"\n   📄 {name}:")
                for issue in data['issues']:
                    print(f"      ⚠️  {issue}")
        else:
            print(f"\n✅ Tous les templates sont corrects!")
        
        # Analyse des dépendances
        print(f"\n🔗 Analyse des dépendances:")
        for name, data in self.templates_data.items():
            if data['extends']:
                print(f"   {name} → étend {data['extends']}")
            if data['includes']:
                for include in data['includes']:
                    print(f"   {name} → inclut {include}")
        
        # Recommandations
        self.generate_recommendations()
    
    def generate_recommendations(self):
        """Génère des recommandations d'amélioration"""
        print(f"\n💡 RECOMMANDATIONS:")
        
        # Vérifier base_pharmacien.html
        base_data = self.templates_data.get('base_pharmacien.html')
        if base_data:
            print("   1. Vérifier que base_pharmacien.html contient tous les blocs nécessaires")
            print("   2. S'assurer que les URLs avec arguments ont des valeurs par défaut")
        
        # Vérifier les URLs problématiques
        all_urls = []
        for data in self.templates_data.values():
            all_urls.extend(data['urls'])
        
        risky_urls = [url for url in all_urls if 'valider_ordonnance' in url[0] and not url[2].strip()]
        if risky_urls:
            print("   3. Corriger les URLs 'valider_ordonnance' sans arguments")
        
        print("   4. Tester tous les templates avec un contexte vide")
        print("   5. Vérifier les inclusions conditionnelles (user.is_authenticated)")

def main():
    # Chemin vers vos templates pharmacien
    templates_path = "/Users/koffitanohsoualiho/Documents/projet/templates/pharmacien"
    
    if not os.path.exists(templates_path):
        print(f"❌ Le dossier {templates_path} n'existe pas!")
        return
    
    analyzer = TemplateAnalyzer(templates_path)
    analyzer.analyze_all_templates()

if __name__ == "__main__":
    main()