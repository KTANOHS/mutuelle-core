#!/usr/bin/env python3
"""
Script pour lister récursivement tous les dossiers et fichiers d'un projet Django
Avec analyse de la structure et statistiques
"""

import os
import sys
from pathlib import Path
import argparse
from datetime import datetime
import json
from django.utils import timezone

class ProjectLister:
    """Classe pour lister l'ensemble du projet"""
    
    def __init__(self, project_path, output_file=None):
        self.project_path = Path(project_path).resolve()
        self.output_file = output_file
        self.stats = {
            'total_files': 0,
            'total_dirs': 0,
            'file_types': {},
            'largest_files': [],
            'recent_files': [],
            'ignored_items': 0
        }
        
        # Patterns à ignorer
        self.ignore_patterns = [
            '__pycache__', '.git', '.vscode', '.idea', 'node_modules',
            'venv', 'env', '.env', 'virtualenv', 'dist', 'build',
            '*.pyc', '*.pyo', '*.pyd', '.DS_Store', 'Thumbs.db',
            '*.sqlite3', '*.log', '*.tmp', '*.swp', '*.swo'
        ]
        
        # Extensions de fichiers avec icônes
        self.file_icons = {
            '.py': '🐍', '.html': '🌐', '.css': '🎨', '.js': '📜', '.json': '📋',
            '.md': '📖', '.txt': '📄', '.sql': '🗃️', '.yml': '⚙️', '.yaml': '⚙️',
            '.xml': '📊', '.csv': '📊', '.pdf': '📕', '.jpg': '🖼️', '.png': '🖼️',
            '.gif': '🖼️', '.svg': '🖼️', '.ico': '🖼️', '.zip': '📦', '.tar': '📦',
            '.gz': '📦', '.env': '🔐', '.gitignore': '👁️', 'requirements': '📦',
            'Dockerfile': '🐳', '.dockerignore': '🐳', 'docker-compose': '🐳'
        }

    def should_ignore(self, path):
        """Détermine si un chemin doit être ignoré"""
        path_str = str(path)
        name = path.name
        
        for pattern in self.ignore_patterns:
            if pattern.startswith('*'):
                # Pattern de fichier (*.ext)
                if name.endswith(pattern[1:]):
                    return True
            elif pattern in path_str:
                return True
                
        return False

    def get_file_icon(self, filename):
        """Retourne l'icône appropriée pour le fichier"""
        for key, icon in self.file_icons.items():
            if key in filename.lower():
                return icon
        return '📄'

    def get_size_info(self, filepath):
        """Retourne la taille formatée d'un fichier"""
        try:
            size = filepath.stat().st_size
            if size == 0:
                return "0 B"
            
            # Formatage de la taille
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        except:
            return "N/A"

    def scan_project(self):
        """Scanne récursivement le projet"""
        print(f"🔍 Scan du projet: {self.project_path}")
        print("=" * 80)
        
        if not self.project_path.exists():
            print(f"❌ Erreur: Le chemin {self.project_path} n'existe pas")
            return False
            
        results = {
            'project_name': self.project_path.name,
            'scan_date': timezone.now().isoformat(),
            'total_size': 0,
            'structure': {}
        }
        
        for root, dirs, files in os.walk(self.project_path):
            root_path = Path(root)
            relative_path = root_path.relative_to(self.project_path)
            
            # Filtrer les dossiers à ignorer
            dirs[:] = [d for d in dirs if not self.should_ignore(root_path / d)]
            
            current_level = results['structure']
            if str(relative_path) != '.':
                for part in relative_path.parts:
                    current_level = current_level.setdefault(part, {})
            
            # Ajouter les dossiers
            for dir_name in dirs:
                dir_path = root_path / dir_name
                if not self.should_ignore(dir_path):
                    current_level[f"📁 {dir_name}"] = {}
                    self.stats['total_dirs'] += 1
            
            # Ajouter les fichiers
            for file_name in files:
                file_path = root_path / file_name
                if not self.should_ignore(file_path):
                    try:
                        size_info = self.get_size_info(file_path)
                        icon = self.get_file_icon(file_name)
                        file_ext = Path(file_name).suffix.lower()
                        
                        # Mise à jour des statistiques
                        self.stats['total_files'] += 1
                        self.stats['file_types'][file_ext] = self.stats['file_types'].get(file_ext, 0) + 1
                        
                        # Track des plus gros fichiers
                        file_size = file_path.stat().st_size
                        self.stats['largest_files'].append((file_path, file_size))
                        
                        # Track des fichiers récents
                        mtime = file_path.stat().st_mtime
                        self.stats['recent_files'].append((file_path, mtime))
                        
                        current_level[f"{icon} {file_name}"] = size_info
                        
                    except Exception as e:
                        current_level[f"❌ {file_name}"] = f"Erreur: {str(e)}"
                else:
                    self.stats['ignored_items'] += 1
        
        # Trier les plus gros fichiers
        self.stats['largest_files'].sort(key=lambda x: x[1], reverse=True)
        self.stats['largest_files'] = self.stats['largest_files'][:10]
        
        # Trier les fichiers récents
        self.stats['recent_files'].sort(key=lambda x: x[1], reverse=True)
        self.stats['recent_files'] = self.stats['recent_files'][:10]
        
        self.results = results
        return True

    def print_tree(self, node=None, prefix="", is_last=True, is_root=True):
        """Affiche l'arborescence de manière récursive"""
        if node is None:
            node = self.results['structure']
            
        if is_root:
            print(f"📦 {self.project_path.name}")
            is_root = False
        
        # Trier: dossiers d'abord, puis fichiers
        items = []
        for key, value in node.items():
            if isinstance(value, dict):
                items.append((key, value, 'dir'))
            else:
                items.append((key, value, 'file'))
        
        # Trier par type puis par nom
        items.sort(key=lambda x: (x[2] != 'dir', x[0].lower()))
        
        for i, (name, value, item_type) in enumerate(items):
            is_last_item = i == len(items) - 1
            
            if item_type == 'dir':
                # Dossier
                connector = "└── " if is_last_item else "├── "
                print(f"{prefix}{connector}{name}")
                
                new_prefix = prefix + ("    " if is_last_item else "│   ")
                self.print_tree(value, new_prefix, is_last_item, False)
            else:
                # Fichier avec taille
                connector = "└── " if is_last_item else "├── "
                print(f"{prefix}{connector}{name} ({value})")

    def print_stats(self):
        """Affiche les statistiques détaillées"""
        print("\n" + "=" * 80)
        print("📊 STATISTIQUES DU PROJET")
        print("=" * 80)
        
        print(f"\n📁 Structure:")
        print(f"  • Dossiers: {self.stats['total_dirs']:,}")
        print(f"  • Fichiers: {self.stats['total_files']:,}")
        print(f"  • Éléments ignorés: {self.stats['ignored_items']:,}")
        
        print(f"\n📄 Types de fichiers:")
        for ext, count in sorted(self.stats['file_types'].items(), key=lambda x: x[1], reverse=True):
            icon = self.get_file_icon(f"test{ext}")
            ext_display = ext if ext else "Sans extension"
            print(f"  {icon} {ext_display}: {count:,}")
        
        print(f"\n🏆 Top 10 des plus gros fichiers:")
        for file_path, size in self.stats['largest_files']:
            size_fmt = self.get_size_info(file_path)
            relative_path = file_path.relative_to(self.project_path)
            print(f"  📏 {size_fmt:>8} - {relative_path}")
        
        print(f"\n🕒 Top 10 des fichiers modifiés récemment:")
        for file_path, mtime in self.stats['recent_files']:
            mod_time = datetime.fromtimestamp(mtime).strftime("%d/%m/%Y %H:%M")
            relative_path = file_path.relative_to(self.project_path)
            print(f"  🕐 {mod_time} - {relative_path}")

    def save_to_file(self):
        """Sauvegarde les résultats dans un fichier"""
        if not self.output_file:
            return
            
        output = {
            'scan_info': {
                'project_path': str(self.project_path),
                'scan_date': self.results['scan_date'],
                'project_name': self.results['project_name']
            },
            'statistics': self.stats,
            'file_structure': self.results['structure']
        }
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
            
        print(f"\n💾 Résultats sauvegardés dans: {self.output_file}")

    def generate_summary_report(self):
        """Génère un rapport sommaire"""
        print("\n" + "=" * 80)
        print("📋 RAPPORT SYNTHÉTIQUE")
        print("=" * 80)
        
        # Détection du type de projet
        django_files = [
            'manage.py', 'requirements.txt', 'settings.py',
            'urls.py', 'wsgi.py', 'asgi.py'
        ]
        
        django_count = sum(1 for f in django_files if (self.project_path / f).exists())
        
        if django_count >= 3:
            project_type = "🚀 Projet Django"
        elif (self.project_path / 'package.json').exists():
            project_type = "📦 Projet Node.js"
        elif (self.project_path / 'Dockerfile').exists():
            project_type = "🐳 Projet Dockerisé"
        else:
            project_type = "📁 Projet Générique"
            
        print(f"\n{project_type}")
        print(f"Chemin: {self.project_path}")
        print(f"Scan effectué le: {timezone.now().strftime('%d/%m/%Y à %H:%M')}")
        
        # Recommandations
        print(f"\n💡 Recommandations:")
        if self.stats['file_types'].get('.py', 0) > 0:
            print("  • Vérifier les imports et les dépendances Python")
        if self.stats['file_types'].get('.html', 0) > 0:
            print("  • Valider la structure des templates")
        if self.stats['file_types'].get('.js', 0) > 0:
            print("  • Optimiser les fichiers JavaScript")
            
        # Points d'attention
        large_files_count = sum(1 for _, size in self.stats['largest_files'] if size > 10 * 1024 * 1024)
        if large_files_count > 0:
            print(f"  ⚠️  {large_files_count} fichier(s) volumineux détecté(s)")

def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(description='Lister tous les dossiers et fichiers d\'un projet')
    parser.add_argument('project_path', help='Chemin vers le projet à analyser')
    parser.add_argument('-o', '--output', help='Fichier de sortie pour sauvegarder les résultats')
    parser.add_argument('-s', '--stats', action='store_true', help='Afficher les statistiques détaillées')
    parser.add_argument('-q', '--quiet', action='store_true', help='Mode silencieux (pas d\'arborescence)')
    
    args = parser.parse_args()
    
    # Vérifier que le chemin existe
    if not os.path.exists(args.project_path):
        print(f"❌ Erreur: Le chemin '{args.project_path}' n'existe pas")
        sys.exit(1)
    
    # Scanner le projet
    lister = ProjectLister(args.project_path, args.output)
    
    if lister.scan_project():
        if not args.quiet:
            print("\n🌳 ARBORESCENCE DU PROJET")
            print("=" * 80)
            lister.print_tree()
        
        if args.stats:
            lister.print_stats()
        else:
            lister.generate_summary_report()
            
        if args.output:
            lister.save_to_file()
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()