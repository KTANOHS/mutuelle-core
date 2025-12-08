# trouver_vues_manquantes.py
import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyser_urls_pour_vues_manquantes():
    """Analyse tous les fichiers urls.py pour trouver les vues manquantes"""
    print("🔍 RECHERCHE DES VUES MANQUANTES")
    print("=" * 50)
    
    # Liste des fichiers urls.py à analyser
    fichiers_urls = [
        'mutuelle_core/urls.py',
        'medecin/urls.py',
        'pharmacien/urls.py',
        'assureur/urls.py',
        'soins/urls.py',
        'membres/urls.py'
    ]
    
    vues_manquantes = []
    
    for fichier_urls in fichiers_urls:
        if not os.path.exists(fichier_urls):
            continue
            
        print(f"\n📄 Analyse de {fichier_urls}:")
        
        with open(fichier_urls, 'r', encoding='utf-8') as f:
            contenu = f.read()
            
            # Trouver tous les appels de vues dans les URLs
            pattern = r"path\([^)]+,\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*[,\)]"
            matches = re.findall(pattern, contenu)
            
            for vue_name in matches:
                if vue_name not in ['views', 'include', 'admin'] and not vue_name.startswith('auth_'):
                    # Vérifier si la vue existe dans le module correspondant
                    module_name = fichier_urls.split('/')[0].replace('.py', '')
                    
                    try:
                        if module_name == 'mutuelle_core':
                            from mutuelle_core import views as module_views
                        elif module_name == 'medecin':
                            from medecin import views as module_views
                        elif module_name == 'pharmacien':
                            from pharmacien import views as module_views
                        elif module_name == 'assureur':
                            from assureur import views as module_views
                        elif module_name == 'soins':
                            from soins import views as module_views
                        elif module_name == 'membres':
                            from membres import views as module_views
                        else:
                            continue
                        
                        if not hasattr(module_views, vue_name):
                            vues_manquantes.append({
                                'fichier': fichier_urls,
                                'vue': vue_name,
                                'module': module_name
                            })
                            print(f"   ❌ {vue_name} MANQUANTE dans {module_name}.views")
                        else:
                            print(f"   ✅ {vue_name} existe")
                            
                    except ImportError as e:
                        print(f"   ⚠️  Impossible d'importer {module_name}.views: {e}")
    
    return vues_manquantes

def generer_vues_manquantes(vues_manquantes):
    """Génère le code pour les vues manquantes"""
    if not vues_manquantes:
        print("\n🎉 AUCUNE VUE MANQUANTE TROUVÉE!")
        return
    
    print(f"\n🔧 GÉNÉRATION DES {len(vues_manquantes)} VUES MANQUANTES")
    print("=" * 50)
    
    code_vues = """
# ========================
# VUES MANQUANTES - À AJOUTER
# ========================
"""
    
    for vue_info in vues_manquantes:
        vue_name = vue_info['vue']
        module_name = vue_info['module']
        
        code_vue = f"""
@login_required
def {vue_name}(request):
    \"\"\"Vue {vue_name} - À IMPLÉMENTER\"\"\"
    context = get_dashboard_context(request.user)
    messages.info(request, "Fonctionnalité {vue_name} en cours de développement")
    return render(request, '{module_name}/{vue_name}.html', context)
"""
        code_vues += code_vue
        print(f"✅ Code généré pour {vue_name}")
    
    # Écrire dans un fichier séparé
    with open('vues_manquantes.py', 'w', encoding='utf-8') as f:
        f.write(code_vues)
    
    print(f"\n📁 Code des vues manquantes sauvegardé dans 'vues_manquantes.py'")
    print("💡 Copiez-collez ces fonctions dans les fichiers views.py appropriés")

if __name__ == '__main__':
    vues_manquantes = analyser_urls_pour_vues_manquantes()
    generer_vues_manquantes(vues_manquantes)