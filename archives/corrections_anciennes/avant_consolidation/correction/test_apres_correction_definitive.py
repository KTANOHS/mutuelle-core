import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate
import json

def test_apres_correction():
    """Test après correction définitive"""
    print("🧪 TEST APRÈS CORRECTION DÉFINITIVE")
    print("===================================")
    
    client = Client()
    user = authenticate(username='agent_operateur', password='agent123')
    
    if not user:
        print("❌ Authentification échouée")
        return False
    
    client.force_login(user)
    print("✅ Authentification réussie")
    
    # Test avec le bon 17
    print(f"\n🔍 Test API pour le bon #17")
    response = client.get(f'/api/agents/bons/17/details/')
    print(f"📡 Statut: {response.status_code}")
    
    if response.status_code == 200:
        data = json.loads(response.content)
        print(f"✅ API fonctionne")
        
        # Vérifier la structure
        print(f"\n📦 STRUCTURE DE LA RÉPONSE (À LA RACINE):")
        
        # Afficher tous les champs à la racine
        for key, value in data.items():
            print(f"   {key}: {value}")
        
        # Vérifier les champs critiques sont maintenant à la racine
        champs_critiques = ['code', 'membre', 'montant_max', 'statut', 'date_creation', 'motif']
        print(f"\n🎯 CHAMPS CRITIQUES (À LA RACINE):")
        tous_presents = True
        
        for champ in champs_critiques:
            if champ in data:
                valeur = data[champ]
                statut = "✅" if valeur and valeur != 'undefined' else "❌"
                print(f"   {statut} {champ}: {valeur}")
            else:
                print(f"   ❌ {champ}: MANQUANT")
                tous_presents = False
        
        # Vérifier qu'il n'y a plus d'objet 'bon'
        if 'bon' not in data:
            print(f"\n✅ PLUS D'OBJET 'bon' - Les champs sont bien à la racine!")
        else:
            print(f"\n❌ IL Y A ENCORE UN OBJET 'bon' - La correction n'a pas fonctionné")
            tous_presents = False
        
        return tous_presents
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        return False

if __name__ == "__main__":
    success = test_apres_correction()
    
    if success:
        print("\n🎉 CORRECTION RÉUSSIE!")
        print("🌐 Les détails des bons devraient maintenant s'afficher correctement")
        print("\n💡 Testez manuellement: http://127.0.0.1:8000/agents/historique-bons/")
    else:
        print("\n⚠️  LA CORRECTION N'A PAS FONCTIONNÉ")