# diagnostic_simple.py
import os
import sys

print("🔍 DIAGNOSTIC SIMPLIFIÉ")
print("=" * 40)

# Vérifier le fichier views.py spécifique
target_file = "mutuelle_core/views.py"

if os.path.exists(target_file):
    print(f"✅ Fichier trouvé: {target_file}")
    
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        print(f"📊 Nombre de lignes: {len(lines)}")
        
        # Afficher la zone de l'erreur
        if len(lines) >= 254:
            print(f"\n📝 Ligne 254 (erreur):")
            print(f"   {lines[253].strip()}")
            
            print(f"\n📋 Contexte (lignes 245-265):")
            for i in range(244, 264):
                if i < len(lines):
                    prefix = ">>>" if i == 253 else "   "
                    print(f"{prefix} {i+1:3}: {lines[i].rstrip()}")
        
        # Rechercher 'html' dans le fichier
        html_lines = []
        for i, line in enumerate(lines):
            if 'html' in line.lower() and 'html.' in line:
                html_lines.append((i+1, line.strip()))
        
        if html_lines:
            print(f"\n⚠️  Utilisations de 'html' détectées:")
            for line_num, line_content in html_lines:
                print(f"   Ligne {line_num}: {line_content}")
        
        # Vérifier les imports
        imports = [line for line in lines if line.strip().startswith(('import', 'from'))]
        has_html_import = any('html' in imp.lower() for imp in imports)
        
        print(f"\n📦 Import 'html' trouvé: {'✅ Oui' if has_html_import else '❌ Non'}")
        
        if not has_html_import and html_lines:
            print(f"\n💡 SOLUTION:")
            print("   1. Ajouter en haut du fichier:")
            print("      from django.utils.html import escape, format_html, mark_safe")
            print("\n   2. Remplacer dans le code:")
            print("      ❌ html.escape() → ✅ escape()")
            print("      ❌ html.format() → ✅ format_html()")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
else:
    print(f"❌ Fichier non trouvé: {target_file}")
    print("   Chercher dans les dossiers...")
    
    # Chercher le fichier
    for root, dirs, files in os.walk('.'):
        if 'views.py' in files and 'mutuelle_core' in root:
            print(f"   Trouvé: {os.path.join(root, 'views.py')}")
            break