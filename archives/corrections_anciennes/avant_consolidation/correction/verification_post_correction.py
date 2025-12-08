# verification_post_correction.py
import os
import sys
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from django.contrib.auth.models import User
from membres.models import Membre
from django.db.models import Count, Q

print("✅ VÉRIFICATION POST-CORRECTION")
print("=" * 50)

# Statistiques après correction
total_users = User.objects.count()
total_membres = Membre.objects.count()
membres_avec_user = Membre.objects.filter(user__isnull=False).count()
membres_sans_user = Membre.objects.filter(user__isnull=True).count()

print(f"📊 STATISTIQUES:")
print(f"   👥 Utilisateurs: {total_users}")
print(f"   👤 Membres: {total_membres}")
print(f"   🔗 Membres avec user: {membres_avec_user}")
print(f"   ❌ Membres sans user: {membres_sans_user}")

if total_membres > 0:
    ratio = (membres_avec_user / total_membres) * 100
    print(f"   📈 Taux de synchronisation: {ratio:.1f}%")
    
    if ratio == 100:
        print("🎉 SYNCHRONISATION COMPLÈTE!")
    elif ratio >= 90:
        print("✅ SYNCHRONISATION EXCELLENTE")
    elif ratio >= 75:
        print("⚠️  SYNCHRONISATION BONNE")
    else:
        print("🚨 SYNCHRONISATION INSUFFISANTE")

# Vérifier l'intégrité des numéros uniques
try:
    doublons = Membre.objects.values('numero_unique').annotate(
        count=Count('id')
    ).filter(count__gt=1, numero_unique__isnull=False)
    
    if doublons.exists():
        print(f"\n⚠️  {doublons.count()} numéros uniques encore en double")
    else:
        print(f"\n✅ Aucun numéro unique en double")

except Exception as e:
    print(f"\n⚠️  Vérification numéros: {e}")

# Membres sans numéro unique
try:
    sans_numero = Membre.objects.filter(
        Q(numero_unique__isnull=True) | Q(numero_unique='')
    ).count()
    
    if sans_numero > 0:
        print(f"⚠️  {sans_numero} membres sans numéro unique")
    else:
        print(f"✅ Tous les membres ont un numéro unique")

except Exception as e:
    print(f"⚠️  Vérification numéros manquants: {e}")

print("\n" + "=" * 50)
print("🎯 ÉTAT FINAL DE LA SYNCHRONISATION")
print("=" * 50)