#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC DES PERMISSIONS ET REDIRECTIONS
Analyse complète du système d'authentification et de permissions
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Initialiser Django
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse, resolve, Resolver404
from django.test import Client
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
import json

print("=" * 80)
print("DIAGNOSTIC COMPLET DES PERMISSIONS")
print("=" * 80)

# ============================================================================
# SECTION 1: VÉRIFICATION DES GROUPES ET PERMISSIONS
# ============================================================================

print("\n🔐 SECTION 1: GROUPES ET PERMISSIONS")
print("-" * 40)

# Lister tous les groupes
print("\n📋 GROUPES DISPONIBLES:")
print("-" * 30)
groups = Group.objects.all()
for group in groups:
    permissions = group.permissions.all()
    print(f"• {group.name} ({group.user_set.count()} utilisateurs)")
    for perm in permissions[:3]:  # Afficher seulement 3 permissions
        print(f"  - {perm.codename}")
    if permissions.count() > 3:
        print(f"  ... et {permissions.count() - 3} autres permissions")

# ============================================================================
# SECTION 2: ANALYSE DES UTILISATEURS
# ============================================================================

print("\n👥 SECTION 2: UTILISATEURS ET LEURS PERMISSIONS")
print("-" * 40)

users = User.objects.all().order_by('id')
for user in users:
    print(f"\n👤 {user.username} (ID: {user.id})")
    print(f"   📧 Email: {user.email or 'Non défini'}")
    print(f"   👑 Superuser: {user.is_superuser}")
    print(f"   🏢 Staff: {user.is_staff}")
    print(f"   🔐 Actif: {user.is_active}")
    
    # Groupes
    user_groups = user.groups.all()
    if user_groups:
        print(f"   🏷️  Groupes: {[g.name for g in user_groups]}")
    else:
        print(f"   🏷️  Groupes: Aucun")
    
    # Permissions directes
    user_perms = user.user_permissions.all()
    if user_perms:
        print(f"   🔑 Permissions directes:")
        for perm in user_perms[:5]:
            print(f"      - {perm.name}")
        if user_perms.count() > 5:
            print(f"      ... et {user_perms.count() - 5} autres")

# ============================================================================
# SECTION 3: VÉRIFICATION DES PROBLÈMES IDENTIFIÉS
# ============================================================================

print("\n⚠️ SECTION 3: PROBLÈMES IDENTIFIÉS DANS LES LOGS")
print("-" * 40)

# 1. Problème DOUA1 (Assureur détecté comme Membre)
print("\n1. PROBLÈME DOUA1:")
doua1 = User.objects.filter(username='DOUA1').first()
if doua1:
    print(f"   ✅ DOUA1 existe (ID: {doua1.id})")
    groups = doua1.groups.all()
    print(f"   🏷️  Groupes: {[g.name for g in groups]}")
    
    # Vérifier la logique de détection
    from django.contrib.auth.models import Group
    
    is_assureur = groups.filter(name='Assureur').exists()
    is_membre = groups.filter(name='Membre').exists()
    
    print(f"   📊 Vérification:")
    print(f"      • Dans groupe Assureur: {is_assureur}")
    print(f"      • Dans groupe Membre: {is_membre}")
    
    if is_assureur and not is_membre:
        print("   ❌ PROBLÈME: DOUA1 est dans 'Assureur' mais détecté comme 'MEMBRE'")
        print("      Solution: Vérifier la fonction get_user_primary_group()")

# 2. Problème des assureurs redirigés vers /admin/
print("\n2. PROBLÈME REDIRECTION ASSUREURS:")
assureurs = User.objects.filter(groups__name='Assureur')
for assureur in assureurs:
    print(f"\n   👤 {assureur.username}:")
    print(f"      👑 Superuser: {assureur.is_superuser}")
    print(f"      🏢 Staff: {assureur.is_staff}")
    
    # Vérifier les permissions admin
    can_access_admin = assureur.is_staff and assureur.is_active
    print(f"      🔐 Peut accéder à /admin/: {can_access_admin}")
    
    if can_access_admin:
        print("      ⚠️  Attention: Les assureurs staff sont redirigés vers /admin/")
        print("      Solution: Créer un décorateur @assureur_required spécifique")

