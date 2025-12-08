# analyze_redirects.py
import os
import sys
import re
from pathlib import Path

def analyze_redirect_flow():
    """Analyse spécifique du flux de redirection"""
    print("🔄 ANALYSE SPÉCIFIQUE DU FLUX DE REDIRECTION")
    print("=" * 60)
    
    project_path = Path('/Users/koffitanohsoualiho/Documents/projet')
    core_path = project_path / 'mutuelle_core'
    
    # 1. Analyser utils.py - fonctions de redirection
    utils_file = core_path / 'utils.py'
    if utils_file.exists():
        print("1. 🔍 ANALYSE UTILS.PY (fonctions de redirection)")
        content = utils_file.read_text()
        
        # Trouver get_user_redirect_url
        redirect_func_pattern = r'def get_user_redirect_url\(.*?\):.*?(?=def|\Z)'
        match = re.search(redirect_func_pattern, content, re.DOTALL)
        
        if match:
            func_code = match.group(0)
            print("   ✅ Fonction get_user_redirect_url trouvée")
            
            # Analyser la logique
            lines = func_code.split('\n')
            print(f"   📝 Code ({len(lines)} lignes):")
            for i, line in enumerate(lines[:15], 1):  # Premières 15 lignes
                print(f"      {i:3}: {line}")
                
            # Vérifier les problèmes
            if "redirect-after-login" in func_code:
                print("   ⚠️  Fait référence à 'redirect-after-login'")
            if "dashboard" in func_code:
                print("   ⚠️  Fait référence à 'dashboard'")
                
        else:
            print("   ❌ Fonction get_user_redirect_url non trouvée")
    
    # 2. Analyser views.py - vue de redirection
    views_file = core_path / 'views.py'
    if views_file.exists():
        print("\n2. 🔍 ANALYSE VIEWS.PY (vue redirect_to_user_dashboard)")
        content = views_file.read_text()
        
        redirect_view_pattern = r'def redirect_to_user_dashboard\(.*?\):.*?(?=def|\Z)'
        match = re.search(redirect_view_pattern, content, re.DOTALL)
        
        if match:
            func_code = match.group(0)
            print("   ✅ Vue redirect_to_user_dashboard trouvée")
            
            lines = func_code.split('\n')
            print(f"   📝 Code ({len(lines)} lignes):")
            for i, line in enumerate(lines, 1):
                if any(keyword in line for keyword in ['return', 'redirect', 'get_user_redirect_url']):
                    print(f"      {i:3}: {line.strip()}")
                    
        else:
            print("   ❌ Vue redirect_to_user_dashboard non trouvée")
    
    # 3. Analyser urls.py - configuration URLs
    urls_file = core_path / 'urls.py'
    if urls_file.exists():
        print("\n3. 🔍 ANALYSE URLS.PY (configuration)")
        content = urls_file.read_text()
        
        # Trouver les URLs de redirection
        redirect_urls = re.findall(r"path\(.*redirect-after-login.*\)", content)
        dashboard_urls = re.findall(r"path\(.*dashboard.*\)", content)
        
        print("   📍 URLs de redirection:")
        for url in redirect_urls:
            print(f"      {url}")
            
        print("   📍 URLs dashboard:")
        for url in dashboard_urls:
            print(f"      {url}")

def analyze_user_groups_logic():
    """Analyse la logique des groupes utilisateurs"""
    print("\n\n👥 ANALYSE LOGIQUE GROUPES UTILISATEURS")
    print("=" * 60)
    
    core_path = Path('/Users/koffitanohsoualiho/Documents/projet') / 'mutuelle_core'
    utils_file = core_path / 'utils.py'
    
    if utils_file.exists():
        content = utils_file.read_text()
        
        # Analyser les fonctions de groupe
        group_functions = [
            'get_user_primary_group',
            'user_has_group', 
            'user_is_assureur',
            'user_is_medecin',
            'user_is_pharmacien',
            'user_is_membre'
        ]
        
        print("Fonctions de gestion des groupes:")
        for func_name in group_functions:
            pattern = rf'def {func_name}\(.*?\):.*?(?=def|\Z)'
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                lines = match.group(0).count('\n')
                print(f"   ✅ {func_name} ({lines} lignes)")
            else:
                print(f"   ❌ {func_name} (NON TROUVÉE)")

if __name__ == "__main__":
    analyze_redirect_flow()
    analyze_user_groups_logic()