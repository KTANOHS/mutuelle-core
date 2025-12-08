# diagnostic_urls.py
import os
import sys
import django
from django.urls import reverse, NoReverseMatch, get_resolver
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostic_complet():
    print("=" * 80)
    print("DIAGNOSTIC COMPLET DES URLS DJANGO")
    print("=" * 80)
    
    # 1. Vérifier l'URL problématique
    url_problematique = 'communication:liste_notifications'
    print(f"\n1. VÉRIFICATION DE L'URL: {url_problematique}")
    print("-" * 50)
    
    try:
        url = reverse(url_problematique)
        print(f"✅ SUCCÈS: URL trouvée -> {url}")
    except NoReverseMatch as e:
        print(f"❌ ERREUR: {e}")
    
    # 2. Lister toutes les URLs de l'app communication
    print(f"\n2. URLS DE L'APP 'communication'")
    print("-" * 50)
    
    resolver = get_resolver()
    urls_communication = []
    
    for pattern in resolver.url_patterns:
        if hasattr(pattern, 'url_patterns'):  # Namespace ou include
            for sub_pattern in pattern.url_patterns:
                if hasattr(sub_pattern, 'app_name') and sub_pattern.app_name == 'communication':
                    for url_pattern in sub_pattern.url_patterns:
                        urls_communication.append({
                            'pattern': url_pattern.pattern,
                            'name': getattr(url_pattern, 'name', 'SANS_NOM'),
                            'callback': getattr(url_pattern, 'callback', None)
                        })
    
    if not urls_communication:
        print("❌ Aucune URL trouvée pour l'app 'communication'")
        # Essayer une autre méthode
        print("\n🔍 Recherche alternative des URLs...")
        all_urls = []
        for namespace, (url_name, url_pattern) in resolver.reverse_dict.items():
            if isinstance(namespace, str) and 'communication' in namespace:
                all_urls.append((namespace, url_name))
        
        for url in all_urls[:10]:  # Afficher les 10 premières
            print(f"  {url[0]} -> {url[1]}")
    else:
        for url_info in urls_communication:
            statut = "✅" if url_info['name'] else "⚠️"
            print(f"{statut} {url_info['name']:30} -> {url_info['pattern']}")
    
    # 3. Vérifier les templates qui utilisent cette URL
    print(f"\n3. RECHERCHE DANS LES TEMPLATES")
    print("-" * 50)
    
    import glob
    templates_dir = os.path.join(settings.BASE_DIR, 'templates')
    
    fichiers_trouves = []
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'liste_notifications' in content:
                            fichiers_trouves.append(file_path)
                except:
                    pass
    
    if fichiers_trouves:
        print("📁 Fichiers templates contenant 'liste_notifications':")
        for fichier in fichiers_trouves:
            print(f"  📄 {fichier}")
    else:
        print("❌ Aucun template trouvé contenant 'liste_notifications'")
    
    # 4. Vérifier la vue directement
    print(f"\n4. VÉRIFICATION DE LA VUE")
    print("-" * 50)
    
    try:
        from communication import views
        if hasattr(views, 'liste_notifications'):
            print("✅ La vue 'liste_notifications' existe dans communication.views")
        elif hasattr(views, 'NotificationListView'):
            print("✅ La classe 'NotificationListView' existe dans communication.views")
        else:
            print("❌ Aucune vue trouvée pour les notifications")
            
        # Vérifier si c'est une vue fonction ou classe
        if hasattr(views, 'NotificationListView'):
            view_class = views.NotificationListView
            print(f"   📋 Type: Classe (NotificationListView)")
            print(f"   🔗 Héritage: {view_class.__bases__}")
    except ImportError as e:
        print(f"❌ Impossible d'importer communication.views: {e}")
    
    # 5. Vérifier la configuration des URLs principales
    print(f"\n5. CONFIGURATION DES URLS PRINCIPALES")
    print("-" * 50)
    
    try:
        from django.conf import settings
        root_urlconf = settings.ROOT_URLCONF
        print(f"📋 ROOT_URLCONF: {root_urlconf}")
        
        # Importer le module d'URLs racine
        root_urls = __import__(root_urlconf, fromlist=['urlpatterns'])
        url_patterns = getattr(root_urls, 'urlpatterns', [])
        
        print("🔗 URLs incluses dans la racine:")
        for pattern in url_patterns:
            if hasattr(pattern, 'url_patterns'):
                print(f"  📁 {pattern.pattern} -> {getattr(pattern, 'app_name', 'SANS_APP_NAME')}")
            else:
                print(f"  📄 {pattern.pattern} -> {getattr(pattern, 'name', 'SANS_NOM')}")
                
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

def test_url_specifique():
    """Test spécifique pour l'URL liste_notifications"""
    print(f"\n{'='*60}")
    print("TEST SPÉCIFIQUE: communication:liste_notifications")
    print('='*60)
    
    # Test avec différentes variantes
    tests = [
        'communication:liste_notifications',
        'liste_notifications',
        'communication:notification_list',
        'notification_list',
    ]
    
    for test_url in tests:
        try:
            result = reverse(test_url)
            print(f"✅ {test_url:40} -> {result}")
        except NoReverseMatch:
            print(f"❌ {test_url:40} -> NON TROUVÉE")

def verifier_vue_notification():
    """Vérifier en détail la vue notification"""
    print(f"\n{'='*60}")
    print("VÉRIFICATION DÉTAILLÉE DE LA VUE NOTIFICATION")
    print('='*60)
    
    try:
        from communication.views import NotificationListView, liste_notifications
        
        print("✅ Vues importées avec succès:")
        if 'NotificationListView' in locals():
            print("   📋 NotificationListView disponible")
        if 'liste_notifications' in locals():
            print("   📋 liste_notifications (fonction) disponible")
            
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        
        # Essayer d'importer manuellement
        try:
            import importlib
            views_module = importlib.import_module('communication.views')
            
            if hasattr(views_module, 'NotificationListView'):
                print("✅ NotificationListView trouvée via importlib")
            if hasattr(views_module, 'liste_notifications'):
                print("✅ liste_notifications trouvée via importlib")
                
            # Lister toutes les vues disponibles
            print("\n📋 Vues disponibles dans communication.views:")
            for attr_name in dir(views_module):
                if not attr_name.startswith('_'):
                    attr = getattr(views_module, attr_name)
                    if callable(attr) or hasattr(attr, 'as_view'):
                        print(f"   🔹 {attr_name}")
                        
        except Exception as e2:
            print(f"❌ Erreur lors de l'import manuel: {e2}")

if __name__ == "__main__":
    print("🚀 LANCEMENT DU DIAGNOSTIC DJANGO URLS")
    print("Base Directory:", settings.BASE_DIR)
    
    diagnostic_complet()
    test_url_specifique() 
    verifier_vue_notification()
    
    print(f"\n{'='*80}")
    print("DIAGNOSTIC TERMINÉ")
    print("=" * 80)