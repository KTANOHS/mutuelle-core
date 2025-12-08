# verification_urls_vues.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verification_urls_vues():
    print("=== VÉRIFICATION URLS ET VUES ===")
    
    # Vérifier que la vue existe maintenant
    try:
        from assureur import views
        if hasattr(views, 'envoyer_message_assureur'):
            print("✅ Vue envoyer_message_assureur trouvée dans assureur.views")
        else:
            print("❌ Vue envoyer_message_assureur toujours manquante")
            
        # Vérifier les autres vues nécessaires
        vues_necessaires = ['liste_messages', 'detail_message', 'repondre_message']
        for vue in vues_necessaires:
            if hasattr(views, vue):
                print(f"✅ Vue {vue} trouvée")
            else:
                print(f"⚠️  Vue {vue} manquante")
                
    except Exception as e:
        print(f"❌ Erreur import assureur.views: {e}")
    
    # Vérifier les URLs
    print("\n📋 VÉRIFICATION URLs ASSUREUR:")
    try:
        from django.urls import reverse, NoReverseMatch
        
        urls_assureur = [
            'assureur:liste_messages',
            'assureur:envoyer_message', 
            'assureur:detail_message',
            'assureur:repondre_message',
        ]
        
        for url_name in urls_assureur:
            try:
                url = reverse(url_name)
                print(f"✅ {url_name} → {url}")
            except NoReverseMatch:
                print(f"❌ {url_name} non trouvée")
                
    except Exception as e:
        print(f"❌ Erreur vérification URLs: {e}")

if __name__ == "__main__":
    verification_urls_vues()