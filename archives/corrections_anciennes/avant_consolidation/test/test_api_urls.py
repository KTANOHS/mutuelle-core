# test_api_urls.py
import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_urls():
    """Teste toutes les URLs API possibles"""
    
    urls_to_test = [
        # URLs directes
        ("/communication/conversations/5/messages/", "Messages direct"),
        ("/api/communication/conversations/5/messages/", "API Messages"),
        ("/api/v1/communication/conversations/5/messages/", "API v1 Messages"),
        ("/communication/api/conversations/5/messages/", "Communication API"),
        ("/communication/conversations/5/api/messages/", "Conversation API"),
        
        # URLs avec JSON
        ("/communication/conversations/5/messages/json/", "Messages JSON"),
        ("/communication/conversations/5/json/", "Conversation JSON"),
        
        # URLs de l'application existante
        ("/communication/api_messages/5/", "API Messages direct"),
        ("/communication/conversation/5/messages/", "Conversation messages"),
        
        # URLs avec format
        ("/communication/conversations/5/?format=json", "Format JSON"),
        ("/communication/conversations/5/messages/?format=json", "Messages format JSON"),
    ]
    
    print("🔍 Test de toutes les URLs API possibles...")
    print("=" * 60)
    
    working_urls = []
    
    for url_path, description in urls_to_test:
        url = BASE_URL + url_path
        print(f"\n📡 Testing: {description}")
        print(f"   URL: {url}")
        
        try:
            response = requests.get(url, timeout=5)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                print(f"   Content-Type: {content_type}")
                
                if 'application/json' in content_type:
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            print(f"   ✅ JSON valide - {len(data)} éléments")
                            print(f"   📊 Exemple: {json.dumps(data[0] if data else {}, indent=2)[:100]}...")
                        elif isinstance(data, dict):
                            print(f"   ✅ JSON valide - dictionnaire")
                            keys = list(data.keys())[:5]
                            print(f"   📊 Clés: {keys}")
                        working_urls.append((url, description))
                    except json.JSONDecodeError:
                        print(f"   ⚠️  Réponse non-JSON: {response.text[:100]}")
                else:
                    print(f"   📄 Non-JSON: {response.text[:100]}...")
            elif response.status_code == 404:
                print(f"   ❌ Non trouvé")
            elif response.status_code == 403:
                print(f"   🔒 Accès refusé (login requis)")
            elif response.status_code == 500:
                print(f"   💥 Erreur serveur")
            elif response.status_code == 405:
                print(f"   ⚠️  Méthode non autorisée (GET non supporté)")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Impossible de se connecter")
        except Exception as e:
            print(f"   ⚠️  Erreur: {e}")
    
    return working_urls

