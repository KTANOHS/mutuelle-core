
# simple_test.py
import requests

def test_simple_login():
    base_url = "http://127.0.0.1:8000"
    
    print("🎯 TEST SIMPLE DE CONNEXION")
    print("=" * 40)
    
    # Quelques utilisateurs de test
    test_users = [
        {'username': 'test_membre', 'password': 'test123', 'type': 'membre'},
        {'username': 'test_assureur', 'password': 'test123', 'type': 'assureur'},
        {'username': 'test_admin', 'password': 'test123', 'type': 'admin'},
    ]
    
    for user_info in test_users:
        print(f"\\n🔐 {user_info['username']}:")
        
        session = requests.Session()
        
        try:
            # Connexion
            login_page = session.get(f"{base_url}/accounts/login/")
            csrf_token = session.cookies.get('csrftoken')
            
            login_data = {
                'username': user_info['username'],
                'password': user_info['password'],
                'csrfmiddlewaretoken': csrf_token,
            }
            
            login_response = session.post(
                f"{base_url}/accounts/login/",
                data=login_data,
                allow_redirects=False
            )
            
            print(f"   Connexion: {login_response.status_code}")
            
            if login_response.status_code == 302:
                print("   ✅ CONNEXION RÉUSSIE!")
                
                # Suivre la redirection
                redirect_url = login_response.headers.get('Location')
                print(f"   Redirection: {redirect_url}")
                
                # Page finale
                if redirect_url:
                    final_response = session.get(f"{base_url}{redirect_url}", allow_redirects=False)
                    if final_response.status_code == 200:
                        print(f"   📍 Dashboard: ✅ Accessible")
                    else:
                        print(f"   📍 Dashboard: ❌ {final_response.status_code}")
            else:
                print("   ❌ ÉCHEC CONNEXION")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")

if __name__ == "__main__":
    test_simple_login()
