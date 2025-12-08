# diagnostics_medecin.py
import os
import django
from django.urls import get_resolver, reverse, NoReverseMatch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostiquer_medecin_complet():
    """
    Diagnostic complet de l'application medecin
    """
    print("DIAGNOSTIC COMPLET MEDECIN")
    print("=" * 60)
    
    # 1. Analyse de la structure des URLs
    print("\n1. URLS DISPONIBLES DANS MEDECIN")
    print("-" * 40)
    
    resolver = get_resolver()
    all_medecin_urls = []
    
    def extract_all_medecin_urls(url_patterns, prefix='', namespace=''):
        for pattern in url_patterns:
            if hasattr(pattern, 'url_patterns'):
                new_namespace = namespace
                if pattern.namespace:
                    new_namespace = f"{namespace}:{pattern.namespace}" if namespace else pattern.namespace
                extract_all_medecin_urls(pattern.url_patterns, prefix + str(pattern.pattern), new_namespace)
            else:
                if pattern.name and ('medecin' in str(namespace) or 'medecin' in str(pattern.pattern)):
                    url_info = {
                        'pattern': prefix + str(pattern.pattern),
                        'name': pattern.name,
                        'namespace': namespace,
                        'full_name': f"{namespace}:{pattern.name}" if namespace and pattern.name else pattern.name,
                        'view': getattr(pattern, 'callback', None)
                    }
                    all_medecin_urls.append(url_info)
    
    extract_all_medecin_urls(resolver.url_patterns)
    
    # URLs groupées par namespace
    urls_par_namespace = {}
    for url in all_medecin_urls:
        namespace = url['namespace'] or 'racine'
        if namespace not in urls_par_namespace:
            urls_par_namespace[namespace] = []
        urls_par_namespace[namespace].append(url)
    
    for namespace, urls in urls_par_namespace.items():
        print(f"\nNamespace: {namespace}")
        print("-" * 30)
        for url in urls:
            print(f"  {url['full_name']} -> {url['pattern']}")
    
    # 2. Test des URLs essentielles
    print("\n2. TEST DES URLs ESSENTIELLES")
    print("-" * 40)
    
    urls_essentielles = [
        'medecin:dashboard',
        'medecin:login', 
        'medecin:profil',
        'medecin:consultations',
        'medecin:ordonnances',
    ]
    
    for url_name in urls_essentielles:
        try:
            url = reverse(url_name)
            print(f"✓ {url_name:<30} -> {url}")
        except NoReverseMatch as e:
            print(f"✗ {url_name:<30} -> {e}")
    
    # 3. Analyse des fichiers
    print("\n3. ANALYSE DES FICHIERS MEDECIN")
    print("-" * 40)
    
    def analyser_fichier_medecin(chemin):
        if os.path.exists(chemin):
            print(f"\n📁 {chemin}:")
            try:
                with open(chemin, 'r') as f:
                    lignes = f.readlines()
                    # Afficher les lignes importantes
                    for i, ligne in enumerate(lignes[:50], 1):  # Premières 50 lignes
                        if any(mot in ligne for mot in ['urlpatterns', 'path(', 'include(', 'app_name', 'def ', 'class ']):
                            print(f"  {i:3}: {ligne.rstrip()}")
            except Exception as e:
                print(f"  Erreur lecture: {e}")
        else:
            print(f"✗ {chemin} non trouvé")
    
    analyser_fichier_medecin('medecin/urls.py')
    analyser_fichier_medecin('medecin/views.py')
    
    # 4. Vérification des modèles
    print("\n4. VERIFICATION DES MODELES")
    print("-" * 40)
    
    try:
        from medecin import models
        modeles = [attr for attr in dir(models) if not attr.startswith('_')]
        print(f"Modèles trouvés: {', '.join(modeles)}")
    except ImportError as e:
        print(f"✗ Impossible d'importer les modèles: {e}")
    except Exception as e:
        print(f"✗ Erreur avec les modèles: {e}")
    
    # 5. Recommandations
    print("\n5. RECOMMANDATIONS")
    print("-" * 40)
    
    if not any('medecin:' in str(url.get('full_name', '')) for url in all_medecin_urls):
        print("""
PROBLEME: Aucune URL trouvée dans le namespace 'medecin'

SOLUTIONS:
1. Créer le fichier medecin/urls.py avec:
   ```python
   from django.urls import path
   from . import views
   
   app_name = 'medecin'
   
   urlpatterns = [
       path('dashboard/', views.dashboard, name='dashboard'),
       path('login/', views.login_medecin, name='login'),
       path('profil/', views.profil, name='profil'),
       path('consultations/', views.liste_consultations, name='consultations'),
       path('ordonnances/', views.liste_ordonnances, name='ordonnances'),
   ]