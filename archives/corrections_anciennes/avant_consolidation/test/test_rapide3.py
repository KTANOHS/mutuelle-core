# test_rapide.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from agents.models import Membre
from django.db.models import Q

print("🔍 TEST RAPIDE DE LA RECHERCHE")
print("="*50)

# 1. Compter les données
print(f"Total membres: {Membre.objects.count()}")

# 2. Tester différentes recherches
test_cases = [
    ('ASIA', 'nom/prénom'),
    ('Jean', 'nom/prénom'),
    ('Dupont', 'nom'),
    ('test', 'email'),
    ('MEM', 'numéro'),
    ('@', 'tous les emails'),
]

for term, description in test_cases:
    count = Membre.objects.filter(
        Q(nom__icontains=term) |
        Q(prenom__icontains=term) |
        Q(email__icontains=term) |
        Q(numero_unique__icontains=term) |
        Q(telephone__icontains=term)
    ).count()
    
    print(f"• '{term}' ({description}): {count} résultat(s)")

# 3. Afficher quelques exemples
print("\n📋 EXEMPLES DE DONNÉES:")
for m in Membre.objects.all()[:3]:
    print(f"  • {m.prenom} {m.nom} - {m.numero_unique} - {m.email}")

# 4. Vérifier les champs critiques
print("\n✅ VÉRIFICATION DES CHAMPS:")
sample = Membre.objects.first()
if sample:
    fields = ['numero_unique', 'date_inscription', 'statut', 'nom', 'prenom']
    for field in fields:
        exists = hasattr(sample, field)
        value = getattr(sample, field, 'N/A')
        status = "✓" if exists else "✗"
        print(f"  {status} {field}: {value}")

print("\n" + "="*50)
print("🎯 Si 'ASIA' > 0, la recherche fonctionne!")
print("="*50)