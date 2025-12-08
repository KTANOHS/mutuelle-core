#!/usr/bin/env python3
"""
SCRIPT D'ANALYSE - Diagnostic complet de l'erreur Django Template
Analyse : Could not parse some characters: |((stats.membres_a_jour / stats.membres_actifs) * 100)||floatformat:0
"""

import os
import re
import sys
from pathlib import Path

class TemplateAnalyzer:
    def __init__(self):
        self.problems = []
        self.template_files = []
        
    def analyze_project_structure(self):
        """Analyse la structure du projet"""
        print("📁 ANALYSE DE LA STRUCTURE DU PROJET")
        print("=" * 50)
        
        # Vérifier la structure des dossiers
        required_dirs = [
            'agents',
            'agents/templates',
            'agents/templates/agents',
            'templates'
        ]
        
        for dir_path in required_dirs:
            if os.path.exists(dir_path):
                print(f"✅ {dir_path}/")
            else:
                print(f"❌ {dir_path}/ - MANQUANT")
                self.problems.append(f"Dossier manquant: {dir_path}")
    
    def find_template_files(self):
        """Trouve tous les fichiers templates"""
        print("\n🔍 RECHERCHE DES FICHIERS TEMPLATES")
        print("=" * 50)
        
        patterns = [
            '**/*.html',
            '**/templates/**/*.html',
            'agents/**/*.html'
        ]
        
        for pattern in patterns:
            for file_path in Path('.').glob(pattern):
                if file_path.is_file():
                    self.template_files.append(str(file_path))
                    print(f"📄 {file_path}")
        
        print(f"\n📊 Total templates trouvés: {len(self.template_files)}")
    
    def analyze_dashboard_template(self):
        """Analyse spécifique du template dashboard"""
        print("\n🎯 ANALYSE DU TEMPLATE DASHBOARD")
        print("=" * 50)
        
        dashboard_paths = [
            'agents/templates/agents/dashboard.html',
            'templates/agents/dashboard.html',
            'dashboard.html'
        ]
        
        dashboard_content = None
        dashboard_path = None
        
        for path in dashboard_paths:
            if os.path.exists(path):
                dashboard_path = path
                with open(path, 'r', encoding='utf-8') as f:
                    dashboard_content = f.read()
                print(f"✅ Template dashboard trouvé: {path}")
                break
        
        if not dashboard_content:
            print("❌ Template dashboard non trouvé!")
            self.problems.append("Template dashboard introuvable")
            return
        
        # Recherche du pattern problématique
        problematic_patterns = [
            r'\|\s*\(\([^)]+\)\s*\*\s*100\)\s*\|\|',
            r'\{\{\s*\|\s*\(\([^}]+\}\}',
            r'\|\|floatformat',
            r'stats\.membres_a_jour.*stats\.membres_actifs'
        ]
        
        print("\n🔎 RECHERCHE DES PATTERNS PROBLÉMATIQUES:")
        for pattern in problematic_patterns:
            matches = re.finditer(pattern, dashboard_content)
            for match in matches:
                line_num = dashboard_content[:match.start()].count('\n') + 1
                context = dashboard_content[max(0, match.start()-50):match.end()+50]
                print(f"🚨 Ligne {line_num}: {match.group()}")
                print(f"   Contexte: ...{context}...")
                self.problems.append(f"Pattern problématique ligne {line_num}: {match.group()}")
        
        # Vérifier la syntaxe spécifique du taux de conformité
        print("\n📊 VÉRIFICATION SYNTAXE TAUX CONFORMITÉ:")
        conformite_patterns = {
            'ERREUR': r'\{\{\s*\|\s*\(\(stats\.membres_a_jour\s*/\s*stats\.membres_actifs\)\s*\*\s*100\)\s*\|\|floatformat:0\s*\}\}',
            'CORRIGÉ': r'\{\{\s*stats\.pourcentage_conformite\s*\|\s*floatformat:0\s*\}\}%',
        }
        
        for name, pattern in conformite_patterns.items():
            matches = list(re.finditer(pattern, dashboard_content))
            if matches:
                print(f"🔍 {name} trouvé: {len(matches)} occurrence(s)")
                for match in matches:
                    line_num = dashboard_content[:match.start()].count('\n') + 1
                    print(f"   Ligne {line_num}: {match.group()}")
            else:
                print(f"ℹ️  {name}: Non trouvé")
    
    def analyze_views_file(self):
        """Analyse du fichier views.py"""
        print("\n🐍 ANALYSE DU FICHIER VIEWS.PY")
        print("=" * 50)
        
        views_paths = [
            'agents/views.py',
            'views.py'
        ]
        
        views_content = None
        for path in views_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    views_content = f.read()
                print(f"✅ Fichier views trouvé: {path}")
                break
        
        if not views_content:
            print("❌ Fichier views.py non trouvé!")
            self.problems.append("Fichier views.py introuvable")
            return
        
        # Vérifier la fonction dashboard
        if 'def dashboard(' in views_content:
            print("✅ Fonction dashboard() trouvée")
            
            # Extraire la fonction dashboard
            start = views_content.find('def dashboard(')
            if start != -1:
                # Trouver la fin de la fonction
                brace_count = 0
                i = start
                while i < len(views_content):
                    if views_content[i] == '{':
                        brace_count += 1
                    elif views_content[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            break
                    i += 1
                
                dashboard_func = views_content[start:i+1]
                
                # Vérifier les variables critiques
                required_vars = [
                    'pourcentage_conformite',
                    'membres_a_jour',
                    'membres_actifs',
                    'stats.pourcentage_conformite'
                ]
                
                print("\n📋 VARIABLES DANS LA FONCTION DASHBOARD:")
                for var in required_vars:
                    if var in dashboard_func:
                        print(f"✅ '{var}' trouvé")
                    else:
                        print(f"❌ '{var}' NON TROUVÉ")
                        self.problems.append(f"Variable manquante dans dashboard: {var}")
                
                # Vérifier le calcul du pourcentage
                if 'membres_a_jour / membres_actifs' in dashboard_func:
                    print("✅ Calcul du pourcentage trouvé DANS LA VUE")
                else:
                    print("❌ Calcul du pourcentage NON trouvé dans la vue")
                    self.problems.append("Calcul du pourcentage manquant dans la vue")
        
        else:
            print("❌ Fonction dashboard() non trouvée!")
            self.problems.append("Fonction dashboard() introuvable")
    
    def check_template_syntax(self, file_path):
        """Vérifie la syntaxe Django d'un template"""
        print(f"\n🔧 VÉRIFICATION SYNTAXE: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Patterns de syntaxe incorrecte
            bad_patterns = [
                (r'\{\{\s*\|\s*[^}]', "Pipe | au début d'expression"),
                (r'\|\|[^}]*\}', "Double pipe ||"),
                (r'\{\{[^}]*\|\|[^}]*\}\}', "Double pipe dans une expression"),
                (r'\{\{\s*\([^}]*\)\s*\|\|', "Calcul avec double pipe"),
            ]
            
            issues = []
            for pattern, description in bad_patterns:
                matches = list(re.finditer(pattern, content))
                if matches:
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        issues.append(f"Ligne {line_num}: {description} - '{match.group()}'")
            
            if issues:
                print(f"🚨 {len(issues)} problème(s) de syntaxe trouvé(s):")
                for issue in issues:
                    print(f"   {issue}")
                return issues
            else:
                print("✅ Aucun problème de syntaxe détecté")
                return []
                
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse: {e}")
            return [f"Erreur d'analyse: {e}"]
    
    def generate_fix_script(self):
        """Génère un script de correction automatique"""
        print("\n🔧 GÉNÉRATION DU SCRIPT DE CORRECTION")
        print("=" * 50)
        
        fix_script = '''#!/usr/bin/env python3
"""
SCRIPT DE CORRECTION AUTOMATIQUE
Généré par l'analyseur de problèmes Django
"""

import os
import re
import shutil
from datetime import datetime
from django.utils import timezone

def corriger_template_dashboard():
    """Corrige le template dashboard"""
    
    template_paths = [
        'agents/templates/agents/dashboard.html',
        'templates/agents/dashboard.html'
    ]
    
    for template_path in template_paths:
        if os.path.exists(template_path):
            print(f"🔧 Correction de: {template_path}")
            
            # Sauvegarde
            backup_path = f"{template_path}.backup_{timezone.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(template_path, backup_path)
            print(f"💾 Backup créé: {backup_path}")
            
            # Lire le contenu
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # CORRECTION PRINCIPALE
            ancien = r'\\{\\{\\s*\\|\\s*\\(\\(stats\\.membres_a_jour\\s*/\\s*stats\\.membres_actifs\\)\\s*\\*\\s*100\\)\\s*\\|\\|floatformat:0\\s*\\}\\}'
            nouveau = '{{ stats.pourcentage_conformite|floatformat:0 }}%'
            
            content_corrige = re.sub(ancien, nouveau, content)
            
            # CORRECTIONS ALTERNATIVES
            corrections = [
                (r'\\|\\s*\\(\\([^)]+\\)\\s*\\*\\s*100\\)\\s*\\|\\|floatformat', r'\\1|floatformat'),
                (r'\\{\\{\\s*\\|\\s*[^}]+\\|\\|[^}]+\\}\\}', '{{ stats.pourcentage_conformite|floatformat:0 }}%'),
            ]
            
            for ancien_pat, nouveau_pat in corrections:
                content_corrige = re.sub(ancien_pat, nouveau_pat, content_corrige)
            
            # Écrire les corrections
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content_corrige)
            
            print(f"✅ Template corrigé: {template_path}")
            return True
    
    print("❌ Aucun template dashboard trouvé à corriger")
    return False

def verifier_correction():
    """Vérifie que la correction a fonctionné"""
    print("\\n🔍 VÉRIFICATION DE LA CORRECTION...")
    
    template_paths = [
        'agents/templates/agents/dashboard.html',
        'templates/agents/dashboard.html'
    ]
    
    for template_path in template_paths:
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier que l'erreur n'est plus présente
            patterns_erreur = [
                r'\\|\\s*\\(\\(stats\\.membres_a_jour',
                r'\\|\\|floatformat'
            ]
            
            erreurs_trouvees = False
            for pattern in patterns_erreur:
                if re.search(pattern, content):
                    print(f"🚨 Erreur toujours présente dans {template_path}: {pattern}")
                    erreurs_trouvees = True
            
            if not erreurs_trouvees:
                print(f"✅ Aucune erreur détectée dans {template_path}")
            
            # Vérifier que la correction est présente
            if 'stats.pourcentage_conformite' in content:
                print(f"✅ Correction appliquée dans {template_path}")
            else:
                print(f"❌ Correction non trouvée dans {template_path}")

if __name__ == "__main__":
    print("🛠️  LANCEMENT DE LA CORRECTION AUTOMATIQUE")
    print("=" * 50)
    
    if corriger_template_dashboard():
        verifier_correction()
        print("\\n🎉 Correction terminée! Redémarrez votre serveur Django.")
    else:
        print("\\n❌ La correction a échoué. Vérifiez manuellement.")
'''
        
        with open('fix_template_problem.py', 'w', encoding='utf-8') as f:
            f.write(fix_script)
        
        print("✅ Script de correction généré: fix_template_problem.py")
        print("💡 Utilisation: python fix_template_problem.py")
    
    def generate_report(self):
        """Génère un rapport complet"""
        print("\n📊 RAPPORT D'ANALYSE COMPLET")
        print("=" * 50)
        print(f"🔍 Problèmes détectés: {len(self.problems)}")
        print(f"📄 Templates analysés: {len(self.template_files)}")
        
        if self.problems:
            print("\n🚨 PROBLEMES IDENTIFIÉS:")
            for i, problem in enumerate(self.problems, 1):
                print(f"  {i}. {problem}")
            
            print(f"\n💡 RECOMMANDATIONS:")
            print("  1. Exécutez le script de correction généré")
            print("  2. Vérifiez que 'stats.pourcentage_conformite' est bien défini dans la vue")
            print("  3. Redémarrez le serveur Django")
            print("  4. Testez l'accès au dashboard")
        else:
            print("✅ Aucun problème critique détecté")
    
    def run_full_analysis(self):
        """Exécute l'analyse complète"""
        print("🛠️  LANCEMENT DE L'ANALYSE COMPLÈTE")
        print("=" * 60)
        
        self.analyze_project_structure()
        self.find_template_files()
        self.analyze_dashboard_template()
        self.analyze_views_file()
        
        # Analyser la syntaxe des templates principaux
        for template_file in self.template_files[:3]:  # Les 3 premiers
            self.check_template_syntax(template_file)
        
        self.generate_fix_script()
        self.generate_report()

def main():
    """Fonction principale"""
    if not os.path.exists('manage.py'):
        print("❌ Ce script doit être exécuté à la racine du projet Django")
        print("💡 Assurez-vous que manage.py est dans le répertoire courant")
        return
    
    analyzer = TemplateAnalyzer()
    analyzer.run_full_analysis()

if __name__ == "__main__":
    main()