# test_permissions.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

django.setup()

from django.contrib.auth.models import User
from core.utils import est_agent

def tester_permissions():
    print("🔐 TEST DES PERMISSIONS")
    print("=" * 50)
    
    # Tester koffitanoh
    try:
        koffitanoh = User.objects.get(username='koffitanoh')
        print(f"👤 koffitanoh:")
        print(f"   - Superuser: {koffitanoh.is_superuser}")
        print(f"   - Staff: {koffitanoh.is_staff}")
        print(f"   - Est agent: {est_agent(koffitanoh)}")
        print()
    except User.DoesNotExist:
        print("❌ koffitanoh non trouvé")
    
    # Tester test_agent
    try:
        test_agent_user = User.objects.get(username='test_agent')
        print(f"👤 test_agent:")
        print(f"   - Superuser: {test_agent_user.is_superuser}")
        print(f"   - Staff: {test_agent_user.is_staff}")
        print(f"   - Est agent: {est_agent(test_agent_user)}")
        print()
    except User.DoesNotExist:
        print("❌ test_agent non trouvé")
    
    # Recommandation
    print("💡 RECOMMANDATION:")
    if est_agent(koffitanoh):
        print("✅ koffitanoh peut créer des bons de soin")
    else:
        print("❌ koffitanoh NE peut PAS créer des bons de soin")
        print("   Exécutez: python ajouter_koffitanoh_agent.py")

if __name__ == "__main__":
    tester_permissions()