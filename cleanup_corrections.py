#!/usr/bin/env python3
"""
SCRIPT DE NETTOYAGE ET CONSOLIDATION DES FICHIERS DE CORRECTION
Auteur: Assistant Technique
Date: 2024
Description: Nettoie et consolide les 889 fichiers de correction/tests en un système organisé
"""

import os
import sys
import shutil
import hashlib
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter

# =============================================================================
# CONFIGURATION
# =============================================================================

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Chemin du projet
BASE_DIR = Path("/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30")

# Catégories pour l'organisation
CATEGORIES = {
    'correction': ['correction', 'fix', 'correct', 'repair', 'corrig', 'résoudre'],
    'diagnostic': ['diagnostic', 'analyze', 'analyse', 'check', 'verify', 'verif', 'inspect'],
    'test': ['test', '_test', 'test_', 'tester', 'validation'],
    'script': ['script', '.sh', '.bat', 'run_', 'lancer', 'execute'],
    'report': ['report', 'rapport', 'summary', 'synthese', 'resume'],
    'debug': ['debug', 'debug_', 'debugage', 'trouver_erreur'],
    'data': ['data', 'donnee', 'create_', 'generer_', 'creer_'],
    'migration': ['migration', 'migrate', 'sync', 'synchronisation'],
    'urgence': ['urgence', 'emergency', 'hotfix', 'patch', 'immediate'],
    'cleanup': ['clean', 'clear', 'nettoyage', 'purge', 'reset'],
    'guide': ['guide', 'GUIDE', 'manuel', 'instruction', 'tutorial'],
    'config': ['config', 'settings', 'setup', 'install', 'configure'],
}

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def get_file_hash(file_path):
    """Calcule le hash MD5 d'un fichier"""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def get_file_info(file_path):
    """Récupère les informations d'un fichier"""
    try:
        stat = file_path.stat()
        return {
            'path': str(file_path),
            'name': file_path.name,
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'created': datetime.fromtimestamp(stat.st_ctime),
            'hash': get_file_hash(file_path),
            'is_old': datetime.now() - datetime.fromtimestamp(stat.st_mtime) > timedelta(days=30),
        }
    except:
        return None

def categorize_file(file_name):
    """Catégorise un fichier en fonction de son nom"""
    file_lower = file_name.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in file_lower:
                return category
    return 'autre'

