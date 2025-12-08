# create_public_api.py
import os

def create_public_api_view():
    """Crée une vue API publique sans authentification"""
    
    public_view_code = '''
# =============================================================================
# VUE API PUBLIQUE (sans authentification)
# =============================================================================

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404
import json

@csrf_exempt
@require_GET
def api_public_conversation_messages(request, conversation_id):
    """API publique pour récupérer les messages d'une conversation - sans authentification"""
    try:
        from communication.models import Conversation, Message
        
        # Récupérer la conversation
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        # Récupérer les messages
        messages = Message.objects.filter(
            conversation=conversation
        ).select_related('expediteur', 'destinataire').order_by('id')
        
        # Formater les données
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
                } if msg.expediteur else None,
                'destinataire': {
                    'id': msg.destinataire.id,
                    'username': msg.destinataire.username,
                    'email': msg.destinataire.email,
                } if msg.destinataire else None,
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
@require_GET
def api_public_test(request):
    """Endpoint de test public"""
    return JsonResponse({
        'status': 'API publique fonctionnelle',
        'timestamp': 'test',
        'instructions': 'Utilisez /api/public/conversations/5/messages/ pour les messages'
    })
'''
    
    # Ajouter à views_api.py
    with open('communication/views_api.py', 'a', encoding='utf-8') as f:
        f.write(public_view_code)
    
    print("✅ Vue API publique ajoutée à communication/views_api.py")
    
    # Ajouter les URLs publiques à urls.py
    urls_to_add = '''
    # API publique (sans authentification)
    path('api/public/test/', 
         views_api.api_public_test, 
         name='api_public_test'),
    
    path('api/public/conversations/<int:conversation_id>/messages/', 
         views_api.api_public_conversation_messages, 
         name='api_public_conversation_messages'),
'''
    
    # Lire le fichier urls.py
    with open('communication/urls.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver la dernière occurrence de ']' et ajouter avant
    lines = content.split('\n')
    for i in range(len(lines)-1, -1, -1):
        if lines[i].strip() == ']':
            # Insérer les nouvelles URLs avant la fermeture
            lines.insert(i, urls_to_add)
            break
    
    # Réécrire le fichier
    with open('communication/urls.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print("✅ URLs publiques ajoutées à communication/urls.py")

def restart_server_instructions():
    """Affiche les instructions pour redémarrer le serveur"""
    print("\n" + "=" * 60)
    print("📋 INSTRUCTIONS :")
    print("=" * 60)
    print("\n1. Arrêtez le serveur Django actuel (Ctrl+C dans le terminal)")
    print("\n2. Redémarrez le serveur :")
    print("   python manage.py runserver")
    print("\n3. Dans un NOUVEAU terminal, testez l'API :")
    print("   curl http://127.0.0.1:8000/communication/api/public/test/")
    print("   curl http://127.0.0.1:8000/communication/api/public/conversations/5/messages/")
    print("\n4. Alternative : testez avec le script :")
    print("   python test_messages_api.py")

def test_quick():
    """Teste rapidement si le serveur répond"""
    import requests
    import json
    
    print("\n🔍 Test rapide des endpoints...")
    
    endpoints = [
        ("/communication/api/public/test/", "Test API publique"),
        ("/communication/api/simple/conversations/5/messages/", "API simple (avec auth)"),
        ("/communication/api/test/messages/", "Test API"),
    ]
    
    for endpoint, description in endpoints:
        url = f"http://127.0.0.1:8000{endpoint}"
        print(f"\n📡 Testing: {description}")
        print(f"   URL: {url}")
        
        try:
            response = requests.get(url, timeout=5)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ Réponse JSON: {json.dumps(data)[:100]}...")
                except:
                    print(f"   📄 Réponse: {response.text[:100]}")
            elif response.status_code == 403:
                print(f"   🔒 Accès refusé (authentification requise)")
            elif response.status_code == 404:
                print(f"   ❌ Non trouvé")
            else:
                print(f"   ❌ Erreur: {response.text[:100]}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Impossible de se connecter (serveur non démarré?)")
        except Exception as e:
            print(f"   ⚠️  Erreur: {e}")

def main():
    print("=" * 60)
    print("CRÉATION D'API PUBLIQUE POUR TEST")
    print("=" * 60)
    
    # Créer les vues publiques
    create_public_api_view()
    
    # Afficher les instructions
    restart_server_instructions()
    
    # Tester rapidement
    test_quick()

if __name__ == "__main__":
    main()