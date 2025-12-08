#!/usr/bin/env python3
# SCRIPT DE CORRECTION AUTOMATIQUE - Erreur 'membre'
# Généré automatiquement par diagnostic_membre_erreur.py

import os
import re
import sys
from pathlib import Path

def corriger_erreurs_membre():
    corrections = [
        # Patterns pour Soin.objects.filter
        (r'Soin\\.objects\\.filter\\(.*)membre=', r'Soin.objects.filter\\1patient='),
        (r'soin\\.membre', r'soin.patient'),
        (r'filter\\(membre=', r'filter(patient='),
        (r'filter\\(membre__', r'filter(patient__'),
    ]
    
    fichiers_corriges = 0
    
    # Fichiers à corriger basés sur l'analyse
    fichiers_a_corriger = ['/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/membres/forms.py', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/medecin/detail_bon.html', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/assureur/creer_paiement.html', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/membres/models.py', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/assureur/modifier_paiement.html', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/assureur/views.py', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/membres/tests.py', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/assureur/views_selection.py', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/soins/forms.py', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/membres/views.py', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/assureur/forms.py', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/membres/correction_membres.py', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/assureur/services.py', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/assureur/liste_bons.html', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/membres/management/commands/debug_simple.py', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/assureur/tests.py', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/agents/historique_bons.html', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/assureur/management/commands/init_groups.py', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/assureur/detail_bon.html', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/assureur/export_bons_pdf.html', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/membres/analytics.py', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/assureur/export_bons_html.html', '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/medecin/bons_attente.html']
    
    for fichier_pattern in fichiers_a_corriger:
        for fichier_path in Path('.').rglob(fichier_pattern):
            if fichier_path.exists():
                try:
                    with open(fichier_path, 'r', encoding='utf-8') as f:
                        contenu = f.read()
                    
                    contenu_corrige = contenu
                    for pattern_avant, pattern_apres in corrections:
                        contenu_corrige = re.sub(pattern_avant, pattern_apres, contenu_corrige)
                    
                    if contenu_corrige != contenu:
                        with open(fichier_path, 'w', encoding='utf-8') as f:
                            f.write(contenu_corrige)
                        print(f"✅ Corrections appliquées: {fichier_path}")
                        fichiers_corriges += 1
                    else:
                        print(f"✅ Aucune correction nécessaire: {fichier_path}")
                        
                except Exception as e:
                    print(f"❌ Erreur correction {fichier_path}: {e}")
    
    print(f"\\n🎯 {fichiers_corriges} fichiers corrigés")

if __name__ == "__main__":
    corriger_erreurs_membre()
