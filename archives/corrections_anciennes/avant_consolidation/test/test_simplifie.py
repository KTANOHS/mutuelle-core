# test_simplifie.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre
from scoring.calculators import CalculateurScoreMembre

print("🧪 TEST SIMPLIFIÉ DU SCORING")
print("=" * 40)

membre = Membre.objects.first()
if membre:
    print(f"👤 Test avec: {membre.nom}")
    
    calculateur = CalculateurScoreMembre()
    resultat = calculateur.calculer_score_complet(membre)
    
    print(f"✅ Score: {resultat['score_final']}")
    print(f"✅ Niveau risque: {resultat['niveau_risque']}")
    print(f"✅ Détails: {resultat['details_scores']}")
    
    # Vérifier que le membre est mis à jour
    membre.refresh_from_db()
    print(f"✅ Membre mis à jour - Score: {membre.score_risque}, Risque: {membre.niveau_risque}")
else:
    print("❌ Aucun membre trouvé")