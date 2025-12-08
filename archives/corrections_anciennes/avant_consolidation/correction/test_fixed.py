# test_fixed.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from agents.views import verifier_cotisation_membre_simplifiee
from membres.models import Membre

try:
    membre = Membre.objects.get(id=6)
    print(f"🔍 Test avec membre: {membre.prenom} {membre.nom}")
    print(f"📅 Date inscription: {membre.date_inscription} (type: {type(membre.date_inscription)})")
    
    resultat, details = verifier_cotisation_membre_simplifiee(membre)
    
    print(f"✅ SUCCÈS : Test complété sans erreur")
    print(f"📊 Résultat: {resultat}")
    print(f"📝 Détails: {details['message']}")
    print(f"💰 Montant: {details['montant_dette_str']}")
    print(f"📅 Prochaine échéance: {details['prochaine_echeance']}")
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()