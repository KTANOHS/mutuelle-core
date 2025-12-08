#!/usr/bin/env python3
"""
Script de correction automatique des templates
Corrige les problèmes identifiés par check_templates_compatibility.py
"""

import os
import re
from pathlib import Path

def fix_base_html():
    """Corrige base.html en ajoutant les blocs manquants"""
    base_path = "templates/base.html"
    
    if not os.path.exists(base_path):
        print("❌ base.html introuvable")
        return False
    
    print("🔧 CORRECTION DE base.html...")
    
    with open(base_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier et ajouter les blocs manquants
    fixes_applied = 0
    
    # Ajouter extra_css avant la fermeture de </head>
    if '{% block extra_css %}' not in content:
        if '</head>' in content:
            content = content.replace('</head>', '{% block extra_css %}{% endblock %}\n</head>')
            fixes_applied += 1
            print("✅ Bloc extra_css ajouté avant </head>")
    
    # Ajouter extra_js avant la fermeture de </body>
    if '{% block extra_js %}' not in content:
        if '</body>' in content:
            content = content.replace('</body>', '{% block extra_js %}{% endblock %}\n</body>')
            fixes_applied += 1
            print("✅ Bloc extra_js ajouté avant </body>")
    
    # Sauvegarder les corrections
    if fixes_applied > 0:
        # Créer une sauvegarde
        backup_path = "templates/base.html.backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(open(base_path, 'r', encoding='utf-8').read())
        print(f"📦 Sauvegarde créée: {backup_path}")
        
        # Écrire le contenu corrigé
        with open(base_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ base.html corrigé avec {fixes_applied} modification(s)")
    else:
        print("⏩ base.html ne nécessite pas de correction")
    
    return fixes_applied > 0

def fix_application_bases():
    """Corrige les bases d'applications pour qu'elles étendent base_app.html"""
    app_bases = [
        "apps/assureur/base_assureur.html",
        "apps/medecin/base_medecin.html",
        "apps/pharmacien/base_pharmacien.html",
        "apps/membres/base_membres.html",
        "apps/paiements/base_paiements.html",
        "apps/soins/base_soins.html",
        "apps/api/base_api.html"
    ]
    
    fixes_applied = 0
    
    for app_base in app_bases:
        app_path = f"templates/{app_base}"
        
        if not os.path.exists(app_path):
            print(f"⚠️  {app_path} introuvable - ignoré")
            continue
        
        print(f"🔧 Correction de {app_base}...")
        
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer l'extension par base_app.html
        old_extends = re.findall(r'{% extends "[^"]*" %}', content)
        
        if old_extends:
            # Remplacer l'extension existante
            for old_extend in old_extends:
                content = content.replace(old_extend, '{% extends "base_app.html" %}')
                print(f"✅ {app_base}: extension remplacée par base_app.html")
        else:
            # Ajouter l'extension au début
            lines = content.split('\n')
            if lines and not lines[0].strip().startswith('{%'):
                # Ajouter l'extension en première ligne
                content = '{% extends "base_app.html" %}\n' + content
                print(f"✅ {app_base}: extension base_app.html ajoutée")
            else:
                # Insérer après les commentaires éventuels
                insert_pos = 0
                for i, line in enumerate(lines):
                    if line.strip() and not line.strip().startswith('{#') and not line.strip().startswith('<!--'):
                        insert_pos = i
                        break
                
                lines.insert(insert_pos, '{% extends "base_app.html" %}')
                content = '\n'.join(lines)
                print(f"✅ {app_base}: extension base_app.html insérée")
        
        # Sauvegarder
        backup_path = f"{app_path}.backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(open(app_path, 'r', encoding='utf-8').read())
        
        with open(app_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        fixes_applied += 1
    
    print(f"✅ {fixes_applied} bases d'applications corrigées")
    return fixes_applied

def fix_home_html():
    """Corrige home.html pour qu'il utilise base_home.html"""
    home_path = "templates/home.html"
    
    if not os.path.exists(home_path):
        print("❌ home.html introuvable")
        return False
    
    print("🔧 CORRECTION DE home.html...")
    
    with open(home_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier l'extension actuelle
    extends_pattern = r'{% extends "[^"]*" %}'
    extends_match = re.search(extends_pattern, content)
    
    if extends_match:
        current_extends = extends_match.group(0)
        if 'base_home.html' not in current_extends:
            # Remplacer par base_home.html
            content = content.replace(current_extends, '{% extends "base_home.html" %}')
            print("✅ home.html: extension remplacée par base_home.html")
        else:
            print("⏩ home.html: extension déjà correcte")
            return True
    else:
        # Ajouter l'extension au début
        lines = content.split('\n')
        if lines and not lines[0].strip().startswith('{%'):
            content = '{% extends "base_home.html" %}\n' + content
            print("✅ home.html: extension base_home.html ajoutée")
        else:
            # Insérer après les commentaires
            insert_pos = 0
            for i, line in enumerate(lines):
                if line.strip() and not line.strip().startswith('{#') and not line.strip().startswith('<!--'):
                    insert_pos = i
                    break
            
            lines.insert(insert_pos, '{% extends "base_home.html" %}')
            content = '\n'.join(lines)
            print("✅ home.html: extension base_home.html insérée")
    
    # Sauvegarder et écrire
    backup_path = "templates/home.html.backup"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(open(home_path, 'r', encoding='utf-8').read())
    
    with open(home_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ home.html corrigé")
    return True

def verify_fixes():
    """Vérifie que les corrections ont été appliquées"""
    print("\n🔍 VÉRIFICATION DES CORRECTIONS")
    print("=" * 40)
    
    # Vérifier base.html
    base_path = "templates/base.html"
    if os.path.exists(base_path):
        with open(base_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = [
            ('extra_css', '{% block extra_css %}' in content),
            ('extra_js', '{% block extra_js %}' in content)
        ]
        
        for check_name, check_result in checks:
            status = "✅" if check_result else "❌"
            print(f"{status} base.html - bloc {check_name}: {'PRÉSENT' if check_result else 'MANQUANT'}")
    
    # Vérifier home.html
    home_path = "templates/home.html"
    if os.path.exists(home_path):
        with open(home_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        uses_base_home = '{% extends "base_home.html" %}' in content
        status = "✅" if uses_base_home else "❌"
        print(f"{status} home.html - utilise base_home.html: {'OUI' if uses_base_home else 'NON'}")
    
    # Vérifier une base d'application
    sample_app = "templates/apps/assureur/base_assureur.html"
    if os.path.exists(sample_app):
        with open(sample_app, 'r', encoding='utf-8') as f:
            content = f.read()
        
        uses_base_app = '{% extends "base_app.html" %}' in content
        status = "✅" if uses_base_app else "❌"
        print(f"{status} base_assureur.html - utilise base_app.html: {'OUI' if uses_base_app else 'NON'}")

def create_quick_fix_script():
    """Crée un script de correction rapide pour référence future"""
    script_content = """#!/usr/bin/env python3
"""
    script_path = "quick_fix_templates.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"✅ Script de correction rapide créé: {script_path}")

def main():
    """Fonction principale"""
    print("🔄 CORRECTION AUTOMATIQUE DES TEMPLATES")
    print("=" * 50)
    
    # Demander confirmation
    response = input("❓ Voulez-vous appliquer les corrections automatiques? (oui/non): ")
    if response.lower() not in ['oui', 'o', 'yes', 'y']:
        print("⏹️  Correction annulée")
        return
    
    print("\n🚀 DÉMARRAGE DES CORRECTIONS...")
    
    # Appliquer les corrections
    fix_base_html()
    print()
    
    fix_application_bases()
    print()
    
    fix_home_html()
    print()
    
    # Vérifier les corrections
    verify_fixes()
    
    print("\n🎉 CORRECTIONS TERMINÉES!")
    print("\n📚 RECOMMANDATIONS FINALES:")
    print("1. Testez votre application pour vérifier que tout fonctionne")
    print("2. Les fichiers originaux ont été sauvegardés avec l'extension .backup")
    print("3. Supprimez les sauvegardes (.backup) une fois que tout est validé")
    print("4. Utilisez base_app.html pour les nouvelles pages d'application")
    print("5. Utilisez base_home.html pour la page d'accueil")

if __name__ == "__main__":
    main()