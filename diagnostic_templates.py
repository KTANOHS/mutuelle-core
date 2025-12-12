#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC DES TEMPLATES DJANGO
==========================================
Ce script analyse tous les templates HTML du projet pour détecter :
1. Chemins statiques incorrects
2. Fichiers manquants
3. URLs incorrects
4. Problèmes courants de déploiement Render
"""

import os
import re
import sys
import json
import shutil
from pathlib import Path
from collections import defaultdict

class TemplateDiagnostic:
    def __init__(self, project_root=None):
        self.project_root = project_root or os.getcwd()
        self.static_dir = None
        self.templates_dir = None
        self.results = defaultdict(list)
        self.file_stats = defaultdict(dict)
        
    def setup_paths(self):
        """Définit les chemins du projet"""
        print("📁 Configuration des chemins...")
        
        # Chercher les dossiers importants
        possible_static_dirs = [
            os.path.join(self.project_root, 'static'),
            os.path.join(self.project_root, 'staticfiles'),
            os.path.join(self.project_root, 'mutuelle_core/static'),
            os.path.join(self.project_root, 'static_root'),
        ]
        
        possible_template_dirs = [
            os.path.join(self.project_root, 'templates'),
            os.path.join(self.project_root, 'mutuelle_core/templates'),
        ]
        
        # Trouver static
        for dir_path in possible_static_dirs:
            if os.path.exists(dir_path):
                self.static_dir = dir_path
                print(f"✅ Dossier static trouvé: {dir_path}")
                break
        
        if not self.static_dir:
            print("❌ Aucun dossier static trouvé!")
            self.static_dir = os.path.join(self.project_root, 'static')
            os.makedirs(self.static_dir, exist_ok=True)
            print(f"📁 Création du dossier: {self.static_dir}")
        
        # Trouver templates
        for dir_path in possible_template_dirs:
            if os.path.exists(dir_path):
                self.templates_dir = dir_path
                print(f"✅ Dossier templates trouvé: {dir_path}")
                break
        
        if not self.templates_dir:
            print("❌ Aucun dossier templates trouvé!")
            sys.exit(1)
    
    def find_all_templates(self):
        """Trouve tous les fichiers templates HTML"""
        print("\n🔍 Recherche des templates HTML...")
        templates = []
        
        for root, dirs, files in os.walk(self.templates_dir):
            for file in files:
                if file.endswith('.html'):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.templates_dir)
                    templates.append((full_path, rel_path))
        
        print(f"📄 {len(templates)} templates trouvés")
        return templates
    
    def analyze_static_references(self, content, filepath, rel_path):
        """Analyse les références aux fichiers statiques"""
        patterns = {
            'static_tag': r'\{%\s*static\s+[\'"]([^\'"]+)[\'"]\s*%\}',
            'static_url': r'src=["\']/static/([^"\']+)["\']',
            'static_css': r'href=["\']/static/([^"\']+)["\']',
            'static_js': r'script\s+src=["\']/static/([^"\']+)["\']',
        }
        
        issues = []
        line_num = 0
        
        for line in content.split('\n'):
            line_num += 1
            line_issues = []
            
            # Vérifier les tags {% static %}
            static_matches = re.findall(patterns['static_tag'], line)
            for match in static_matches:
                if 'mutuelle_core/' in match:
                    line_issues.append({
                        'type': 'static_path',
                        'message': f"Chemin avec 'mutuelle_core/': {match}",
                        'suggestion': match.replace('mutuelle_core/', ''),
                        'line': line_num,
                        'code': line.strip()
                    })
                
                # Vérifier si le fichier existe
                static_file_path = os.path.join(self.static_dir, match)
                if not os.path.exists(static_file_path):
                    # Chercher dans d'autres dossiers
                    found = False
                    for search_dir in ['static', 'staticfiles', 'mutuelle_core/static']:
                        alt_path = os.path.join(self.project_root, search_dir, match)
                        if os.path.exists(alt_path):
                            found = True
                            break
                    
                    if not found:
                        line_issues.append({
                            'type': 'missing_file',
                            'message': f"Fichier statique introuvable: {match}",
                            'line': line_num,
                            'code': line.strip()
                        })
            
            # Vérifier les URLs statiques en dur
            for pattern_name, pattern in [('static_url', patterns['static_url']),
                                         ('static_css', patterns['static_css']),
                                         ('static_js', patterns['static_js'])]:
                matches = re.findall(pattern, line)
                for match in matches:
                    if 'mutuelle_core/' in match:
                        line_issues.append({
                            'type': 'hardcoded_static',
                            'message': f"URL statique en dur avec 'mutuelle_core/': {match}",
                            'suggestion': f"{{% static '{match.replace('mutuelle_core/', '')}' %}}",
                            'line': line_num,
                            'code': line.strip()
                        })
            
            if line_issues:
                issues.extend(line_issues)
        
        return issues
    
    def analyze_url_references(self, content, filepath, rel_path):
        """Analyse les références aux URLs Django"""
        patterns = {
            'url_tag': r'\{%\s*url\s+[\'"]([^\'":]+)(?::[^\'"]*)?[\'"]\s*%\}',
            'url_with_args': r'\{%\s*url\s+[\'"]([^\'"]+)[\'"]([^%]*)?%\}',
        }
        
        issues = []
        line_num = 0
        
        for line in content.split('\n'):
            line_num += 1
            line_issues = []
            
            # Vérifier les tags {% url %}
            url_matches = re.findall(patterns['url_tag'], line)
            for match in url_matches:
                # Nettoyer le match (pourrait contenir des arguments)
                url_name = match.strip()
                if ':' in url_name:
                    url_name = url_name.split(':')[0]
                
                # Liste des URLs connues problématiques
                problematic_urls = {
                    'undefined': "URL non définie (vérifier urls.py)",
                    'nouveau': "URL 'nouveau' probablement incorrecte",
                }
                
                for pattern, message in problematic_urls.items():
                    if pattern in url_name.lower():
                        line_issues.append({
                            'type': 'url_issue',
                            'message': f"{message}: {url_name}",
                            'line': line_num,
                            'code': line.strip()
                        })
            
            if line_issues:
                issues.extend(line_issues)
        
        return issues
    
    def analyze_template_errors(self, content, filepath, rel_path):
        """Détecte les erreurs courantes dans les templates"""
        issues = []
        line_num = 0
        
        error_patterns = [
            (r'(\{\{.*?\}\}.*?\{%)|(\{%.*?\}\}.*?\}\})', 'balises Django mal fermées'),
            (r'\{%\s*(endfor|endif|endblock|endfor|empty)\s*\}', 'balise de fermeture mal formatée'),
            (r'src=["\']\s*\{\{.*?\}\}\s*["\']', 'variable dans src sans filtre safe'),
        ]
        
        for line in content.split('\n'):
            line_num += 1
            
            for pattern, message in error_patterns:
                if re.search(pattern, line):
                    issues.append({
                        'type': 'template_syntax',
                        'message': f"Erreur de syntaxe potentielle: {message}",
                        'line': line_num,
                        'code': line.strip()
                    })
        
        return issues
    
    def scan_template(self, filepath, rel_path):
        """Analyse un template spécifique"""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        issues = []
        
        # Analyser les problèmes
        issues.extend(self.analyze_static_references(content, filepath, rel_path))
        issues.extend(self.analyze_url_references(content, filepath, rel_path))
        issues.extend(self.analyze_template_errors(content, filepath, rel_path))
        
        # Statistiques
        self.file_stats[rel_path] = {
            'lines': len(content.split('\n')),
            'size_kb': os.path.getsize(filepath) / 1024,
            'issues_count': len(issues)
        }
        
        return issues
    
    def create_fix_script(self):
        """Crée un script de correction automatique"""
        fix_script = """#!/usr/bin/env python
