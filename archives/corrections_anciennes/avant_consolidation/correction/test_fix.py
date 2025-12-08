# test_fix.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

# Test d'import des fonctions corrigées
try:
    from agents.views import verifier_statut_cotisation_simple, verifier_cotisation_membre_simplifiee
    from membres.models import Membre
    
    print("✅ SUCCÈS : Les fonctions sont maintenant importables")
    
    # Test avec un membre réel
    try:
        membre = Membre.objects.get(id=6)
        resultat_simple = verifier_statut_cotisation_simple(membre)
        resultat_complet = verifier_cotisation_membre_simplifiee(membre)
        
        print(f"✅ Test fonction simple: {resultat_simple}")
        print(f"✅ Test fonction complète: {resultat_complet[0]} - {resultat_complet[1]['message']}")
        
    except Membre.DoesNotExist:
        print("⚠️  Membre ID=6 non trouvé, test avec premier membre")
        membre = Membre.objects.first()
        if membre:
            resultat_simple = verifier_statut_cotisation_simple(membre)
            resultat_complet = verifier_cotisation_membre_simplifiee(membre)
            print(f"✅ Test avec premier membre: {resultat_simple} - {resultat_complet[1]['message']}")
        
except ImportError as e:
    print(f"❌ ÉCHEC Import: {e}")
except Exception as e:
    print(f"❌ ERREUR: {e}")