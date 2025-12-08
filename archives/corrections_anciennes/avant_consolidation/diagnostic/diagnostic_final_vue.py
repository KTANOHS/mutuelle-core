# diagnostic_final_vue.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostic_final_vue():
    """Diagnostic final de la vue messagerie originale"""
    
    print("🔍 DIAGNOSTIC FINAL VUE MESSAGERIE ORIGINALE")
    print("=" * 60)
    
    # 1. Vérifier le type de réponse de la vue
    from communication.views import messagerie
    from django.test import RequestFactory
    from django.contrib.auth.models import User
    
    try:
        pharmacien = User.objects.get(username='test_pharmacien')
        factory = RequestFactory()
        request = factory.get('/communication/')
        request.user = pharmacien
        
        print("1. 🧪 TEST DU TYPE DE RÉPONSE:")
        response = messagerie(request)
        
        print(f"   - Type de réponse: {type(response)}")
        print(f"   - Statut: {response.status_code}")
        print(f"   - Content-Type: {response.get('Content-Type', 'Non défini')}")
        
        # Vérifier si c'est un TemplateResponse
        from django.template.response import TemplateResponse
        if isinstance(response, TemplateResponse):
            print("   ✅ C'est un TemplateResponse")
            print(f"   - Template: {response.template_name}")
            if hasattr(response, 'context_data'):
                print(f"   - Contexte: {len(response.context_data)} éléments")
            else:
                print("   ❌ Pas de context_data")
        else:
            print("   ❌ Ce n'est pas un TemplateResponse")
            print(f"   - C'est un: {response.__class__.__name__}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
    
    # 2. Vérifier les logs Django en temps réel
    print(f"\n2. 📋 CONSEILS POUR LES LOGS:")
    print("   - Regardez la console où tourne 'python manage.py runserver'")
    print("   - Vous devriez voir les prints de debug de la vue messagerie")
    print("   - Cherchez '🔍 VUE MESSAGERIE' dans les logs")

if __name__ == "__main__":
    diagnostic_final_vue()