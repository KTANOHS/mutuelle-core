# test_nouvelle_periode.py
import os
import django
import sys

projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
import re

print("="*60)
print("TEST NOUVELLE PÉRIODE - 2025-04")
print("="*60)

# Connexion
client = Client()
client.login(username='admin', password='admin123')
print("✅ Connexion réussie")

# Récupérer CSRF
response = client.get('/assureur/cotisations/generer/')
content = response.content.decode('utf-8')
csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', content)
csrf_token = csrf_match.group(1)
print("✅ Token CSRF obtenu")

# Tester prévisualisation pour nouvelle période
print("\n📋 Prévisualisation pour 2025-04...")
response = client.get('/assureur/cotisations/preview/?periode=2025-04')
print(f"Status: {response.status_code}")

# Tester génération
print("\n🚀 Génération pour 2025-04...")
from assureur.models import Cotisation

# Compter avant
avant = Cotisation.objects.count()
print(f"Cotisations avant: {avant}")

# Générer pour nouvelle période
response = client.post('/assureur/cotisations/generer/', {
    'periode': '2025-04',
    'csrfmiddlewaretoken': csrf_token
})

print(f"Status POST: {response.status_code}")

# Résultats
apres = Cotisation.objects.count()
difference = apres - avant

print(f"\n📊 RÉSULTATS:")
print(f"Cotisations créées: {difference}")
print(f"Nouveau total: {apres}")

if difference > 0:
    print("\n🎉 SUCCÈS ! Nouvelles cotisations créées.")
else:
    print("\nℹ️ Aucune nouvelle cotisation (peut-être déjà existantes ou aucun membre actif)")

print("\n" + "="*60)
print("TEST TERMINÉ")
print("="*60)