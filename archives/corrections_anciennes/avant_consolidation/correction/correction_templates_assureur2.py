#!/usr/bin/env python3
"""
Script de correction automatique des templates assureur
Corrige les URLs problématiques dans les templates
"""

import os
import re
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class TemplateCorrector:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.corrections_made = 0
        self.files_processed = 0
        
    def find_template_files(self):
        """Trouve tous les fichiers templates HTML dans le projet"""
        template_files = []
        patterns = [
            "**/templates/assureur/*.html",
            "**/assureur/templates/**/*.html",
            "**/templates/**/assureur/*.html"
        ]
        
        for pattern in patterns:
            template_files.extend(self.project_root.glob(pattern))
        
        return template_files
    
    def correct_urls_in_template(self, file_path):
        """Corrige les URLs problématiques dans un template"""
        corrections = {
            'assureur:rapports': 'assureur:rapport_statistiques',
            # Ajouter d'autres corrections si nécessaire
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            file_corrections = 0
            
            for wrong_url, correct_url in corrections.items():
                # Pattern pour trouver l'URL dans les templates Django
                patterns = [
                    f"'{wrong_url}'",
                    f'"{wrong_url}"',
                    f"\\{{% url '{wrong_url}'",
                    f'\\{{% url "{wrong_url}"',
                    f"url:'{wrong_url}'",
                    f'url:"{wrong_url}"',
                ]
                
                for pattern in patterns:
                    if pattern in content:
                        replacement = pattern.replace(wrong_url, correct_url)
                        content = content.replace(pattern, replacement)
                        file_corrections += content.count(replacement)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.corrections_made += file_corrections
                logger.info(f"✓ Corrigé {file_corrections} URL(s) dans {file_path.relative_to(self.project_root)}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"✗ Erreur lors du traitement de {file_path}: {e}")
            return False
    
    def remove_duplicate_templates(self):
        """Supprime les templates en double identifiés comme problématiques"""
        duplicates = {
            'base_assureur.html': [
                self.project_root / "assureur/templates/assureur/base_assureur.html",
                self.project_root / "templates/assureur/base_assureur.html"
            ],
            'dashboard.html': [
                self.project_root / "assureur/templates/assureur/dashboard.html", 
                self.project_root / "templates/assureur/dashboard.html"
            ]
        }
        
        for template_name, paths in duplicates.items():
            existing_paths = [p for p in paths if p.exists()]
            if len(existing_paths) > 1:
                logger.info(f"📋 Doublons détectés pour {template_name}:")
                for i, path in enumerate(existing_paths):
                    size = path.stat().st_size
                    logger.info(f"  {i+1}. {path.relative_to(self.project_root)} ({size} octets)")
                
                # Garder le plus récent ou le plus complet
                main_template = self.choose_main_template(existing_paths, template_name)
                logger.info(f"🎯 Template principal conservé: {main_template.relative_to(self.project_root)}")
    
    def choose_main_template(self, paths, template_name):
        """Choisit le template principal à conserver"""
        if template_name == 'base_assureur.html':
            # Préférer celui dans assureur/templates/assureur/
            for path in paths:
                if 'assureur/templates/assureur' in str(path):
                    return path
        elif template_name == 'dashboard.html':
            # Préférer le plus récent ou le plus complet
            for path in paths:
                if 'assureur/templates/assureur' in str(path):
                    return path
        
        # Par défaut, le premier
        return paths[0]
    
    def standardize_template_extensions(self):
        """S'assure que tous les templates étendent le bon template de base"""
        template_files = self.find_template_files()
        
        for file_path in template_files:
            if file_path.name in ['base_assureur.html', 'base.html']:
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Vérifier si le template étend base.html au lieu de base_assureur.html
                if '{% extends "base.html" %}' in content and 'assureur' in str(file_path):
                    content = content.replace(
                        '{% extends "base.html" %}', 
                        '{% extends "assureur/base_assureur.html" %}'
                    )
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    logger.info(f"🔄 Standardisé l'extension dans {file_path.relative_to(self.project_root)}")
                    self.corrections_made += 1
                    
            except Exception as e:
                logger.error(f"✗ Erreur lors de la standardisation de {file_path}: {e}")
    
    def verify_corrections(self):
        """Vérifie que les corrections ont été appliquées"""
        problematic_urls = ['assureur:rapports']
        template_files = self.find_template_files()
        remaining_issues = 0
        
        for file_path in template_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for url in problematic_urls:
                    if url in content:
                        logger.warning(f"⚠️  URL problématique toujours présente: {url} dans {file_path.relative_to(self.project_root)}")
                        remaining_issues += 1
                        
            except Exception as e:
                logger.error(f"✗ Erreur lors de la vérification de {file_path}: {e}")
        
        return remaining_issues
    
    def run_corrections(self):
        """Exécute toutes les corrections"""
        logger.info("🔧 LANCEMENT DES CORRECTIONS DES TEMPLATES ASSUREUR")
        logger.info("=" * 60)
        
        # Étape 1: Trouver tous les templates
        template_files = self.find_template_files()
        logger.info(f"📁 {len(template_files)} templates trouvés")
        
        # Étape 2: Corriger les URLs
        logger.info("\n1. 🔗 CORRECTION DES URLs PROBLÉMATIQUES")
        for file_path in template_files:
            self.files_processed += 1
            self.correct_urls_in_template(file_path)
        
        # Étape 3: Standardiser les extensions
        logger.info("\n2. 🏗️ STANDARDISATION DES EXTENSIONS DE TEMPLATES")
        self.standardize_template_extensions()
        
        # Étape 4: Gérer les doublons
        logger.info("\n3. 📋 GESTION DES TEMPLATES EN DOUBLE")
        self.remove_duplicate_templates()
        
        # Étape 5: Vérification
        logger.info("\n4. ✅ VÉRIFICATION DES CORRECTIONS")
        remaining_issues = self.verify_corrections()
        
        # Rapport final
        logger.info("\n" + "=" * 60)
        logger.info("📊 RAPPORT FINAL DES CORRECTIONS")
        logger.info(f"📄 Templates traités: {self.files_processed}")
        logger.info(f"🔧 Corrections appliquées: {self.corrections_made}")
        logger.info(f"⚠️  Problèmes restants: {remaining_issues}")
        
        if remaining_issues == 0:
            logger.info("🎉 TOUTES LES CORRECTIONS ONT ÉTÉ APPLIQUÉES AVEC SUCCÈS!")
        else:
            logger.warning("💡 Certains problèmes nécessitent une attention manuelle")
        
        return remaining_issues == 0

def main():
    """Fonction principale"""
    # Déterminer automatiquement la racine du projet
    script_dir = Path(__file__).parent
    project_root = script_dir
    
    corrector = TemplateCorrector(project_root)
    
    try:
        success = corrector.run_corrections()
        
        if success:
            print("\n" + "=" * 60)
            print("🎯 PROCHAINES ÉTAPES:")
            print("1. 🔄 Redémarrer le serveur Django")
            print("2. 🧪 Tester l'accès au dashboard assureur") 
            print("3. 📱 Vérifier toutes les fonctionnalités")
            print("4. 🐛 Signaler tout problème résiduel")
            print("=" * 60)
        else:
            print("\n❌ Des problèmes persistent. Vérifiez les logs ci-dessus.")
            
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'exécution des corrections: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())