#!/usr/bin/env python3
"""
Script de gestion des erreurs dans les templates
Objectif : Nettoyer et standardiser la structure des templates
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from django.utils import timezone

class TemplateManager:
    def __init__(self, templates_dir="templates"):
        self.templates_dir = Path(templates_dir)
        self.backup_patterns = [
            r'\.backup\..*',
            r'\.save$',
            r'\.old$',
            r'\.bak$',
            r'backup.*\.html',
            r'.*\.backup\..*'
        ]
        self.problem_files = []
        
    def scan_templates(self):
        """Scanner tous les templates et identifier les problèmes"""
        print("🔍 Scan des templates en cours...")
        
        for file_path in self.templates_dir.rglob("*.html"):
            relative_path = file_path.relative_to(self.templates_dir)
            
            # Vérifier les problèmes de nommage
            issues = self._check_file_issues(str(relative_path), file_path)
            if issues:
                self.problem_files.append({
                    'path': relative_path,
                    'issues': issues,
                    'full_path': file_path
                })
                
        return self.problem_files
    
    def _check_file_issues(self, file_path, full_path):
        """Vérifier les problèmes individuels d'un fichier"""
        issues = []
        
        # Vérifier les fichiers de backup
        for pattern in self.backup_patterns:
            if re.search(pattern, file_path):
                issues.append(f"Fichier de backup détecté (pattern: {pattern})")
                break
        
        # Vérifier les extensions incorrectes
        if file_path.endswith('.htm.save'):
            issues.append("Extension incorrecte: .htm.save")
        
        # Vérifier la taille du fichier (trop petit = potentiellement vide)
        if full_path.stat().st_size < 50:
            issues.append("Fichier potentiellement vide ou trop petit")
        
        # Vérifier les doublons dans le nom
        name_parts = Path(file_path).stem.split('_')
        if len(name_parts) > 3 and name_parts[-1] in ['updated', 'new', 'old']:
            issues.append("Nom avec suffixe générique (updated/new/old)")
        
        return issues
    
    def create_backup(self):
        """Créer une sauvegarde avant toute modification"""
        backup_dir = f"templates_backup_{timezone.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copytree(self.templates_dir, backup_dir)
        print(f"✅ Sauvegarde créée: {backup_dir}")
        return backup_dir
    
    def clean_backup_files(self, dry_run=True):
        """Nettoyer les fichiers de backup"""
        backup_files = []
        
        for file_path in self.templates_dir.rglob("*.html"):
            relative_path = file_path.relative_to(self.templates_dir)
            
            for pattern in self.backup_patterns:
                if re.search(pattern, str(relative_path)):
                    backup_files.append(file_path)
                    break
        
        print(f"🗑️  {len(backup_files)} fichiers de backup trouvés")
        
        if not dry_run:
            for file_path in backup_files:
                print(f"Suppression: {file_path}")
                file_path.unlink()
        
        return backup_files
    
    def find_duplicate_templates(self):
        """Trouver les templates potentiellement dupliqués"""
        templates_by_stem = {}
        
        for file_path in self.templates_dir.rglob("*.html"):
            stem = file_path.stem
            if stem not in templates_by_stem:
                templates_by_stem[stem] = []
            templates_by_stem[stem].append(file_path)
        
        duplicates = {k: v for k, v in templates_by_stem.items() 
                     if len(v) > 1 and not any(p in k for p in ['base', 'partial'])}
        
        return duplicates
    
    def generate_consolidation_plan(self):
        """Générer un plan de consolidation des templates"""
        plan = {
            'dashboard_consolidation': [],
            'sidebar_consolidation': [],
            'base_templates': []
        }
        
        # Consolidation des dashboards
        dashboards = list(self.templates_dir.rglob("*dashboard*.html"))
        plan['dashboard_consolidation'] = dashboards
        
        # Consolidation des sidebars
        sidebars = list(self.templates_dir.rglob("*sidebar*.html"))
        plan['sidebar_consolidation'] = sidebars
        
        # Templates de base
        base_templates = list(self.templates_dir.rglob("base*.html"))
        plan['base_templates'] = base_templates
        
        return plan
    
    def generate_report(self):
        """Générer un rapport complet"""
        self.scan_templates()
        
        print("\n" + "="*80)
        print("📊 RAPPORT D'ANALYSE DES TEMPLATES")
        print("="*80)
        
        print(f"\n❌ Fichiers problématiques: {len(self.problem_files)}")
        for file_info in self.problem_files:
            print(f"\n📁 {file_info['path']}")
            for issue in file_info['issues']:
                print(f"   ⚠️  {issue}")
        
        # Doublons
        duplicates = self.find_duplicate_templates()
        print(f"\n🔄 Templates potentiellement dupliqués: {len(duplicates)}")
        for stem, files in duplicates.items():
            print(f"\n📋 {stem}:")
            for file_path in files:
                print(f"   📍 {file_path.relative_to(self.templates_dir)}")
        
        # Plan de consolidation
        plan = self.generate_consolidation_plan()
        print(f"\n🎯 Dashboards à consolider: {len(plan['dashboard_consolidation'])}")
        print(f"🎯 Sidebars à consolider: {len(plan['sidebar_consolidation'])}")

def main():
    manager = TemplateManager()
    
    # Mode interactif
    print("🛠️  Gestionnaire de Templates - Nettoyage et Validation")
    print("1. Scanner seulement (dry run)")
    print("2. Scanner et nettoyer les fichiers de backup")
    print("3. Générer un rapport complet")
    
    choice = input("\nChoisissez une option (1-3): ").strip()
    
    if choice == "1":
        manager.scan_templates()
        manager.generate_report()
    
    elif choice == "2":
        # Créer une sauvegarde avant suppression
        backup_dir = manager.create_backup()
        
        # Scanner d'abord
        manager.scan_templates()
        manager.generate_report()
        
        # Demander confirmation
        confirm = input("\n❓ Confirmer la suppression des fichiers de backup? (oui/non): ")
        if confirm.lower() == 'oui':
            backup_files = manager.clean_backup_files(dry_run=False)
            print(f"✅ {len(backup_files)} fichiers supprimés")
        else:
            print("❌ Opération annulée")
    
    elif choice == "3":
        manager.generate_report()
        
        # Sauvegarder le rapport
        report_file = f"template_analysis_report_{timezone.now().strftime('%Y%m%d_%H%M%S')}.txt"
        # Implémenter la sauvegarde du rapport si nécessaire

if __name__ == "__main__":
    main()