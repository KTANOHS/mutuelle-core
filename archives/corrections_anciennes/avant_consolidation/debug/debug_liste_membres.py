# debug_liste_membres.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from assureur import views

print("🔍 DEBUG DE LA VUE liste_membres")
print("="*60)

# Créer une requête simulée
factory = RequestFactory()

# Créer un utilisateur test (ou utiliser un existant)
try:
    user = User.objects.get(username='DOUA')  # L'utilisateur de vos logs
    print(f"✅ Utilisateur trouvé: {user.username}")
except:
    user = User.objects.filter(is_superuser=True).first()
    if user:
        print(f"✅ Superuser utilisé: {user.username}")

# Test 1: Sans paramètre de recherche
print("\n1. Test sans recherche:")
request1 = factory.get('/assureur/membres/')
request1.user = user

try:
    response1 = views.liste_membres(request1)
    print(f"   Status: Simulé (pas de vrai HTTP)")
    
    # Extraire le contexte si possible
    if hasattr(response1, 'context_data'):
        ctx = response1.context_data
        print(f"   Context keys: {list(ctx.keys())}")
        
        if 'page_obj' in ctx:
            page_obj = ctx['page_obj']
            print(f"   page_obj: {len(page_obj)} éléments")
            for i, m in enumerate(page_obj[:3]):
                print(f"     {i+1}. {m.prenom} {m.nom} - {m.numero_unique}")
    else:
        print("   ❌ Pas de contexte disponible")
        
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# Test 2: Avec recherche 'ASIA'
print("\n2. Test avec recherche 'ASIA':")
request2 = factory.get('/assureur/membres/?q=ASIA')
request2.user = user

try:
    response2 = views.liste_membres(request2)
    print(f"   Status: Simulé (pas de vrai HTTP)")
    
    if hasattr(response2, 'context_data'):
        ctx = response2.context_data
        print(f"   Context keys: {list(ctx.keys())}")
        
        if 'page_obj' in ctx:
            page_obj = ctx['page_obj']
            print(f"   page_obj: {len(page_obj)} éléments")
            
            if len(page_obj) > 0:
                print("   ✅ Résultats trouvés:")
                for i, m in enumerate(page_obj):
                    print(f"     {i+1}. {m.prenom} {m.nom} - {m.numero_unique}")
            else:
                print("   ❌ Aucun résultat dans page_obj")
        else:
            print("   ❌ page_obj absent du contexte")
            
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# Test 3: Vérification directe de la base
print("\n3. Vérification directe dans la base:")
from agents.models import Membre
from django.db.models import Q

asia_membres = Membre.objects.filter(
    Q(nom__icontains='ASIA') | Q(prenom__icontains='ASIA')
)
print(f"   Résultats en base: {asia_membres.count()}")
for m in asia_membres:
    print(f"     • {m.id}: {m.prenom} {m.nom} - {m.numero_unique}")

print("\n" + "="*60)
print("🎯 Si les tests 1-2 montrent des résultats mais pas le navigateur,")
print("   le problème est dans le TEMPLATE.")
print("="*60)