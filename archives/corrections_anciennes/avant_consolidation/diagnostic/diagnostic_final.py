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

def diagnostic_final():
    """Diagnostic final pour identifier le problème restant"""
    print("🐛 DIAGNOSTIC FINAL")
    print("==================")
    
    client = Client()
    user = authenticate(username='agent_operateur', password='agent123')
    
    if not user:
        print("❌ Authentification échouée")
        return
    
    client.force_login(user)
    print("✅ Authentification réussie")
    
    # Test de l'API
    print(f"\n🔍 Test API bon #17")
    response = client.get(f'/api/agents/bons/17/details/')
    
    print(f"📡 URL appelée: /api/agents/bons/17/details/")
    print(f"📊 Statut: {response.status_code}")
    print(f"📦 Réponse complète:")
    print(json.dumps(json.loads(response.content), indent=2, ensure_ascii=False))
    
    # Vérifier le JavaScript frontend
    print(f"\n🔍 VÉRIFICATION DU FRONTEND")
    print(f"💡 Le problème pourrait être dans le JavaScript qui parse la réponse")
    print(f"🌐 Ouvrez les outils de développement (F12) et vérifiez:")
    print(f"   - La requête réseau vers /api/agents/bons/17/details/")
    print(f"   - La réponse reçue par le navigateur")
    print(f"   - Les erreurs JavaScript dans la console")

if __name__ == "__main__":
    diagnostic_final()