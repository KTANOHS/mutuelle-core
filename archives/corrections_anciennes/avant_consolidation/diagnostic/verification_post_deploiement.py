# verification_post_deploiement.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_deploiement():
    print("🔍 VÉRIFICATION POST-DÉPLOIEMENT")
    
    # Vérifier les modèles
    from django.apps import apps
    apps_attendues = ['ia_detection', 'scoring', 'relances']
    
    for app in apps_attendues:
        try:
            app_config = apps.get_app_config(app)
            print(f"✅ App {app} chargée - {len(app_config.get_models())} modèles")
        except:
            print(f"❌ App {app} NON trouvée")
    
    # Vérifier les données initialisées
    from ia_detection.models import ModeleIA
    from scoring.models import RegleScoring
    from relances.models import TemplateRelance
    
    print(f"📊 Modèles IA: {ModeleIA.objects.count()}")
    print(f"📊 Règles scoring: {RegleScoring.objects.count()}") 
    print(f"📊 Templates relance: {TemplateRelance.objects.count()}")
    
    # Tester une fonctionnalité
    from membres.models import Membre
    from scoring.calculators import CalculateurScoreMembre
    
    membre = Membre.objects.first()
    if membre:
        calculateur = CalculateurScoreMembre()
        score = calculateur.calculer_score_complet(membre)
        print(f"🎯 Test scoring: {membre.nom} → {score['score_final']} ({score['niveau_risque']})")
    
    print("✅ Vérification terminée")

if __name__ == "__main__":
    verifier_deploiement()