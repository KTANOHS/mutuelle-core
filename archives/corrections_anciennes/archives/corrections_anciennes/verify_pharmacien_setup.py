# clean_pharmacien_views.py
from pathlib import Path

def clean_pharmacien_views():
    """Nettoie le fichier pharmacien/views.py des doublons et problèmes"""
    
    views_file = Path('pharmacien/views.py')
    
    with open(views_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Supprimer les réimports en double (lignes ~355)
    duplicate_imports = '''from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import FiltreParPartageMixin'''
    
    # Compter combien de fois ces imports apparaissent
    if content.count(duplicate_imports) > 1:
        # Garder seulement la première occurrence
        first_occurrence = content.find(duplicate_imports)
        second_occurrence = content.find(duplicate_imports, first_occurrence + len(duplicate_imports))
        
        if second_occurrence != -1:
            content = content[:second_occurrence] + content[second_occurrence + len(duplicate_imports):]
            print("✅ Réimports en double supprimés")
    
    # 2. Ajouter un alias pour la compatibilité
    alias_code = '''

# =============================================================================
# ALIAS POUR COMPATIBILITÉ
# =============================================================================

@login_required
@pharmacien_required
def dashboard(request):
    """Alias pour compatibilité avec les URLs existantes"""
    return dashboard_pharmacien(request)
'''
    
    if 'def dashboard(request):' not in content:
        # Ajouter avant la section des vues génériques
        generic_section = '# =============================================================================\n# VUES GÉNÉRIQUES'
        if generic_section in content:
            content = content.replace(generic_section, alias_code + '\n\n' + generic_section)
            print("✅ Alias dashboard ajouté")
    
    # Écrire le fichier corrigé
    with open(views_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fichier pharmacien/views.py nettoyé avec succès")

if __name__ == '__main__':
    clean_pharmacien_views()