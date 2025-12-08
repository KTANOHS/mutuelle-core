#!/usr/bin/env python
"""
SCRIPT DE CORRECTION AUTOMATIQUE DES TEMPLATES
Corrige les champs problématiques dans les templates
"""

import os
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

# Corrections à appliquer
CORRECTIONS = {
    'numero_membre': 'numero_unique',
    'date_adhesion': 'date_inscription',
    'membre.numero_membre': 'membre.numero_unique',
    'membre.date_adhesion': 'membre.date_inscription'
}

def corriger_template(file_path):
    """Corrige un template HTML"""
    print(f"🔧 Correction de : {file_path}")
    
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
    """Corrige tous les templates problématiques"""
    print("🚀 CORRECTION AUTOMATIQUE DES TEMPLATES")
    
    # Templates identifiés comme problématiques
    templates_problematiques = [
        "membres/detail_membre.html",
        # Ajouter d'autres templates si nécessaire
    ]
    
    for template_relatif in templates_problematiques:
        template_path = TEMPLATES_DIR / template_relatif
        if template_path.exists():
            corriger_template(template_path)
        else:
            print(f"❌ Template non trouvé: {template_path}")
    
    print("\n" + "="*60)
    print("✅ CORRECTIONS TERMINÉES")
    print("📋 Résumé des corrections appliquées:")
    print("   • numero_membre → numero_unique")
    print("   • date_adhesion → date_inscription")
    print("\n💡 Vérifiez que les templates fonctionnent correctement")

if __name__ == "__main__":
    main()