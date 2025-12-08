# verifier_structure_complete.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps

def analyser_structure_cotisations():
    print("🔍 ANALYSE COMPLÈTE DE LA STRUCTURE COTISATIONS...")
    
    # 1. Lister tous les modèles liés aux cotisations
    print("\n📋 MODÈLES LIÉS AUX COTISATIONS:")
    for model in apps.get_models():
        model_name = model.__name__.lower()
        if any(keyword in model_name for keyword in ['cotisation', 'verification', 'agent']):
            print(f"✅ {model.__name__} → {model.__module__}")
    
    # 2. Vérifier les membres
    from membres.models import Membre
    print(f"\n👥 MEMBRES TOTAUX: {Membre.objects.count()}")
    
    # 3. Vérifier les agents
    try:
        Agent = apps.get_model('agents', 'Agent')
        print(f"👨‍💼 AGENTS DISPONIBLES: {Agent.objects.count()}")
    except:
        print("❌ MODÈLE AGENT NON TROUVÉ")
    
    # 4. Essayer de trouver VerificationCotisation
    print("\n🔎 RECHERCHE VerificationCotisation:")
    for app_config in apps.get_app_configs():
        try:
            model = apps.get_model(app_config.label, 'VerificationCotisation')
            print(f"✅ TROUVÉ: {app_config.label}.VerificationCotisation")
            break
        except:
            continue

if __name__ == "__main__":
    analyser_structure_cotisations()