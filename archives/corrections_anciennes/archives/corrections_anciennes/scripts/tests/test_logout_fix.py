#!/usr/bin/env python
"""
TEST DE LA DÉCONNEXION APRÈS CORRECTION
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

from pathlib import Path

print("🔍 TEST DU TEMPLATE DE DÉCONNEXION")
print("=" * 50)

# Vérifier le template
logout_path = Path('templates/registration/logout.html')

if logout_path.exists():
    content = logout_path.read_text()
    print("✅ Template logout.html existe")
    print(f"📏 Taille: {len(content)} caractères")
    
    # Vérifier le contenu essentiel
    essential_elements = [
        ('DOCTYPE html', 'Structure HTML'),
        ('Déconnexion réussie', 'Titre'),
        ("{% url 'login' %}", 'Lien connexion'),
        ("{% url 'home' %}", 'Lien accueil')
    ]
    
    for element, description in essential_elements:
        if element in content:
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description}")
else:
    print("❌ Template logout.html manquant")

# Vérifier la configuration URL
print("\n🔗 CONFIGURATION URL:")
try:
    from django.urls import reverse
    logout_url = reverse('logout')
    print(f"✅ URL déconnexion: {logout_url}")
except Exception as e:
    print(f"❌ Erreur URL: {e}")

print("\n🎯 POUR TESTER:")
print("   1. Redémarrez le serveur: python manage.py runserver")
print("   2. Connectez-vous")
print("   3. Cliquez sur Déconnexion")
print("   4. Vous devriez voir la page de déconnexion")