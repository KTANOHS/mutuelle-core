# analyser_pharmacien_complet.py
import os
import re

def analyser_pharmacien_complet():
    """Analyse complète du module pharmacien"""
    print("🔍 ANALYSE COMPLÈTE DU MODULE PHARMACIEN")
    print("=" * 50)
    
    # 1. Analyser pharmacien/urls.py
    fichier_urls = 'pharmacien/urls.py'
    print("1. 📄 ANALYSE DE pharmacien/urls.py:")
    print("-" * 30)
    
    if not os.path.exists(fichier_urls):
        print("   ❌ pharmacien/urls.py non trouvé")
        return
    
    with open(fichier_urls, 'r', encoding='utf-8') as f:
        contenu_urls = f.read()
        print(contenu_urls)
    
    # 2. Analyser pharmacien/views.py
    fichier_views = 'pharmacien/views.py'
    print("\n2. 📄 ANALYSE DE pharmacien/views.py:")
    print("-" * 30)
    
    if not os.path.exists(fichier_views):
        print("   ❌ pharmacien/views.py non trouvé")
        return
    
    with open(fichier_views, 'r', encoding='utf-8') as f:
        contenu_views = f.read()
        
        # Extraire les noms des fonctions
        pattern = r"def ([a-zA-Z_][a-zA-Z0-9_]*)\("
        fonctions = re.findall(pattern, contenu_views)
        
        print("   Fonctions trouvées:")
        for fonction in sorted(fonctions):
            print(f"     - {fonction}")
    
    # 3. Vérifier la cohérence URLs vs Vues
    print("\n3. 🔗 VÉRIFICATION COHÉRENCE URLs ↔ VUES:")
    print("-" * 40)
    
    # URLs attendues depuis les templates
    urls_attendues = [
        'valider_ordonnance',
        'detail_ordonnance', 
        'historique_validation',
        'liste_ordonnances_attente',
        'dashboard_pharmacien'
    ]
    
    for url_attendue in urls_attendues:
        # Vérifier dans URLs
        dans_urls = f"name='{url_attendue}'" in contenu_urls or f'name="{url_attendue}"' in contenu_urls
        # Vérifier dans Views
        dans_views = f"def {url_attendue}(" in contenu_views
        
        statut_url = "✅" if dans_urls else "❌"
        statut_view = "✅" if dans_views else "❌"
        
        print(f"   {url_attendue:25} URL: {statut_url}   Vue: {statut_view}")

if __name__ == '__main__':
    analyser_pharmacien_complet()