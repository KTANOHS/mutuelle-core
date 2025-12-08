# test_final_complet.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

django.setup()

from django.contrib.auth.models import User
from core.utils import est_agent

def test_complet():
    print("🎯 TEST COMPLET APRÈS CORRECTION")
    print("=" * 50)
    
    # Test des utilisateurs principaux
    users_to_test = ['koffitanoh', 'test_agent']
    
    for username in users_to_test:
        try:
            user = User.objects.get(username=username)
            est_agent_result = est_agent(user)
            
            print(f"\n👤 {username}:")
            print(f"   - Superuser: {user.is_superuser}")
            print(f"   - Staff: {user.is_staff}")
            print(f"   - Est agent: {est_agent_result}")
            
            if est_agent_result:
                print("   ✅ PEUT créer des bons de soin")
            else:
                print("   ❌ NE peut PAS créer des bons de soin")
                
        except User.DoesNotExist:
            print(f"❌ Utilisateur {username} non trouvé")
    
    # Recommandation finale
    print("\n" + "=" * 50)
    koffitanoh = User.objects.get(username='koffitanoh')
    if est_agent(koffitanoh):
        print("🎉 TOUT EST FONCTIONNEL! koffitanoh peut créer des bons de soin.")
        print("\n📝 Procédure de test:")
        print("   1. Allez sur: http://localhost:8000/agents/creer-bon-soin/")
        print("   2. Sélectionnez un membre")
        print("   3. Remplissez le formulaire")
        print("   4. Cliquez sur 'Créer le bon de soin'")
    else:
        print("❌ koffitanoh ne peut toujours pas créer de bons de soin.")
        print("\n🔧 Solutions:")
        print("   A. Modifiez core/utils.py pour autoriser les superutilisateurs")
        print("   B. Exécutez: python ajouter_koffitanoh_agent_final.py")

if __name__ == "__main__":
    test_complet()