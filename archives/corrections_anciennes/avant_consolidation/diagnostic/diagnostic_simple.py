#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    print("✅ Django configuré avec succès")
except Exception as e:
    print(f"❌ Erreur Django setup: {e}")
    sys.exit(1)

from django.urls import reverse, NoReverseMatch

print("\n🔍 DIAGNOSTIC DES URLs PROBLEMATIQUES")
print("="*50)

# Liste des URLs à vérifier
urls_a_verifier = [
    ('assureur:creer_bon_pour_membre', [21]),
    ('assureur:creer_bon', []),
    ('assureur:liste_membres', []),
    ('assureur:detail_membre', [21]),
    ('assureur:detail_bon', [1]),
]

print("\n1. Vérification des URLs par nom:")
for url_name, args in urls_a_verifier:
    try:
        if args:
            url = reverse(url_name, args=args)
        else:
            url = reverse(url_name)
        print(f"   ✅ {url_name} -> {url}")
    except NoReverseMatch as e:
        print(f"   ❌ {url_name}: {e}")

# Vérifier l'URL spécifique avec arguments
print("\n2. Test spécifique de 'creer_bon_pour_membre':")
try:
    url = reverse('assureur:creer_bon_pour_membre', args=[21])
    print(f"   ✅ creer_bon_pour_membre(21) -> {url}")
except NoReverseMatch as e:
    print(f"   ❌ creer_bon_pour_membre(21): {e}")
    
# Vérifier sans namespace
try:
    url = reverse('creer_bon_pour_membre', args=[21])
    print(f"   ✅ creer_bon_pour_membre(21) sans namespace -> {url}")
except NoReverseMatch as e:
    print(f"   ❌ creer_bon_pour_membre(21) sans namespace: {e}")

print("\n3. Vérification des templates...")
import glob
for template in glob.glob("./templates/assureur/*.html"):
    print(f"\n   📄 {template}")
    try:
        with open(template, 'r') as f:
            content = f.read()
            if 'creer_bon' in content:
                print("      ⚠️  Contient 'creer_bon'")
            if '{% url' in content:
                lines = content.split('\n')
                for i, line in enumerate(lines[:10], 1):
                    if '{% url' in line:
                        print(f"      Ligne {i}: {line.strip()}")
    except Exception as e:
        print(f"      ❌ Erreur lecture: {e}")

print("\n🎉 Diagnostic terminé!")
