# test_final_integration_fixed.py
import os
import django
from django.test import Client
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
django.setup()

print("=== TEST D'INTÉGRATION FINAL ===")

# 1. Vérifier les données
from assureur.models import Membre, Cotisation
print("1. Données dans la base :")
print(f"   - Membres actifs: {Membre.objects.filter(statut='actif').count()}")
print(f"   - Cotisations totales: {Cotisation.objects.count()}")

# 2. Créer un superutilisateur pour les tests
try:
    user = User.objects.create_user(
        username='test_admin',
        password='test123',
        is_staff=True,
        is_superuser=True
    )
    print("2. Utilisateur de test créé")
except Exception as e:
    user = User.objects.get(username='test_admin')
    print("2. Utilisateur de test existe déjà")

# 3. Tester avec le client Django
client = Client()
login = client.login(username='test_admin', password='test123')
print(f"3. Connexion réussie: {login}")

# 4. Tester la page de génération
response = client.get('/assureur/cotisations/generer/')
print(f"4. Page génération - Status: {response.status_code}")

if response.status_code == 200:
    print("   ✓ Page accessible")
    # Vérifier le contenu en utilisant une approche différente pour éviter l'erreur ASCII
    content_str = response.content.decode('utf-8', errors='ignore')
    if 'Générer' in content_str or 'Cotisations' in content_str:
        print("   ✓ Titre présent")
    if 'periode' in content_str:
        print("   ✓ Champ période présent")
else:
    print(f"   ✗ Erreur: {response.status_code}")
    print(f"   Contenu (premiers 500 caractères): {response.content[:500]}...")

# 5. Tester la prévisualisation
response = client.get('/assureur/cotisations/preview/?periode=2024-12')
print(f"5. Prévisualisation - Status: {response.status_code}")

if response.status_code == 200:
    print("   ✓ Prévisualisation fonctionnelle")
    # Vérifier le contenu
    content_str = response.content.decode('utf-8', errors='ignore')
    if 'Prévisualisation' in content_str or 'membres' in content_str.lower():
        print("   ✓ Contenu valide retourné")
    else:
        print(f"   Contenu retourné: {content_str[:200]}...")
else:
    print(f"   ✗ Erreur: {response.status_code}")

# 6. Tester la génération (POST)
print("6. Test génération (POST) :")
# Compter avant
avant = Cotisation.objects.count()

response = client.post('/assureur/cotisations/generer/', {
    'periode': '2024-12'
})

apres = Cotisation.objects.count()
print(f"   Cotisations avant: {avant}")
print(f"   Cotisations après: {apres}")
print(f"   Différence: {apres - avant}")

if response.status_code in [200, 302]:  # 302 pour redirection
    print("   ✓ Génération réussie")
    if response.status_code == 302:
        print(f"   Redirection vers: {response.url}")
else:
    print(f"   ✗ Erreur: {response.status_code}")
    print(f"   Contenu: {response.content[:500]}...")

print("\n=== TEST COMPLETÉ ===")