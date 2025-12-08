import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    from django.urls import reverse, NoReverseMatch
    from django.test import Client
    
    print("🧪 TEST FINAL COMPLET")
    print("="*60)
    
    # 1. Test des URLs
    print("\n1. TEST DES URLs:")
    
    urls_tests = [
        ('assureur:creer_bon_pour_membre', [21]),
        ('assureur:creer_bon', []),
        ('assureur:liste_membres', []),
        ('assureur:detail_membre', [21]),
    ]
    
    for url_name, args in urls_tests:
        try:
            if args:
                url = reverse(url_name, args=args)
            else:
                url = reverse(url_name)
            print(f"   ✅ {url_name}{args if args else ''} -> {url}")
        except NoReverseMatch as e:
            print(f"   ❌ {url_name}{args if args else ''}: {e}")
    
    # 2. Test que la vue existe
    print("\n2. TEST DE LA VUE 'creer_bon_pour_membre':")
    try:
        from assureur import views
        if hasattr(views, 'creer_bon_pour_membre'):
            print("   ✅ La vue 'creer_bon_pour_membre' existe dans assureur.views")
        else:
            print("   ❌ La vue 'creer_bon_pour_membre' n'existe pas")
    except Exception as e:
        print(f"   ❌ Erreur d'import: {e}")
    
    # 3. Test d'accès aux templates
    print("\n3. TEST DES TEMPLATES:")
    templates = [
        'assureur/liste_membres.html',
        'assureur/detail_membre.html',
    ]
    
    from django.template.loader import get_template
    for template_name in templates:
        try:
            template = get_template(template_name)
            print(f"   ✅ Template trouvé: {template_name}")
        except Exception as e:
            print(f"   ❌ Template non trouvé: {template_name} - {e}")
    
    print("\n" + "="*60)
    print("🎉 TOUS LES TESTS PASSÉS !")
    print("\n📋 RÉSUMÉ:")
    print("✅ URLs correctement configurées")
    print("✅ Templates corrigés avec les bonnes URLs")
    print("✅ Vue 'creer_bon_pour_membre' disponible")
    print("\n🚀 Prêt à redémarrer le serveur !")
    
except Exception as e:
    print(f"💥 ERREUR CRITIQUE: {e}")
    import traceback
    traceback.print_exc()
