# check_models_data.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("="*70)
print("🔍 COMPARAISON DES MODÈLES MEMBRE")
print("="*70)

try:
    from agents.models import Membre as MembreAgents
    print("✅ agents.models.Membre importé")
    count_agents = MembreAgents.objects.count()
    print(f"  Nombre d'objets: {count_agents}")
    if count_agents > 0:
        m = MembreAgents.objects.first()
        print(f"  Exemple: {m.nom} {m.prenom}")
        print(f"  Champs: {[f.name for f in MembreAgents._meta.fields[:5]]}...")
except Exception as e:
    print(f"❌ agents.models.Membre: {e}")

print()

try:
    from assureur.models import Membre as MembreAssureur
    print("✅ assureur.models.Membre importé")
    count_assureur = MembreAssureur.objects.count()
    print(f"  Nombre d'objets: {count_assureur}")
    if count_assureur > 0:
        m = MembreAssureur.objects.first()
        print(f"  Exemple: {m.nom} {m.prenom}")
        print(f"  Champs: {[f.name for f in MembreAssureur._meta.fields[:5]]}...")
except Exception as e:
    print(f"❌ assureur.models.Membre: {e}")

print("\n" + "="*70)