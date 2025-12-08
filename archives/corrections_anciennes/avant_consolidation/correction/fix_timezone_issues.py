#!/usr/bin/env python
"""
Script de correction automatique des problèmes de timezone
Corrige les datetime.now() en timezone.now() et ajoute les imports manquants
"""

import os
import re
from pathlib import Path

def fix_timezone_in_file(file_path):
    """Corrige les problèmes de timezone dans un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Vérifier si timezone est déjà importé
        needs_timezone_import = 'from django.utils import timezone' not in content
        
        # Remplacer les patterns problématiques
        replacements = [
            # Pattern 1: datetime.datetime.now()
            (r'datetime\.datetime\.now\(\)', 'timezone.now()'),
            # Pattern 2: datetime.now() (avec import from datetime)
            (r'(?<!\.)datetime\.now\(\)', 'timezone.now()'),
            # Pattern 3: __import__('datetime').datetime.now()
            (r"__import__\('datetime'\)\.datetime\.now\(\)", "timezone.now()"),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # Ajouter l'import timezone si nécessaire et si des corrections ont été faites
        if needs_timezone_import and any(replacement in content for pattern, replacement in replacements):
            # Trouver où ajouter l'import (après les imports Django)
            lines = content.split('\n')
            new_lines = []
            timezone_import_added = False
            
            for i, line in enumerate(lines):
                new_lines.append(line)
                
                # Ajouter après les imports Django standards
                if (not timezone_import_added and 
                    ('from django.' in line or 'import django' in line) and
                    i + 1 < len(lines) and 
                    not lines[i + 1].strip().startswith('from ') and
                    not lines[i + 1].strip().startswith('import ')):
                    new_lines.append('from django.utils import timezone')
                    timezone_import_added = True
            
            # Si pas trouvé d'endroit approprié, ajouter après le dernier import
            if not timezone_import_added:
                import_section_end = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith(('import ', 'from ')):
                        import_section_end = i
                
                if import_section_end > 0:
                    new_lines = lines[:import_section_end + 1] + ['from django.utils import timezone'] + lines[import_section_end + 1:]
                else:
                    # Ajouter au début du fichier
                    new_lines.insert(0, 'from django.utils import timezone')
            
            content = '\n'.join(new_lines)
        
        # Écrire le fichier modifié seulement si des changements ont été faits
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction de {file_path}: {e}")
        return False

def main():
    project_root = Path('.').absolute()
    
    # Liste des fichiers à corriger basée sur votre rapport
    files_to_fix = [
        'diagnostic_final_complet.py',
        'analyse_configuration_communication.py',
        'project_lister.py',
        'template_analysis.py',
        'medecin_analysis.py',
        'correction_finale_relations.py',
        'analyser_mutuelle_core3.py',
        'utils.py',
        'analyze_post_delete_corrected.py',
        'check_templates.py',
        'analyser_mutuelle_core2.py',
        'medecin_realtime_monitor.py',
        'rebuild_agent_templates.py',
        'generate_detailed_report.py',
        'analyze_post_delete.py',
        'analyse_cotisations_existant.py',
        'recovery_script.py',
        'analyse_projet.py',
        'test_bon_soin.py',
        'fix_agents_paths.py',
        'analyse_probleme.py',
        'analyse_configuration_communication1.py',
        'creation_relations_reelles.py',
        'mutuelle_core/logging_config.py',
        'mutuelle_core/validators.py',
        'mutuelle_core/utils.py',
        'tests/test_connexion_medecin.py',
        'scripts/test_connexion_manuel.py',
        'scripts/analysis/analyze_admin.py',
        'scripts/analysis/analyze_views.py',
        'communication/services.py',
    ]
    
    print("🔧 Démarrage de la correction automatique des timezones...")
    print(f"📁 Répertoire du projet: {project_root}")
    
    fixed_count = 0
    total_files = len(files_to_fix)
    
    for file_rel_path in files_to_fix:
        file_path = project_root / file_rel_path
        
        if not file_path.exists():
            print(f"❌ Fichier introuvable: {file_rel_path}")
            continue
            
        print(f"🔧 Correction de: {file_rel_path}")
        
        if fix_timezone_in_file(file_path):
            print(f"  ✅ Fichier corrigé")
            fixed_count += 1
        else:
            print(f"  ℹ️  Aucune correction nécessaire")
    
    print(f"\n{'='*60}")
    print(f"🎉 CORRECTION TERMINÉE!")
    print(f"{'='*60}")
    print(f"📄 Fichiers traités: {total_files}")
    print(f"✅ Fichiers corrigés: {fixed_count}")
    print(f"📊 Taux de réussite: {fixed_count/total_files*100:.1f}%")
    
    # Générer un rapport des corrections appliquées
    print(f"\n📋 RAPPORT DES CORRECTIONS:")
    print(f"   • datetime.datetime.now() → timezone.now()")
    print(f"   • datetime.now() → timezone.now()")
    print(f"   • Ajout automatique de: from django.utils import timezone")
    print(f"   • Suppression des warnings de timezone naive")

if __name__ == "__main__":
    main()