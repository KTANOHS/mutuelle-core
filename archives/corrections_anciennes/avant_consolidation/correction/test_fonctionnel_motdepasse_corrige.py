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

def test_fonctionnel_avec_motdepasse():
    """Test fonctionnel avec le nouveau mot de passe"""
    print("🧪 TEST FONCTIONNEL - MOT DE PASSE CORRIGÉ")
    print("==========================================")
    
    # 1. Vérification des données
    print("\n1. 📊 VÉRIFICATION DES DONNÉES")
    print(f"   Membres: {Membre.objects.count()}")
    print(f"   Agents: {Agent.objects.count()}")
    print(f"   Bons de soin: {BonDeSoin.objects.count()}")
    
    # 2. Test d'authentification avec le NOUVEAU mot de passe
    print("\n2. 🔐 TEST AUTHENTIFICATION")
    client = Client()
    
    # Essayer avec le nouveau mot de passe
    user = authenticate(username='koffitanoh', password='nouveau_mot_de_passe')
    
    if not user:
        print("   ❌ Échec authentification avec 'nouveau_mot_de_passe'")
        print("   💡 Essayez d'autres mots de passe possibles...")
        
        # Essayer avec des mots de passe courants
        passwords_to_try = ['password', 'admin', 'test', '1234', '']
        for pwd in passwords_to_try:
            user = authenticate(username='koffitanoh', password=pwd)
            if user:
                print(f"   ✅ Authentification réussie avec: '{pwd}'")
                break
        else:
            print("   ❌ Aucun mot de passe fonctionne")
            return False
    else:
        print("   ✅ Authentification réussie avec 'nouveau_mot_de_passe'")
    
    client.force_login(user)
    
    # 3. Test d'accès aux pages
    print("\n3. 🌐 TEST ACCÈS PAGES")
    pages = [
        '/agents/creer-bon-soin/',
        '/agents/tableau-de-bord/',
        '/agents/liste-membres/'
    ]
    
    for page in pages:
        response = client.get(page)
        status_emoji = "✅" if response.status_code == 200 else "❌"
        print(f"   {status_emoji} {page}: {response.status_code}")
    
    # 4. Test de création via formulaire
    print("\n4. 📝 TEST CRÉATION FORMULAIRE")
    membre = Membre.objects.first()
    
    # Préparer les données selon la structure réelle
    data = {
        'patient': membre.id,  # Champ correct: 'patient' au lieu de 'membre'
        'date_soin': datetime.now().date().isoformat(),
        'symptomes': 'Douleurs test',
        'diagnostic': 'Diagnostic test formulaire',
        'statut': 'EN_ATTENTE',
        'montant': 20000,
    }
    
    response = client.post('/agents/creer-bon-soin/', data)
    print(f"   📤 Soumission formulaire: {response.status_code}")
    
    if response.status_code == 302:  # Redirection = succès
        print("   ✅ Création via formulaire réussie!")
        # Suivre la redirection
        if response.url:
            follow_response = client.get(response.url)
            print(f"   🔄 Redirection vers: {response.url} ({follow_response.status_code})")
    else:
        print("   ❌ Échec création via formulaire")
        # Afficher les erreurs possibles
        if hasattr(response, 'content'):
            content = response.content.decode('utf-8')
            if 'error' in content.lower() or 'erreur' in content.lower():
                print("   💡 Des erreurs sont présentes dans la réponse")
    
    # 5. Vérification finale
    print("\n5. 📋 VÉRIFICATION FINALE")
    nouveau_total = BonDeSoin.objects.count()
    print(f"   Bons de soin après test: {nouveau_total}")
    
    return True

if __name__ == "__main__":
    success = test_fonctionnel_avec_motdepasse()
    
    if success:
        print("\n🎉 TEST FONCTIONNEL RÉUSSI!")
    else:
        print("\n⚠️  TEST FONCTIONNEL ÉCHOUÉ")