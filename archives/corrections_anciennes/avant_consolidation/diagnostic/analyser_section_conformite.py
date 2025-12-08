#!/usr/bin/env python3
"""
ANALYSE SPÉCIFIQUE - Trouver la section exacte du taux de conformité
"""

import os
import re

def trouver_section_conformite():
    """Trouve exactement où se trouve la section problématique"""
    
    template_path = 'templates/agents/dashboard.html'
    
    print("🔍 RECHERCHE DE LA SECTION 'TAUX CONFORMITÉ'")
    print("=" * 50)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Rechercher toutes les occurrences de "Taux conformité" ou similaires
    patterns = [
        r'Taux conformité',
        r'Taux.*conformité', 
        r'conformité',
        r'pourcentage',
        r'%',
        r'stats\.membres_a_jour.*stats\.membres_actifs'
    ]
    
    for pattern in patterns:
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        if matches:
            print(f"\n📌 Pattern: '{pattern}' - {len(matches)} occurrence(s)")
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                
                # Afficher le contexte (5 lignes avant/après)
                lines = content.split('\n')
                start_line = max(0, line_num - 6)  # -1 car index 0-based
                end_line = min(len(lines), line_num + 4)
                
                print(f"   Ligne {line_num}:")
                for i in range(start_line, end_line):
                    marker = ">>>" if i == line_num - 1 else "   "
                    print(f"   {marker} {i+1}: {lines[i]}")
    
    # Recherche spécifique de la section carte
    print("\n🎯 RECHERCHE DES CARTES DE STATISTIQUES:")
    carte_sections = re.finditer(r'<div class="card[^>]*>.*?</div>\s*</div>\s*</div>', content, re.DOTALL)
    
    for i, section in enumerate(carte_sections):
        if 'Taux' in section.group() or 'conformité' in section.group() or '%' in section.group():
            print(f"\n📊 CARTE {i+1} (Taux conformité):")
            print(section.group()[:500] + "..." if len(section.group()) > 500 else section.group())

def corriger_section_specifique():
    """Corrige la section spécifique du taux de conformité"""
    
    template_path = 'templates/agents/dashboard.html'
    
    print("\n🔧 CORRECTION DE LA SECTION SPÉCIFIQUE")
    print("=" * 50)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Sauvegarder l'original
    backup_path = f"{template_path}.backup_section"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"💾 Backup créé: {backup_path}")
    
    # Pattern pour trouver la section problématique
    # Chercher la section qui contient le calcul erroné
    ancien_pattern = r'''
        (<!--\s*Taux\s*conformité[^>]*-->.*?)      # Commentaire avant
        ({%\s*if\s*stats\.membres_a_jour\s*and\s*stats\.membres_actifs\s*%}.*?)  # Condition if
        ({{ \s*\(\s*\(\s*stats\.membres_a_jour\s*/\s*stats\.membres_actifs\s*\)\s*\*\s*100\s*\)\s*\|\s*floatformat:0\s*}}%)  # Calcul erroné
        (.*?{%\s*else\s*%}.*?)                     # Else
        (.*?{%\s*endif\s*%})                       # Endif
    '''
    
    nouveau_contenu = r'''
\1
\2
                                {{ stats.pourcentage_conformite|floatformat:0 }}%
\4
\5
'''
    
    # Essayer la substitution
    content_corrige, nb_subs = re.subn(ancien_pattern, nouveau_contenu, content, flags=re.DOTALL | re.VERBOSE | re.IGNORECASE)
    
    if nb_subs > 0:
        print(f"✅ {nb_subs} substitution(s) effectuée(s)")
        
        # Écrire le contenu corrigé
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content_corrige)
        print("✅ Template corrigé")
        
        # Vérifier la correction
        with open(template_path, 'r', encoding='utf-8') as f:
            nouveau_content = f.read()
        
        if 'stats.pourcentage_conformite' in nouveau_content and 'stats.membres_a_jour / stats.membres_actifs' not in nouveau_content:
            print("✅ Vérification: Correction appliquée avec succès")
        else:
            print("❌ Vérification: Problème avec la correction")
            
    else:
        print("❌ Aucune substitution effectuée - Pattern non trouvé")
        print("🔍 Tentative avec un pattern plus simple...")
        
        # Pattern plus simple
        ancien_simple = r'{{\s*\(\s*\(\s*stats\.membres_a_jour\s*/\s*stats\.membres_actifs\s*\)\s*\*\s*100\s*\)\s*\|\s*floatformat:0\s*}}%'
        nouveau_simple = r'{{ stats.pourcentage_conformite|floatformat:0 }}%'
        
        content_corrige, nb_subs = re.subn(ancien_simple, nouveau_simple, content)
        
        if nb_subs > 0:
            print(f"✅ {nb_subs} substitution(s) effectuée(s) avec pattern simple")
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content_corrige)
            print("✅ Template corrigé avec pattern simple")
        else:
            print("❌ Échec de la correction automatique")
            print("💡 Correction manuelle nécessaire")

def afficher_section_conformite():
    """Affiche uniquement la section du taux de conformité"""
    
    template_path = 'templates/agents/dashboard.html'
    
    print("\n📋 SECTION 'TAUX CONFORMITÉ' ACTUELLE:")
    print("=" * 50)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver la section par contexte
    if 'Taux conformité' in content:
        start = content.find('Taux conformité')
        # Trouver la fin de la carte
        end = content.find('</div>', content.find('</div>', content.find('</div>', start))) + 6
        
        section = content[start:end]
        lines = section.split('\n')
        
        print("🔍 Contenu actuel de la section:")
        for i, line in enumerate(lines):
            print(f"{i+1:3d}: {line}")

if __name__ == "__main__":
    trouver_section_conformite()
    afficher_section_conformite()
    corriger_section_specifique()