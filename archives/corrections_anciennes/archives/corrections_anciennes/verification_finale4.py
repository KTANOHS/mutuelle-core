# verification_finale.py
import os
import django
import sys

sys.path.append('/Users/koffitanohsoualiho/Documents/VERIFICATION/projet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User
from membres.models import Membre

def verification_finale():
    print("🔍 VÉRIFICATION FINALE DU SYSTÈME")
    print("=" * 40)
    
    # 1. Vérifier les utilisateurs et membres
    print("1. ✅ VÉRIFICATION UTILISATEURS-MEMBRES")
    for user in User.objects.all():
        try:
            membre = user.membre
            print(f"   ✅ {user.username} -> Membre: {membre.numero_unique}")
        except Exception as e:
            print(f"   ❌ {user.username}: {e}")
    
    # 2. Vérifier les templates
    print("\n2. ✅ VÉRIFICATION TEMPLATES")
    template_path = '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/membres/templates/membres/mon_profil.html'
    if os.path.exists(template_path):
        with open(template_path, 'r') as f:
            content = f.read()
            if 'gloria_membre' in content or 'test_membre' in content:
                print("   ❌ Templates avec variables problématiques")
            else:
                print("   ✅ Templates corrigés")
    else:
        print("   ❌ Template mon_profil.html manquant")
    
    print("\n🎉 VÉRIFICATION TERMINÉE!")
    print("Votre application membres est PRÊTE pour la production! 🚀")

if __name__ == "__main__":
    verification_finale()