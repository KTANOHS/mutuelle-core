# test_generation_complet.py
import os
import django
import sys
import re

# Configuration Django
projet_path = '/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30'
sys.path.append(projet_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

print("=== TEST COMPLET DE GÉNÉRATION ===")
print(f"Chemin: {projet_path}")

# 1. Création utilisateur de test
try:
    # Supprimer l'utilisateur test s'il existe
    User.objects.filter(username='test_gen').delete()
    
    user = User.objects.create_superuser(
        username='test_gen',
        email='test@generation.com',
        password='test123'
    )
    print("✅ Utilisateur de test créé")
except Exception as e:
    print(f"⚠ Erreur création: {e}")
    user = User.objects.get(username='admin')
    print("✅ Utilisation de l'admin existant")

# 2. Connexion
client = Client()
login = client.login(username=user.username, password='test123' if user.username == 'test_gen' else 'admin123')
print(f"Connexion: {'✅ Réussie' if login else '❌ Échec'}")

if not login:
    exit(1)

# 3. Test GET de la page génération
print(f"\n{'='*50}")
print("1. Récupération de la page génération")
response = client.get('/assureur/cotisations/generer/')
print(f"Status: {response.status_code}")

if response.status_code != 200:
    print("❌ Échec, arrêt du test")
    exit(1)

# 4. Extraction du token CSRF
content = response.content.decode('utf-8')
csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', content)

if not csrf_match:
    print("❌ Token CSRF non trouvé")
    exit(1)

csrf_token = csrf_match.group(1)
print(f"✅ Token CSRF obtenu: {csrf_token[:20]}...")

# 5. Test POST de génération
print(f"\n{'='*50}")
print("2. Test de génération (POST)")

# Compter les cotisations avant
try:
    from assureur.models import Cotisation
    avant = Cotisation.objects.count()
    print(f"Nombre de cotisations avant: {avant}")
except Exception as e:
    print(f"⚠ Impossible de compter les cotisations: {e}")
    avant = 0

# Envoyer la requête POST
periode = "2025-03"
print(f"Période testée: {periode}")

response = client.post('/assureur/cotisations/generer/', {
    'periode': periode,
    'csrfmiddlewaretoken': csrf_token
})

print(f"Status POST: {response.status_code}")

# Analyser la réponse
if response.status_code == 302:
    print("✅ Redirection détectée (succès)")
    print(f"Redirection vers: {response.url}")
    
    # Suivre la redirection
    response2 = client.get(response.url)
    print(f"Page de redirection - Status: {response2.status_code}")
    
    # Vérifier le contenu de la page de redirection
    content2 = response2.content.decode('utf-8', errors='ignore')
    if 'succès' in content2.lower() or 'généré' in content2.lower():
        print("✅ Message de succès détecté")
    else:
        print("⚠ Message de succès non détecté")
        
elif response.status_code == 200:
    print("⚠ Pas de redirection (réponse directe)")
    content_post = response.content.decode('utf-8', errors='ignore')
    
    # Chercher des messages
    if 'erreur' in content_post.lower():
        print("❌ Erreur détectée dans la réponse")
        print(f"Extrait: {content_post[:500]}...")
    elif 'succès' in content_post.lower() or 'généré' in content_post.lower():
        print("✅ Succès détecté dans la réponse")
    else:
        print("⚠ Statut indéterminé")
        print(f"Extrait: {content_post[:500]}...")
else:
    print(f"❌ Statut inattendu: {response.status_code}")

# 6. Vérifier les résultats
print(f"\n{'='*50}")
print("3. Vérification des résultats")

try:
    from assureur.models import Cotisation
    apres = Cotisation.objects.count()
    print(f"Nombre de cotisations après: {apres}")
    print(f"Différence: {apres - avant}")
    
    if apres > avant:
        print("✅ Nouvelles cotisations créées avec succès !")
        
        # Afficher quelques détails
        nouvelles = Cotisation.objects.order_by('-id')[:3]
        print(f"\nDernières cotisations créées:")
        for c in nouvelles:
            print(f"  - ID: {c.id}, Période: {c.periode}, Montant: {c.montant}")
    else:
        print("⚠ Aucune nouvelle cotisation créée")
        print("   Causes possibles:")
        print("   1. Aucun membre actif pour cette période")
        print("   2. Les cotisations existent déjà pour cette période")
        print("   3. Erreur dans le processus de génération")
        
except Exception as e:
    print(f"❌ Erreur lors de la vérification: {e}")

# 7. Nettoyage (optionnel)
print(f"\n{'='*50}")
print("4. Nettoyage")

# Supprimer l'utilisateur de test s'il a été créé
if user.username == 'test_gen':
    try:
        user.delete()
        print("✅ Utilisateur de test supprimé")
    except:
        print("⚠ Impossible de supprimer l'utilisateur de test")

print(f"\n{'='*50}")
print("TEST TERMINÉ")
print(f"{'='*50}")