"""
        return fix_script
    
    def generate_report(self):
        """Génère un rapport HTML détaillé"""
        report_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diagnostic Templates Django - Rapport</title>
    <style>
        :root {
            --primary: #2c5aa0;
            --success: #34c759;
            --warning: #ffc107;
            --danger: #dc3545;
            --dark: #343a40;
            --light: #f8f9fa;
        }
        
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: #f5f7fa;
            color: var(--dark);
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            background: linear-gradient(135deg, var(--primary), #1e3a8a);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(44, 90, 160, 0.2);
        }
        
        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }
        
        .card.success { border-left: 4px solid var(--success); }
        .card.warning { border-left: 4px solid var(--warning); }
        .card.danger { border-left: 4px solid var(--danger); }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }
        
        .file-list {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 15px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        
        .file-header {
            background: var(--light);
            padding: 1rem;
            border-bottom: 1px solid #dee2e6;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .file-content {
            padding: 1rem;
            border-top: 1px solid #dee2e6;
        }
        
        .issue {
            padding: 0.75rem;
            margin: 0.5rem 0;
            border-radius: 6px;
            background: #fff;
            border-left: 3px solid var(--warning);
        }
        
        .issue.danger { border-left-color: var(--danger); }
        .issue.success { border-left-color: var(--success); }
        
        .badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-right: 0.5rem;
        }
        
        .badge-danger { background: var(--danger); color: white; }
        .badge-warning { background: var(--warning); color: var(--dark); }
        .badge-info { background: #17a2b8; color: white; }
        
        .suggestion {
            background: #e8f4fd;
            padding: 0.75rem;
            margin-top: 0.5rem;
            border-radius: 4px;
            font-family: monospace;
        }
        
        @media print {
            body { background: white; }
            .file-content { display: block !important; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Diagnostic des Templates Django</h1>
            <p>Généré le {{timestamp}}</p>
        </div>
        
        <div class="summary-cards">
            <div class="card success">
                <h3>Templates Analysés</h3>
                <div class="stat-number">{{total_templates}}</div>
            </div>
            <div class="card warning">
                <h3>Problèmes Trouvés</h3>
                <div class="stat-number">{{total_issues}}</div>
            </div>
            <div class="card danger">
                <h3>Fichiers à Corriger</h3>
                <div class="stat-number">{{critical_files}}</div>
            </div>
        </div>
        
        <div class="file-list">
"""
        
        # Ajouter chaque template au rapport
        for rel_path, issues in self.results.items():
            if issues:  # Seulement les templates avec problèmes
                stats = self.file_stats.get(rel_path, {})
                
                report_html += f"""
            <div class="file-header" onclick="toggleFile('{rel_path.replace('/', '_')}')">
                <div>
                    <strong>📄 {rel_path}</strong>
                    <span style="margin-left: 1rem; color: #6c757d;">
                        {stats.get('lines', 0)} lignes • {stats.get('size_kb', 0):.1f} KB
                    </span>
                </div>
                <div>
                    <span class="badge badge-danger">{len(issues)} problèmes</span>
                </div>
            </div>
            <div class="file-content" id="{rel_path.replace('/', '_')}" style="display: none;">
"""
                
                for issue in issues:
                    badge_class = {
                        'static_path': 'badge-warning',
                        'missing_file': 'badge-danger',
                        'hardcoded_static': 'badge-warning',
                        'url_issue': 'badge-info',
                        'template_syntax': 'badge-danger'
                    }.get(issue['type'], 'badge-info')
                    
                    report_html += f"""
                <div class="issue {issue['type']}">
                    <div>
                        <span class="badge {badge_class}">{issue['type']}</span>
                        <strong>Ligne {issue['line']}:</strong> {issue['message']}
                    </div>
                    <div style="margin: 0.5rem 0; padding: 0.5rem; background: #f8f9fa; border-radius: 4px; font-family: monospace;">
                        {issue['code']}
                    </div>
"""
                    
                    if 'suggestion' in issue:
                        report_html += f"""
                    <div class="suggestion">
                        💡 <strong>Suggestion:</strong> {issue['suggestion']}
                    </div>
"""
                    
                    report_html += """
                </div>
"""
                
                report_html += """
            </div>
"""
        
        report_html += """
        </div>
        
        <div class="card">
            <h3>📋 Résumé des Actions Requises</h3>
            <ul>
                <li><strong>1. Chemins statiques incorrects:</strong> Remplacer 'mutuelle_core/' par des chemins directs</li>
                <li><strong>2. Fichiers manquants:</strong> Vérifier l'existence des fichiers référencés</li>
                <li><strong>3. URLs en dur:</strong> Utiliser les tags {% url %} au lieu des chemins absolus</li>
                <li><strong>4. Syntaxe des templates:</strong> Vérifier la fermeture des balises Django</li>
            </ul>
        </div>
    </div>
    
    <script>
        function toggleFile(fileId) {
            const element = document.getElementById(fileId);
            if (element.style.display === 'none') {
                element.style.display = 'block';
            } else {
                element.style.display = 'none';
            }
        }
        
        // Ouvrir tous les fichiers avec des problèmes critiques
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.badge-danger').forEach(badge => {
                const fileHeader = badge.closest('.file-header');
                if (fileHeader) {
                    const fileId = fileHeader.getAttribute('onclick').match(/'([^']+)'/)[1];
                    document.getElementById(fileId).style.display = 'block';
                }
            });
        });
    </script>
</body>
</html>
"""
        
        return report_html
    
    def run_diagnostic(self):
        """Exécute le diagnostic complet"""
        print("\n" + "="*60)
        print("🔍 DIAGNOSTIC COMPLET DES TEMPLATES")
        print("="*60)
        
        # Configuration
        self.setup_paths()
        
        # Trouver tous les templates
        templates = self.find_all_templates()
        
        if not templates:
            print("❌ Aucun template trouvé!")
            return
        
        # Analyser chaque template
        total_issues = 0
        problematic_files = 0
        
        for filepath, rel_path in templates:
            print(f"\n📄 Analyse de: {rel_path}")
            
            issues = self.scan_template(filepath, rel_path)
            
            if issues:
                problematic_files += 1
                total_issues += len(issues)
                self.results[rel_path] = issues
                
                # Afficher un résumé
                print(f"   ⚠️  {len(issues)} problème(s) trouvé(s):")
                for issue in issues[:3]:  # Afficher les 3 premiers problèmes
                    print(f"      • {issue['type']}: {issue['message']} (ligne {issue['line']})")
                
                if len(issues) > 3:
                    print(f"      ... et {len(issues) - 3} autres")
            else:
                print(f"   ✅ Aucun problème détecté")
        
        # Afficher le résumé
        print("\n" + "="*60)
        print("📊 RÉSUMÉ DU DIAGNOSTIC")
        print("="*60)
        print(f"📁 Templates analysés: {len(templates)}")
        print(f"⚠️  Fichiers problématiques: {problematic_files}")
        print(f"❌ Problèmes totaux: {total_issues}")
        
        # Afficher les problèmes par catégorie
        categories = defaultdict(int)
        for issues in self.results.values():
            for issue in issues:
                categories[issue['type']] += 1
        
        print("\n📈 DÉTAIL PAR CATÉGORIE:")
        for category, count in categories.items():
            print(f"   • {category}: {count}")
        
        # Générer un rapport si des problèmes sont trouvés
        if total_issues > 0:
            print("\n📝 Génération du rapport...")
            
            # Créer le répertoire de rapports
            report_dir = os.path.join(self.project_root, 'diagnostic_reports')
            os.makedirs(report_dir, exist_ok=True)
            
            # Générer le rapport HTML
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            report_html = self.generate_report()
            report_html = report_html.replace("{{timestamp}}", timestamp)
            report_html = report_html.replace("{{total_templates}}", str(len(templates)))
            report_html = report_html.replace("{{total_issues}}", str(total_issues))
            report_html = report_html.replace("{{critical_files}}", str(problematic_files))
            
            report_path = os.path.join(report_dir, 'template_diagnostic.html')
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_html)
            
            print(f"✅ Rapport généré: {report_path}")
            
            # Créer un fichier de correction automatique
            fix_script = self.create_fix_script()
            fix_path = os.path.join(report_dir, 'fix_templates.py')
            with open(fix_path, 'w', encoding='utf-8') as f:
                f.write(fix_script)
            
            print(f"✅ Script de correction: {fix_path}")
            
            # Afficher les recommandations
            print("\n" + "="*60)
            print("🎯 RECOMMANDATIONS")
            print("="*60)
            
            if categories.get('static_path'):
                print("""
1. CHEMINS STATIQUES INCORRECTS:
   ---------------------------------
   • Remplacer: {% static 'mutuelle_core/images/logo.jpg' %}
   • Par: {% static 'images/logo.jpg' %}
   
   Commandes de correction:
   sed -i '' "s|mutuelle_core/images/|images/|g" templates/*.html templates/**/*.html
   sed -i '' "s|mutuelle_core/videos/|videos/|g" templates/*.html templates/**/*.html
   sed -i '' "s|mutuelle_core/js/|js/|g" templates/*.html templates/**/*.html
""")
            
            if categories.get('missing_file'):
                print("""
2. FICHIERS STATIQUES MANQUANTS:
   ---------------------------------
   • Vérifiez que ces fichiers existent dans static/:
     - images/logo.jpg
     - videos/presentation.webm
     - js/messagerie-integration.js
   
   Commandes de vérification:
   find . -name "logo.jpg" -o -name "presentation.webm" -o -name "messagerie-integration.js"
""")
            
            if categories.get('url_issue'):
                print("""
3. URLS NON DÉFINIES:
   ---------------------------------
   • Vérifiez les URLs dans urls.py
   • Testez avec: python manage.py show_urls
""")
            
            print("\n" + "="*60)
            print("🚀 ACTIONS IMMÉDIATES")
            print("="*60)
            print("""
1. Vérifiez le rapport HTML détaillé
2. Appliquez les corrections suggérées
3. Testez avec: python manage.py collectstatic
4. Redémarrez le serveur: python manage.py runserver
""")
        else:
            print("\n🎉 FÉLICITATIONS! Aucun problème détecté dans les templates.")
        
        return total_issues == 0
    
    def create_auto_fix_script(self):
        """Crée un script de correction automatique"""
        script_content = """#!/usr/bin/env python
"""
        return script_content

def main():
    """Fonction principale"""
    print("🔧 DIAGNOSTIC DES TEMPLATES DJANGO")
    print("==================================")
    
    # Demander le chemin du projet
    project_root = input("Chemin du projet Django (laisser vide pour courant): ").strip()
    if not project_root:
        project_root = os.getcwd()
    
    diagnostic = TemplateDiagnostic(project_root)
    success = diagnostic.run_diagnostic()
    
    if not success:
        print("\n❌ Des problèmes ont été détectés. Consultez le rapport.")
        sys.exit(1)
    else:
        print("\n✅ Diagnostic terminé avec succès!")
        sys.exit(0)

if __name__ == "__main__":
    main()