# test_final.sh
#!/bin/bash
echo "🎯 TEST FINAL DES REDIRECTIONS EN TEMPS RÉEL"

python manage.py shell << EOF
from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()
client = Client()

users = [
    ('test_membre', 'mot_de_passe_test', '/membres/dashboard/'),
    ('test_agent', 'mot_de_passe_test', '/agents/dashboard/'),
    ('test_assureur', 'mot_de_passe_test', '/assureur/dashboard/'),
    ('test_medecin', 'mot_de_passe_test', '/medecin/dashboard/'),
    ('test_pharmacien', 'mot_de_passe_test', '/pharmacien/dashboard/')
]

print("🔐 Test de connexion et redirection:")
print("=" * 60)

for username, password, expected_url in users:
    # Connexion
    login_success = client.login(username=username, password=password)
    
    if login_success:
        # Accès à la page de redirection après login
        response = client.get('/redirect-after-login/', follow=True)
        
        # Vérifier la redirection finale
        final_url = response.redirect_chain[-1][0] if response.redirect_chain else response.request['PATH_INFO']
        
        status = "✅" if expected_url in final_url else "❌"
        print(f"{status} {username}:")
        print(f"   Connexion: {'✅' if login_success else '❌'}")
        print(f"   URL attendue: {expected_url}")
        print(f"   URL obtenue: {final_url}")
        
        # Déconnexion pour le prochain test
        client.logout()
    else:
        print(f"❌ {username}: Échec de connexion")

print("=" * 60)
EOF