# debug_urls.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.urls import reverse, NoReverseMatch
from django.template import Template, Context

print("=== DIAGNOSTIC FINAL ===")

# Test 1: L'URL existe-t-elle dans le système Django ?
try:
    url = reverse('assureur:preview_generation')
    print(f"1. ✅ reverse('assureur:preview_generation') = {url}")
except NoReverseMatch as e:
    print(f"1. ❌ reverse('assureur:preview_generation') échoue: {e}")
    # Vérifier toutes les URLs
    from django.urls import get_resolver
    resolver = get_resolver()
    all_urls = []
    for pattern in resolver.url_patterns:
        if hasattr(pattern, 'name') and pattern.name:
            all_urls.append(pattern.name)
    print(f"   URLs disponibles: {all_urls}")

# Test 2: Le template tag fonctionne-t-il ?
try:
    template_code = """{% url "assureur:preview_generation" %}"""
    template = Template(template_code)
    result = template.render(Context({}))
    print(f"2. ✅ Template tag fonctionne: {result}")
except Exception as e:
    print(f"2. ❌ Template tag échoue: {e}")

# Test 3: Vérifier le contenu exact du template
print("\n3. Vérification du template :")
with open('templates/assureur/generer_cotisations.html', 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines, 1):
        if 'preview_generation' in line:
            print(f"   Ligne {i}: {line.rstrip()}")
            if 'assureur:preview_generation' in line:
                print("     ✅ Correct (avec namespace)")
            else:
                print("     ❌ Problème potentiel")

print("\n=== SOLUTION D'URGENCE ===")
print("Si l'erreur persiste, remplacez dans le template :")
print("  url: '{% url \"assureur:preview_generation\" %}',")
print("Par :")
print("  url: '/assureur/cotisations/preview/',")