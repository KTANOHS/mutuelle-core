#!/usr/bin/env python
"""
ANALYSE DES TEMPLATES PHARMACIEN
Vérifie la cohérence entre les modèles et les templates pharmacien
"""

import os
import re
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates" / "pharmacien"

def analyser_template(file_path):
    """Analyse un template HTML pharmacien"""
    print(f"\n📄 Analyse de : {file_path.name}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Recherche des variables Django
        variables = re.findall(r'\{\{\s*([^\s\}]+)\s*\}\}', content)
        urls = re.findall(r'\{\%\s*url\s+[\'\"]([^\'\"]+)[\'\"]', content)
        
        variables_filtrees = []
        for var in set(variables):
            # Filtrer les variables intéressantes
            if '|' not in var and any(keyword in var for keyword in 
                                    ['membre', 'numero', 'date', 'medicament', 'ordonnance', 'stock']):
                variables_filtrees.append(var)
        
        if variables_filtrees:
            print("   📊 Variables importantes trouvées:")
            for var in sorted(variables_filtrees):
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
    """Analyse tous les templates pharmacien"""
    print("🔍 ANALYSE DES TEMPLATES PHARMACIEN")
    print(f"📁 Répertoire templates: {TEMPLATES_DIR}")
    
    if not TEMPLATES_DIR.exists():
        print(f"❌ Répertoire templates non trouvé: {TEMPLATES_DIR}")
        return
    
    templates = list(TEMPLATES_DIR.rglob("*.html"))
    print(f"📁 {len(templates)} templates trouvés dans pharmacien/")
    
    # Analyser d'abord les templates critiques
    templates_critiques = ['dashboard.html', 'liste_ordonnances.html', 'valider_ordonnance.html']
    
    for template_critique in templates_critiques:
        template_path = TEMPLATES_DIR / template_critique
        if template_path.exists():
            analyser_template(template_path)
    
    # Puis les autres templates
    for template in sorted(templates):
        if template.name not in templates_critiques:
            analyser_template(template)
    
    print("\n" + "="*60)
    print("📋 RÉSUMÉ DE L'ANALYSE:")
    print("   • Vérifier l'intégration avec le module medecin")
    print("   • S'assurer de la cohérence des URLs")
    print("   • Valider les relations avec les modèles membres")
    print("✅ Analyse terminée")

if __name__ == "__main__":
    main()