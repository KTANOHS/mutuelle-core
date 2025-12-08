# test_rapide.py
import os
import django
import sys

# Trouver automatiquement le nom du projet
current_dir = os.path.dirname(os.path.abspath(__file__))
project_name = None

for item in os.listdir(current_dir):
    if os.path.isdir(item) and 'settings.py' in os.listdir(item):
        project_name = item
        break

if project_name:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
    print(f"🎯 Projet détecté: {project_name}")
else:
    print("❌ Impossible de détecter le projet")
    sys.exit(1)

django.setup()

print("🧪 TEST RAPIDE - SYSTÈME AGENTS")
print("=" * 40)

from django.contrib.auth.models import User
from django.urls import reverse

print("1. Vérification des modèles...")
try:
    from agents.models import Agent
    from membres.models import Membre
    print("   ✅ Modèles importés")
except Exception as e:
    print(f"   ❌ Erreur modèles: {e}")

print("2. Vérification des URLs...")
try:
    urls = [
        ('Dashboard', 'agents:dashboard'),
        ('Créer bon', 'agents:creer_bon_soin'),
        ('Recherche', 'agents:rechercher_membre'),
    ]
    
    for nom, url_name in urls:
        try:
            url = reverse(url_name)
            print(f"   ✅ {nom}: {url}")
        except:
            print(f"   ❌ {nom}: URL non trouvée")
except Exception as e:
    print(f"   ❌ Erreur URLs: {e}")

print("3. Données existantes...")
print(f"   👥 Utilisateurs: {User.objects.count()}")
try:
    print(f"   🎯 Agents: {Agent.objects.count()}")
    print(f"   👤 Membres: {Membre.objects.count()}")
except:
    print("   ⚠️ Impossible de compter agents/membres")

print("\n🎯 POUR TESTER MANUELLEMENT:")
print("   python manage.py runserver")
print("   http://localhost:8000/agents/creer-bon-soin/")