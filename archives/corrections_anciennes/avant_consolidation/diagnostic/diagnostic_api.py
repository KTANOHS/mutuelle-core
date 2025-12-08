import requests
import json

BASE_URL = "http://127.0.0.1:8000"
CONVERSATION_ID = 5

def test_endpoint(method, endpoint, data=None):
    """Test un endpoint de l'API"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            return {"error": f"Méthode {method} non supportée"}
        
        return {
            "status_code": response.status_code,
            "success": response.status_code in [200, 201],
            "data": response.json() if response.content else None,
            "headers": dict(response.headers)
        }
        
    except requests.exceptions.ConnectionError:
        return {"error": "Impossible de se connecter au serveur"}
    except requests.exceptions.Timeout:
        return {"error": "Timeout - Le serveur ne répond pas"}
    except json.JSONDecodeError:
        return {"error": "Réponse JSON invalide"}
    except Exception as e:
        return {"error": f"Erreur inattendue: {str(e)}"}

def run_diagnostics():
    """Exécute tous les tests de diagnostic"""
    print("=" * 60)
    print(f"DIAGNOSTIC API - Conversation {CONVERSATION_ID}")
    print("=" * 60)
    
    # 1. Test de base - Le serveur répond-il?
    print("\n1. Test de connexion au serveur...")
    ping_test = test_endpoint("GET", "/")
    if ping_test.get("error"):
        print(f"   ❌ ÉCHEC: {ping_test['error']}")
        return
    else:
        print(f"   ✅ Succès - Code: {ping_test['status_code']}")
    
    # 2. Récupérer les détails de la conversation
    print(f"\n2. Récupération de la conversation {CONVERSATION_ID}...")
    conv_test = test_endpoint("GET", f"/communication/conversations/{CONVERSATION_ID}/")
    
    if conv_test.get("error"):
        print(f"   ❌ ÉCHEC: {conv_test['error']}")
    elif conv_test["success"]:
        print(f"   ✅ Succès - Code: {conv_test['status_code']}")
        if conv_test["data"]:
            print(f"   📝 Titre: {conv_test['data'].get('title', 'Non spécifié')}")
            print(f"   👤 Utilisateur: {conv_test['data'].get('user', 'Non spécifié')}")
            print(f"   📅 Créée le: {conv_test['data'].get('created_at', 'Non spécifié')}")
    else:
        print(f"   ❌ ÉCHEC - Code: {conv_test['status_code']}")
    
    # 3. Récupérer les messages de la conversation
    print(f"\n3. Récupération des messages de la conversation...")
    messages_test = test_endpoint("GET", f"/communication/conversations/{CONVERSATION_ID}/messages/")
    
    if messages_test.get("error"):
        print(f"   ❌ ÉCHEC: {messages_test['error']}")
    elif messages_test["success"]:
        print(f"   ✅ Succès - Code: {messages_test['status_code']}")
        
        if messages_test["data"]:
            messages = messages_test["data"]
            print(f"   📨 Nombre de messages: {len(messages)}")
            
            # Afficher les derniers messages (les 5 derniers)
            print(f"\n   Derniers messages trouvés:")
            for i, msg in enumerate(messages[-5:] if len(messages) >= 5 else messages):
                msg_id = msg.get('id', 'N/A')
                content = msg.get('content', '')[0:50] + "..." if len(msg.get('content', '')) > 50 else msg.get('content', '')
                print(f"   - Message {msg_id}: {content}")
        else:
            print("   ℹ️ Aucun message trouvé")
    else:
        print(f"   ❌ ÉCHEC - Code: {messages_test['status_code']}")
    
    # 4. Tester l'envoi d'un message de test
    print(f"\n4. Test d'envoi d'un message...")
    test_message = {
        "content": "Message de test diagnostique",
        "sender_type": "user"  # ou "assistant" selon votre modèle
    }
    
    send_test = test_endpoint("POST", f"/communication/conversations/{CONVERSATION_ID}/messages/", test_message)
    
    if send_test.get("error"):
        print(f"   ❌ ÉCHEC: {send_test['error']}")
    elif send_test["success"]:
        print(f"   ✅ Succès - Code: {send_test['status_code']}")
        if send_test["data"]:
            print(f"   📤 Message envoyé - ID: {send_test['data'].get('id', 'N/A')}")
    else:
        print(f"   ❌ ÉCHEC - Code: {send_test['status_code']}")
        if send_test["data"]:
            print(f"   Détails: {send_test['data']}")
    
    # 5. Vérifier les problèmes courants
    print(f"\n5. Vérification des problèmes courants...")
    
    # Vérifier CORS
    if conv_test.get("headers"):
        cors_headers = [h for h in conv_test["headers"] if "access-control" in h.lower()]
        if cors_headers:
            print(f"   ✅ En-têtes CORS détectés")
        else:
            print(f"   ⚠️ Aucun en-tête CORS détecté (peut causer des problèmes en frontend)")
    
    # Vérifier le content-type
    if conv_test.get("headers", {}).get("content-type", "").startswith("application/json"):
        print(f"   ✅ Content-Type JSON correct")
    else:
        print(f"   ⚠️ Content-Type incorrect: {conv_test.get('headers', {}).get('content-type')}")
    
    print("\n" + "=" * 60)
    print("DIAGNOSTIC TERMINÉ")
    print("=" * 60)

if __name__ == "__main__":
    # Installation requise: pip install requests
    print("Lancement du diagnostic...")
    run_diagnostics()
    
    # Instructions supplémentaires
    print("\nInstructions:")
    print("1. Assurez-vous que le serveur Django est en cours d'exécution")
    print("2. Vérifiez que les migrations sont appliquées")
    print("3. Si vous voyez des erreurs 404, vérifiez vos URLs dans urls.py")
    print("4. Pour les erreurs 500, vérifiez les logs du serveur Django")