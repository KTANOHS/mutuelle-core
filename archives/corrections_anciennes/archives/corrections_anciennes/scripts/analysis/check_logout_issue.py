#!/usr/bin/env python
"""
DIAGNOSTIC DE LA DÉCONNEXION
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

import django
django.setup()

from pathlib import Path

print("🔍 DIAGNOSTIC DÉCONNEXION")
print("=" * 50)

# 1. Vérifier le template
template_path = Path('templates/registration/logged_out.html')
print(f"1. 📁 Template déconnexion: {template_path}")
if template_path.exists():
    print("   ✅ Template trouvé")
else:
    print("   ❌ Template MANQUANT - Création nécessaire")

# 2. Vérifier la configuration
from django.conf import settings
print(f"\n2. ⚙️  Configuration déconnexion:")
print(f"   LOGOUT_REDIRECT_URL: {getattr(settings, 'LOGOUT_REDIRECT_URL', 'Non défini')}")

# 3. Vérifier les URLs
print(f"\n3. 🔗 URL de déconnexion:")
try:
    from django.urls import reverse
    logout_url = reverse('logout')
    print(f"   URL déconnexion: {logout_url}")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

print(f"\n💡 SOLUTIONS:")
print(f"   • Créer templates/registration/logged_out.html")
print(f"   • Vérifier next_page dans LogoutView")
print(f"   • Tester avec redirection directe vers home")