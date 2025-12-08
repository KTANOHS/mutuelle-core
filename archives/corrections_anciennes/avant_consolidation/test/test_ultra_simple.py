# test_ultra_simple.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

print("🔍 TEST ULTRA SIMPLE")
print("="*50)

# Vérification la plus basique
from agents.models import Membre
from django.db.models import Q

# Recherche dans la base
asia_count = Membre.objects.filter(
    Q(nom__icontains='ASIA') | Q(prenom__icontains='ASIA')
).count()

print(f"✅ Recherche 'ASIA' en base : {asia_count} résultat(s)")

if asia_count == 2:
    print("✅ CORRECT : DRAMANE ASIA et Koné Asia")
    
    # Afficher les détails
    membres = Membre.objects.filter(
        Q(nom__icontains='ASIA') | Q(prenom__icontains='ASIA')
    )
    
    for m in membres:
        print(f"  • {m.id}: {m.prenom} {m.nom} - {m.numero_unique}")
else:
    print(f"❌ ATTENDU : 2 résultats, obtenu : {asia_count}")

print("\n🚀 Pour tester dans le navigateur :")
print("1. python manage.py runserver")
print("2. http://127.0.0.1:8000/assureur/membres/?q=ASIA")
print("="*50)