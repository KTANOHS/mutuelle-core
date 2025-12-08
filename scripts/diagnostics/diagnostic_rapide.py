# diagnostic_rapide.py
import os
import sys

print("🔍 DIAGNOSTIC URGENCE - Erreur 'html' non défini")
print("=" * 50)

# Chemin spécifique
chemin_views = "/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30/mutuelle_core/views.py"

if os.path.exists(chemin_views):
    print(f"✅ Fichier trouvé: {chemin_views}")
    
    with open(chemin_views, 'r', encoding='utf-8') as f:
        lignes = f.readlines()
    
    # Ligne 254
    if len(lignes) >= 254:
        print(f"\n📝 LIGNE 254: {lignes[253].strip()}")
        
        # Solution immédiate
        print("\n💡 CORRECTION IMMÉDIATE:")
        print("Ajoutez cette ligne EN HAUT du fichier:")
        print("from django.utils.html import escape, format_html, mark_safe")
        
        # Si la ligne 254 contient html.escape
        if 'html.escape' in lignes[253]:
            print("\n🔧 Remplacez dans la ligne 254:")
            print(f"   ❌ {lignes[253].strip()}")
            print(f"   ✅ {lignes[253].strip().replace('html.escape', 'escape')}")
    else:
        print(f"❌ Le fichier n'a que {len(lignes)} lignes")
else:
    print(f"❌ Fichier non trouvé: {chemin_views}")
    print("\n🔎 Cherchez le fichier avec:")
    print("find . -name 'views.py' -type f | grep -i core")