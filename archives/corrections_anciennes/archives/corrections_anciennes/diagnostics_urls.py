# diagnostics_urls.py
import os
import sys
import django
from django.urls import get_resolver, reverse, NoReverseMatch
from django.conf import settings

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostiquer_urls():
    """
    Script complet de diagnostic des URLs Django
    """
    print("=" * 80)
    print("DIAGNOSTIC COMPLET DES URLs DJANGO")
    print("=" * 80)
    
    # 1. Vérifier la structure des URLs
    print("\n1. STRUCTURE DES URLs DISPONIBLES")
    print("-" * 40)
    
    resolver = get_resolver()
    all_urls = []
    
    def extract_urls(url_patterns, prefix='', namespace=''):
        for pattern in url_patterns:
            if hasattr(pattern, 'url_patterns'):
                # C'est un include
                new_namespace = namespace
                if pattern.namespace:
                    new_namespace = f"{namespace}:{pattern.namespace}" if namespace else pattern.namespace
                
                extract_urls(
                    pattern.url_patterns,
                    prefix + str(pattern.pattern),
                    new_namespace
                )
            else:
                # C'est un pattern simple
                url_info = {
                    'pattern': prefix + str(pattern.pattern),
                    'name': pattern.name,
                    'namespace': namespace,
                    'full_name': f"{namespace}:{pattern.name}" if namespace and pattern.name else pattern.name
                }
                all_urls.append(url_info)
    
    extract_urls(resolver.url_patterns)
    
    # Afficher toutes les URLs
    for url in all_urls:
        print(f"Pattern: {url['pattern']}")
        print(f"Nom: {url['name']}")
        print(f"Namespace: {url['namespace']}")
        print(f"Nom complet: {url['full_name']}")
        print("-" * 40)
    
    # 2. Vérifier spécifiquement le namespace 'pharmacien'
    print("\n2. URLs DANS LE NAMESPACE 'pharmacien'")
    print("-" * 40)
    
    urls_pharmacien = [url for url in all_urls if 'pharmacien' in url['namespace']]
    
    if urls_pharmacien:
        for url in urls_pharmacien:
            print(f"✓ {url['full_name']} -> {url['pattern']}")
    else:
        print("✗ Aucune URL trouvée dans le namespace 'pharmacien'")
    
    # 3. Tester les URLs spécifiques
    print("\n3. TEST DES URLs SPECIFIQUES")
    print("-" * 40)
    
    urls_a_tester = [
        'pharmacien:gestion_stock',
        'pharmacien:dashboard',
        'pharmacien:rechercher_ordonnances',
        'pharmacien:historique_validation'
    ]
    
    for url_name in urls_a_tester:
        try:
            url = reverse(url_name)
            print(f"✓ {url_name} -> {url}")
        except NoReverseMatch as e:
            print(f"✗ {url_name} -> ERREUR: {e}")
    
    # 4. Vérifier la structure des fichiers
    print("\n4. VERIFICATION DE LA STRUCTURE DES FICHIERS")
    print("-" * 40)
    
    fichiers_importants = [
        'votre_projet/urls.py',
        'pharmacien/urls.py',
        'pharmacien/views.py',
        'templates/pharmacien/dashboard.html'
    ]
    
    for fichier in fichiers_importants:
        if os.path.exists(fichier):
            print(f"✓ {fichier} existe")
        else:
            print(f"✗ {fichier} n'existe pas")
    
    # 5. Vérifier le contenu des fichiers URLs
    print("\n5. ANALYSE DES FICHIERS URLs")
    print("-" * 40)
    
    def analyser_fichier_urls(chemin_fichier):
        if os.path.exists(chemin_fichier):
            print(f"\nContenu de {chemin_fichier}:")
            print("-" * 20)
            with open(chemin_fichier, 'r') as f:
                lignes = f.readlines()
                for i, ligne in enumerate(lignes, 1):
                    if 'urlpatterns' in ligne or 'path(' in ligne or 'include(' in ligne or 'app_name' in ligne:
                        print(f"{i:3}: {ligne.rstrip()}")
        else:
            print(f"✗ {chemin_fichier} non trouvé")
    
    analyser_fichier_urls('votre_projet/urls.py')
    analyser_fichier_urls('pharmacien/urls.py')
    
    # 6. Suggestions de correctifs
    print("\n6. SUGGESTIONS DE CORRECTIFS")
    print("-" * 40)
    
    if not any('pharmacien:gestion_stock' in url['full_name'] for url in all_urls):
        print("\nPROBLEME: 'pharmacien:gestion_stock' non trouvé")
        print("\nSOLUTIONS:")
        print("1. Ajouter dans pharmacien/urls.py:")
        print("""
   from django.urls import path
   from . import views
   
   app_name = 'pharmacien'
   
   urlpatterns = [
       path('dashboard/', views.dashboard_pharmacien, name='dashboard'),
       path('gestion-stock/', views.gestion_stock, name='gestion_stock'),  # AJOUTER CETTE LIGNE
       path('rechercher-ordonnances/', views.rechercher_ordonnances, name='rechercher_ordonnances'),
       path('historique-validation/', views.historique_validation, name='historique_validation'),
   ]
        """)
        
        print("\n2. Vérifier que la vue existe dans pharmacien/views.py:")
        print("""
   def gestion_stock(request):
       # Votre logique ici
       return render(request, 'pharmacien/gestion_stock.html')
        """)
    
    print("\n" + "=" * 80)
    print("DIAGNOSTIC TERMINÉ")
    print("=" * 80)

if __name__ == "__main__":
    diagnostiquer_urls()