# 3. Problème ORNELLA (Agent non trouvé)
print("\n3. PROBLÈME ORNELLA (Agent):")
ornella = User.objects.filter(username='ORNELLA').first()
if ornella:
    print(f"   ✅ ORNELLA existe (ID: {ornella.id})")
    
    # Vérifier si c'est un agent
    is_agent = ornella.groups.filter(name='Agent').exists()
    print(f"   🏷️  Dans groupe Agent: {is_agent}")
    
    if is_agent:
        # Vérifier le modèle Agent associé
        try:
            from agents.models import Agent
            agent_profile = Agent.objects.filter(user=ornella).first()
            if agent_profile:
                print(f"   ✅ Profil Agent trouvé: {agent_profile}")
            else:
                print("   ❌ PROBLÈME: Pas de profil Agent associé")
                print("      Solution: Créer un objet Agent pour ORNELLA")
        except ImportError:
            print("   ⚠️  Modèle Agent non disponible")
        except Exception as e:
            print(f"   ⚠️  Erreur: {e}")

# ============================================================================
# SECTION 4: TEST DES REDIRECTIONS AVEC CLIENT HTTP
# ============================================================================

print("\n🌐 SECTION 4: TEST DES REDIRECTIONS HTTP")
print("-" * 40)

client = Client()
test_users = ['DOUA', 'DOUA1', 'ktanos', 'ORNELLA']

print("\n🔍 Test des connexions et redirections:")
print("-" * 30)

for username in test_users:
    user = User.objects.filter(username=username).first()
    if not user:
        print(f"❌ {username}: Utilisateur non trouvé")
        continue
    
    # Tenter de se connecter
    print(f"\n👤 Test {username}:")
    
    # Tester la connexion (on suppose que le mot de passe est le nom d'utilisateur)
    try:
        # Tenter une connexion
        login_success = client.login(username=username, password=username)
        
        if login_success:
            print(f"   ✅ Connexion réussie")
            
            # Accéder à la page de redirection après login
            response = client.get('/redirect-after-login/', follow=True)
            
            if response.redirect_chain:
                print(f"   🔗 Redirections:")
                for i, (url, status) in enumerate(response.redirect_chain):
                    print(f"      {i+1}. {status} -> {url}")
            
            # Vérifier la page finale
            final_url = response.request['PATH_INFO']
            print(f"   🎯 Page finale: {final_url}")
            
            # Déconnexion pour le prochain test
            client.logout()
        else:
            print(f"   ❌ Échec de connexion")
            print(f"      Essayez avec: client.login(username='{username}', password='{username}')")
            
    except Exception as e:
        print(f"   ⚠️  Erreur lors du test: {e}")

# ============================================================================
# SECTION 5: VÉRIFICATION DES DÉCORATEURS DE PERMISSION
# ============================================================================

print("\n🔧 SECTION 5: DÉCORATEURS DE PERMISSION")
print("-" * 40)

# Vérifier si les décorateurs personnalisés existent
print("\n🔍 Recherche des décorateurs:")
decorators_to_check = [
    'assureur_required',
    'agent_required', 
    'medecin_required',
    'pharmacien_required',
    'membre_required'
]

try:
    # Importer les utilitaires pour vérifier
    from core.utils import (
        get_user_primary_group,
        get_user_redirect_url,
        get_user_type,
        user_is_assureur,
        user_is_agent,
        user_is_medecin,
        user_is_pharmacien,
        est_assureur,
        est_agent,
        est_medecin,
        est_pharmacien
    )
    
    print("✅ Module core.utils importé avec succès")
    
    # Tester les fonctions
    test_user = User.objects.filter(username='DOUA').first()
    if test_user:
        print(f"\n🧪 Test des fonctions avec DOUA:")
        print(f"   • get_user_primary_group: {get_user_primary_group(test_user)}")
        print(f"   • get_user_type: {get_user_type(test_user)}")
        print(f"   • get_user_redirect_url: {get_user_redirect_url(test_user)}")
        print(f"   • user_is_assureur: {user_is_assureur(test_user)}")
        print(f"   • est_assureur: {est_assureur(test_user)}")
        
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
except Exception as e:
    print(f"⚠️  Erreur: {e}")

# ============================================================================
# SECTION 6: CORRECTIONS RECOMMANDÉES
# ============================================================================

print("\n🔨 SECTION 6: CORRECTIONS RECOMMANDÉES")
print("-" * 40)

