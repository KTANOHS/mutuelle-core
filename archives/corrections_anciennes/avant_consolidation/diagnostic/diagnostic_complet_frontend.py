import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate
from soins.models import BonDeSoin
import json

def diagnostic_complet():
    """Diagnostic complet du problème frontend"""
    print("🐛 DIAGNOSTIC COMPLET FRONTEND")
    print("==============================")
    
    client = Client()
    user = authenticate(username='agent_operateur', password='agent123')
    
    if not user:
        print("❌ Authentification échouée")
        return
    
    client.force_login(user)
    print("✅ Authentification réussie")
    
    # 1. Test de l'API avec le dernier bon créé (ID: 17)
    bon = BonDeSoin.objects.get(id=17)
    print(f"\n1. 🔍 TEST API POUR LE BON #17")
    
    response = client.get(f'/api/agents/bons/17/details/')
    print(f"   📡 Statut: {response.status_code}")
    
    if response.status_code == 200:
        data = json.loads(response.content)
        print(f"   ✅ API répond correctement")
        
        if data.get('success'):
            bon_data = data['bon']
            print(f"   📦 DONNÉES RÉELLES RENVOYÉES PAR L'API:")
            for key, value in bon_data.items():
                print(f"      {key}: {value}")
        else:
            print(f"   ❌ Erreur API: {data.get('error')}")
    
    # 2. Vérifier la structure exacte attendue par le frontend
    print(f"\n2. 🎯 STRUCTURE ATTENDUE PAR LE FRONTEND")
    print(f"   D'après l'interface, le frontend attend ces champs:")
    champs_attendus = [
        'code', 'membre', 'montant_max', 'statut',
        'date_creation', 'date_expiration', 'temps_restant', 
        'motif', 'type_soin', 'urgence'
    ]
    
    for champ in champs_attendus:
        print(f"      - {champ}")
    
    # 3. Comparaison
    print(f"\n3. 🔄 COMPARAISON STRUCTURE")
    if response.status_code == 200:
        data = json.loads(response.content)
        if data.get('success'):
            bon_data = data['bon']
            
            print(f"   📊 CHAMPS MANQUANTS/DÉCALÉS:")
            for champ in champs_attendus:
                if champ in bon_data:
                    valeur = bon_data[champ]
                    statut = "✅" if valeur and valeur != 'undefined' else "❌ VIDE/UNDEFINED"
                    print(f"      {statut} {champ}: {valeur}")
                else:
                    print(f"      ❌ {champ}: CHAMP MANQUANT")
    
    # 4. Test de la réponse brute
    print(f"\n4. 📡 RÉPONSE BRUTE DE L'API:")
    print(f"   {response.content.decode('utf-8')}")
    
    return True

if __name__ == "__main__":
    diagnostic_complet()