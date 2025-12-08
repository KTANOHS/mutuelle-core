# diagnostic_complet_final.py
import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def test_all_endpoints():
    """Teste tous les endpoints API"""
    print("=" * 60)
    print("DIAGNOSTIC COMPLET - API DE COMMUNICATION")
    print("=" * 60)
    
    endpoints = [
        {
            "url": "/communication/api/public/test/",
            "description": "Test API publique",
            "method": "GET"
        },
        {
            "url": "/communication/api/public/conversations/5/messages/",
            "description": "Messages conversation 5 (API publique)",
            "method": "GET"
        },
        {
            "url": "/communication/api/simple/conversations/5/messages/",
            "description": "Messages conversation 5 (avec auth)",
            "method": "GET"
        },
        {
            "url": "/communication/api/test/messages/",
            "description": "Test API simple",
            "method": "GET"
        }
    ]
    
    results = []
    
    for endpoint in endpoints:
        url = BASE_URL + endpoint["url"]
        print(f"\n🔍 Testing: {endpoint['description']}")
        print(f"   URL: {url}")
        
        try:
            if endpoint["method"] == "GET":
                response = requests.get(url, timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    if endpoint["url"] == "/communication/api/public/conversations/5/messages/":
                        if isinstance(data, dict) and 'messages' in data:
                            messages = data['messages']
                            print_success(f"{len(messages)} messages trouvés")
                            results.append({
                                "endpoint": endpoint["url"],
                                "status": "SUCCESS",
                                "message_count": len(messages),
                                "messages": messages[:3]  # Garder 3 premiers pour affichage
                            })
                        else:
                            print_info(f"Données: {json.dumps(data, indent=2)[:100]}...")
                    else:
                        print_success(f"API fonctionnelle: {json.dumps(data, indent=2)[:100]}...")
                        results.append({
                            "endpoint": endpoint["url"],
                            "status": "SUCCESS",
                            "data": data
                        })
                        
                except json.JSONDecodeError:
                    print_error(f"Réponse non-JSON: {response.text[:100]}")
                    results.append({
                        "endpoint": endpoint["url"],
                        "status": "ERROR",
                        "error": "Invalid JSON"
                    })
            elif response.status_code == 403:
                print_info("Accès refusé (authentification requise)")
                results.append({
                    "endpoint": endpoint["url"],
                    "status": "AUTH_REQUIRED"
                })
            elif response.status_code == 404:
                print_error("Endpoint non trouvé")
                results.append({
                    "endpoint": endpoint["url"],
                    "status": "NOT_FOUND"
                })
            else:
                print_error(f"Erreur: {response.text[:100]}")
                results.append({
                    "endpoint": endpoint["url"],
                    "status": "ERROR",
                    "error": f"Status {response.status_code}"
                })
                
        except Exception as e:
            print_error(f"Exception: {e}")
            results.append({
                "endpoint": endpoint["url"],
                "status": "EXCEPTION",
                "error": str(e)
            })
    
    return results

def display_summary(results):
    """Affiche un résumé des résultats"""
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r["status"] == "SUCCESS")
    total_count = len(results)
    
    print(f"Endpoints testés: {total_count}")
    print(f"Endpoints réussis: {success_count}")
    
    # Trouver les messages de la conversation 5
    messages_data = None
    for result in results:
        if result.get("endpoint") == "/communication/api/public/conversations/5/messages/":
            if result["status"] == "SUCCESS":
                messages_data = result
                break
    
    if messages_data:
        print("\n" + "=" * 60)
        print("📨 MESSAGES DE LA CONVERSATION 5")
        print("=" * 60)
        
        messages = messages_data["messages"]
        total_messages = messages_data.get("message_count", 0)
        
        print(f"Total de messages: {total_messages}")
        
        # Afficher les titres de tous les messages
        print("\nListe des messages:")
        for i, msg in enumerate(messages_data.get("messages", []), 1):
            print(f"  {i}. ID {msg.get('id')}: {msg.get('titre')}")
        
        # Vérifier les messages spécifiques demandés
        print("\n🔍 Vérification des messages spécifiques:")
        target_messages = [
            "Test diagnostique",
            "Test API diagnostique",
            "Test API",
            "Shell Test",
            "Test Diagnostic",
            "CAPTURE",
            "Message via API",
            "Conversation avec Almoravide"
        ]
        
        found_count = 0
        for target in target_messages:
            found = False
            for msg in messages:
                if target in str(msg.get('titre', '')) or target in str(msg.get('contenu', '')):
                    found = True
                    break
            if found:
                print(f"  ✅ '{target}' - TROUVÉ")
                found_count += 1
            else:
                print(f"  ❌ '{target}' - NON TROUVÉ")
        
        print(f"\n📈 Résultat: {found_count}/{len(target_messages)} messages trouvés")

def generate_report():
    """Génère un rapport JSON des résultats"""
    print("\n" + "=" * 60)
    print("📄 RAPPORT JSON DE DIAGNOSTIC")
    print("=" * 60)
    
    # Tester les endpoints
    results = test_all_endpoints()
    
    # Créer le rapport
    report = {
        "timestamp": "2025-12-02",
        "base_url": BASE_URL,
        "conversation_id": 5,
        "endpoints_tested": len(results),
        "results": results
    }
    
    # Afficher le rapport
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    # Sauvegarder dans un fichier
    with open('diagnostic_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("\n✅ Rapport sauvegardé dans: diagnostic_report.json")
    
    return report

def main():
    """Fonction principale"""
    print("🚀 LANCEMENT DU DIAGNOSTIC COMPLET")
    
    # Test des endpoints
    results = test_all_endpoints()
    
    # Affichage du résumé
    display_summary(results)
    
    # Générer un rapport
    generate_report()
    
    print("\n" + "=" * 60)
    print("🎯 DIAGNOSTIC TERMINÉ AVEC SUCCÈS !")
    print("=" * 60)
    print("\n📋 URLS DISPONIBLES:")
    print("   1. API publique test: http://127.0.0.1:8000/communication/api/public/test/")
    print("   2. Messages conv 5: http://127.0.0.1:8000/communication/api/public/conversations/5/messages/")
    print("\n🔧 POUR LES TESTS:")
    print("   curl http://127.0.0.1:8000/communication/api/public/conversations/5/messages/ | python -m json.tool")

if __name__ == "__main__":
    main()