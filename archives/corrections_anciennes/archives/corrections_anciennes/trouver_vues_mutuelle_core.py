# trouver_vues_mutuelle_core.py
import os
import re

def analyser_mutuelle_core_urls():
    """Analyse spécifique de mutuelle_core/urls.py"""
    print("🔍 ANALYSE SPÉCIFIQUE DE mutuelle_core/urls.py")
    print("=" * 50)
    
    fichier_urls = 'mutuelle_core/urls.py'
    
    if not os.path.exists(fichier_urls):
        print("❌ Fichier mutuelle_core/urls.py non trouvé")
        return
    
    with open(fichier_urls, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # Pattern pour trouver les vues dans les URLs
    pattern = r"path\([^)]+,\s*views\.([a-zA-Z_][a-zA-Z0-9_]*)\s*[,\)]"
    vues_appelees = re.findall(pattern, contenu)
    
    print("Vues référencées dans mutuelle_core/urls.py:")
    for vue in sorted(set(vues_appelees)):
        print(f"  - {vue}")
    
    # Vérifier si ces vues existent dans mutuelle_core/views.py
    fichier_views = 'mutuelle_core/views.py'
    
    if not os.path.exists(fichier_views):
        print("❌ Fichier mutuelle_core/views.py non trouvé")
        return
    
    with open(fichier_views, 'r', encoding='utf-8') as f:
        contenu_views = f.read()
    
    print("\n📋 VUES MANQUANTES:")
    vues_manquantes = []
    for vue in sorted(set(vues_appelees)):
        if f"def {vue}(" not in contenu_views:
            vues_manquantes.append(vue)
            print(f"  ❌ {vue} - MANQUANTE")
        else:
            print(f"  ✅ {vue} - EXISTE")
    
    return vues_manquantes

def generer_code_vues_manquantes(vues_manquantes):
    """Génère le code pour les vues manquantes"""
    if not vues_manquantes:
        print("\n🎉 AUCUNE VUE MANQUANTE DANS mutuelle_core/views.py!")
        return
    
    print(f"\n🔧 GÉNÉRATION DU CODE POUR {len(vues_manquantes)} VUES MANQUANTES:")
    print("=" * 50)
    
    code_vues = "\n# ========================\n"
    code_vues += "# VUES MANQUANTES - À AJOUTER\n"
    code_vues += "# ========================\n\n"
    
    for vue in vues_manquantes:
        code_vue = f"""@login_required
def {vue}(request):
    \"\"\"Vue {vue} - À IMPLÉMENTER\"\"\"
    from django.contrib import messages
    context = get_dashboard_context(request.user)
    messages.info(request, "Fonctionnalité {vue} en cours de développement")
    return render(request, 'membres/{vue}.html', context)

"""
        code_vues += code_vue
        print(f"✅ Code généré pour: {vue}")
    
    # Afficher le code à copier-coller
    print("\n📋 COPIEZ-COLLEZ CE CODE DANS mutuelle_core/views.py:")
    print("=" * 50)
    print(code_vues)
    
    # Optionnel: écrire dans un fichier
    with open('vues_manquantes_mutuelle_core.py', 'w', encoding='utf-8') as f:
        f.write(code_vues)
    print("💡 Code également sauvegardé dans 'vues_manquantes_mutuelle_core.py'")

if __name__ == '__main__':
    vues_manquantes = analyser_mutuelle_core_urls()
    generer_code_vues_manquantes(vues_manquantes)