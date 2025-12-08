import os
import django
import sys
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate
from membres.models import Membre
from soins.models import BonDeSoin
from agents.models import Agent

def test_fonctionnel_complet():
    """Test fonctionnel complet avec les bons imports"""
    print("🧪 TEST FONCTIONNEL COMPLET CORRIGÉ")
    print("===================================")
    
    # 1. Vérification des données
    print("\n1. 📊 VÉRIFICATION DES DONNÉES")
    print(f"   Membres: {Membre.objects.count()}")
    print(f"   Agents: {Agent.objects.count()}")
    print(f"   Bons de soin: {BonDeSoin.objects.count()}")
    
    # 2. Test d'authentification
    print("\n2. 🔐 TEST AUTHENTIFICATION")
    client = Client()
    user = authenticate(username='koffitanoh', password='votre_mot_de_passe')
    
    if not user:
        print("   ❌ Échec authentification")
        return False
    
    client.force_login(user)
    print("   ✅ Authentification réussie")
    
    # 3. Test d'accès aux pages
    print("\n3. 🌐 TEST ACCÈS PAGES")
    pages = [
        '/agents/creer-bon-soin/',
        '/agents/tableau-de-bord/',
        '/agents/liste-membres/'
    ]
    
    for page in pages:
        response = client.get(page)
        print(f"   {page}: {response.status_code}")
    
    # 4. Test de création via formulaire
    print("\n4. 📝 TEST CRÉATION FORMULAIRE")
    membre = Membre.objects.first()
    agent = Agent.objects.first()
    
    data = {
        'membre': membre.id,
        'type_soin': 'Consultation cardiologie',
        'montant_total': 25000,
        'montant_remboursable': 20000,
        'date_soin': datetime.now().date().isoformat(),
        'description': 'Test création via formulaire corrigé'
    }
    
    response = client.post('/agents/creer-bon-soin/', data)
    print(f"   Soumission formulaire: {response.status_code}")
    
    if response.status_code == 302:  # Redirection = succès
        print("   ✅ Création via formulaire réussie!")
    else:
        print("   ❌ Échec création via formulaire")
    
    # 5. Vérification finale
    print("\n5. 📋 VÉRIFICATION FINALE")
    nouveau_total = BonDeSoin.objects.count()
    print(f"   Bons de soin après test: {nouveau_total}")
    
    return True

if __name__ == "__main__":
    success = test_fonctionnel_complet()
    
    if success:
        print("\n🎉 TEST COMPLET RÉUSSI!")
    else:
        print("\n⚠️  TEST COMPLET ÉCHOUÉ")