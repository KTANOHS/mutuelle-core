# diagnostic_vue_message.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostic_vue_message():
    print("=== DIAGNOSTIC VUE MESSAGE ===")
    
    try:
        # Vérifier la vue qui envoie les messages
        from assureur import views as assureur_views
        print("✅ Module assureur.views importé")
        
        # Vérifier si la vue envoyer_message existe
        if hasattr(assureur_views, 'envoyer_message'):
            print("✅ Vue envoyer_message trouvée dans assureur.views")
        else:
            print("❌ Vue envoyer_message NON trouvée dans assureur.views")
            
    except ImportError as e:
        print(f"❌ Erreur import assureur.views: {e}")
    
    # Vérifier les URLs
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        
        print("\n📋 URLs de message trouvées:")
        url_patterns = []
        
        def list_urls(patterns, base=''):
            for pattern in patterns:
                if hasattr(pattern, 'pattern'):
                    if hasattr(pattern, 'url_patterns'):
                        list_urls(pattern.url_patterns, base + str(pattern.pattern))
                    else:
                        url_name = getattr(pattern, 'name', 'Sans nom')
                        if 'message' in str(pattern.pattern).lower() or 'message' in str(url_name).lower():
                            url_patterns.append({
                                'pattern': base + str(pattern.pattern),
                                'name': url_name
                            })
        
        list_urls(resolver.url_patterns)
        
        for url in url_patterns:
            print(f"   - {url['pattern']} (name: {url['name']})")
            
    except Exception as e:
        print(f"❌ Erreur analyse URLs: {e}")

if __name__ == "__main__":
    diagnostic_vue_message()