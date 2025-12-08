#!/usr/bin/env python
"""
CORRECTION AUTOMATIQUE DES TEMPLATES ASSUREUR
Corrige les champs problématiques dans les templates assureur
"""

import os
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates" / "assureur"

# Corrections à appliquer
CORRECTIONS = {
    'numero_membre': 'numero_unique',
    'date_adhesion': 'date_inscription',
    'membre.numero_membre': 'membre.numero_unique',
    'membre.date_adhesion': 'membre.date_inscription'
}

def corriger_template(file_path):
    """Corrige un template HTML assureur"""
    print(f"🔧 Correction de : {file_path.name}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        contenu_original = content
        corrections_appliquees = []
        
        # Appliquer les corrections
        for ancien, nouveau in CORRECTIONS.items():
            if ancien in content:
                content = content.replace(ancien, nouveau)
                corrections_appliquees.append(f"   • {ancien} → {nouveau}")
        
        # Sauvegarder si des corrections ont été appliquées
        if content != contenu_original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Corrections appliquées:")
            for correction in corrections_appliquees:
                print(correction)
        else:
            print("✅ Aucune correction nécessaire")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def main():
    """Corrige tous les templates assureur problématiques"""
    print("🚀 CORRECTION AUTOMATIQUE DES TEMPLATES ASSUREUR")
    
    # Templates identifiés comme problématiques
    templates_problematiques = [
        "liste_membres.html",
        "creer_cotisation.html", 
        "detail_cotisation.html",
        "liste_cotisations.html",
        "detail_soin.html",
        "export_bons_html.html",
        "liste_bons.html",
        "liste_paiements.html"
    ]
    
    templates_corriges = 0
    
    for template_relatif in templates_problematiques:
        template_path = TEMPLATES_DIR / template_relatif
        if template_path.exists():
            corriger_template(template_path)
            templates_corriges += 1
        else:
            print(f"❌ Template non trouvé: {template_path}")
    
    print("\n" + "="*60)
    print("✅ CORRECTIONS TERMINÉES")
    print(f"📋 {templates_corriges}/{len(templates_problematiques)} templates corrigés")
    print("\n💡 Vérifiez que les templates fonctionnent correctement")

if __name__ == "__main__":
    main()