def read_file_content(file_path, max_lines=50):
    """Lit le contenu d'un fichier (limité pour l'analyse)"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    lines.append('... (tronqué)')
                    break
                lines.append(line.rstrip())
            return '\n'.join(lines)
    except:
        return ''

# =============================================================================
# ANALYSEUR DE FICHIERS DE CORRECTION
# =============================================================================

class CorrectionFileAnalyzer:
    """Analyse et nettoie les fichiers de correction"""
    
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.correction_files = []
        self.duplicates = defaultdict(list)
        self.categories = defaultdict(list)
        self.total_size = 0
        self.results = {}
    
    def find_correction_files(self):
        """Trouve tous les fichiers de correction"""
        print(f"{Colors.CYAN}🔍 Recherche des fichiers de correction...{Colors.END}")
        
        correction_patterns = [
            'correction', 'fix', 'correct', 'repair', 'debug', 'diagnostic',
            'test_', '_test', 'verify', 'verification', 'check', 'validate',
            'urgence', 'emergency', 'hotfix', 'patch', 'solution',
            'trouver_', 'find_', 'scan_', 'analyze', 'analyse',
            'clean_', 'clear_', 'nettoyage', 'reset',
        ]
        
        for root, dirs, files in os.walk(self.project_dir):
            # Ignorer certains dossiers
            if any(pattern in root for pattern in ['__pycache__', '.git', 'venv', 'node_modules', '.idea', '.vscode']):
                continue
            
            for file in files:
                file_lower = file.lower()
                if any(pattern in file_lower for pattern in correction_patterns):
                    file_path = Path(root) / file
                    file_info = get_file_info(file_path)
                    
                    if file_info:
                        self.correction_files.append(file_info)
                        self.total_size += file_info['size']
        
        print(f"✅ {len(self.correction_files)} fichiers trouvés ({self.total_size / 1024 / 1024:.1f} MB)")
        return self.correction_files
    
    def analyze_categories(self):
        """Analyse les fichiers par catégorie"""
        print(f"\n{Colors.CYAN}📊 Analyse par catégorie...{Colors.END}")
        
        for file_info in self.correction_files:
            category = categorize_file(file_info['name'])
            self.categories[category].append(file_info)
        
        # Afficher les statistiques par catégorie
        for category, files in sorted(self.categories.items(), key=lambda x: len(x[1]), reverse=True):
            size = sum(f['size'] for f in files)
            print(f"  {category}: {len(files):3d} fichiers ({size / 1024 / 1024:.1f} MB)")
        
        return self.categories
    
    def find_duplicates(self):
        """Trouve les fichiers en double"""
        print(f"\n{Colors.CYAN}🔍 Recherche des doublons...{Colors.END}")
        
        # Grouper par hash
        hash_groups = defaultdict(list)
        for file_info in self.correction_files:
            if file_info['hash']:
                hash_groups[file_info['hash']].append(file_info)
        
        # Garder seulement les groupes avec plus d'un fichier
        self.duplicates = {h: files for h, files in hash_groups.items() if len(files) > 1}
        
        if self.duplicates:
            print(f"⚠️  {len(self.duplicates)} groupes de doublons trouvés")
            for i, (hash_val, files) in enumerate(list(self.duplicates.items())[:5], 1):
                print(f"  Groupe {i} ({len(files)} fichiers):")
                for file_info in files[:3]:
                    print(f"    • {file_info['path']}")
                if len(files) > 3:
                    print(f"    • ... et {len(files) - 3} autres")
        else:
            print(f"✅ Aucun doublon trouvé")
        
        return self.duplicates
    
    def find_old_files(self, days=30):
        """Trouve les fichiers anciens"""
        print(f"\n{Colors.CYAN}📅 Recherche des fichiers anciens (> {days} jours)...{Colors.END}")
        
        cutoff_date = datetime.now() - timedelta(days=days)
        old_files = []
        
        for file_info in self.correction_files:
            if file_info['modified'] < cutoff_date:
                old_files.append(file_info)
        
        old_files.sort(key=lambda x: x['modified'])
        
        if old_files:
            print(f"⚠️  {len(old_files)} fichiers anciens trouvés")
            for i, file_info in enumerate(old_files[:10], 1):
                age = (datetime.now() - file_info['modified']).days
                print(f"  {i:2d}. {file_info['name']:30s} ({age} jours)")
            if len(old_files) > 10:
                print(f"  ... et {len(old_files) - 10} autres")
        else:
            print(f"✅ Aucun fichier ancien trouvé")
        
        return old_files
    
    def find_empty_files(self):
        """Trouve les fichiers vides ou presque"""
        print(f"\n{Colors.CYAN}📄 Recherche des fichiers vides...{Colors.END}")
        
        empty_files = []
        small_files = []
        
        for file_info in self.correction_files:
            if file_info['size'] == 0:
                empty_files.append(file_info)
            elif file_info['size'] < 100:  # Moins de 100 bytes
                small_files.append(file_info)
        
        if empty_files:
            print(f"⚠️  {len(empty_files)} fichiers vides trouvés")
            for file_info in empty_files[:5]:
                print(f"  • {file_info['path']}")
        else:
            print(f"✅ Aucun fichier vide trouvé")
        
        if small_files:
            print(f"⚠️  {len(small_files)} fichiers très petits (< 100 bytes)")
            for file_info in small_files[:5]:
                print(f"  • {file_info['path']} ({file_info['size']} bytes)")
        
        return empty_files + small_files
    
    def generate_report(self):
        """Génère un rapport complet"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'project_dir': str(self.project_dir),
            'total_files': len(self.correction_files),
            'total_size_mb': self.total_size / 1024 / 1024,
            'categories': {},
            'duplicates_count': len(self.duplicates),
            'duplicates_size_mb': sum(sum(f['size'] for f in files) for files in self.duplicates.values()) / 1024 / 1024,
        }
        
        for category, files in self.categories.items():
            report['categories'][category] = {
                'count': len(files),
                'size_mb': sum(f['size'] for f in files) / 1024 / 1024,
            }
        
        return report

# =============================================================================
# NETTOYEUR DE FICHIERS
# =============================================================================

