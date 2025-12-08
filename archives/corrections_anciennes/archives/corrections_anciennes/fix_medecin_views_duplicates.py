# fix_medecin_views_duplicates.py
from pathlib import Path

def fix_medecin_views_duplicates():
    """Corrige les doublons dans medecin/views.py"""
    
    medecin_views = Path('medecin/views.py')
    
    with open(medecin_views, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Supprimer les sections en double
    sections_a_supprimer = [
        # Première section de vues manquantes (lignes 470-520 environ)
        '''# =============================================================================
# VUES MANQUANTES - AJOUTÉES AUTOMATIQUEMENT
# =============================================================================

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required  
def mes_ordonnances(request):''',
        
        # Deuxième section de vues manquantes (lignes 570-620 environ)
        '''# ==========================================================================
# VUES MANQUANTES AJOUTÉES AUTOMATIQUEMENT
# ==========================================================================

@login_required
def mes_rendez_vous(request):'''
    ]
    
    for section in sections_a_supprimer:
        if section in content:
            # Trouver la fin de cette section
            start_idx = content.find(section)
            if start_idx != -1:
                # Trouver la prochaine fonction ou section
                next_section = content.find('@login_required\ndef ', start_idx + len(section))
                if next_section != -1:
                    # Supprimer cette section
                    content = content[:start_idx] + content[next_section:]
                    print("✅ Section de doublons supprimée")
    
    # Écrire le fichier corrigé
    with open(medecin_views, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fichier medecin/views.py corrigé")

if __name__ == '__main__':
    fix_medecin_views_duplicates()