def create_simple_api_view():
    """Crée une vue API simple si aucune n'existe"""
    print("\n" + "=" * 60)
    print("🛠️  Création d'une vue API simple...")
    
    vue_code = '''
# =============================================================================
# VUE API SIMPLE POUR LES MESSAGES
# =============================================================================

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
import json

@require_GET
@login_required
def api_conversation_messages_simple(request, conversation_id):
    """API simple pour récupérer les messages d'une conversation"""
    try:
        from communication.models import Conversation, Message
        
        # Récupérer la conversation (vérifier que l'utilisateur est participant)
        conversation = get_object_or_404(
            Conversation.objects.filter(participants=request.user),
            id=conversation_id
        )
        
        # Récupérer les messages
        messages = Message.objects.filter(
            conversation=conversation
        ).select_related('expediteur', 'destinataire').order_by('date_envoi')
        
        # Construire la réponse JSON
        data = []
        for msg in messages:
            data.append({
                'id': msg.id,
                'titre': msg.titre,
                'contenu': msg.contenu,
                'expediteur': {
                    'id': msg.expediteur.id,
                    'username': msg.expediteur.username,
                    'email': msg.expediteur.email,
                },
                'destinataire': {
                    'id': msg.destinataire.id,
                    'username': msg.destinataire.username,
                    'email': msg.destinataire.email,
                },
                'date_envoi': msg.date_envoi.isoformat() if msg.date_envoi else None,
                'est_lu': msg.est_lu,
                'type_message': msg.type_message,
            })
        
        return JsonResponse({
            'success': True,
            'conversation_id': conversation_id,
            'total_messages': len(data),
            'messages': data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'conversation_id': conversation_id
        }, status=500)

@csrf_exempt
@require_POST
def api_send_message(request):
    """API pour envoyer un message (sans authentification pour test)"""
    try:
        from communication.models import Conversation, Message
        from django.contrib.auth.models import User
        
        # Parser les données JSON
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({
                'success': False,
                'error': 'Données JSON invalides'
            }, status=400)
        
        # Récupérer les paramètres
        expediteur_id = data.get('expediteur_id')
        destinataire_id = data.get('destinataire_id')
        contenu = data.get('contenu', '').strip()
        titre = data.get('titre', 'Message via API')
        
        # Validation
        if not all([expediteur_id, destinataire_id, contenu]):
            return JsonResponse({
                'success': False,
                'error': 'Paramètres manquants: expediteur_id, destinataire_id et contenu sont requis'
            }, status=400)
        
        # Récupérer les utilisateurs
        expediteur = User.objects.get(id=expediteur_id)
        destinataire = User.objects.get(id=destinataire_id)
        
        # Trouver ou créer la conversation
        conversation = Conversation.objects.filter(
            participants=expediteur
        ).filter(
            participants=destinataire
        ).first()
        
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(expediteur, destinataire)
        
        # Créer le message
        message = Message.objects.create(
            expediteur=expediteur,
            destinataire=destinataire,
            conversation=conversation,
            titre=titre,
            contenu=contenu,
            type_message=data.get('type_message', 'NORMAL')
        )
        
        return JsonResponse({
            'success': True,
            'message_id': message.id,
            'conversation_id': conversation.id,
            'created_at': message.date_envoi.isoformat() if message.date_envoi else None
        })
        
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Utilisateur non trouvé'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
'''
    
    # Écrire le fichier de vue
    with open('communication/views_api.py', 'w', encoding='utf-8') as f:
        f.write(vue_code)
    
    print("✅ Fichier de vue créé: communication/views_api.py")
    
    # Ajouter les URLs
    urls_code = '''
# =============================================================================
# URLS API SIMPLES
# =============================================================================

from django.urls import path
from . import views_api

urlpatterns = [
    # API pour récupérer les messages d'une conversation
    path('api/simple/conversations/<int:conversation_id>/messages/', 
         views_api.api_conversation_messages_simple, 
         name='api_simple_conversation_messages'),
    
    # API pour envoyer un message
    path('api/simple/messages/send/', 
         views_api.api_send_message, 
         name='api_simple_send_message'),
    
    # API pour tester
    path('api/test/messages/', 
         lambda request: JsonResponse({'status': 'API test working'}), 
         name='api_test'),
]
'''
    
    # Ajouter ces URLs au fichier urls.py existant
    try:
        with open('communication/urls.py', 'a', encoding='utf-8') as f:
            f.write('\n\n' + urls_code)
        print("✅ URLs ajoutées à communication/urls.py")
    except Exception as e:
        print(f"⚠️  Impossible de modifier urls.py: {e}")
        print("\nAjoutez manuellement ces URLs à votre fichier urls.py:")
        print(urls_code)

def test_new_api():
    """Teste la nouvelle API"""
    print("\n" + "=" * 60)
    print("🧪 Test de la nouvelle API...")
    
    # URLs de la nouvelle API
    test_urls = [
        ("/communication/api/simple/conversations/5/messages/", "Messages conversation 5"),
        ("/communication/api/test/messages/", "Test API"),
    ]
    
    for url_path, description in test_urls:
        url = BASE_URL + url_path
        print(f"\n🔍 Testing: {description}")
        print(f"   URL: {url}")
        
        try:
            response = requests.get(url, timeout=5)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ Réponse JSON:")
                    print(f"      {json.dumps(data, indent=2)[:200]}...")
                except:
                    print(f"   📄 Réponse: {response.text[:200]}")
            else:
                print(f"   ❌ Erreur: {response.text[:200]}")
                
        except Exception as e:
            print(f"   ⚠️  Erreur: {e}")

