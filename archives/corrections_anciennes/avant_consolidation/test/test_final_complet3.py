# test_final_complet.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from scoring.calculators import CalculateurScoreMembre
from scoring.models import HistoriqueScore
from relances.models import TemplateRelance
from relances.services import ServiceRelances

print("🎯 TEST FINAL COMPLET")
print("=" * 50)

# 1. Test du scoring
print("\\n1. 🧪 TEST DU SCORING")
membre = Membre.objects.first()
if membre:
    print(f"👤 Membre test: {membre.nom}")
    
    calculateur = CalculateurScoreMembre()
    resultat = calculateur.calculer_score_complet(membre)
    
    print(f"✅ Score calculé: {resultat['score_final']}")
    print(f"✅ Niveau risque: {resultat['niveau_risque']}")
    
    # Vérifier que le membre est mis à jour
    membre.refresh_from_db()
    if hasattr(membre, 'score_risque'):
        print(f"✅ Membre mis à jour - Score: {membre.score_risque}, Risque: {membre.niveau_risque}")
    else:
        print("❌ Champs manquants dans le modèle Membre")
else:
    print("❌ Aucun membre trouvé")

# 2. Test des relances
print("\\n2. 📧 TEST DES RELANCES")
service = ServiceRelances()
membres_a_relancer = service.identifier_membres_a_relancer()
print(f"✅ Membres à relancer: {len(membres_a_relancer)}")

# 3. Vérification des données
print("\\n3. 📊 VÉRIFICATION DES DONNÉES")
print(f"✅ Historiques scores: {HistoriqueScore.objects.count()}")
print(f"✅ Templates relance: {TemplateRelance.objects.count()}")

# 4. Test de tous les membres
print("\\n4. 👥 SCORES DE TOUS LES MEMBRES")
membres = Membre.objects.all()[:5]  # Premiers 5 seulement
for m in membres:
    if hasattr(m, 'score_risque') and m.score_risque:
        print(f"   {m.nom}: {m.score_risque} → {m.niveau_risque}")
    else:
        print(f"   {m.nom}: Score non calculé")

print("\\n" + "=" * 50)
print("🎉 TEST TERMINÉ!")