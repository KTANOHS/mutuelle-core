# diagnostic_conversation_complet.py - VERSION CORRIGÉE
import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
CONVERSATION_ID = 5

def print_section(title):
    """Affiche une section avec style"""
    print(f"\n{'='*60}")
    print(f"📊 {title}")
    print(f"{'='*60}")

def test_conversation_api():
    """Teste l'API de conversation 5"""
    print_section("TEST DE L'API DE CONVERSATION 5")
    
    # URL de l'API publique
    api_url = f"{BASE_URL}/communication/api/public/conversations/{CONVERSATION_ID}/messages/"
    
    print(f"🔗 URL testée: {api_url}")
    
    try:
        # Test GET - Récupération des messages
        print(f"\n1. Test GET - Récupération des messages...")
        response = requests.get(api_url, timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                messages = data.get('messages', [])
                total_messages = data.get('total_messages', 0)
                
                print(f"   ✅ SUCCÈS: {total_messages} messages récupérés")
                print(f"   📊 Conversation ID: {data.get('conversation_id')}")
                
                # Afficher un résumé des messages
                print(f"\n   📝 Résumé des messages:")
                for i, msg in enumerate(messages[:5]):  # Afficher les 5 premiers
                    print(f"      {i+1}. ID {msg['id']}: {msg['titre'][:30]}...")
                    print(f"         De: {msg['expediteur']['username']} → À: {msg['destinataire']['username']}")
                    print(f"         Contenu: {msg['contenu'][:50]}...")
                
                if total_messages > 5:
                    print(f"      ... et {total_messages - 5} autres messages")
                    
                # Vérification des messages spécifiques
                print(f"\n   🔍 Vérification des messages spécifiques:")
                target_messages = [
                    "Test diagnostique",
                    "Test API diagnostique",
                    "Test API",
                    "Shell Test",
                    "Test Diagnostic",
                    "CAPTURE",
                    "Message via API"
                ]
                
                found_count = 0
                for target in target_messages:
                    found = any(target in msg.get('titre', '') or target in msg.get('contenu', '') for msg in messages)
                    if found:
                        print(f"      ✅ '{target}' - TROUVÉ")
                        found_count += 1
                    else:
                        print(f"      ❌ '{target}' - NON TROUVÉ")
                
                print(f"\n   📈 Résultat: {found_count}/{len(target_messages)} messages cibles trouvés")
                
                return {
                    'success': True,
                    'total_messages': total_messages,
                    'messages': messages,
                    'data': data
                }
            else:
                print(f"   ❌ ÉCHEC: API retourne success=False")
                print(f"   Erreur: {data.get('error')}")
                return {'success': False, 'error': data.get('error')}
        else:
            print(f"   ❌ ÉCHEC: Code de réponse {response.status_code}")
            print(f"   Message: {response.text[:200]}")
            return {'success': False, 'status_code': response.status_code}
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ ERREUR: Impossible de se connecter au serveur")
        print(f"   Vérifiez que le serveur Django est démarré: python manage.py runserver")
        return {'success': False, 'error': 'Connection refused'}
    except requests.exceptions.Timeout:
        print(f"   ❌ ERREUR: Timeout - Le serveur ne répond pas")
        return {'success': False, 'error': 'Timeout'}
    except json.JSONDecodeError:
        print(f"   ❌ ERREUR: Réponse JSON invalide")
        print(f"   Réponse brute: {response.text[:200]}")
        return {'success': False, 'error': 'Invalid JSON'}
    except Exception as e:
        print(f"   ❌ ERREUR: {str(e)}")
        return {'success': False, 'error': str(e)}

def test_other_endpoints():
    """Teste d'autres endpoints de l'API"""
    print_section("TEST DES AUTRES ENDPOINTS")
    
    endpoints = [
        (f"/communication/api/public/test/", "Test API publique"),
        (f"/communication/conversations/{CONVERSATION_ID}/", "Page conversation 5 (HTML)"),
        (f"/communication/", "Accueil communication"),
    ]
    
    results = []
    
    for endpoint, description in endpoints:
        url = BASE_URL + endpoint
        print(f"\n🔗 Testing: {description}")
        print(f"   URL: {url}")
        
        try:
            response = requests.get(url, timeout=5)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                
                if 'application/json' in content_type:
                    print(f"   ✅ Réponse JSON reçue")
                    try:
                        data = response.json()
                        if 'status' in data:
                            print(f"   📊 Message: {data['status']}")
                    except:
                        pass
                elif 'text/html' in content_type:
                    print(f"   ✅ Page HTML chargée")
                    # Vérifier si la page contient des données de conversation
                    if 'conversation' in response.text.lower() or 'message' in response.text.lower():
                        print(f"   📄 Page semble contenir des données de messagerie")
                    else:
                        print(f"   ℹ️  Page HTML standard")
                else:
                    print(f"   ℹ️  Type de contenu: {content_type}")
                    
                results.append((endpoint, 'SUCCESS', response.status_code))
            elif response.status_code == 404:
                print(f"   ❌ Endpoint non trouvé")
                results.append((endpoint, 'NOT_FOUND', response.status_code))
            elif response.status_code == 403:
                print(f"   🔒 Accès refusé (authentification requise)")
                results.append((endpoint, 'AUTH_REQUIRED', response.status_code))
            elif response.status_code == 500:
                print(f"   💥 Erreur serveur interne")
                results.append((endpoint, 'SERVER_ERROR', response.status_code))
            else:
                print(f"   ⚠️  Code inattendu: {response.status_code}")
                results.append((endpoint, 'UNKNOWN', response.status_code))
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            results.append((endpoint, 'ERROR', str(e)))
    
    return results

def generate_report(api_result, endpoint_results):
    """Génère un rapport complet"""
    print_section("📄 RAPPORT DE DIAGNOSTIC COMPLET")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Date du diagnostic: {timestamp}")
    print(f"URL de base: {BASE_URL}")
    print(f"Conversation ID: {CONVERSATION_ID}")
    print(f"\n{'─'*60}")
    
    # Résumé de l'API
    print(f"\n🎯 RÉSULTAT API PRINCIPALE:")
    if api_result.get('success'):
        total_msgs = api_result.get('total_messages', 0)
        print(f"   ✅ API FONCTIONNELLE")
        print(f"   📨 Messages récupérés: {total_msgs}")
        
        # Vérifier les messages spécifiques
        messages = api_result.get('messages', [])
        
        print(f"\n   🔍 Messages présents:")
        msg_titles = [msg['titre'] for msg in messages if 'titre' in msg]
        unique_titles = list(set(msg_titles))
        
        for title in unique_titles[:10]:  # Afficher les 10 premiers titres uniques
            count = msg_titles.count(title)
            print(f"      • {title}: {count} message(s)")
        
        if len(unique_titles) > 10:
            print(f"      ... et {len(unique_titles) - 10} autres titres")
    else:
        print(f"   ❌ API EN ÉCHEC")
        print(f"   Erreur: {api_result.get('error', 'Inconnue')}")
    
    # Résumé des autres endpoints
    print(f"\n🌐 AUTRES ENDPOINTS TESTÉS:")
    success_count = sum(1 for _, status, _ in endpoint_results if status == 'SUCCESS')
    total_endpoints = len(endpoint_results)
    
    print(f"   Endpoints testés: {total_endpoints}")
    print(f"   Endpoints réussis: {success_count}")
    
    for endpoint, status, code in endpoint_results:
        status_icon = "✅" if status == 'SUCCESS' else "❌"
        print(f"   {status_icon} {endpoint}: {status} (Code: {code})")
    
    # Recommandations
    print(f"\n💡 RECOMMANDATIONS:")
    
    if api_result.get('success'):
        print(f"   1. ✅ L'API principale fonctionne correctement")
        print(f"   2. 📊 Utilisez l'URL pour intégrer dans d'autres applications:")
        print(f"      {BASE_URL}/communication/api/public/conversations/{CONVERSATION_ID}/messages/")
        print(f"   3. 🔒 Pour une utilisation en production, envisagez d'ajouter:")
        print(f"      - Authentification")
        print(f"      - Limitation de débit (rate limiting)")
        print(f"      - Cache")
    else:
        print(f"   1. ❌ Problème avec l'API principale")
        print(f"   2. 🔧 Vérifiez que:")
        print(f"      - Le serveur Django est démarré")
        print(f"      - La conversation {CONVERSATION_ID} existe")
        print(f"      - Le fichier views_api.py est présent")
        print(f"      - Les URLs sont correctement configurées")
    
    # Commandes utiles (version corrigée sans erreur de syntaxe)
    print(f"\n🔧 COMMANDES UTILES:")
    print(f"   # Tester l'API avec curl")
    print(f"   curl {BASE_URL}/communication/api/public/conversations/{CONVERSATION_ID}/messages/")
    print(f"   ")
    print(f"   # Tester avec format JSON")
    print(f"   curl -s {BASE_URL}/communication/api/public/conversations/{CONVERSATION_ID}/messages/ | python -m json.tool")
    print(f"   ")
    print(f"   # Compter les messages")
    cmd = f"curl -s {BASE_URL}/communication/api/public/conversations/{CONVERSATION_ID}/messages/ | python -c \"import sys, json; data=json.load(sys.stdin); print(f'{len(data[\"messages\"])} messages')\""
    print(f"   {cmd}")

def export_data(api_result):
    """Exporte les données en JSON"""
    if api_result.get('success'):
        try:
            filename = f"conversation_{CONVERSATION_ID}_export.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(api_result['data'], f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 DONNÉES EXPORTÉES:")
            print(f"   Fichier: {filename}")
            print(f"   Taille: {len(json.dumps(api_result['data']))} octets")
            
            # Créer un résumé
            summary = {
                'export_date': datetime.now().isoformat(),
                'conversation_id': CONVERSATION_ID,
                'total_messages': api_result.get('total_messages'),
                'message_ids': [msg['id'] for msg in api_result.get('messages', [])],
                'participants': list(set([
                    f"{msg['expediteur']['username']} -> {msg['destinataire']['username']}"
                    for msg in api_result.get('messages', [])
                ]))
            }
            
            summary_file = f"conversation_{CONVERSATION_ID}_summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            print(f"   Résumé: {summary_file}")
            
        except Exception as e:
            print(f"   ❌ Erreur lors de l'export: {e}")

def main():
    """Fonction principale"""
    print("🚀 DIAGNOSTIC COMPLET - Conversation 5")
    print("="*60)
    
    # Test de l'API principale
    api_result = test_conversation_api()
    
    # Test des autres endpoints
    endpoint_results = test_other_endpoints()
    
    # Génération du rapport
    generate_report(api_result, endpoint_results)
    
    # Export des données
    if api_result.get('success'):
        export_data(api_result)
    
    print(f"\n{'='*60}")
    print("🎯 DIAGNOSTIC TERMINÉ")
    print(f"{'='*60}")
    
    # Statut final
    if api_result.get('success'):
        print(f"✅ SUCCÈS: L'API de conversation 5 fonctionne correctement!")
        print(f"📊 {api_result.get('total_messages')} messages disponibles via l'API")
    else:
        print(f"❌ ÉCHEC: Problèmes détectés avec l'API")
        print(f"🔧 Consultez les recommandations ci-dessus pour résoudre les problèmes")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Diagnostic interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")