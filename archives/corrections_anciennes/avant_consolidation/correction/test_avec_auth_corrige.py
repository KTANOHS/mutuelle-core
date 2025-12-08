# test_avec_auth_corrige.py
import os
import sys
import django

# IMPORTANT : Configurer Django AVANT d'importer quoi que ce soit d'autre
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

# Ajouter le chemin du projet
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

try:
    django.setup()
    print("✅ Django configuré avec succès")
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

print("🧪 TEST AVEC AUTHENTIFICATION (CORRIGÉ)")
print("="*50)

try:
    from django.test import RequestFactory
    from django.contrib.auth.models import User, Group
    from assureur import views
    
    # Créer un utilisateur test
    try:
        # Essayer de récupérer un utilisateur existant
        user = User.objects.filter(username='test_assureur').first()
        
        if not user:
            # Créer un nouvel utilisateur
            user = User.objects.create_user(
                username='test_assureur',
                email='test@assureur.com',
                password='testpass123'
            )
            print("✅ Nouvel utilisateur créé")
        else:
            print("✅ Utilisateur existant trouvé")
        
        # Vérifier/créer le groupe assureur
        assureur_group, created = Group.objects.get_or_create(name='assureur')
        user.groups.add(assureur_group)
        user.is_staff = True
        user.save()
        
        print(f"✅ Utilisateur '{user.username}' ajouté au groupe 'assureur'")
        
    except Exception as e:
        print(f"⚠️  Erreur création utilisateur: {e}")
        # Utiliser un superuser existant
        user = User.objects.filter(is_superuser=True).first()
        if user:
            print(f"✅ Utilisation du superuser: {user.username}")
        else:
            print("❌ Aucun utilisateur disponible")
            sys.exit(1)
    
    # Test 1 : Requête sans filtre
    print("\n🔍 Test 1: Requête sans filtre")
    factory = RequestFactory()
    request = factory.get('/assureur/membres/')
    request.user = user
    
    try:
        response = views.liste_membres(request)
        print(f"✅ Réponse générée: {response}")
        
        # Vérifier si c'est un HttpResponse
        if hasattr(response, 'content'):
            content = response.content.decode('utf-8', errors='ignore')
            print(f"✅ Contenu généré ({len(content)} caractères)")
            
            # Vérifications rapides
            checks = [
                ('numero_unique', '✅ Template utilise numero_unique'),
                ('date_inscription', '✅ Template utilise date_inscription'),
                ('ASIA', '✅ Mot "ASIA" présent'),
                ('Koné', '✅ Mot "Koné" présent'),
                ('DRAMANE', '✅ Mot "DRAMANE" présent'),
            ]
            
            for text, message in checks:
                if text in content:
                    print(message)
                else:
                    print(f"⚠️  '{text}' non trouvé")
                    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2 : Recherche 'ASIA'
    print("\n🔍 Test 2: Recherche 'ASIA'")
    request2 = factory.get('/assureur/membres/?q=ASIA')
    request2.user = user
    
    try:
        response2 = views.liste_membres(request2)
        print(f"✅ Réponse générée pour la recherche")
        
        if hasattr(response2, 'content'):
            content = response2.content.decode('utf-8', errors='ignore')
            
            # Compter approximativement les résultats
            asia_count = content.upper().count('ASIA')
            print(f"✅ Le mot 'ASIA' apparaît {asia_count} fois")
            
            # Chercher des indicateurs de résultats
            if 'Aucun résultat' in content or '0 membre' in content:
                print("⚠️  Aucun résultat trouvé")
            elif '2 membre' in content or '2 résultat' in content:
                print("✅ 2 résultats trouvés (correspond à la base de données)")
                
    except Exception as e:
        print(f"❌ Erreur: {e}")
        
except Exception as e:
    print(f"❌ Erreur générale: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)
print("🎉 TEST TERMINÉ")