#!/usr/bin/env python3
"""
Script de correction amélioré pour les templates assureur
"""

import os
import re
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class AdvancedTemplateCorrector:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.corrections_made = 0
        self.files_processed = 0
        
    def find_all_template_files(self):
        """Trouve tous les fichiers templates HTML dans le projet"""
        template_files = []
        
        # Recherche récursive de tous les fichiers HTML
        for html_file in self.project_root.glob("**/*.html"):
            template_files.append(html_file)
        
        return template_files
    
    def advanced_url_correction(self, file_path):
        """Correction avancée des URLs avec plusieurs patterns"""
        corrections = {
            'assureur:rapports': 'assureur:rapport_statistiques',
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            file_corrections = 0
            
            for wrong_url, correct_url in corrections.items():
                # Patterns complets pour détecter les URLs dans différents contextes
                patterns_replacements = [
                    # Pattern: {% url 'assureur:rapports' %}
                    (f"\\{{%\\s*url\\s+['\"]{wrong_url}['\"]\\s*%\\}}", 
                     f"{{% url '{correct_url}' %}}"),
                    
                    # Pattern: href="{% url 'assureur:rapports' %}"
                    (f'href=[\'"]\\s*\\{{%\\s*url\\s+[\'"]{wrong_url}[\'"]\\s*%\\}}\\s*[\'"]', 
                     f'href="{{% url \'{correct_url}\' %}}"'),
                    
                    # Pattern: href='{% url "assureur:rapports" %}'
                    (f"href=['\"]\\s*\\{{%\\s*url\\s+[\"']{wrong_url}[\"']\\s*%\\}}\\s*['\"]", 
                     f'href="{{% url "{correct_url}" %}}"'),
                    
                    # Pattern simple dans le texte
                    (f"['\"]{wrong_url}['\"]", f"'{correct_url}'"),
                ]
                
                for pattern, replacement in patterns_replacements:
                    try:
                        new_content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
                        if count > 0:
                            content = new_content
                            file_corrections += count
                            logger.info(f"   → Remplacé {pattern} par {replacement} ({count} fois)")
                    except re.error as e:
                        logger.warning(f"   ⚠️  Pattern regex invalide: {pattern} - {e}")
            
            if content != original_content:
                # Sauvegarde de backup
                backup_path = file_path.with_suffix('.html.backup')
                if not backup_path.exists():
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(original_content)
                
                # Écriture du contenu corrigé
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.corrections_made += file_corrections
                logger.info(f"✅ Corrigé {file_corrections} occurrence(s) dans {file_path.relative_to(self.project_root)}")
                return True
            
            return False
            
        except UnicodeDecodeError:
            logger.warning(f"⚠️  Impossible de lire {file_path} (encodage non-UTF-8)")
            return False
        except Exception as e:
            logger.error(f"❌ Erreur avec {file_path}: {e}")
            return False
    
    def fix_specific_problematic_files(self):
        """Correction manuelle des fichiers spécifiques identifiés"""
        problematic_files = [
            self.project_root / "templates/assureur/dashboard.html",
            self.project_root / "templates/assureur/partials/_sidebar.html"
        ]
        
        logger.info("\n🔧 CORRECTION MANUELLE DES FICHIERS PROBLÉMATIQUES")
        
        for file_path in problematic_files:
            if file_path.exists():
                logger.info(f"📄 Traitement de {file_path.relative_to(self.project_root)}")
                self.advanced_url_correction(file_path)
            else:
                logger.warning(f"⚠️  Fichier non trouvé: {file_path}")
    
    def analyze_url_usage(self, file_path):
        """Analyse l'utilisation des URLs dans un fichier"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Recherche de tous les appels d'URL
            url_patterns = [
                r"{%\s*url\s+['\"]([^'\"]+)['\"]\s*%}",
                r"href=['\"]([^'\"]+)['\"]",
                r"['\"](assureur:[^'\"]+)['\"]"
            ]
            
            urls_found = []
            for pattern in url_patterns:
                matches = re.findall(pattern, content)
                urls_found.extend(matches)
            
            # Filtrer les URLs problématiques
            problematic = [url for url in urls_found if 'rapports' in url and 'rapport_statistiques' not in url]
            
            if problematic:
                logger.warning(f"⚠️  URLs problématiques dans {file_path.relative_to(self.project_root)}:")
                for url in set(problematic):
                    logger.warning(f"   - {url}")
                
                return problematic
            
            return []
            
        except Exception as e:
            logger.error(f"❌ Erreur d'analyse de {file_path}: {e}")
            return []
    
    def resolve_duplicates(self):
        """Résolution des templates en double"""
        logger.info("\n📋 RÉSOLUTION DES TEMPLATES EN DOUBLE")
        
        duplicates = {
            'base_assureur.html': {
                'primary': self.project_root / "assureur/templates/assureur/base_assureur.html",
                'secondary': self.project_root / "templates/assureur/base_assureur.html"
            },
            'dashboard.html': {
                'primary': self.project_root / "assureur/templates/assureur/dashboard.html", 
                'secondary': self.project_root / "templates/assureur/dashboard.html"
            }
        }
        
        for template_name, paths in duplicates.items():
            primary_exists = paths['primary'].exists()
            secondary_exists = paths['secondary'].exists()
            
            if primary_exists and secondary_exists:
                logger.info(f"📄 {template_name}:")
                logger.info(f"   🎯 Principal: {paths['primary'].relative_to(self.project_root)}")
                logger.info(f"   📍 Secondaire: {paths['secondary'].relative_to(self.project_root)}")
                
                # Suggérer de supprimer le secondaire
                try:
                    # Créer un backup avant suppression
                    backup_path = paths['secondary'].with_suffix('.html.duplicate_backup')
                    if not backup_path.exists():
                        with open(paths['secondary'], 'r', encoding='utf-8') as src:
                            with open(backup_path, 'w', encoding='utf-8') as dst:
                                dst.write(src.read())
                        
                        # Supprimer le doublon
                        paths['secondary'].unlink()
                        logger.info(f"   ✅ Doublon déplacé vers: {backup_path.name}")
                        self.corrections_made += 1
                        
                except Exception as e:
                    logger.warning(f"   ⚠️  Impossible de supprimer le doublon: {e}")
    
    def comprehensive_verification(self):
        """Vérification complète après corrections"""
        logger.info("\n🔍 VÉRIFICATION COMPLÈTE")
        
        all_templates = self.find_all_template_files()
        remaining_issues = 0
        
        for template_path in all_templates:
            issues = self.analyze_url_usage(template_path)
            remaining_issues += len(issues)
        
        # Vérifier les doublons résiduels
        duplicates_check = [
            self.project_root / "templates/assureur/base_assureur.html",
            self.project_root / "templates/assureur/dashboard.html"
        ]
        
        for path in duplicates_check:
            if path.exists():
                logger.warning(f"⚠️  Doublon toujours présent: {path.relative_to(self.project_root)}")
                remaining_issues += 1
        
        return remaining_issues
    
    def run_comprehensive_correction(self):
        """Exécute la correction complète"""
        logger.info("🔧 CORRECTION AVANCÉE DES TEMPLATES ASSUREUR")
        logger.info("=" * 60)
        
        # Étape 1: Correction manuelle des fichiers problématiques
        self.fix_specific_problematic_files()
        
        # Étape 2: Correction de tous les templates
        logger.info("\n📁 CORRECTION DE TOUS LES TEMPLATES")
        all_templates = self.find_all_template_files()
        
        for template_path in all_templates:
            if 'assureur' in str(template_path):
                self.files_processed += 1
                self.advanced_url_correction(template_path)
        
        # Étape 3: Résolution des doublons
        self.resolve_duplicates()
        
        # Étape 4: Vérification finale
        remaining_issues = self.comprehensive_verification()
        
        # Rapport final
        logger.info("\n" + "=" * 60)
        logger.info("📊 RAPPORT FINAL")
        logger.info(f"📄 Fichiers traités: {self.files_processed}")
        logger.info(f"🔧 Corrections appliquées: {self.corrections_made}")
        logger.info(f"⚠️  Problèmes restants: {remaining_issues}")
        
        if remaining_issues == 0:
            logger.info("🎉 CORRECTIONS TERMINÉES AVEC SUCCÈS!")
            return True
        else:
            logger.warning("💡 Certains problèmes persistent - vérification manuelle recommandée")
            return False

def main():
    """Fonction principale"""
    project_root = Path(__file__).parent
    
    corrector = AdvancedTemplateCorrector(project_root)
    
    try:
        success = corrector.run_comprehensive_correction()
        
        if not success:
            print("\n🔄 Tentative de correction manuelle...")
            manual_fix()
        
    except Exception as e:
        logger.error(f"❌ Erreur critique: {e}")
        return 1
    
    return 0

def manual_fix():
    """Correction manuelle pour les fichiers persistants"""
    print("\n🔧 CORRECTION MANUELLE URGENTE")
    print("Si les problèmes persistent, exécutez ces commandes:")
    print()
    print("1. Supprimer les doublons manuellement:")
    print("   rm templates/assureur/base_assureur.html")
    print("   rm templates/assureur/dashboard.html")
    print()
    print("2. Ou déplacer les doublons:")
    print("   mv templates/assureur/base_assureur.html templates/assureur/base_assureur_backup.html")
    print("   mv templates/assureur/dashboard.html templates/assureur/dashboard_backup.html")
    print()
    print("3. Vérifier les URLs manuellement dans:")
    print("   - templates/assureur/dashboard.html")
    print("   - templates/assureur/partials/_sidebar.html")

if __name__ == "__main__":
    exit(main())