#!/usr/bin/env python3
"""
Script de mise à jour automatique des templates
VERSION CORRIGÉE - Détection automatique du dossier templates
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from django.utils import timezone

class TemplateUpdater:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.templates_dir = self.find_templates_directory()
        self.backup_dir = self.project_root / 'templates_backup'
        self.changes_log = []
        
        # Mapping des remplacements
        self.replacements = {
            'ordonnance.numero': 'ordonnance.ordonnance_medecin.numero',
            'ordonnance.patient': 'ordonnance.ordonnance_medecin.patient',
            'ordonnance.medecin': 'ordonnance.ordonnance_medecin.medecin',
            'ordonnance.date_prescription': 'ordonnance.ordonnance_medecin.date_prescription',
            'ordonnance.date_expiration': 'ordonnance.ordonnance_medecin.date_expiration',
            'ordonnance.diagnostic': 'ordonnance.ordonnance_medecin.diagnostic',
            'ordonnance.medicaments': 'ordonnance.ordonnance_medecin.medicaments',
            'ordonnance.posologie': 'ordonnance.ordonnance_medecin.posologie',
            'ordonnance.duree_traitement': 'ordonnance.ordonnance_medecin.duree_traitement',
            'ordonnance.bon_de_soin': 'ordonnance.bon_prise_charge',
        }

    def find_templates_directory(self):
        """Trouve automatiquement le dossier templates"""
        # Essayer différents emplacements possibles
        possible_locations = [
            self.project_root / 'templates',
            self.project_root / 'mutuelle_core' / 'templates',
            self.project_root / '..' / 'templates',
            self.project_root / 'src' / 'templates',
        ]
        
        for location in possible_locations:
            absolute_path = location.resolve()
            if absolute_path.exists() and absolute_path.is_dir():
                print(f"✅ Dossier templates trouvé: {absolute_path}")
                return absolute_path
        
        # Si aucun trouvé, demander à l'utilisateur
        print("❌ Dossier templates non trouvé automatiquement.")
        custom_path = input("Veuillez entrer le chemin complet du dossier templates: ").strip()
        custom_path = Path(custom_path)
        
        if custom_path.exists() and custom_path.is_dir():
            return custom_path
        else:
            print(f"❌ Chemin invalide: {custom_path}")
            return None

    def create_backup(self):
        """Crée une sauvegarde des templates"""
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)
        
        shutil.copytree(self.templates_dir, self.backup_dir)
        self.log_change(f"✅ Sauvegarde créée: {self.backup_dir}")

    def analyze_template(self, file_path):
        """Analyse un template et détecte les anciens patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.log_change(f"❌ Erreur lecture {file_path}: {e}")
            return [], ""
        
        issues = []
        
        # Détection des anciens champs
        for old_field, new_field in self.replacements.items():
            if old_field in content and old_field != new_field:
                count = content.count(old_field)
                if count > 0:
                    issues.append({
                        'pattern': f'FIELD:{old_field}',
                        'matches': [old_field],
                        'count': count
                    })
        
        return issues, content

    def update_template(self, file_path, content):
        """Met à jour le template avec les nouveaux champs"""
        original_content = content
        
        # Remplacements simples
        for old_field, new_field in self.replacements.items():
            if old_field != new_field:
                content = content.replace(old_field, new_field)
        
        return content, content != original_content

    def log_change(self, message):
        """Enregistre un changement"""
        timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        self.changes_log.append(f"[{timestamp}] {message}")
        print(message)

    def generate_migration_report(self):
        """Génère un rapport de migration"""
        report_path = self.project_root / 'template_migration_report.txt'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RAPPORT DE MIGRATION DES TEMPLATES\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("RÉSUMÉ DES CHANGEMENTS:\n")
            f.write("-" * 40 + "\n")
            
            for log_entry in self.changes_log:
                f.write(f"{log_entry}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("CHANGEMENTS EFFECTUÉS:\n")
            f.write("=" * 80 + "\n\n")
            
            for old_field, new_field in self.replacements.items():
                if old_field != new_field:
                    f.write(f"- {old_field} → {new_field}\n")
        
        self.log_change(f"📄 Rapport généré: {report_path}")

    def run_migration(self):
        """Exécute la migration complète"""
        print("🚀 Démarrage de la migration des templates...")
        
        if not self.templates_dir:
            print("❌ Impossible de trouver le dossier templates")
            return
        
        if not self.templates_dir.exists():
            print(f"❌ Dossier templates introuvable: {self.templates_dir}")
            return
        
        # Créer la sauvegarde
        self.create_backup()
        
        # Analyser tous les templates
        templates_analyzed = 0
        templates_updated = 0
        
        template_files = list(self.templates_dir.rglob('*.html'))
        print(f"📁 {len(template_files)} templates à analyser...")
        
        for file_path in template_files:
            templates_analyzed += 1
            issues, content = self.analyze_template(file_path)
            
            if issues:
                self.log_change(f"🔍 {file_path.relative_to(self.templates_dir)} - {len(issues)} problème(s) détecté(s)")
                
                # Mettre à jour le template
                new_content, changed = self.update_template(file_path, content)
                
                if changed:
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        templates_updated += 1
                        self.log_change(f"✅ {file_path.relative_to(self.templates_dir)} - Mis à jour")
                    except Exception as e:
                        self.log_change(f"❌ Erreur écriture {file_path}: {e}")
            else:
                relative_path = file_path.relative_to(self.templates_dir)
                print(f"✅ {relative_path} - Aucun changement nécessaire")
        
        # Générer le rapport
        self.generate_migration_report()
        
        print(f"\n📊 RÉSUMÉ DE LA MIGRATION:")
        print(f"   Templates analysés: {templates_analyzed}")
        print(f"   Templates mis à jour: {templates_updated}")
        print(f"   Sauvegarde: {self.backup_dir}")
        print(f"   Rapport: template_migration_report.txt")

def main():
    """Fonction principale"""
    project_root = input("Entrez le chemin du projet Django (ou laissez vide pour le répertoire actuel): ").strip()
    
    if not project_root:
        project_root = os.getcwd()
    
    project_root = Path(project_root)
    
    # Vérifier si c'est le bon dossier
    if not (project_root / 'manage.py').exists():
        print("❌ Fichier manage.py introuvable. Vérifiez le chemin du projet.")
        return
    
    updater = TemplateUpdater(project_root)
    
    # Confirmation
    confirm = input("❓ Voulez-vous lancer la migration des templates? (oui/non): ").strip().lower()
    if confirm in ['oui', 'o', 'yes', 'y']:
        updater.run_migration()
    else:
        print("❌ Migration annulée")

if __name__ == "__main__":
    main()