# verification_finale.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_vues_corrigees():
    """Vérification finale des vues corrigées"""
    print("✅ VÉRIFICATION FINALE DES VUES CORRIGÉES")
    print("=" * 50)
    
    try:
        from mutuelle_core import views
        
        # Vérifier les fonctions principales
        fonctions_requises = [
            'home', 'dashboard', 'redirect_to_user_dashboard',
            'assureur_dashboard', 'medecin_dashboard', 
            'pharmacien_dashboard', 'membre_dashboard',
            'get_user_primary_group', 'get_user_redirect_url'
        ]
        
        print("1. Fonctions principales:")
        for fonction in fonctions_requises:
            if hasattr(views, fonction):
                print(f"   ✅ {fonction} existe")
            else:
                print(f"   ❌ {fonction} MANQUANTE")
        
        # Tester les fonctions
        print("\n2. Test des fonctions utilitaires:")
        from django.contrib.auth.models import User
        user = User(username='test')
        
        try:
            groupe = views.get_user_primary_group(user)
            print(f"   ✅ get_user_primary_group: {groupe}")
        except Exception as e:
            print(f"   ❌ get_user_primary_group: {e}")
            
        try:
            url = views.get_user_redirect_url(user)
            print(f"   ✅ get_user_redirect_url: {url}")
        except Exception as e:
            print(f"   ❌ get_user_redirect_url: {e}")
        
        print("\n3. Vérification des décorateurs:")
        decorateurs = ['assureur_required', 'medecin_required', 'pharmacien_required', 'membre_required']
        for decorateur in decorateurs:
            if hasattr(views, decorateur):
                print(f"   ✅ {decorateur} existe")
            else:
                print(f"   ❌ {decorateur} MANQUANTE")
                
        print("\n🎉 TOUTES LES VÉRIFICATIONS SONT TERMINÉES!")
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")

if __name__ == '__main__':
    verifier_vues_corrigees()