class CorrectionFileCleaner:
    """Nettoie et organise les fichiers de correction"""
    
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.archive_dir = self.project_dir / 'archives' / 'corrections_anciennes'
        self.consolidated_dir = self.project_dir / 'scripts_consolides'
        
        # Créer les dossiers nécessaires
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        self.consolidated_dir.mkdir(parents=True, exist_ok=True)
        
        # Sous-dossiers pour les scripts consolidés
        (self.consolidated_dir / 'diagnostics').mkdir(exist_ok=True)
        (self.consolidated_dir / 'corrections').mkdir(exist_ok=True)
        (self.consolidated_dir / 'tests').mkdir(exist_ok=True)
        (self.consolidated_dir / 'utilitaires').mkdir(exist_ok=True)
        (self.consolidated_dir / 'rapports').mkdir(exist_ok=True)
        
        self.moved_files = []
        self.consolidated_files = []
    
    def archive_old_files(self, days=30):
        """Archive les fichiers anciens"""
        print(f"\n{Colors.YELLOW}📦 Archivage des fichiers anciens (> {days} jours)...{Colors.END}")
        
        analyzer = CorrectionFileAnalyzer(self.project_dir)
        analyzer.find_correction_files()
        old_files = analyzer.find_old_files(days)
        
        moved_count = 0
        
        for file_info in old_files:
            try:
                src_path = Path(file_info['path'])
                rel_path = src_path.relative_to(self.project_dir)
                dst_path = self.archive_dir / rel_path
                
                # Créer les sous-dossiers si nécessaire
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Déplacer le fichier
                shutil.move(str(src_path), str(dst_path))
                
                self.moved_files.append({
                    'from': str(src_path),
                    'to': str(dst_path),
                    'reason': f'Fichier ancien ({file_info["modified"].strftime("%Y-%m-%d")})',
                })
                moved_count += 1
                
            except Exception as e:
                print(f"{Colors.RED}❌ Erreur lors de l'archivage de {file_info['path']}: {e}{Colors.END}")
        
        print(f"✅ {moved_count} fichiers archivés dans {self.archive_dir}")
        return moved_count
    
    def remove_empty_files(self):
        """Supprime les fichiers vides"""
        print(f"\n{Colors.YELLOW}🗑️  Suppression des fichiers vides...{Colors.END}")
        
        analyzer = CorrectionFileAnalyzer(self.project_dir)
        analyzer.find_correction_files()
        empty_files = analyzer.find_empty_files()
        
        removed_count = 0
        
        for file_info in empty_files:
            try:
                if file_info['size'] == 0:
                    os.remove(file_info['path'])
                    print(f"  • Supprimé: {file_info['path']}")
                    removed_count += 1
            except Exception as e:
                print(f"{Colors.RED}❌ Erreur lors de la suppression de {file_info['path']}: {e}{Colors.END}")
        
        print(f"✅ {removed_count} fichiers vides supprimés")
        return removed_count
    
    def consolidate_duplicates(self):
        """Consolide les fichiers en double"""
        print(f"\n{Colors.YELLOW}🔄 Consolidation des doublons...{Colors.END}")
        
        analyzer = CorrectionFileAnalyzer(self.project_dir)
        analyzer.find_correction_files()
        analyzer.find_duplicates()
        
        consolidated_count = 0
        
        for hash_val, files in analyzer.duplicates.items():
            if len(files) < 2:
                continue
            
            # Garder le fichier le plus récent
            files.sort(key=lambda x: x['modified'], reverse=True)
            keeper = files[0]
            duplicates = files[1:]
            
            # Créer un dossier pour les doublons
            dup_dir = self.archive_dir / 'doublons' / keeper['name']
            dup_dir.mkdir(parents=True, exist_ok=True)
            
            # Déplacer les doublons
            for dup in duplicates:
                try:
                    src_path = Path(dup['path'])
                    dst_path = dup_dir / f"{src_path.parent.name}_{src_path.name}"
                    
                    shutil.move(str(src_path), str(dst_path))
                    
                    self.moved_files.append({
                        'from': str(src_path),
                        'to': str(dst_path),
                        'reason': f'Doublon de {keeper["path"]}',
                    })
                    consolidated_count += 1
                    
                except Exception as e:
                    print(f"{Colors.RED}❌ Erreur lors du déplacement du doublon {dup['path']}: {e}{Colors.END}")
        
        print(f"✅ {consolidated_count} doublons consolidés")
        return consolidated_count
    
    def consolidate_by_category(self):
        """Consolide les fichiers similaires par catégorie"""
        print(f"\n{Colors.YELLOW}📁 Consolidation par catégorie...{Colors.END}")
        
        analyzer = CorrectionFileAnalyzer(self.project_dir)
        analyzer.find_correction_files()
        analyzer.analyze_categories()
        
        consolidated_files = []
        
        # Pour chaque catégorie, analyser les fichiers similaires
        for category, files in analyzer.categories.items():
            if len(files) < 3:  # Seulement si on a plusieurs fichiers
                continue
            
            # Grouper par préfixe similaire
            prefix_groups = defaultdict(list)
            for file_info in files:
                name = file_info['name']
                # Extraire le préfixe (avant le premier '_' ou '.')
                prefix = name.split('_')[0] if '_' in name else name.split('.')[0]
                prefix_groups[prefix].append(file_info)
            
            # Consolider les groupes avec plusieurs fichiers
            for prefix, group_files in prefix_groups.items():
                if len(group_files) > 2:
                    self._consolidate_group(category, prefix, group_files)
                    consolidated_files.extend(group_files)
        
        print(f"✅ Groupes consolidés")
        return consolidated_files
    
    def _consolidate_group(self, category, prefix, files):
        """Consolide un groupe de fichiers similaires"""
        # Trier par date de modification (le plus récent d'abord)
        files.sort(key=lambda x: x['modified'], reverse=True)
        
        # Lire le contenu des fichiers
        contents = []
        for file_info in files:
            content = read_file_content(file_info['path'])
            if content:
                contents.append({
                    'file': file_info['name'],
                    'date': file_info['modified'].strftime('%Y-%m-%d'),
                    'content': content,
                })
        
        # Créer un fichier consolidé
        consolidated_file = self.consolidated_dir / category / f"{prefix}_consolide.py"
        
        with open(consolidated_file, 'w', encoding='utf-8') as f:
            f.write(f'"""\nFICHIER CONSOLIDÉ: {prefix}\n')
            f.write(f'Catégorie: {category}\n')
            f.write(f'Fusion de {len(files)} fichiers\n')
            f.write(f'Date de consolidation: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.write('"""\n\n')
            
            f.write('import sys\nimport os\nfrom pathlib import Path\n\n')
            f.write(f'# =============================================================================\n')
            f.write(f'# FICHIERS D\'ORIGINE CONSOLIDÉS\n')
            f.write(f'# =============================================================================\n\n')
            
            for i, item in enumerate(contents, 1):
                f.write(f'# {"="*60}\n')
                f.write(f'# ORIGINE {i}: {item["file"]} ({item["date"]})\n')
                f.write(f'# {"="*60}\n\n')
                f.write(item['content'])
                f.write('\n\n')
        
        print(f"  • Créé: {consolidated_file}")
        self.consolidated_files.append(str(consolidated_file))
        
        # Déplacer les fichiers originaux vers les archives
        archive_category_dir = self.archive_dir / 'avant_consolidation' / category
        archive_category_dir.mkdir(parents=True, exist_ok=True)
        
        for file_info in files:
            try:
                src_path = Path(file_info['path'])
                dst_path = archive_category_dir / src_path.name
                
                shutil.move(str(src_path), str(dst_path))
                
                self.moved_files.append({
                    'from': str(src_path),
                    'to': str(dst_path),
                    'reason': f'Consolidé dans {consolidated_file.name}',
                })
                
            except Exception as e:
                print(f"{Colors.RED}❌ Erreur lors du déplacement: {file_info['path']}: {e}{Colors.END}")
    
    def create_unified_system(self):
        """Crée un système unifié de gestion des corrections"""
        print(f"\n{Colors.YELLOW}🛠️  Création du système unifié...{Colors.END}")
        
        system_dir = self.project_dir / 'systeme_corrections'
        system_dir.mkdir(exist_ok=True)
        
        # Créer la structure
        (system_dir / 'diagnostics').mkdir(exist_ok=True)
        (system_dir / 'corrections').mkdir(exist_ok=True)
        (system_dir / 'tests').mkdir(exist_ok=True)
        (system_dir / 'rapports').mkdir(exist_ok=True)
        (system_dir / 'utilitaires').mkdir(exist_ok=True)
        (system_dir / 'config').mkdir(exist_ok=True)
        
        # Créer le fichier principal
        main_file = system_dir / 'systeme_corrections.py'
        
        main_content = '''#!/usr/bin/env python3
"""
SYSTÈME UNIFIÉ DE CORRECTIONS ET DIAGNOSTICS
Auteur: Assistant Technique
Date: 2024
Description: Système centralisé pour gérer toutes les corrections et diagnostics
"""

import os
import sys
import json
import argparse
from pathlib import Path

class CorrectionSystem:
    """Système de gestion des corrections"""
    
    def __init__(self, project_path=None):
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.config = self.load_config()
    
    def load_config(self):
        """Charge la configuration"""
        config_path = self.project_path / 'systeme_corrections' / 'config' / 'config.json'
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        return {
            'version': '1.0.0',
            'applications': [],
            'last_analysis': None,
            'active_corrections': []
        }
    
    def save_config(self):
        """Sauvegarde la configuration"""
        config_path = self.project_path / 'systeme_corrections' / 'config' / 'config.json'
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def analyze_project(self):
        """Analyse complète du projet"""
        from diagnostics.complet import DiagnosticComplet
        analyzer = DiagnosticComplet(self.project_path)
        return analyzer.analyze()
    
    def run_correction(self, correction_name, *args):
        """Exécute une correction spécifique"""
        from corrections.manager import CorrectionManager
        manager = CorrectionManager(self.project_path)
        return manager.run(correction_name, *args)
    
    def run_test_suite(self):
        """Exécute la suite de tests complète"""
        from tests.suite import TestSuite
        suite = TestSuite(self.project_path)
        return suite.run_all()
    
    def generate_report(self, format='html'):
        """Génère un rapport"""
        from rapports.generator import ReportGenerator
        generator = ReportGenerator(self.project_path)
        return generator.generate(format)

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description='Système unifié de corrections')
    parser.add_argument('command', choices=['analyze', 'correct', 'test', 'report', 'config'])
    parser.add_argument('--target', help='Cible spécifique')
    parser.add_argument('--format', default='html', help='Format du rapport')
    parser.add_argument('--project', help='Chemin du projet')
    
    args = parser.parse_args()
    
    system = CorrectionSystem(args.project)
    
    if args.command == 'analyze':
        result = system.analyze_project()
        print(json.dumps(result, indent=2))
    
    elif args.command == 'correct':
        if not args.target:
            print("Erreur: --target requis pour 'correct'")
            sys.exit(1)
        result = system.run_correction(args.target)
        print(f"Correction exécutée: {result}")
    
    elif args.command == 'test':
        result = system.run_test_suite()
        print(f"Tests exécutés: {len(result['tests'])} réussis, {len(result['failures'])} échecs")
    
    elif args.command == 'report':
        result = system.generate_report(args.format)
        print(f"Rapport généré: {result}")
    
    elif args.command == 'config':
        print(json.dumps(system.config, indent=2))

if __name__ == '__main__':
    main()
'''
        
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(main_content)
        
        # Créer les fichiers de base pour chaque module
        modules = {
            'diagnostics/complet.py': self._create_diagnostic_module(),
            'corrections/manager.py': self._create_correction_module(),
            'tests/suite.py': self._create_test_module(),
            'rapports/generator.py': self._create_report_module(),
            'utilitaires/cleaner.py': self._create_cleaner_module(),
            'config/config.json': json.dumps({
                'version': '1.0.0',
                'created': datetime.now().isoformat(),
                'applications': [],
                'corrections_available': [],
                'settings': {}
            }, indent=2)
        }
        
        for module_path, content in modules.items():
            module_file = system_dir / module_path
            module_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(module_file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print(f"✅ Système unifié créé dans {system_dir}")
        return system_dir
    
    def _create_diagnostic_module(self):
        """Crée le module de diagnostic"""
        return '''"""
Module de diagnostic complet
"""
import os
import sys
from pathlib import Path

class DiagnosticComplet:
    """Diagnostic complet du projet"""
    
    def __init__(self, project_path):
        self.project_path = Path(project_path)
    
    def analyze(self):
        """Analyse complète"""
        return {
            'applications': self._analyze_applications(),
            'models': self._analyze_models(),
            'views': self._analyze_views(),
            'urls': self._analyze_urls(),
            'templates': self._analyze_templates(),
            'issues': self._find_issues(),
        }
    
    def _analyze_applications(self):
        """Analyse les applications Django"""
        # Implémentation simplifiée
        return []
    
    def _analyze_models(self):
        """Analyse les modèles"""
        return []
    
    def _analyze_views(self):
        """Analyse les vues"""
        return []
    
    def _analyze_urls(self):
        """Analyse les URLs"""
        return []
    
    def _analyze_templates(self):
        """Analyse les templates"""
        return []
    
    def _find_issues(self):
        """Trouve les problèmes"""
        return []
'''
    
    def _create_correction_module(self):
        """Crée le module de correction"""
        return '''"""
Module de gestion des corrections
"""
import importlib

class CorrectionManager:
    """Gestionnaire de corrections"""
    
    def __init__(self, project_path):
        self.project_path = project_path
        self.corrections = self._load_corrections()
    
    def _load_corrections(self):
        """Charge toutes les corrections disponibles"""
        # À implémenter: charger dynamiquement les corrections
        return {
            'urls': 'Correction des URLs',
            'models': 'Correction des modèles',
            'views': 'Correction des vues',
            'templates': 'Correction des templates',
        }
    
    def run(self, correction_name, *args):
        """Exécute une correction"""
        if correction_name not in self.corrections:
            return {'error': f'Correction {correction_name} non trouvée'}
        
        # À implémenter: exécuter la correction spécifique
        return {'success': True, 'correction': correction_name}
'''
    
    def _create_test_module(self):
        """Crée le module de tests"""
        return '''"""
Module de tests
"""
import unittest

class TestSuite:
    """Suite de tests complète"""
    
    def __init__(self, project_path):
        self.project_path = project_path
    
    def run_all(self):
        """Exécute tous les tests"""
        loader = unittest.TestLoader()
        # À implémenter: charger les tests
        return {
            'tests': [],
            'failures': [],
            'errors': [],
            'success': True
        }
'''
    
    def _create_report_module(self):
        """Crée le module de rapports"""
        return '''"""
Module de génération de rapports
"""

class ReportGenerator:
    """Générateur de rapports"""
    
    def __init__(self, project_path):
        self.project_path = project_path
    
    def generate(self, format='html'):
        """Génère un rapport"""
        if format == 'html':
            return self._generate_html()
        elif format == 'json':
            return self._generate_json()
        elif format == 'text':
            return self._generate_text()
        else:
            return {'error': f'Format {format} non supporté'}
    
    def _generate_html(self):
        """Génère un rapport HTML"""
        return '<html><body>Rapport HTML</body></html>'
    
    def _generate_json(self):
        """Génère un rapport JSON"""
        return {'report': 'json'}
    
    def _generate_text(self):
        """Génère un rapport texte"""
        return 'Rapport texte'
'''
    
    def _create_cleaner_module(self):
        """Crée le module de nettoyage"""
        return '''"""
Module de nettoyage
"""
import os
import shutil
from pathlib import Path

class Cleaner:
    """Nettoyeur de projet"""
    
    def __init__(self, project_path):
        self.project_path = Path(project_path)
    
    def clean_pycache(self):
        """Nettoie les dossiers __pycache__"""
        deleted = []
        for root, dirs, files in os.walk(self.project_path):
            if '__pycache__' in root:
                shutil.rmtree(root)
                deleted.append(root)
        return deleted
    
    def clean_backup_files(self, patterns=['.bak', '.backup', '~']):
        """Nettoie les fichiers de backup"""
        deleted = []
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if any(file.endswith(pattern) for pattern in patterns):
                    file_path = Path(root) / file
                    os.remove(file_path)
                    deleted.append(str(file_path))
        return deleted
'''
    
    def save_operations_report(self):
        """Sauvegarde un rapport des opérations"""
        report_file = self.project_dir / 'operations_nettoyage.json'
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'archive_dir': str(self.archive_dir),
            'consolidated_dir': str(self.consolidated_dir),
            'moved_files': self.moved_files,
            'consolidated_files': self.consolidated_files,
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n{Colors.GREEN}✅ Rapport des opérations sauvegardé: {report_file}{Colors.END}")
        return report_file

# =============================================================================
# FONCTION PRINCIPALE
# =============================================================================

def main():
    """Fonction principale"""
    print(f"{Colors.BOLD}{Colors.MAGENTA}🧹 NETTOYEUR ET CONSOLIDATEUR DE FICHIERS DE CORRECTION{Colors.END}")
    print(f"{Colors.GRAY}Projet: {BASE_DIR}{Colors.END}")
    print("=" * 100)
    
    # 1. Analyse initiale
    print(f"\n{Colors.BOLD}{Colors.CYAN}📊 ÉTAPE 1: ANALYSE INITIALE{Colors.END}")
    analyzer = CorrectionFileAnalyzer(BASE_DIR)
    analyzer.find_correction_files()
    analyzer.analyze_categories()
    analyzer.find_duplicates()
    analyzer.find_old_files(14)  # Fichiers de plus de 14 jours
    analyzer.find_empty_files()
    
    report = analyzer.generate_report()
    print(f"\n📈 Résumé: {report['total_files']} fichiers, {report['total_size_mb']:.1f} MB")
    
    # 2. Menu de nettoyage
    print(f"\n{Colors.BOLD}{Colors.CYAN}🛠️  MENU DE NETTOYAGE:{Colors.END}")
    print("  1. 📦 Archiver les fichiers anciens (> 30 jours)")
    print("  2. 🗑️  Supprimer les fichiers vides")
    print("  3. 🔄 Consolider les doublons")
    print("  4. 📁 Consolider par catégorie")
    print("  5. 🛠️  Créer un système unifié")
    print("  6. 🚀 Exécuter toutes les opérations")
    print("  7. 📋 Afficher le rapport seulement")
    print("  8. 🚪 Quitter")
    
    choice = input(f"\n{Colors.YELLOW}👉 Votre choix (1-8): {Colors.END}").strip()
    
    cleaner = CorrectionFileCleaner(BASE_DIR)
    
    if choice == '1':
        cleaner.archive_old_files(30)
    
    elif choice == '2':
        cleaner.remove_empty_files()
    
    elif choice == '3':
        cleaner.consolidate_duplicates()
    
    elif choice == '4':
        cleaner.consolidate_by_category()
    
    elif choice == '5':
        cleaner.create_unified_system()
    
    elif choice == '6':
        print(f"\n{Colors.BOLD}{Colors.YELLOW}🚀 EXÉCUTION DE TOUTES LES OPÉRATIONS{Colors.END}")
        cleaner.archive_old_files(30)
        cleaner.remove_empty_files()
        cleaner.consolidate_duplicates()
        cleaner.consolidate_by_category()
        cleaner.create_unified_system()
    
    elif choice == '7':
        print(f"\n{Colors.BOLD}{Colors.CYAN}📋 RAPPORT D'ANALYSE{Colors.END}")
        print(json.dumps(report, indent=2))
        return
    
    elif choice == '8':
        print(f"{Colors.GREEN}👋 Au revoir!{Colors.END}")
        return
    
    else:
        print(f"{Colors.RED}❌ Choix invalide{Colors.END}")
        return
    
    # Sauvegarder le rapport des opérations
    cleaner.save_operations_report()
    
    # Analyse finale
    print(f"\n{Colors.BOLD}{Colors.CYAN}📊 ÉTAPE FINALE: ANALYSE APRÈS NETTOYAGE{Colors.END}")
    analyzer_after = CorrectionFileAnalyzer(BASE_DIR)
    analyzer_after.find_correction_files()
    
    print(f"\n📈 AVANT: {report['total_files']} fichiers, {report['total_size_mb']:.1f} MB")
    print(f"📈 APRÈS: {len(analyzer_after.correction_files)} fichiers, {analyzer_after.total_size / 1024 / 1024:.1f} MB")
    
    if analyzer_after.total_size < report['total_size_mb']:
        reduction = (1 - (analyzer_after.total_size / 1024 / 1024) / report['total_size_mb']) * 100
        print(f"🎉 RÉDUCTION: {reduction:.1f}%")
    
    print(f"\n{Colors.GREEN}✅ Opérations terminées avec succès!{Colors.END}")

# =============================================================================
# EXÉCUTION
# =============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Opération interrompue par l'utilisateur{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ Erreur: {e}{Colors.END}")
        import traceback
        traceback.print_exc()