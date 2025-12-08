# test_reel_avec_votre_compte.py
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre

def test_reel_avec_votre_compte():
    """Test pour vérifier que vous pouvez créer des membres avec votre compte réel"""
    print("🎯 TEST RÉEL - CRÉATION AVEC VOTRE COMPTE")
    print("=" * 50)
    
    # Vérifier l'état actuel
    total_avant = Membre.objects.count()
    print(f"📊 Membres en base: {total_avant}")
    
    print("\n💡 INSTRUCTIONS:")
    print("1. Allez sur: http://127.0.0.1:8000/agents/creer-membre/")
    print("2. Connectez-vous avec votre compte agent")
    print("3. Créez un nouveau membre avec ces données:")
    print("   - Nom: TestReel")
    print("   - Prénom: VotrePrenom")
    print("   - Téléphone: 0100000000")
    print("   - Email: test.reel@example.com")
    print("4. Revenez ici et appuyez sur Entrée...")
    
    input("\n⏳ Appuyez sur Entrée après avoir créé le membre...")
    
    # Vérifier le résultat
    total_apres = Membre.objects.count()
    print(f"\n📊 Résultat:")
    print(f"   Membres avant: {total_avant}")
    print(f"   Membres après: {total_apres}")
    
    if total_apres > total_avant:
        print("🎉 SUCCÈS ! Le membre a été créé via l'interface web")
        
        # Trouver le nouveau membre
        nouveau_membre = Membre.objects.filter(nom="TestReel").first()
        if nouveau_membre:
            print(f"📋 Détails du membre créé:")
            print(f"   - ID: {nouveau_membre.id}")
            print(f"   - Nom: {nouveau_membre.prenom} {nouveau_membre.nom}")
            print(f"   - Numéro: {getattr(nouveau_membre, 'numero_unique', 'N/A')}")
            print(f"   - Téléphone: {nouveau_membre.telephone}")
        else:
            print("⚠️  Membre créé mais non trouvé par recherche")
    else:
        print("❌ Aucun nouveau membre créé")
        print("💡 Vérifiez:")
        print("   - Que vous êtes bien connecté en tant qu'agent")
        print("   - Que le formulaire a été correctement soumis")
        print("   - Les messages d'erreur éventuels")
    
    print("=" * 50)

if __name__ == "__main__":
    test_reel_avec_votre_compte()