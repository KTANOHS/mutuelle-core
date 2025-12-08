# test_permissions.py
import os
import django
import sys

sys.path.append('/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

print("🔐 Vérification des permissions assureur")
print("="*50)

# Chercher le groupe assureur
try:
    assureur_group = Group.objects.get(name='assureur')
    print(f"✅ Groupe 'assureur' trouvé")
    print(f"   Membres: {[u.username for u in assureur_group.user_set.all()]}")
    print(f"   Permissions: {assureur_group.permissions.count()}")
except Group.DoesNotExist:
    print("❌ Groupe 'assureur' non trouvé")

# Vérifier les permissions de l'utilisateur assureur_system
try:
    user = User.objects.get(username='assureur_system')
    print(f"\n👤 Utilisateur: {user.username}")
    print(f"   Groupes: {[g.name for g in user.groups.all()]}")
    print(f"   Permissions: {user.user_permissions.count()}")
    print(f"   Toutes permissions: {user.get_all_permissions()}")
except User.DoesNotExist:
    print("❌ Utilisateur assureur_system non trouvé")