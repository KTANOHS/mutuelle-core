# test_manuel_creation.py
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre

def test_manuel_rapide():
    """Test manuel rapide de la création de membre"""
    print("🎯 TEST MANUEL RAPIDE - CRÉATION MEMBRE")
    print("=" * 50)
    
    # 1. Vérifier l'état actuel
    total_avant = Membre.objects.count()
    print(f"1. Membres en base avant test: {total_avant}")
    
    # 2. Créer un membre de test manuellement
    try:
        nouveau_membre = Membre.objects.create(
            nom="TEST_MANUEL",
            prenom="Diagnostic",
            telephone="0100000000",
            email="test.manuel@example.com",
            numero_unique="MEMTEST123",
            statut="actif"
        )
        print("2. ✅ Membre de test créé manuellement")
        print(f"   ID: {nouveau_membre.id}")
        print(f"   Numéro: {nouveau_membre.numero_unique}")
        
        # 3. Vérifier la persistance
        total_apres = Membre.objects.count()
        print(f"3. Membres en base après création: {total_apres}")
        
        if total_apres > total_avant:
            print("   ✅ Données persistées en base")
        else:
            print("   ❌ Données non persistées")
            
        # 4. Nettoyer (optionnel)
        nouveau_membre.delete()
        print("4. ✅ Membre de test supprimé (nettoyage)")
        
    except Exception as e:
        print(f"❌ Erreur création manuelle: {e}")
    
    print("=" * 50)
    print("🎯 TEST MANUEL TERMINÉ")

if __name__ == "__main__":
    test_manuel_rapide()