def create_test_script():
    """Crée un script de test pour l'API"""
    script_code = '''#!/usr/bin/env python3
"""
Script de test pour l'API de messages
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_get_messages(conversation_id=5):
    """Teste la récupération des messages"""
    print(f"📨 Récupération des messages de la conversation {conversation_id}...")
    
    urls = [
        f"/communication/api/simple/conversations/{conversation_id}/messages/",
        f"/api/communication/conversations/{conversation_id}/messages/",
        f"/communication/conversations/{conversation_id}/messages/json/",
    ]
    
    for url_path in urls:
        url = BASE_URL + url_path
        print(f"\n🔗 Test URL: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict) and 'messages' in data:
                        messages = data['messages']
                        print(f"   ✅ {len(messages)} messages trouvés")
                        
                        # Afficher les messages
                        for i, msg in enumerate(messages[:5]):  # Afficher les 5 premiers
                            print(f"   📝 Message {i+1}: {msg.get('titre', 'Sans titre')}")
                            print(f"      Contenu: {msg.get('contenu', '')[:50]}...")
                            print(f"      De: {msg.get('expediteur', {}).get('username', 'Inconnu')}")
                            print(f"      À: {msg.get('destinataire', {}).get('username', 'Inconnu')}")
                            print()
                    elif isinstance(data, list):
                        print(f"   ✅ {len(data)} messages trouvés (liste directe)")
                        
                        # Afficher les messages
                        for i, msg in enumerate(data[:3]):  # Afficher les 3 premiers
                            print(f"   📝 Message {i+1}: {msg.get('titre', 'Sans titre')}")
                            print(f"      Contenu: {msg.get('contenu', '')[:50]}...")
                    else:
                        print(f"   ℹ️  Format de réponse: {type(data)}")
                        print(f"   📊 Données: {json.dumps(data, indent=2)[:200]}...")
                        
                except json.JSONDecodeError:
                    print(f"   ❌ Réponse non-JSON: {response.text[:200]}")
            elif response.status_code == 404:
                print(f"   ❌ Endpoint non trouvé")
            elif response.status_code == 403:
                print(f"   🔒 Accès refusé (authentification requise)")
            else:
                print(f"   ❌ Erreur {response.status_code}: {response.text[:200]}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Impossible de se connecter au serveur")
        except Exception as e:
            print(f"   ⚠️  Erreur: {e}")

def test_send_message():
    """Teste l'envoi d'un message"""
    print("\n📤 Test d'envoi de message...")
    
    # Données de test
    test_data = {
        "expediteur_id": 1,  # GLORIA1
        "destinataire_id": 2,  # Almoravide
        "titre": "Test depuis script API",
        "contenu": "Ceci est un message de test envoyé via l'API",
        "type_message": "TEST"
    }
    
    url = BASE_URL + "/communication/api/simple/messages/send/"
    
    print(f"🔗 URL: {url}")
    print(f"📝 Données: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            url,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"\n📨 Réponse - Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Succès!")
            print(f"   📊 Résultat: {json.dumps(result, indent=2)}")
        else:
            print(f"   ❌ Erreur: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ⚠️  Exception: {e}")

def main():
    print("=" * 60)
    print("SCRIPT DE TEST API MESSAGES")
    print("=" * 60)
    
    # Test de récupération
    test_get_messages(5)
    
    # Test d'envoi (optionnel)
    print("\n" + "=" * 60)
    choice = input("Voulez-vous tester l'envoi d'un message? (o/n): ")
    if choice.lower() == 'o':
        test_send_message()
    
    print("\n" + "=" * 60)
    print("TEST TERMINÉ")
    print("=" * 60)

if __name__ == "__main__":
    main()
'''
    
    with open('test_messages_api.py', 'w', encoding='utf-8') as f:
        f.write(script_code)
    
    print("✅ Script de test créé: test_messages_api.py")
    print("   Pour l'exécuter: python test_messages_api.py")

def main():
    print("🚀 DIAGNOSTIC ET CRÉATION API MESSAGES")
    print("=" * 60)
    
    # 1. Tester les URLs existantes
    working_urls = test_urls()
    
    if working_urls:
        print("\n" + "=" * 60)
        print("✅ URLs API fonctionnelles trouvées:")
        for url, desc in working_urls:
            print(f"   • {desc}: {url}")
    else:
        print("\n" + "=" * 60)
        print("❌ Aucune URL API fonctionnelle trouvée")
        
        # 2. Créer une API simple
        create_simple_api_view()
        
        # 3. Tester la nouvelle API
        test_new_api()
        
        # 4. Créer un script de test
        create_test_script()
        
        print("\n" + "=" * 60)
        print("🎯 INSTRUCTIONS:")
        print("1. Redémarrez le serveur Django:")
        print("   python manage.py runserver")
        print("\n2. Testez l'API avec:")
        print("   python test_messages_api.py")
        print("\n3. Pour récupérer les messages de la conversation 5:")
        print("   http://127.0.0.1:8000/communication/api/simple/conversations/5/messages/")

if __name__ == "__main__":
    main()