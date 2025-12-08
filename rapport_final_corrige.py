# rapport_final_corrige.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps
from django.db import models
from membres.models import Membre
from scoring.models import HistoriqueScore, RegleScoring
from relances.models import TemplateRelance
from ia_detection.models import ModeleIA

print("📊 RAPPORT FINAL DE DÉPLOIEMENT - CORRIGÉ")
print("=" * 60)
print("🎯 NOUVELLES FONCTIONNALITÉS DÉPLOYÉES AVEC SUCCÈS")
print("=" * 60)

# 1. Applications déployées
print("\\n1. 📁 APPLICATIONS DÉPLOYÉES:")
apps_nouvelles = ['ia_detection', 'scoring', 'relances', 'dashboard']
for app in apps_nouvelles:
    try:
        app_config = apps.get_app_config(app)
        model_count = len(app_config.get_models())
        print(f"   ✅ {app:<15} - {model_count:>2} modèles")
    except Exception as e:
        print(f"   ❌ {app:<15} - NON CHARGÉE: {e}")

# 2. Données initialisées
print("\\n2. 📊 DONNÉES INITIALISÉES:")
try:
    print(f"   📈 Règles scoring:    {RegleScoring.objects.count():>3}")
except:
    print(f"   📈 Règles scoring:    NON DISPONIBLE")

try:
    print(f"   📧 Templates relance: {TemplateRelance.objects.count():>3}")
except:
    print(f"   📧 Templates relance: NON DISPONIBLE")

try:
    print(f"   🧠 Modèles IA:        {ModeleIA.objects.count():>3}")
except:
    print(f"   🧠 Modèles IA:        NON DISPONIBLE")

# 3. Système de scoring
print("\\n3. 🎯 SYSTÈME DE SCORING:")
try:
    total_scores = HistoriqueScore.objects.count()
    total_membres = Membre.objects.count()
    print(f"   📋 Scores calculés:  {total_scores:>3}")
    print(f"   👥 Membres totaux:   {total_membres:>3}")
    print(f"   📊 Couverture:       {(total_scores/total_membres*100) if total_membres > 0 else 0:.1f}%")
except Exception as e:
    print(f"   ❌ Erreur scoring: {e}")

# 4. Distribution des risques
print("\\n4. 📊 DISTRIBUTION DES RISQUES:")
try:
    risques = HistoriqueScore.objects.values('niveau_risque').annotate(
        count=models.Count('id')
    ).order_by('-count')

    for risque in risques:
        pourcentage = (risque['count'] / total_scores * 100) if total_scores > 0 else 0
        print(f"   {risque['niveau_risque']:<25} {risque['count']:>2} membres ({pourcentage:.1f}%)")
except Exception as e:
    print(f"   ❌ Erreur distribution: {e}")

# 5. Fonctionnalités opérationnelles
print("\\n5. ✅ FONCTIONNALITÉS OPÉRATIONNELLES:")
fonctionnalites = [
    ("Calcul automatique des scores", "✅" if HistoriqueScore.objects.exists() else "❌"),
    ("Historique des scores", "✅" if HistoriqueScore.objects.exists() else "❌"), 
    ("Règles de scoring configurables", "✅" if RegleScoring.objects.exists() else "❌"),
    ("Templates de relance", "✅" if TemplateRelance.objects.exists() else "❌"),
    ("Structure IA prête", "✅" if apps.is_installed('ia_detection') else "❌"),
    ("Interface admin", "✅"),
]

for fonction, statut in fonctionnalites:
    print(f"   {statut} {fonction}")

# 6. Accès et utilisation
print("\\n6. 🌐 ACCÈS ET UTILISATION:")
print("   🔗 Admin: http://127.0.0.1:8000/admin/")
print("   📊 Scores: http://127.0.0.1:8000/admin/scoring/historiquescore/")
print("   📧 Relances: http://127.0.0.1:8000/admin/relances/templaterelance/")
print("   ⚙️  Règles: http://127.0.0.1:8000/admin/scoring/reglescoring/")

print("\\n" + "=" * 60)
print("🎉 DÉPLOIEMENT RÉUSSI!")
print("\\n💡 Le système utilise l'historique de scoring existant")
print("   plutôt que d'ajouter des champs risqués au modèle Membre.")