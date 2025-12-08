# test_generation_simple.py
import os
import django
import sys

# Configuration Django
projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

print("="*60)
print("TEST SIMPLIFIÉ - GÉNÉRATION DE COTISATIONS")
print("="*60)

# 1. Utiliser l'utilisateur existant (éviter les erreurs de création)
try:
    user = User.objects.get(username='admin')
    print(f"✅ Utilisation de l'utilisateur existant: {user.username}")
except:
    print("❌ Aucun utilisateur admin trouvé")
    exit(1)

# 2. Connexion
client = Client()
client.login(username='admin', password='admin123')
print("✅ Connexion réussie")

# 3. Récupérer la page génération
print("\n1. Accès page génération...")
response = client.get('/assureur/cotisations/generer/')
print(f"   Status: {response.status_code} - {'✅ OK' if response.status_code == 200 else '❌ Échec'}")

# 4. Extraire CSRF token
import re
content = response.content.decode('utf-8')
csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', content)

if not csrf_match:
    print("❌ Token CSRF non trouvé")
    exit(1)

csrf_token = csrf_match.group(1)
print(f"✅ Token CSRF obtenu")

# 5. Tester la prévisualisation
print("\n2. Test prévisualisation...")
response = client.get('/assureur/cotisations/preview/?periode=2025-03')
print(f"   Status: {response.status_code} - {'✅ OK' if response.status_code == 200 else '❌ Échec'}")

# 6. Tester la génération POST
print("\n3. Test génération POST...")
from assureur.models import Cotisation

avant = Cotisation.objects.count()
print(f"   Cotisations avant: {avant}")

response = client.post('/assureur/cotisations/generer/', {
    'periode': '2025-03',
    'csrfmiddlewaretoken': csrf_token
})

print(f"   Status POST: {response.status_code}")

# 7. Vérifier les résultats
apres = Cotisation.objects.count()
difference = apres - avant

print(f"\n📊 RÉSULTATS FINAUX:")
print(f"   Cotisations avant génération: {avant}")
print(f"   Cotisations après génération: {apres}")
print(f"   Nouvelles cotisations créées: {difference}")

if difference > 0:
    print(f"\n✅ SUCCÈS: {difference} cotisation(s) créée(s) avec succès!")
    
    # Afficher les détails
    nouvelles = Cotisation.objects.order_by('-id')[:difference]
    print("\n📋 DÉTAILS DES COTISATIONS CRÉÉES:")
    for i, cotisation in enumerate(nouvelles, 1):
        print(f"   {i}. {cotisation.reference} - {cotisation.membre.nom_complet if cotisation.membre else 'N/A'} - {cotisation.montant} FCFA")
    
    # Calculer le total
    total = sum(c.montant for c in nouvelles if c.montant)
    print(f"\n💰 TOTAL GÉNÉRÉ: {total} FCFA")
    
else:
    print(f"\n⚠ ATTENTION: Aucune nouvelle cotisation créée")
    print("   Raisons possibles:")
    print("   - Aucun membre actif")
    print("   - Cotisations déjà existantes pour cette période")

print("\n" + "="*60)
print("TEST TERMINÉ")
print("="*60)