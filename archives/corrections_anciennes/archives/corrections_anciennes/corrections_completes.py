#!/usr/bin/env python
"""
Script pour tester si les corrections ont fonctionné
"""

import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

# Détection application
def detecter_app():
    apps_possibles = ['assurance', 'assurances', 'main', 'core', 'app']
    for app_name in apps_possibles:
        try:
            __import__(app_name + '.models')
            return app_name
        except ImportError:
            continue
    return None

APP_NAME = detecter_app()
if not APP_NAME:
    print("❌ Impossible de détecter l'application")
    sys.exit(1)

print(f"🔍 Application: {APP_NAME}")

try:
    models_module = __import__(APP_NAME + '.models')
    Membre = getattr(models_module.models, 'Membre')
    
    # Test de base
    print("\n🧪 TESTS DE BASE:")
    print("=" * 30)
    
    # Test 1: Accès aux membres
    try:
        membres = Membre.objects.all()[:3]
        print(f"✅ Accès membres: {len(list(membres))} membres trouvés")
    except Exception as e:
        print(f"❌ Erreur accès membres: {e}")
    
    # Test 2: Vérification cotisations
    try:
        membre = Membre.objects.first()
        if membre:
            resultat = membre.est_a_jour_cotisations()
            print(f"✅ Vérification cotisations: {resultat}")
        else:
            print("⚠️  Aucun membre pour test")
    except Exception as e:
        print(f"❌ Erreur vérification cotisations: {e}")
    
    print("\n🎯 Si les tests ci-dessus passent, relancez vos tests originaux:")
    print("   python test_creation_bons.py")
    
except Exception as e:
    print(f"❌ Erreur générale: {e}")