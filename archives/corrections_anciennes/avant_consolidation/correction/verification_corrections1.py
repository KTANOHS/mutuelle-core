#!/usr/bin/env python
"""
VÉRIFICATION RAPIDE DES CORRECTIONS
"""

import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur Django: {e}")
    sys.exit(1)

from django.urls import reverse, NoReverseMatch

print("🔍 VÉRIFICATION DES URLS CORRIGÉES")
print("=" * 60)

urls_a_verifier = [
    'assureur:liste_messages',
    'assureur:envoyer_message',
    'assureur:export_bons_pdf',
    'assureur:creer_cotisation',
    'assureur:preview_generation',
]

for url_name in urls_a_verifier:
    try:
        url = reverse(url_name)
        print(f"✅ {url_name:30} -> {url}")
    except NoReverseMatch as e:
        print(f"❌ {url_name:30} -> ERREUR: {str(e)[:50]}...")

print("\n📋 VÉRIFICATION DES FICHIERS CRÉÉS")
print("=" * 60)

fichiers_a_verifier = [
    'assureur/views.py',
    'assureur/urls.py',
    'templates/assureur/communication/liste_messages.html',
    'templates/assureur/communication/envoyer_message.html',
    'templates/assureur/cotisations/creer_cotisation.html',
]

for fichier in fichiers_a_verifier:
    full_path = os.path.join(BASE_DIR, fichier)
    if os.path.exists(full_path):
        print(f"✅ {fichier}")
    else:
        print(f"❌ {fichier}")

print("\n🚀 COMMANDES À EXÉCUTER:")
print("=" * 60)
print("""
1. Appliquez les migrations:
   python manage.py makemigrations assureur
   python manage.py migrate

2. Testez les nouvelles URLs:
   python manage.py shell -c "
   from django.urls import reverse
   print('1. Liste messages:', reverse('assureur:liste_messages'))
   print('2. Export PDF:', reverse('assureur:export_bons_pdf'))
   print('3. Créer cotisation:', reverse('assureur:creer_cotisation'))
   "

3. Redémarrez le serveur:
   python manage.py runserver

4. Testez dans le navigateur:
   • http://127.0.0.1:8000/assureur/messages/
   • http://127.0.0.1:8000/assureur/cotisations/creer/
""")