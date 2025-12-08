#!/usr/bin/env python
"""
Script pour corriger automatiquement les références aux templates medecin
"""

import os
import re

def corriger_templates_medecin():
    """Corrige toutes les références aux templates base dans les fichiers medecin"""
    print("🔧 CORRECTION AUTOMATIQUE DES TEMPLATES MÉDECIN")
    print("=" * 60)
    
    templates_dir = "templates/medecin"
    
    # Fichiers à corriger et leurs patterns
    corrections = {
        # Fichiers qui utilisent 'medecin/base.html' → doivent utiliser 'medecin/base.html'
        # Mais comme base_medecin.html a été renommé en base.html, on garde 'medecin/base.html'
        'historique_ordonnances.html': (r"{% extends ['\"]medecin/base.html['\"] %}", "{% extends 'medecin/base.html' %}"),
        'statistiques.html': (r"{% extends ['\"]medecin/base.html['\"] %}", "{% extends 'medecin/base.html' %}"),
        'detail_bon.html': (r"{% extends ['\"]medecin/base.html['\"] %}", "{% extends 'medecin/base.html' %}"),
        'bons_attente.html': (r"{% extends ['\"]medecin/base.html['\"] %}", "{% extends 'medecin/base.html' %}"),
        'detail_ordonnance.html': (r"{% extends ['\"]medecin/base.html['\"] %}", "{% extends 'medecin/base.html' %}"),
        'mes_rendez_vous.html': (r"{% extends ['\"]medecin/base.html['\"] %}", "{% extends 'medecin/base.html' %}"),
        
        # Fichiers qui utilisent 'base_medecin.html' → doivent utiliser 'medecin/base.html'
        'liste_ordonnances.html': (r"{% extends ['\"]base_medecin.html['\"] %}", "{% extends 'medecin/base.html' %}"),
        'liste_bons.html': (r"{% extends ['\"]base_medecin.html['\"] %}", "{% extends 'medecin/base.html' %}"),
        'profil_medecin.html': (r"{% extends ['\"]base_medecin.html['\"] %}", "{% extends 'medecin/base.html' %}"),
        'dashboard.html': (r"{% extends ['\"]base_medecin.html['\"] %}", "{% extends 'medecin/base.html' %}"),
        'creer_ordonnance.html': (r"{% extends ['\"]base_medecin.html['\"] %}", "{% extends 'medecin/base.html' %}"),
        
        # Fichiers avec d'autres bases
        'mes_ordonnances.html': (r"{% extends ['\"]membres/base.html['\"] %}", "{% extends 'medecin/base.html' %}"),
        'detail_consultation.html': (r"{% extends ['\"]base.html['\"] %}", "{% extends 'medecin/base.html' %}"),
    }
    
    fichiers_corriges = 0
    
    for filename, (pattern, replacement) in corrections.items():
        filepath = os.path.join(templates_dir, filename)
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Compter les occurrences avant
                avant = len(re.findall(pattern, content))
                
                # Remplacer
                nouveau_content = re.sub(pattern, replacement, content)
                
                # Si changement détecté, sauvegarder
                if nouveau_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(nouveau_content)
                    
                    apres = len(re.findall(pattern, nouveau_content))
                    print(f"✅ {filename}: {avant} → {apres} occurrences corrigées")
                    fichiers_corriges += 1
                else:
                    print(f"ℹ️  {filename}: Aucune correction nécessaire")
                    
            except Exception as e:
                print(f"❌ {filename}: Erreur - {e}")
        else:
            print(f"⚠️  {filename}: Fichier non trouvé")
    
    print(f"\n📊 RÉSUMÉ: {fichiers_corriges} fichiers corrigés sur {len(corrections)}")
    
    # Vérification finale
    print("\n🔍 VÉRIFICATION FINALE:")
    print("-" * 25)
    
    for filename in corrections.keys():
        filepath = os.path.join(templates_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '{% extends' in content:
                lines = content.split('\n')
                for line in lines:
                    if '{% extends' in line:
                        print(f"   {filename}: {line.strip()}")
                        break

if __name__ == "__main__":
    corriger_templates_medecin()
    
    print("\n🎯 PROCHAINES ÉTAPES:")
    print("1. Exécutez à nouveau le test: python scripts/test_final_medecin.py")
    print("2. Si des erreurs persistent, vérifiez les templates manuellement")
    print("3. Testez l'application dans le navigateur")