# verifier_corrections.py - VERSION CORRIGÉE
import os
import sys
import django

# Configuration Django obligatoire
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    django.setup()
    
    from django.contrib.auth.models import User, Group
    from django.test import RequestFactory
    import mutuelle_core.views as views

    def tester_fonctions():
        """Test des fonctions corrigées"""
        print("🧪 TEST DES FONCTIONS CORRIGÉES")
        print("=" * 50)
        
        # Créer une factory pour les requêtes
        factory = RequestFactory()
        
        print("1. Test get_user_primary_group:")
        try:
            # Créer un utilisateur test
            user = User(username='testuser')
            resultat = views.get_user_primary_group(user)
            print(f"   ✅ Résultat: {resultat}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
        
        print("2. Test get_user_redirect_url:")
        try:
            resultat = views.get_user_redirect_url(user)
            print(f"   ✅ Résultat: {resultat}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
        
        print("3. Vérification des vues existantes:")
        vues_a_verifier = [
            'dashboard', 'redirect_to_user_dashboard',
            'assureur_dashboard', 'medecin_dashboard', 
            'pharmacien_dashboard', 'membre_dashboard',
            'generic_dashboard', 'home'
        ]
        
        for vue_name in vues_a_verifier:
            if hasattr(views, vue_name):
                print(f"   ✅ {vue_name} existe")
            else:
                print(f"   ❌ {vue_name} manquante")
        
        print("4. Test de la vue home (sans authentification):")
        try:
            request = factory.get('/')
            response = views.home(request)
            print(f"   ✅ Vue home fonctionne - Statut: {getattr(response, 'status_code', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Erreur vue home: {e}")

    if __name__ == '__main__':
        tester_fonctions()

except Exception as e:
    print(f"❌ ERREUR DE CONFIGURATION DJANGO: {e}")
    print("💡 Assurez-vous que:")
    print("   - Vous êtes dans le dossier du projet")
    print("   - Le fichier settings.py existe")
    print("   - L'environnement virtuel est activé")