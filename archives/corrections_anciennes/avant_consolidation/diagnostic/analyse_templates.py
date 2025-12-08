#!/usr/bin/env python
"""
ANALYSE DES TEMPLATES MEMBRES
Vérifie la cohérence entre les modèles et les templates
"""

import os
import re
from pathlib import Path

# Configuration - CORRECTION DU CHEMIN
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates" / "membres"

def analyser_template(file_path):
    """Analyse un template HTML"""
    print(f"\n📄 Analyse de : {file_path.name}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Recherche des variables Django
        variables = re.findall(r'\{\{\s*([^\s\}]+)\s*\}\}', content)
        urls = re.findall(r'\{\%\s*url\s+[\'\"]([^\'\"]+)[\'\"]', content)
        
        if variables:
            print("   📊 Variables trouvées:")
            for var in sorted(set(variables)):
                # Filtrer les variables simples (sans filtres)
                if '|' not in var:
                    print(f"      • {var}")
        
        if urls:
            print("   🌐 URLs trouvées:")
            for url in sorted(set(urls)):
                print(f"      • {url}")
                
        # Vérification des champs problématiques
        champs_problematiques = {
            'numero_membre': 'Devrait être numero_unique',
            'date_adhesion': 'Devrait être date_inscription',
            'membre.numero_membre': 'Devrait être membre.numero_unique',
            'membre.date_adhesion': 'Devrait être membre.date_inscription'
        }
        
        problemes_trouves = False
        for champ, correction in champs_problematiques.items():
            if champ in content:
                if not problemes_trouves:
                    print("   ⚠️  PROBLÈMES IDENTIFIÉS:")
                    problemes_trouves = True
                print(f"      • '{champ}' → {correction}")
                
        if not problemes_trouves:
            print("   ✅ Aucun problème détecté")
                
    except Exception as e:
        print(f"   ❌ Erreur lecture: {e}")

def main():
    """Analyse tous les templates membres"""
    print("🔍 ANALYSE DES TEMPLATES MEMBRES")
    print(f"📁 Répertoire templates: {TEMPLATES_DIR}")
    
    if not TEMPLATES_DIR.exists():
        print(f"❌ Répertoire templates non trouvé: {TEMPLATES_DIR}")
        print("📋 Templates disponibles:")
        templates_root = BASE_DIR / "templates"
        if templates_root.exists():
            for item in templates_root.iterdir():
                if item.is_dir():
                    print(f"   📁 {item.name}/")
                else:
                    print(f"   📄 {item.name}")
        return
    
    templates = list(TEMPLATES_DIR.glob("*.html"))
    print(f"📁 {len(templates)} templates trouvés dans membres/")
    
    for template in sorted(templates):
        analyser_template(template)
    
    print("\n" + "="*60)
    print("📋 RÉSUMÉ DES CORRECTIONS NÉCESSAIRES:")
    print("   • Remplacer 'numero_membre' par 'numero_unique'")
    print("   • Remplacer 'date_adhesion' par 'date_inscription'")
    print("   • Vérifier les URLs dans les templates")
    print("✅ Analyse terminée")

if __name__ == "__main__":
    main()