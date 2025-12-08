# verifier_acces_agents.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from assureur.models import Cotisation, Membre

print("="*70)
print("🔍 VÉRIFICATION DE L'ACCÈS DES AGENTS")
print("="*70)

# 1. Vérifier si le groupe "Agents" existe
try:
    groupe_agents = Group.objects.get(name='Agents')
    print(f"✅ Groupe 'Agents' trouvé: {groupe_agents}")
    
    # Voir les permissions du groupe
    print(f"\n🔐 Permissions du groupe 'Agents':")
    for perm in groupe_agents.permissions.all():
        print(f"   - {perm.codename}: {perm.name}")
    
except Group.DoesNotExist:
    print("❌ Groupe 'Agents' non trouvé")

# 2. Vérifier les permissions pour le modèle Cotisation
print(f"\n📋 Permissions disponibles pour le modèle Cotisation:")
cotisation_ct = ContentType.objects.get_for_model(Cotisation)
permissions_cotisation = Permission.objects.filter(content_type=cotisation_ct)

for perm in permissions_cotisation:
    print(f"   - {perm.codename}: {perm.name}")

# 3. Vérifier les permissions pour le modèle Membre
print(f"\n👥 Permissions disponibles pour le modèle Membre:")
membre_ct = ContentType.objects.get_for_model(Membre)
permissions_membre = Permission.objects.filter(content_type=membre_ct)

for perm in permissions_membre:
    print(f"   - {perm.codename}: {perm.name}")

# 4. Vérifier les URLs des agents
print(f"\n🌐 URLs disponibles pour les agents:")
try:
    import agents.urls
    print("   URL Patterns dans agents.urls:")
    for pattern in agents.urls.urlpatterns:
        print(f"   - {pattern.pattern}")
except Exception as e:
    print(f"   ❌ Impossible d'importer agents.urls: {e}")

print("\n" + "="*70)
print("📊 SYNTHÈSE DE L'ACCÈS")
print("="*70)