import requests
import json
import sys
from urllib.parse import urljoin

BASE_URL = "http://127.0.0.1:8000"

def test_all_endpoints():
    """Teste tous les endpoints possibles pour comprendre la structure de l'API"""
    
    print("🔍 Exploration de la structure de l'API...")
    print("=" * 60)
    
    endpoints_to_test = [
        ("/api/", "Root API"),
        ("/api/communication/", "Communication API"),
        ("/api/communication/conversations/", "Liste des conversations"),
        ("/api/communication/conversations/5/", "Conversation 5"),
        ("/api/communication/conversations/5/messages/", "Messages conversation 5"),
        ("/api/v1/", "API v1"),
        ("/api/v1/communication/", "Communication API v1"),
        ("/communication/api/", "Communication API endpoint"),
        ("/communication/api/conversations/5/messages/", "Messages via communication API"),
    ]
    
    found_endpoints = []
    
    for endpoint, description in endpoints_to_test:
        url = urljoin(BASE_URL, endpoint)
        print(f"\nTesting: {description}")
        print(f"URL: {url}")
        
        try:
            # Test GET
            response = requests.get(url, timeout=5)
            
            content_type = response.headers.get('content-type', '')
            
            print(f"  Status: {response.status_code}")
            print(f"  Content-Type: {content_type}")
            
            if response.status_code == 200:
                if 'application/json' in content_type:
                    try:
                        data = response.json()
                        print(f"  ✅ JSON valide")
                        if isinstance(data, list):
                            print(f"  📊 Nombre d'éléments: {len(data)}")
                        found_endpoints.append((endpoint, "JSON API"))
                    except:
                        print(f"  ⚠️  Contenu JSON invalide")
                elif 'text/html' in content_type:
                    print(f"  📄 Page HTML (pas une API)")
                    found_endpoints.append((endpoint, "HTML Page"))
                else:
                    print(f"  ℹ️  Autre type: {content_type}")
            elif response.status_code == 404:
                print(f"  ❌ Endpoint non trouvé")
            elif response.status_code == 403:
                print(f"  🔒 Accès refusé")
            elif response.status_code == 500:
                print(f"  💥 Erreur serveur")
            
        except requests.exceptions.ConnectionError:
            print(f"  ❌ Impossible de se connecter")
        except Exception as e:
            print(f"  ⚠️  Erreur: {e}")
    
    # Tester également les endpoints sans /api/
    print("\n" + "=" * 60)
    print("Testing endpoints directs (sans /api/)...")
    
    direct_endpoints = [
        ("/communication/conversations/", "Liste conversations"),
        ("/communication/conversations/5/", "Conversation 5 détail"),
    ]
    
    for endpoint, description in direct_endpoints:
        url = urljoin(BASE_URL, endpoint)
        print(f"\nTesting: {description}")
        print(f"URL: {url}")
        
        try:
            response = requests.get(url, timeout=5)
            print(f"  Status: {response.status_code}")
            print(f"  Content-Type: {response.headers.get('content-type', '')}")
            
            if response.status_code == 200:
                # Essayer de voir si c'est une page avec des données
                if 'text/html' in response.headers.get('content-type', ''):
                    # Chercher des indices de données JSON dans la page
                    html_content = response.text.lower()
                    if 'json' in html_content or 'api' in html_content or 'fetch' in html_content:
                        print(f"  🔍 Page HTML contenant des références API/JSON")
        except Exception as e:
            print(f"  ⚠️  Erreur: {e}")
    
    return found_endpoints

def check_django_urls():
    """Essaie de découvrir les URLs disponibles"""
    print("\n" + "=" * 60)
    print("Vérification des URLs Django...")
    
    # Tenter d'accéder à l'admin pour voir la structure
    admin_url = urljoin(BASE_URL, "/admin/")
    try:
        response = requests.get(admin_url, timeout=5)
        if response.status_code == 200:
            print("✅ Interface admin accessible")
    except:
        print("❌ Admin non accessible")
    
    # Vérifier les URLs de debug si activées
    debug_urls = [
        "/__debug__/",
        "/debug/",
        "/dev/",
    ]
    
    for url in debug_urls:
        full_url = urljoin(BASE_URL, url)
        try:
            response = requests.get(full_url, timeout=3)
            if response.status_code == 200:
                print(f"✅ Debug URL trouvée: {url}")
        except:
            pass

