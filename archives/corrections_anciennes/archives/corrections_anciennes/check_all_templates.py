#!/usr/bin/env python3
"""
Script de vérification de tous les templates pour détecter les URLs problématiques
Recherche spécifiquement les erreurs NoReverseMatch potentielles
"""

import re
from pathlib import Path

class TemplateChecker:
    def __init__(self, templates_dir):
        self.templates_dir = Path(templates_dir)
        self.problems = []
        
    def check_all_templates(self):
        """Vérifie tous les templates HTML"""
        print("🔍 VÉRIFICATION DE TOUS LES TEMPLATES")
        print("=" * 60)
        
        if not self.templates_dir.exists():
            print(f"❌ Dossier templates non trouvé: {self.templates_dir}")
            return
        
        # Compter les templates
        html_files = list(self.templates_dir.rglob("*.html"))
        print(f"📁 Dossier: {self.templates_dir}")
        print(f"📄 {len(html_files)} templates à analyser")
        print("-" * 60)
        
        for html_file in sorted(html_files):
            self.check_template(html_file)
        
        self.generate_report()
    
    def check_template(self, template_path):
        """Vérifie un template spécifique"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = template_path.relative_to(self.templates_dir)
            issues = []
            
            # 1. Vérifier les URLs valider_ordonnance avec ordonnance.id
            valider_issues = self.check_valider_ordonnance_urls(content, relative_path)
            issues.extend(valider_issues)
            
            # 2. Vérifier les URLs avec des variables potentiellement vides
            empty_var_issues = self.check_empty_variable_urls(content, relative_path)
            issues.extend(empty_var_issues)
            
            # 3. Vérifier les URLs avec des arguments manquants
            missing_args_issues = self.check_missing_argument_urls(content, relative_path)
            issues.extend(missing_args_issues)
            
            # 4. Vérifier les includes manquants
            include_issues = self.check_missing_includes(content, relative_path)
            issues.extend(include_issues)
            
            # 5. Vérifier les extends manquants
            extends_issues = self.check_missing_extends(content, relative_path)
            issues.extend(extends_issues)
            
            if issues:
                self.problems.append({
                    'template': relative_path,
                    'issues': issues,
                    'content': content
                })
                print(f"❌ {relative_path}")
                for issue in issues:
                    print(f"   ⚠️  {issue}")
            else:
                print(f"✅ {relative_path}")
                
        except Exception as e:
            error_msg = f"Erreur de lecture: {e}"
            print(f"❌ {template_path.relative_to(self.templates_dir)} - {error_msg}")
    
    def check_valider_ordonnance_urls(self, content, template_path):
        """Vérifie les URLs valider_ordonnance problématiques"""
        issues = []
        
        # Pattern pour détecter les URLs valider_ordonnance avec ordonnance.id
        patterns = [
            r"{%\s*url\s+['\"]pharmacien:valider_ordonnance['\"]\s+ordonnance\.id\s*%}",
            r"{%\s*url\s+['\"]pharmacien:valider_ordonnance['\"]\s+ordonnance\.id\s*%}",
            r'href=[\'"]{%\s*url\s+[\'"]pharmacien:valider_ordonnance[\'"]\s+ordonnance\.id\s*%}[\'"]'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                issues.append(f"Ligne {line_num}: URL 'valider_ordonnance' avec 'ordonnance.id' - risque NoReverseMatch")
        
        return issues
    
    def check_empty_variable_urls(self, content, template_path):
        """Vérifie les URLs avec des variables potentiellement vides"""
        issues = []
        
        # Pattern pour détecter les URLs avec des variables simples qui pourraient être vides
        pattern = r'{%\s*url\s+[\'"]([^\'"]+)[\'"]\s+([^%]+)?%}'
        
        matches = re.finditer(pattern, content)
        for match in matches:
            url_name = match.group(1)
            args = match.group(2) if match.group(2) else ""
            
            # Vérifier les variables simples qui pourraient être vides
            simple_var_pattern = r'(\w+)\.(id|pk)\b'
            var_matches = re.findall(simple_var_pattern, args)
            
            for var_name, field in var_matches:
                # Vérifier si la variable n'est pas protégée par une condition
                line_start = content.rfind('\n', 0, match.start()) + 1
                line_end = content.find('\n', match.start())
                line_content = content[line_start:line_end] if line_end != -1 else content[line_start:]
                
                # Vérifier s'il y a une condition protectrice
                if not self.has_protective_condition(content, match.start(), var_name):
                    line_num = content[:match.start()].count('\n') + 1
                    issues.append(f"Ligne {line_num}: URL '{url_name}' avec '{var_name}.{field}' non protégée")
        
        return issues
    
    def check_missing_argument_urls(self, content, template_path):
        """Vérifie les URLs avec des arguments manquants"""
        issues = []
        
        # URLs qui nécessitent des arguments
        urls_requiring_args = {
            'pharmacien:valider_ordonnance': 'ordonnance_id',
            'pharmacien:detail_ordonnance': 'ordonnance_id',
        }
        
        # Pattern pour détecter les URLs sans arguments
        pattern = r'{%\s*url\s+[\'"]([^\'"]+)[\'"]\s*%}'
        
        matches = re.finditer(pattern, content)
        for match in matches:
            url_name = match.group(1)
            if url_name in urls_requiring_args and not self.is_in_loop(content, match.start()):
                line_num = content[:match.start()].count('\n') + 1
                required_arg = urls_requiring_args[url_name]
                issues.append(f"Ligne {line_num}: URL '{url_name}' sans argument '{required_arg}' requis")
        
        return issues
    
    def check_missing_includes(self, content, template_path):
        """Vérifie les includes de templates manquants"""
        issues = []
        
        pattern = r'{%\s*include\s+[\'"]([^\'"]+)[\'"]\s*%}'
        matches = re.finditer(pattern, content)
        
        for match in matches:
            include_path = match.group(1)
            full_path = self.templates_dir / include_path
            
            if not full_path.exists():
                line_num = content[:match.start()].count('\n') + 1
                issues.append(f"Ligne {line_num}: Include manquant '{include_path}'")
        
        return issues
    
    def check_missing_extends(self, content, template_path):
        """Vérifie les templates étendus manquants"""
        issues = []
        
        pattern = r'{%\s*extends\s+[\'"]([^\'"]+)[\'"]\s*%}'
        match = re.search(pattern, content)
        
        if match:
            extends_path = match.group(1)
            full_path = self.templates_dir / extends_path
            
            if not full_path.exists():
                line_num = content[:match.start()].count('\n') + 1
                issues.append(f"Ligne {line_num}: Template étendu manquant '{extends_path}'")
        
        return issues
    
    def has_protective_condition(self, content, position, variable_name):
        """Vérifie s'il y a une condition protectrice autour de la variable"""
        # Chercher une condition if avant la position
        line_start = content.rfind('\n', 0, position) + 1
        previous_content = content[:line_start]
        
        # Patterns de conditions protectrices
        patterns = [
            rf'{{\%\s*if\s+{variable_name}\s*and\s+{variable_name}\.id\s*\%}}',
            rf'{{\%\s*if\s+{variable_name}\s*\%}}',
            rf'{{\%\s*if\s+{variable_name}\s*and\s+{variable_name}\.pk\s*\%}}',
        ]
        
        for pattern in patterns:
            if re.search(pattern, previous_content, re.IGNORECASE):
                return True
        
        return False
    
    def is_in_loop(self, content, position):
        """Vérifie si la position est dans une boucle for"""
        line_start = content.rfind('\n', 0, position) + 1
        previous_content = content[:line_start]
        
        # Vérifier s'il y a une boucle for ouverte
        for_blocks = re.findall(r'{%\s*for\s+.*?%}', previous_content)
        endfor_blocks = re.findall(r'{%\s*endfor\s*%}', previous_content)
        
        return len(for_blocks) > len(endfor_blocks)
    
    def generate_report(self):
        """Génère un rapport complet"""
        print("\n" + "=" * 60)
        print("📊 RAPPORT DE VÉRIFICATION DES TEMPLATES")
        print("=" * 60)
        
        total_templates = len(list(self.templates_dir.rglob("*.html")))
        total_problems = len(self.problems)
        
        print(f"\n📈 STATISTIQUES:")
        print(f"   Templates analysés: {total_templates}")
        print(f"   Templates avec problèmes: {total_problems}")
        print(f"   Total problèmes détectés: {sum(len(p['issues']) for p in self.problems)}")
        
        if self.problems:
            print(f"\n🚨 TEMPLATES AVEC PROBLÈMES:")
            for problem in self.problems:
                print(f"\n📄 {problem['template']}:")
                for issue in problem['issues']:
                    print(f"   ⚠️  {issue}")
            
            print(f"\n💡 RECOMMANDATIONS:")
            print("   1. Remplacer les URLs 'valider_ordonnance' avec 'ordonnance.id' par des liens statiques")
            print("   2. Ajouter des conditions {% if %} autour des variables d'URL")
            print("   3. Vérifier que tous les templates inclus existent")
            print("   4. S'assurer que les templates étendus existent")
            print("   5. Utiliser des URLs sans arguments dans les menus généraux")
            
            # Générer un script de correction automatique
            self.generate_fix_script()
        else:
            print(f"\n✅ TOUS LES TEMPLATES SONT CORRECTS!")
    
    def generate_fix_script(self):
        """Génère un script de correction automatique"""
        fix_script = """#!/usr/bin/env python3
# Script généré automatiquement pour corriger les templates
# Exécutez ce script après vérification

from pathlib import Path
import re

def fix_templates():
    templates_dir = Path("/Users/koffitanohsoualiho/Documents/projet/templates")
    
    # Corrections pour base.html
    base_path = templates_dir / "base.html"
    if base_path.exists():
        with open(base_path, 'r') as f:
            content = f.read()
        
        # Remplacer valider_ordonnance avec ordonnance.id
        old_valider = 'href="{% url \\'pharmacien:valider_ordonnance\\' ordonnance.id %}"'
        new_valider = 'href="{% url \\'pharmacien:liste_ordonnances_attente\\' %}"'
        content = content.replace(old_valider, new_valider)
        
        with open(base_path, 'w') as f:
            f.write(content)
        print("✅ base.html corrigé")

if __name__ == "__main__":
    fix_templates()
"""
        
        script_path = self.templates_dir.parent / "fix_templates_auto.py"
        with open(script_path, 'w') as f:
            f.write(fix_script)
        
        print(f"\n🔧 Script de correction généré: {script_path}")
        print("   Exécutez: python fix_templates_auto.py")

def main():
    # Chemin vers vos templates
    templates_path = "/Users/koffitanohsoualiho/Documents/projet/templates"
    
    checker = TemplateChecker(templates_path)
    checker.check_all_templates()

if __name__ == "__main__":
    main()