print("\n1. CORRECTION DOUA1:")
print("   " + "=" * 20)
print("""
   DOUA1 est dans le groupe 'Assureur' mais détecté comme 'MEMBRE'.
   Problème probable dans la fonction get_user_type() ou user_is_assureur().
   
   Solution:
   - Vérifier la fonction user_is_assureur() dans core/utils.py
   - S'assurer qu'elle vérifie correctement le groupe 'Assureur'
   - Tester avec DOUA1: user.groups.filter(name='Assureur').exists()
""")

print("\n2. CORRECTION REDIRECTION ASSUREURS:")
print("   " + "=" * 20)
print("""
   Les assureurs (DOUA, ktanos) sont redirigés vers /admin/ au lieu de /assureur/
   Problème: Ils ont is_staff=True, donc Django les redirige vers /admin/
   
   Solutions possibles:
   1. Créer un décorateur @assureur_required personnalisé
   2. Modifier la vue /assureur/ pour utiliser @login_required seulement
   3. Mettre is_staff=False pour les assureurs
""")

print("\n3. CORRECTION ORNELLA (Agent):")
print("   " + "=" * 20)
print("""
   ORNELLA n'a pas de profil Agent associé.
   Cela cause des erreurs dans les vues agents.
   
   Solution:
   python manage.py shell -c "
   from django.contrib.auth.models import User
   from agents.models import Agent
   
   user = User.objects.get(username='ORNELLA')
   agent, created = Agent.objects.get_or_create(
       user=user,
       defaults={
           'nom': 'ORNELLA',
           'prenom': 'Agent',
           'telephone': '0102030405',
           'email': 'ornella@agent.com'
       }
   )
   print(f'Agent créé: {created}')
   "
""")

print("\n4. CONFIGURATION DES MOTS DE PASSE:")
print("   " + "=" * 20)
print("""
   Pour tester les connexions, définir des mots de passe:
   
   python manage.py shell -c "
   from django.contrib.auth.models import User
   
   users = ['DOUA', 'DOUA1', 'ktanos', 'ORNELLA', 'Yacouba', 'GLORIA', 'ASIA']
   for username in users:
       try:
           user = User.objects.get(username=username)
           user.set_password(username)  # MDP = nom d'utilisateur
           user.save()
           print(f'MDP défini pour {username}')
       except:
           pass
   "
""")

# ============================================================================
# SECTION 7: SCRIPT DE CORRECTION AUTOMATIQUE
# ============================================================================

print("\n⚡ SECTION 7: SCRIPT DE CORRECTION AUTOMATIQUE")
print("-" * 40)

correction_script = """
#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group

print("🔧 APPLICATION DES CORRECTIONS...")

# 1. Vérifier et corriger DOUA1
print("\\n1. Correction DOUA1...")
doua1 = User.objects.filter(username='DOUA1').first()
if doua1:
    # S'assurer qu'il n'est que dans Assureur
    assureur_group = Group.objects.get(name='Assureur')
    doua1.groups.clear()
    doua1.groups.add(assureur_group)
    doua1.is_staff = False  # Empêcher la redirection vers /admin/
    doua1.save()
    print("   ✅ DOUA1 corrigé: uniquement dans groupe Assureur, is_staff=False")

# 2. Créer le profil Agent pour ORNELLA
print("\\n2. Création profil Agent pour ORNELLA...")
try:
    from agents.models import Agent
    ornella = User.objects.get(username='ORNELLA')
    agent, created = Agent.objects.get_or_create(
        user=ornella,
        defaults={
            'nom': 'ORNELLA',
            'prenom': 'Agent',
            'telephone': '0102030405',
            'email': 'ornella@agent.com',
            'est_actif': True
        }
    )
    if created:
        print("   ✅ Profil Agent créé pour ORNELLA")
    else:
        print("   ℹ️  Profil Agent existe déjà")
except Exception as e:
    print(f"   ⚠️  Impossible de créer le profil Agent: {e}")

# 3. Définir les mots de passe
print("\\n3. Définition des mots de passe...")
users_to_fix = ['DOUA', 'DOUA1', 'ktanos', 'ORNELLA', 'Yacouba', 'GLORIA', 'ASIA']
for username in users_to_fix:
    try:
        user = User.objects.get(username=username)
        user.set_password(username)  # MDP = nom d'utilisateur
        user.save()
        print(f"   ✅ MDP défini pour {username}")
    except Exception as e:
        print(f"   ❌ Erreur pour {username}: {e}")

print("\\n✅ CORRECTIONS TERMINÉES")
print("\\n📋 POUR TESTER:")
print("1. Redémarrez le serveur: python manage.py runserver")
print("2. Connectez-vous avec:")
print("   - DOUA / DOUA → /assureur/")
print("   - ORNELLA / ORNELLA → /agents/tableau-de-bord/")
"""

