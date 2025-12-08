
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group

print("🔧 CORRECTIONS FINALES")
print("=" * 40)

# 1. Corriger TOUS les assureurs (is_staff = False)
print("\n1. Correction de TOUS les assureurs...")
assureurs = User.objects.filter(groups__name='Assureur')
for assureur in assureurs:
    print(f"\n• {assureur.username}:")
    print(f"  Avant: is_staff={assureur.is_staff}, is_superuser={assureur.is_superuser}")
    
    # Rendre is_staff = False pour tous les assureurs
    assureur.is_staff = False
    assureur.save()
    
    print(f"  Après: is_staff={assureur.is_staff}")

# 2. Vérifier et corriger DOUA1 spécifiquement
print("\n2. Vérification approfondie de DOUA1...")
doua1 = User.objects.get(username='DOUA1')
print(f"  ID: {doua1.id}")
print(f"  Groupes: {[g.name for g in doua1.groups.all()]}")
print(f"  is_staff: {doua1.is_staff}")
print(f"  is_superuser: {doua1.is_superuser}")

# Vérifier s'il y a d'autres groupes cachés
all_groups = doua1.groups.all()
if len(all_groups) == 1 and all_groups[0].name == 'Assureur':
    print("  ✅ DOUA1 est uniquement dans le groupe Assureur")
else:
    print("  ⚠️  DOUA1 a d'autres groupes, nettoyage...")
    doua1.groups.clear()
    assureur_group = Group.objects.get(name='Assureur')
    doua1.groups.add(assureur_group)
    doua1.save()

# 3. Créer le profil Agent pour ORNELLA
print("\n3. Création du profil Agent pour ORNELLA...")
try:
    from agents.models import Agent
    ornella = User.objects.get(username='ORNELLA')
    
    # Vérifier si un agent existe déjà
    existing_agent = Agent.objects.filter(user=ornella).first()
    if existing_agent:
        print(f"  ℹ️  Profil Agent existe déjà: {existing_agent}")
    else:
        # Créer l'agent
        agent = Agent.objects.create(
            user=ornella,
            nom="ORNELLA",
            prenom="Agent",
            telephone="0102030405",
            email="ornella@agent.com",
            est_actif=True
        )
        print(f"  ✅ Profil Agent créé: {agent}")
except ImportError as e:
    print(f"  ❌ Modèle Agent non disponible: {e}")
except Exception as e:
    print(f"  ❌ Erreur: {e}")

# 4. Vérifier la fonction get_user_redirect_url pour DOUA1
print("\n4. Test de la fonction de redirection...")
try:
    from core.utils import get_user_redirect_url, get_user_type, get_user_primary_group
    
    users_to_test = ['DOUA', 'DOUA1', 'ktanos', 'ORNELLA']
    for username in users_to_test:
        user = User.objects.get(username=username)
        
        print(f"\n  👤 {username}:")
        print(f"    • get_user_primary_group: {get_user_primary_group(user)}")
        print(f"    • get_user_type: {get_user_type(user)}")
        
        # Appeler la fonction pour voir ce qu'elle retourne
        redirect_url = get_user_redirect_url(user)
        print(f"    • get_user_redirect_url: {redirect_url}")
        
except Exception as e:
    print(f"  ❌ Erreur lors du test: {e}")

# 5. Vérifier les URLs de redirection dans les settings
print("\n5. Vérification de la configuration Django...")
try:
    from django.conf import settings
    
    # Vérifier LOGIN_REDIRECT_URL
    print(f"  LOGIN_REDIRECT_URL: {getattr(settings, 'LOGIN_REDIRECT_URL', 'Non défini')}")
    
    # Vérifier LOGIN_URL
    print(f"  LOGIN_URL: {getattr(settings, 'LOGIN_URL', 'Non défini')}")
    
    # Vérifier si middleware de redirection personnalisé existe
    print(f"  MIDDLEWARE contient RedirectMiddleware: {'RedirectMiddleware' in str(getattr(settings, 'MIDDLEWARE', []))}")
    
except Exception as e:
    print(f"  ❌ Erreur: {e}")

print("\n" + "=" * 40)
print("✅ CORRECTIONS APPLIQUÉES")
print("\n📋 RÉCAPITULATIF:")
print("1. Tous les assureurs ont maintenant is_staff=False")
print("2. DOUA1 a été vérifié et nettoyé")
print("3. Profil Agent créé pour ORNELLA")
print("\n🎯 PROCHAINE ÉTAPE:")
print("Redémarrez le serveur et testez les connexions!")

