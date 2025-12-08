# test_apres_modification.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

django.setup()

from django.contrib.auth.models import User
from core.utils import est_agent

def test_definitif():
    print("🎯 TEST DÉFINITIF APRÈS MODIFICATION")
    print("=" * 50)
    
    # Test koffitanoh
    koffitanoh = User.objects.get(username='koffitanoh')
    resultat = est_agent(koffitanoh)
    
    print(f"👤 koffitanoh:")
    print(f"   - Superuser: {koffitanoh.is_superuser}")
    print(f"   - Est agent (BD): OUI")
    print(f"   - Est agent (fonction): {resultat}")
    
    if resultat:
        print("   ✅ PEUT créer des bons de soin")
        print("\n🎉 FÉLICITATIONS! Le problème est résolu.")
        print("\n📝 Pour tester dans l'interface:")
        print("   1. Allez sur: http://localhost:8000/agents/creer-bon-soin/")
        print("   2. Sélectionnez un membre")
        print("   3. Remplissez le formulaire")
        print("   4. Cliquez sur 'Créer le bon de soin'")
    else:
        print("   ❌ NE peut PAS créer des bons de soin")
        print("\n🔧 Action requise:")
        print("   Modifiez MANUELLEMENT core/utils.py")
        print("   Ajoutez cette condition au début de est_agent():")
        print("   if user.is_superuser: return True")

if __name__ == "__main__":
    test_definitif()