print("\n📝 Script de correction automatique:")
print("-" * 30)
print(correction_script)

# Demander si on veut exécuter les corrections
response = input("\n🚀 Voulez-vous exécuter les corrections maintenant ? (o/N): ")
if response.lower() == 'o':
    print("\n🔧 Exécution des corrections...")
    
    # 1. Vérifier et corriger DOUA1
    print("\n1. Correction DOUA1...")
    doua1 = User.objects.filter(username='DOUA1').first()
    if doua1:
        # S'assurer qu'il n'est que dans Assureur
        assureur_group = Group.objects.get(name='Assureur')
        doua1.groups.clear()
        doua1.groups.add(assureur_group)
        doua1.is_staff = False  # Empêcher la redirection vers /admin/
        doua1.save()
        print("   ✅ DOUA1 corrigé: uniquement dans groupe Assureur, is_staff=False")
    
    # 2. Définir les mots de passe
    print("\n2. Définition des mots de passe...")
    users_to_fix = ['DOUA', 'DOUA1', 'ktanos', 'ORNELLA', 'Yacouba', 'GLORIA', 'ASIA']
    for username in users_to_fix:
        try:
            user = User.objects.get(username=username)
            user.set_password(username)  # MDP = nom d'utilisateur
            user.save()
            print(f"   ✅ MDP défini pour {username}")
        except Exception as e:
            print(f"   ❌ Erreur pour {username}: {e}")
    
    print("\n✅ CORRECTIONS TERMINÉES")
    
else:
    print("\nℹ️  Correction non exécutée. Copiez le script ci-dessus pour l'exécuter manuellement.")

# ============================================================================
# SECTION 8: TESTS FINAUX
# ============================================================================

print("\n🧪 SECTION 8: TESTS FINAUX DE VALIDATION")
print("-" * 40)

print("\nPour tester manuellement après corrections:")
print("1. Redémarrez le serveur:")
print("   python manage.py runserver")
print("\n2. Testez les connexions:")
print("   http://127.0.0.1:8000/accounts/login/")
print("\n3. Identifiants de test:")
print("   - DOUA (Assureur) → devrait aller sur /assureur/")
print("   - ORNELLA (Agent) → devrait aller sur /agents/tableau-de-bord/")
print("   - DOUA1 (Assureur) → devrait aller sur /assureur/")
print("\n4. Vérifiez les logs pour voir les redirections.")

# ============================================================================
# EXPORT DU RAPPORT
# ============================================================================

print("\n" + "=" * 80)
print("DIAGNOSTIC TERMINÉ")
print("=" * 80)

# Exporter le rapport
with open('diagnostic_permissions.txt', 'w') as f:
    f.write("=" * 80 + "\n")
    f.write("RAPPORT DE DIAGNOSTIC DES PERMISSIONS\n")
    f.write("=" * 80 + "\n")
    
    # Récupérer le contenu affiché (simplifié)
    import io
    from contextlib import redirect_stdout
    
    f.write("\nProblèmes identifiés:\n")
    f.write("1. DOUA1: Assureur détecté comme Membre\n")
    f.write("2. Assureurs redirigés vers /admin/ au lieu de /assureur/\n")
    f.write("3. ORNELLA: Pas de profil Agent associé\n")
    
    f.write("\nSolutions recommandées:\n")
    f.write("1. Exécuter le script de correction\n")
    f.write("2. Vérifier les fonctions dans core/utils.py\n")
    f.write("3. Tester les redirections après correction\n")

print("\n📄 Rapport exporté: diagnostic_permissions.txt")
print("\n💡 Prochaines étapes:")
print("1. Exécutez les corrections si ce n'est pas fait")
print("2. Redémarrez le serveur")
print("3. Testez les connexions avec les différents utilisateurs")
print("4. Vérifiez que chaque type d'utilisateur va sur le bon dashboard")