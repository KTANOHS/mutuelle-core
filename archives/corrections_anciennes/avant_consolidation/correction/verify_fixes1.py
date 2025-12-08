#!/usr/bin/env python
"""
Script de vérification après correction des timezones
"""

import re
from pathlib import Path

def check_file_after_fix(file_path):
    """Vérifie un fichier après correction"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # Vérifier la présence de l'import timezone
        if 'from django.utils import timezone' not in content:
            issues.append("❌ Import timezone manquant")
        
        # Vérifier les patterns problématiques restants
        problematic_patterns = [
            r'datetime\.datetime\.now\(\)',
            r'(?<!\.)datetime\.now\(\)',
        ]
        
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            for pattern in problematic_patterns:
                if re.search(pattern, line) and not line.strip().startswith('#'):
                    issues.append(f"❌ Ligne {i}: {pattern} trouvé")
        
        # Vérifier l'utilisation correcte de timezone
        timezone_uses = len(re.findall(r'timezone\.now\(\)', content))
        
        return {
            'file': file_path.name,
            'path': str(file_path),
            'issues': issues,
            'timezone_uses': timezone_uses,
            'status': '✅ OK' if not issues else '❌ PROBLEMES'
        }
        
    except Exception as e:
        return {
            'file': file_path.name,
            'path': str(file_path),
            'issues': [f"❌ Erreur de lecture: {e}"],
            'timezone_uses': 0,
            'status': '❌ ERREUR'
        }

def main():
    project_root = Path('.').absolute()
    
    # Mêmes fichiers que la correction
    files_to_check = [
        'diagnostic_final_complet.py',
        'analyse_configuration_communication.py',
        # ... ajouter tous les fichiers de la liste précédente
    ]
    
    print("🔍 Vérification après correction...")
    
    results = []
    for file_rel_path in files_to_check:
        file_path = project_root / file_rel_path
        if file_path.exists():
            result = check_file_after_fix(file_path)
            results.append(result)
    
    # Afficher le rapport
    print(f"\n{'='*80}")
    print("📊 RAPPORT DE VÉRIFICATION APRÈS CORRECTION")
    print(f"{'='*80}")
    
    ok_count = sum(1 for r in results if r['status'] == '✅ OK')
    problem_count = sum(1 for r in results if r['status'] != '✅ OK')
    
    print(f"✅ Fichiers OK: {ok_count}")
    print(f"❌ Fichiers avec problèmes: {problem_count}")
    print(f"📊 Total timezone.now() utilisés: {sum(r['timezone_uses'] for r in results)}")
    
    # Afficher les détails
    for result in results:
        print(f"\n📁 {result['file']} - {result['status']}")
        for issue in result['issues']:
            print(f"   {issue}")
        if result['timezone_uses'] > 0:
            print(f"   ✅ {result['timezone_uses']} utilisation(s) de timezone.now()")

if __name__ == "__main__":
    main()