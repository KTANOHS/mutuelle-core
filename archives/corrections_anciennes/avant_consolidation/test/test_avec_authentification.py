# test_avec_authentification.py
import os
import django
from django.test import RequestFactory
from django.contrib.auth.models import User, Group

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from assureur import views

print("🧪 TEST AVEC AUTHENTIFICATION")
print("="*50)

# Créer un utilisateur test
try:
    user, created = User.objects.get_or_create(
        username='test_assureur',
        defaults={'email': 'test@assureur.com', 'password': 'test123'}
    )
    
    # Ajouter au groupe assureur
    assureur_group, _ = Group.objects.get_or_create(name='assureur')
    user.groups.add(assureur_group)
    user.is_staff = True
    user.save()
    
    print(f"✅ Utilisateur créé: {user.username}")
    
except Exception as e:
    print(f"⚠️  Erreur création utilisateur: {e}")
    # Utiliser un utilisateur existant
    user = User.objects.filter(groups__name='assureur').first()
    if user:
        print(f"✅ Utilisation de l'utilisateur existant: {user.username}")
    else:
        user = User.objects.filter(is_superuser=True).first()
        if user:
            print(f"✅ Utilisation du superuser: {user.username}")

# Tester la vue
factory = RequestFactory()

print("\n🔍 Test 1: Requête sans filtre")
request = factory.get('/assureur/membres/')
request.user = user

try:
    response = views.liste_membres(request)
    print("✅ Vue exécutée sans erreur")
    
    # Si c'est un HttpResponse
    if hasattr(response, 'content'):
        print(f"✅ Réponse générée ({len(response.content)} bytes)")
        
        # Extraire le HTML pour vérification rapide
        content = response.content.decode('utf-8', errors='ignore')
        
        if 'ASIA' in content:
            print("✅ Le résultat 'ASIA' est dans la réponse")
        if 'Koné' in content or 'DRAMANE' in content:
            print("✅ Les noms recherchés sont présents")
            
        # Vérifier les champs
        if 'numero_unique' in content:
            print("✅ Template utilise 'numero_unique'")
        else:
            print("⚠️  'numero_unique' non trouvé dans le template")
            
        if 'date_inscription' in content:
            print("✅ Template utilise 'date_inscription'")
        else:
            print("⚠️  'date_inscription' non trouvé dans le template")
            
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

print("\n🔍 Test 2: Recherche 'ASIA'")
request2 = factory.get('/assureur/membres/?q=ASIA')
request2.user = user

try:
    response2 = views.liste_membres(request2)
    print("✅ Recherche exécutée sans erreur")
    
    if hasattr(response2, 'content'):
        content = response2.content.decode('utf-8', errors='ignore')
        
        # Compter les occurrences de "ASIA" (approximatif)
        asia_count = content.upper().count('ASIA')
        print(f"✅ Le mot 'ASIA' apparaît {asia_count} fois dans la réponse")
        
except Exception as e:
    print(f"❌ Erreur: {e}")

print("\n" + "="*50)
print("🎉 TEST TERMINÉ")