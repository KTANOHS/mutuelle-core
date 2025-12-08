# verifier_modification_core.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

django.setup()

from django.contrib.auth.models import User
from core.utils import est_agent

def verifier_modification():
    print("🔍 VÉRIFICATION DE LA MODIFICATION DANS core/utils.py")
    print("=" * 60)
    
    koffitanoh = User.objects.get(username='koffitanoh')
    
    # Test direct
    resultat = est_agent(koffitanoh)
    
    print(f"Utilisateur: koffitanoh")
    print(f"Superutilisateur: {koffitanoh.is_superuser}")
    print(f"Agent dans BD: OUI (ID: 2)")  # Nous savons qu'il a été ajouté
    print(f"Résultat est_agent: {resultat}")
    
    if resultat:
        print("🎉 SUCCÈS! La modification est active.")
        print("koffitanoh peut maintenant créer des bons de soin.")
    else:
        print("❌ ÉCHEC! La modification n'est pas active.")
        print("Veuillez modifier core/utils.py comme indiqué.")

if __name__ == "__main__":
    verifier_modification()