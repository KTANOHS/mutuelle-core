# reinitialisation_apps.py
import os
import django
import sys
from pathlib import Path

# Réinitialiser l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Réimporter Django
import importlib
importlib.reload(django)

# Réinitialiser Django
django.setup()

from django.core.management import call_command
from django.apps import apps

print("🚀 RÉINITIALISATION DES APPLICATIONS DJANGO")
print("=" * 50)

def verifier_et_reparer_apps():
    """Vérifie et répare les applications Django"""
    
    print("\\n🔍 VÉRIFICATION DES APPLICATIONS...")
    
    # Liste des apps à vérifier
    apps_a_verifier = ['ia_detection', 'scoring', 'relances', 'dashboard']
    
    for app in apps_a_verifier:
        try:
            app_config = apps.get_app_config(app)
            print(f"✅ {app}: CHARGÉE - {len(app_config.get_models())} modèles")
        except Exception as e:
            print(f"❌ {app}: NON CHARGÉE - {e}")
    
    print("\\n🔄 RECHARGEMENT DES APPLICATIONS...")
    
    # Recharger les apps
    apps.app_configs = {}
    apps.apps_ready = apps.models_ready = apps.loading = apps.ready = False
    apps.clear_cache()
    
    # Réinitialiser Django
    django.setup()
    
    print("✅ Applications rechargées")
    
    # Vérifier à nouveau
    print("\\n🔍 VÉRIFICATION APRÈS RECHARGEMENT...")
    for app in apps_a_verifier:
        try:
            app_config = apps.get_app_config(app)
            print(f"✅ {app}: CHARGÉE - {len(app_config.get_models())} modèles")
        except Exception as e:
            print(f"❌ {app}: TOUJOURS NON CHARGÉE - {e}")

def verifier_imports():
    """Vérifie que tous les imports fonctionnent"""
    print("\\n🧪 TEST DES IMPORTS...")
    
    imports_a_tester = [
        ('scoring.models', 'HistoriqueScore'),
        ('scoring.models', 'RegleScoring'),
        ('relances.models', 'TemplateRelance'),
        ('ia_detection.models', 'ModeleIA'),
        ('scoring.calculators', 'CalculateurScoreMembre'),
        ('relances.services', 'ServiceRelances'),
    ]
    
    for module, classe in imports_a_tester:
        try:
            module_obj = __import__(module, fromlist=[classe])
            getattr(module_obj, classe)
            print(f"✅ {module}.{classe}")
        except Exception as e:
            print(f"❌ {module}.{classe}: {e}")

def tester_fonctionnalites():
    """Teste les fonctionnalités principales"""
    print("\\n🎯 TEST DES FONCTIONNALITÉS...")
    
    try:
        from membres.models import Membre
        from scoring.models import HistoriqueScore
        from scoring.calculators import CalculateurScoreMembre
        
        # Tester le scoring
        membre = Membre.objects.first()
        if membre:
            calculateur = CalculateurScoreMembre()
            resultat = calculateur.calculer_score_complet(membre)
            print(f"✅ Scoring fonctionnel: {membre.nom} → {resultat['score_final']}")
        else:
            print("⚠️  Aucun membre pour tester")
            
        # Vérifier l'historique
        scores_count = HistoriqueScore.objects.count()
        print(f"✅ Historique scores: {scores_count}")
        
    except Exception as e:
        print(f"❌ Erreur fonctionnalités: {e}")

def main():
    print("🚀 RÉINITIALISATION COMPLÈTE DU SYSTÈME")
    print("=" * 50)
    
    # 1. Vérifier et réparer les apps
    verifier_et_reparer_apps()
    
    # 2. Tester les imports
    verifier_imports()
    
    # 3. Tester les fonctionnalités
    tester_fonctionnalites()
    
    print("\\n" + "=" * 50)
    print("🎉 RÉINITIALISATION TERMINÉE!")

if __name__ == "__main__":
    main()