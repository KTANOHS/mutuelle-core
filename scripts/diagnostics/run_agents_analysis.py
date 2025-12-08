#!/usr/bin/env python
"""
SCRIPT PRINCIPAL D'ANALYSE - LANCE TOUTES LES ANALYSES
"""

import subprocess
import sys
from pathlib import Path

def run_analysis():
    print("🚀 LANCEMENT DE L'ANALYSE COMPLÈTE DU MODULE AGENTS")
    print("=" * 60)
    
    scripts = [
        'agents_analysis.py',
        'urls_analyzer.py', 
        'models_analyzer.py',
        'templates_analyzer.py'
    ]
    
    for script in scripts:
        print(f"\n🎯 Exécution de {script}...")
        print("-" * 40)
        
        try:
            result = subprocess.run([sys.executable, script], 
                                  capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(f"⚠️  Erreurs: {result.stderr}")
        except Exception as e:
            print(f"❌ Erreur exécution {script}: {e}")

if __name__ == '__main__':
    run_analysis()