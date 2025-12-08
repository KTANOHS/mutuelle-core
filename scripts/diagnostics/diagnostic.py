# diagnostic_html_error.py
import os
import sys
import re
from pathlib import Path

def find_django_project():
    """Trouver le répertoire du projet Django"""
    current = Path.cwd()
    
    while current != current.parent:
        manage_py = current / 'manage.py'
        if manage_py.exists():
            return current
        current = current.parent
    
    return None

def analyze_html_error():
    """Analyser spécifiquement l'erreur NameError: name 'html' is not defined"""
    project_dir = find_django_project()
    
    if not project_dir:
        print("❌ Projet Django non trouvé")
        return
    
    print(f"✅ Projet Django trouvé: {project_dir}")
    
    # Chercher le fichier views.py problématique
    views_files = list(project_dir.rglob('*/views.py'))
    
    print(f"\n📁 Fichiers views.py trouvés: {len(views_files)}")
    
    for views_file in views_files:
        print(f"\n🔍 Analyse de: {views_file}")
        
        try:
            with open(views_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Rechercher les utilisations de 'html'
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                # Rechercher les patterns problématiques
                patterns = [
                    (r'html\.', 'html. utilisé comme module'),
                    (r'= html\b', 'html utilisé comme variable'),
                    (r'html\s*=', 'html utilisé comme variable'),
                    (r'import html', 'import html standard (peut être manquant)'),
                ]
                
                for pattern, description in patterns:
                    if re.search(pattern, line):
                        print(f"   ⚠️  Ligne {i+1}: {description}")
                        print(f"      {line.strip()}")
                
                # Rechercher spécifiquement html.escape, html.format, etc.
                if re.search(r'html\.\w+', line):
                    print(f"   ❌ Ligne {i+1}: Utilisation de html.XXX sans import")
                    print(f"      {line.strip()}")
            
            # Vérifier les imports
            imports = [
                line for line in lines if line.strip().startswith(('import', 'from'))
            ]
            
            if imports:
                print(f"\n📦 Imports dans le fichier:")
                for imp in imports:
                    print(f"   {imp}")
            
            # Vérifier si 'html' est importé
            html_imported = any('html' in imp.lower() for imp in imports)
            
            if not html_imported and any('html\.' in content for pattern in ['html\.']):
                print(f"\n💡 PROBLÈME IDENTIFIÉ: html utilisé mais non importé")
                print(f"   Solution: Ajouter 'from django.utils.html import escape'")
                
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse: {e}")

def generate_fix():
    """Générer le code de correction"""
    print("\n" + "=" * 60)
    print("💡 CODE DE CORRECTION")
    print("=" * 60)
    
    correction_code = '''
# 1. CORRECTION DES IMPORTS
# Dans votre fichier views.py, ajoutez:
from django.utils.html import escape, format_html, mark_safe

# 2. REMPLACER LES UTILISATIONS DE html.
# ❌ MAUVAIS:
# texte_echappe = html.escape(user_input)
# message = html.format('<strong>{}</strong>', texte)

# ✅ CORRECT:
# texte_echappe = escape(user_input)
# message = format_html('<strong>{}</strong>', texte_echappe)

# 3. EXEMPLE COMPLET DE CORRECTION:
def home(request):
    """Vue d'accueil corrigée"""
    from django.utils.html import escape, format_html
    
    # Exemple d'utilisation sécurisée
    user_input = "texte <script>alert('xss')</script>"
    safe_text = escape(user_input)  # Échappe le HTML
    
    # Formatage HTML sécurisé
    welcome_message = format_html(
        '<h1>Bienvenue {}</h1>', 
        escape(request.user.username) if request.user.is_authenticated else "visiteur"
    )
    
    context = {
        'title': 'Accueil',
        'welcome_message': welcome_message,
        'safe_text': safe_text,
    }
    
    return render(request, 'home.html', context)
'''
    
    print(correction_code)

def quick_check():
    """Vérification rapide de l'erreur"""
    print("🔍 VÉRIFICATION RAPIDE DE L'ERREUR 'html'")
    print("-" * 40)
    
    # Vérifier si nous pouvons accéder au fichier views.py spécifique
    views_paths = [
        'mutuelle_core/views.py',
        'core/views.py',
        'views.py'
    ]
    
    for path in views_paths:
        if os.path.exists(path):
            print(f"\n📄 Analyse de {path}:")
            
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f, 1):
                        if 'html.' in line and i >= 250 and i <= 260:
                            print(f"   ❌ Problème trouvé ligne {i}:")
                            print(f"      {line.strip()}")
                            
                            # Afficher le contexte
                            print(f"   📋 Contexte (lignes {i-5} à {i+5}):")
                            f.seek(0)
                            all_lines = f.readlines()
                            for j in range(max(0, i-6), min(len(all_lines), i+5)):
                                prefix = ">>>" if j+1 == i else "   "
                                print(f"{prefix} {j+1:3}: {all_lines[j].rstrip()}")
                            break
                            
            except Exception as e:
                print(f"   ❌ Erreur: {e}")

if __name__ == "__main__":
    analyze_html_error()
    quick_check()
    generate_fix()