def analyze_html_content():
    """Analyse le contenu HTML de la conversation pour trouver des données"""
    print("\n" + "=" * 60)
    print("Analyse du contenu HTML de la conversation 5...")
    
    conv_url = urljoin(BASE_URL, "/communication/conversations/5/")
    
    try:
        response = requests.get(conv_url, timeout=5)
        
        if response.status_code == 200:
            html_content = response.text
            
            # Chercher des données JSON dans le HTML
            import re
            
            # Chercher des patterns JSON
            json_patterns = [
                r'var\s+data\s*=\s*({.*?});',
                r'data\s*:\s*({.*?}),',
                r'JSON\.parse\(\s*["\']({.*?})["\']\s*\)',
                r'<script[^>]*>\s*({.*?})\s*</script>',
            ]
            
            found_data = False
            for pattern in json_patterns:
                matches = re.findall(pattern, html_content, re.DOTALL)
                for match in matches:
                    if len(match) > 10:  # Minimum length
                        print(f"🔍 Données JSON potentielles trouvées")
                        try:
                            data = json.loads(match)
                            print(f"   Structure: {type(data)}")
                            if isinstance(data, dict):
                                print(f"   Clés: {list(data.keys())[:5]}")
                            found_data = True
                        except:
                            pass
            
            if not found_data:
                print("ℹ️ Aucune donnée JSON évidente dans la page")
            
            # Chercher des endpoints API dans le JavaScript
            api_patterns = [
                r'fetch\(\s*["\'](.*?/api/.*?)["\']',
                r'axios\.(?:get|post)\(\s*["\'](.*?/api/.*?)["\']',
                r'\.ajax\(\s*{[^}]*url\s*:\s*["\'](.*?/api/.*?)["\']',
                r'url\s*:\s*["\'](.*?/api/.*?)["\']',
            ]
            
            print("\n🔍 Recherche d'endpoints API dans le code JavaScript...")
            for pattern in api_patterns:
                matches = re.findall(pattern, html_content)
                for match in matches:
                    print(f"   📍 Endpoint trouvé: {match}")
            
            # Estimer la taille de la page
            print(f"\n📊 Taille de la page: {len(html_content)} caractères")
            
            # Chercher les mots-clés
            keywords = ['message', 'conversation', 'user', 'content', 'timestamp']
            for keyword in keywords:
                if keyword in html_content.lower():
                    count = html_content.lower().count(keyword)
                    if count > 0:
                        print(f"   📝 Mot-clé '{keyword}' trouvé {count} fois")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_post_requests():
    """Teste les requêtes POST possibles"""
    print("\n" + "=" * 60)
    print("Test des requêtes POST...")
    
    post_endpoints = [
        "/communication/conversations/5/messages/",
        "/api/communication/conversations/5/messages/",
        "/api/v1/communication/conversations/5/messages/",
    ]
    
    test_data = {
        "content": "Message de test diagnostic",
        "sender": "user"
    }
    
    for endpoint in post_endpoints:
        url = urljoin(BASE_URL, endpoint)
        print(f"\nTesting POST: {url}")
        
        try:
            response = requests.post(url, json=test_data, timeout=5)
            print(f"  Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                content_type = response.headers.get('content-type', '')
                print(f"  Content-Type: {content_type}")
                
                if response.content:
                    try:
                        data = response.json()
                        print(f"  ✅ Réponse JSON: {data}")
                    except:
                        print(f"  📄 Réponse: {response.text[:100]}")
            elif response.status_code == 405:
                print(f"  ❌ Méthode non autorisée (GET only?)")
            elif response.status_code == 400:
                print(f"  ⚠️  Mauvaise requête")
                if response.content:
                    try:
                        error_data = response.json()
                        print(f"  Erreur: {error_data}")
                    except:
                        print(f"  Message: {response.text[:100]}")
                        
        except Exception as e:
            print(f"  ⚠️  Erreur: {e}")

def main():
    print("🔬 DIAGNOSTIC APPROFONDI - STRUCTURE API")
    print("=" * 60)
    
    # 1. Explorer tous les endpoints possibles
    found = test_all_endpoints()
    
    # 2. Vérifier les URLs Django
    check_django_urls()
    
    # 3. Analyser le contenu HTML
    analyze_html_content()
    
    # 4. Tester les requêtes POST
    test_post_requests()
    
    # 5. Conclusions
    print("\n" + "=" * 60)
    print("🎯 CONCLUSIONS ET RECOMMANDATIONS")
    print("=" * 60)
    
    if found:
        print("\nEndpoints trouvés:")
        for endpoint, description in found:
            print(f"  • {endpoint} ({description})")
    
    print("\n📋 Problèmes identifiés:")
    print("  1. Les endpoints retournent du HTML au lieu du JSON")
    print("  2. L'endpoint /messages/ n'existe pas ou retourne 404")
    
    print("\n🚀 Solutions possibles:")
    print("  1. Modifier vos vues Django pour retourner du JSON")
    print("  2. Ajouter des endpoints API spécifiques")
    print("  3. Utiliser Django REST Framework pour une API REST")
    print("  4. Vérifier votre fichier urls.py")
    
    print("\n🔧 Vérifiez votre fichier urls.py:")
    print("  from django.urls import path")
    print("  from . import views")
    print("")
    print("  urlpatterns = [")
    print("      path('conversations/<int:pk>/', views.conversation_detail, name='conversation_detail'),")
    print("      path('conversations/<int:pk>/messages/', views.conversation_messages, name='conversation_messages'),")
    print("  ]")
    
    print("\n🐍 Exemple de vue qui retourne du JSON:")
    print("  from django.http import JsonResponse")
    print("  from .models import Conversation, Message")
    print("")
    print("  def conversation_messages(request, pk):")
    print("      conversation = get_object_or_404(Conversation, pk=pk)")
    print("      messages = Message.objects.filter(conversation=conversation)")
    print("      data = [")
    print("          {'id': m.id, 'content': m.content, 'timestamp': m.timestamp}")
    print("          for m in messages")
    print("      ]")
    print("      return JsonResponse(data, safe=False)")

if __name__ == "__main__":
    main()