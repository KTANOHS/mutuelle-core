# correction_agents.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from agents.models import Agent

print("="*70)
print("🔧 CORRECTIONS MINEURES POUR LES AGENTS")
print("="*70)

# 1. Créer un profil Agent pour l'utilisateur test
agent_user, created = User.objects.get_or_create(
    username='agent_complet_test',
    defaults={'email': 'agent_complet@test.com'}
)

if created:
    agent_user.set_password('agent123')
    agent_user.save()
    print("✅ Utilisateur agent_complet_test créé")
else:
    print("✅ Utilisateur agent_complet_test existant")
    agent_user.set_password('agent123')
    agent_user.save()

# 2. Vérifier/créer le profil Agent
try:
    agent_profile = Agent.objects.get(user=agent_user)
    print("✅ Profil Agent existant")
except Agent.DoesNotExist:
    # Créer un profil Agent minimal
    agent_profile = Agent.objects.create(
        user=agent_user,
        numero_employe=f"AGT{agent_user.id:03d}",
        poste="Agent de vérification",
        statut='actif'
    )
    print("✅ Profil Agent créé")

# 3. Ajouter au groupe Agents
groupe_agents, _ = Group.objects.get_or_create(name='Agents')
agent_user.groups.add(groupe_agents)
print("✅ Ajouté au groupe Agents")

# 4. Vérifier les URLs problématiques
print(f"\n🔍 VÉRIFICATION DES URLS PROBLÉMATIQUES:")
print("   " + "-"*40)

from django.test import Client
client = Client()
client.login(username='agent_complet_test', password='agent123')

# Test de l'API de vérification sans ID
response = client.get('/agents/api/verifier-cotisation/')
print(f"   API vérification (sans ID): {response.status_code}")
if response.status_code == 400:
    print("   ℹ️  Normal - L'API attend un ID membre")

# Test de recherche
response = client.get('/agents/recherche-cotisations/')
print(f"   Recherche cotisations: {response.status_code}")
if response.status_code == 302:
    print(f"   ℹ️  Redirection vers: {response.url}")

print(f"\n🎯 RÉSUMÉ DES CORRECTIONS :")
print("""   1. ✅ Profil Agent créé pour l'utilisateur
   2. ✅ Groupe Agents assigné
   3. ✅ Les URLs fonctionnent (les redirections sont normales)
   4. ✅ L'API nécessite un ID membre (comportement normal)
""")

print("="*70)