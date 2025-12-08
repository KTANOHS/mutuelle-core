#!/usr/bin/env python
"""
Script de vérification de l'utilisation correcte de timezone dans un projet Django
Vérifie et corrige les utilisations de datetime.now() non sécurisées
"""

import os
import re
import ast
import argparse
from pathlib import Path

class TimezoneChecker:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.issues = []
        self.files_checked = 0
        
    def check_file(self, file_path):
        """Vérifie un fichier Python pour les problèmes de timezone"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Ignorer les fichiers de migrations et venv
            if 'migrations' in str(file_path) or 'venv' in str(file_path):
                return
                
            self.files_checked += 1
            lines = content.split('\n')
            
            # Vérifier les patterns problématiques
            datetime_patterns = [
                (r'datetime\.datetime\.now\(\)', 'datetime.datetime.now()'),
                (r'datetime\.now\(\)', 'datetime.now()'),
                (r'from datetime import datetime', 'import datetime incorrect'),
                (r'import datetime', 'import datetime générique')
            ]
            
            for i, line in enumerate(lines, 1):
                for pattern, issue_type in datetime_patterns:
                    if re.search(pattern, line) and not line.strip().startswith('#'):
                        # Vérifier si timezone est déjà importé dans le fichier
                        has_timezone_import = any(
                            'from django.utils import timezone' in l or 
                            'import timezone' in l 
                            for l in lines
                        )
                        
                        self.issues.append({
                            'file': str(file_path.relative_to(self.project_root)),
                            'line': i,
                            'content': line.strip(),
                            'issue': issue_type,
                            'has_timezone_import': has_timezone_import
                        })
                        
        except Exception as e:
            print(f"❌ Erreur lors de la vérification de {file_path}: {e}")
    
    def check_project(self):
        """Parcourt tous les fichiers Python du projet"""
        python_files = list(self.project_root.rglob('*.py'))
        
        print(f"🔍 Vérification de {len(python_files)} fichiers Python...")
        
        for file_path in python_files:
            self.check_file(file_path)
    
    def generate_report(self):
        """Génère un rapport détaillé"""
        print(f"\n{'='*80}")
        print("📊 RAPPORT DE VÉRIFICATION TIMEZONE")
        print(f"{'='*80}")
        print(f"📁 Projet vérifié: {self.project_root}")
        print(f"📄 Fichiers analysés: {self.files_checked}")
        print(f"⚠️  Problèmes détectés: {len(self.issues)}")
        print(f"{'='*80}")
        
        if not self.issues:
            print("✅ Aucun problème détecté !")
            return
        
        # Grouper par fichier
        files_issues = {}
        for issue in self.issues:
            file = issue['file']
            if file not in files_issues:
                files_issues[file] = []
            files_issues[file].append(issue)
        
        for file, issues in files_issues.items():
            print(f"\n📁 {file}:")
            for issue in issues:
                status = "🟢" if issue['has_timezone_import'] else "🔴"
                print(f"   Ligne {issue['line']}: {status} {issue['issue']}")
                print(f"      → {issue['content']}")
    
    def generate_fixes(self):
        """Génère les corrections recommandées"""
        print(f"\n{'='*80}")
        print("🔧 CORRECTIONS RECOMMANDÉES")
        print(f"{'='*80}")
        
        for issue in self.issues:
            if not issue['has_timezone_import']:
                print(f"\n📁 {issue['file']}:")
                print("   AJOUTER cet import en haut du fichier:")
                print("   from django.utils import timezone")
                
            print(f"   Ligne {issue['line']}: Remplacer:")
            print(f"      {issue['content']}")
            
            # Suggestion de correction
            if 'datetime.datetime.now()' in issue['content']:
                new_line = issue['content'].replace('datetime.datetime.now()', 'timezone.now()')
            elif 'datetime.now()' in issue['content']:
                new_line = issue['content'].replace('datetime.now()', 'timezone.now()')
            else:
                new_line = issue['content']
                
            print(f"   PAR:")
            print(f"      {new_line}")

def create_timezone_migration_script():
    """Crée un script pour migrer automatiquement les timezones"""
    script_content = '''#!/usr/bin/env python
"""
Script de migration automatique pour corriger les timezones
Utilisation: python migrate_timezones.py
"""

import os
import re
import sys
from pathlib import Path

def migrate_file(file_path):
    """Migre un fichier pour utiliser timezone"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier si timezone est déjà importé
        needs_timezone_import = 'from django.utils import timezone' not in content
        
        # Remplacer les datetime.now()
        new_content = content
        
        # Pattern 1: datetime.datetime.now()
        new_content = re.sub(
            r'datetime\.datetime\.now\(\)', 
            'timezone.now()', 
            new_content
        )
        
        # Pattern 2: datetime.now() (avec import from datetime)
        new_content = re.sub(
            r'(?<!\.)datetime\.now\(\)', 
            'timezone.now()', 
            new_content
        )
        
        # Ajouter l'import timezone si nécessaire
        if needs_timezone_import and ('timezone.now()' in new_content or 'timezone.' in new_content):
            # Trouver où ajouter l'import (après les imports Django)
            lines = new_content.split('\\n')
            new_lines = []
            timezone_import_added = False
            
            for line in lines:
                new_lines.append(line)
                # Ajouter après les imports Django standards
                if not timezone_import_added and ('from django.' in line or 'import django' in line):
                    new_lines.append('from django.utils import timezone')
                    timezone_import_added = True
            
            if not timezone_import_added:
                # Ajouter au début du fichier
                new_lines.insert(0, 'from django.utils import timezone')
            
            new_content = '\\n'.join(new_lines)
        
        # Écrire le fichier modifié
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration de {file_path}: {e}")
        return False

def main():
    project_root = input("Entrez le chemin du projet Django: ").strip()
    if not project_root:
        project_root = "."
    
    project_path = Path(project_root)
    
    if not project_path.exists():
        print("❌ Le chemin spécifié n'existe pas")
        return
    
    python_files = list(project_path.rglob('*.py'))
    migrated_count = 0
    
    print(f"🔄 Migration de {len(python_files)} fichiers...")
    
    for file_path in python_files:
        # Ignorer les migrations et venv
        if 'migrations' in str(file_path) or 'venv' in str(file_path):
            continue
            
        if migrate_file(file_path):
            print(f"✅ Migré: {file_path.relative_to(project_path)}")
            migrated_count += 1
    
    print(f"\\n🎉 Migration terminée! {migrated_count} fichiers modifiés.")

if __name__ == "__main__":
    main()
'''

    with open('migrate_timezones.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("📄 Script de migration créé: migrate_timezones.py")

def main():
    parser = argparse.ArgumentParser(description='Vérificateur de timezone Django')
    parser.add_argument('path', nargs='?', default='.', help='Chemin du projet Django')
    parser.add_argument('--fix', action='store_true', help='Créer un script de correction automatique')
    
    args = parser.parse_args()
    
    # Vérifier que c'est un projet Django
    project_root = Path(args.path)
    if not (project_root / 'manage.py').exists():
        print("❌ Ceci ne semble pas être un projet Django (manage.py introuvable)")
        return
    
    print("🔍 Démarrage de la vérification timezone...")
    
    checker = TimezoneChecker(project_root)
    checker.check_project()
    checker.generate_report()
    checker.generate_fixes()
    
    if args.fix:
        create_timezone_migration_script()
        
        print(f"\n💡 Pour appliquer les corrections automatiquement:")
        print("   python migrate_timezones.py")
        print("   ou exécutez le script interactivement")

if __name__ == "__main__":
    main()