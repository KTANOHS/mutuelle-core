# clear_cache.py
import os
import django
import sys
import importlib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def clear_all_caches():
    """
    Nettoie tous les caches Django
    """
    print("NETTOYAGE DES CACHES DJANGO")
    print("=" * 40)
    
    try:
        # Vider le cache des URLs
        from django.urls import clear_url_caches
        clear_url_caches()
        print("✓ Cache des URLs vidé")
        
        # Vider le cache du template loader
        from django.template.loader import template_source_loaders
        if template_source_loaders:
            for loader in template_source_loaders:
                if hasattr(loader, 'reset'):
                    loader.reset()
        print("✓ Cache des templates vidé")
        
        # Recharger les modules d'URLs
        urls_modules = [m for m in sys.modules.keys() if 'urls' in m]
        for module in urls_modules:
            importlib.reload(sys.modules[module])
        print(f"✓ {len(urls_modules)} modules d'URLs rechargés")
        
        # Vider le cache mémoire si disponible
        try:
            from django.core.cache import cache
            cache.clear()
            print("✓ Cache mémoire vidé")
        except:
            print("⚠ Cache mémoire non disponible")
        
        print("\n✅ Tous les caches ont été nettoyés!")
        print("🎯 Redémarrez votre serveur Django pour une prise en compte complète")
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {e}")

if __name__ == "__main__":
    clear_all_caches()