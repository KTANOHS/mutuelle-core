# test_correction_affichage.py - VERSION CORRIGÉE
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from affichage_unifie import afficher_fiche_cotisation_unifiee, determiner_statut_cotisation

def test_correction():
    print("🧪 TEST DE CORRECTION AFFICHAGE_UNIFIE")
    print("=" * 50)
    
    # Test 1: Fonction determiner_statut_cotisation avec None
    try:
        statut, emoji, classe = determiner_statut_cotisation(None)
        print(f"✅ Test 1 - Gestion None: {statut} {emoji} {classe}")
    except Exception as e:
        print(f"❌ Test 1 - Erreur: {e}")
    
    # Test 2: Fonction determiner_statut_cotisation avec objet factice
    try:
        class MockVerification:
            statut_cotisation = 'a_jour'
        
        statut, emoji, classe = determiner_statut_cotisation(MockVerification())
        print(f"✅ Test 2 - Gestion objet: {statut} {emoji} {classe}")
    except Exception as e:
        print(f"❌ Test 2 - Erreur: {e}")
    
    # Test 3: Fonction afficher_fiche_cotisation_unifiee avec données minimales
    try:
        class MockMembre:
            prenom = "Jean"
            nom = "Dupont"
            numero_unique = "MEM123"
            telephone = "0123456789"
        
        fiche = afficher_fiche_cotisation_unifiee(MockMembre(), None, None)
        if "FICHE COTISATION UNIFIÉE" in fiche:
            print("✅ Test 3 - Génération fiche avec None réussie")
        else:
            print("❌ Test 3 - Format fiche incorrect")
    except Exception as e:
        print(f"❌ Test 3 - Erreur: {e}")
    
    # Test 4: Fonction avec vérification factice
    try:
        class MockMembre:
            prenom = "Marie"
            nom = "Martin"
            numero_unique = "MEM456"
            telephone = "0987654321"
        
        class MockVerification:
            statut_cotisation = 'en_retard'
            montant_dette_str = '5 000 FCFA'
            prochaine_echeance = '2024-12-31'
            
            @property
            def jours_retard(self):
                return 45
        
        fiche = afficher_fiche_cotisation_unifiee(MockMembre(), MockVerification(), None)
        if "FICHE COTISATION UNIFIÉE" in fiche and "5 000 FCFA" in fiche:
            print("✅ Test 4 - Génération fiche complète réussie")
        else:
            print("❌ Test 4 - Données manquantes dans la fiche")
    except Exception as e:
        print(f"❌ Test 4 - Erreur: {e}")
    
    # Test 5: Test de robustesse avec données manquantes
    try:
        class MockMembreIncomplet:
            nom = "Test"
            # pas de prenom, telephone, etc.
        
        fiche = afficher_fiche_cotisation_unifiee(MockMembreIncomplet(), None, None)
        if "Membre non identifié" in fiche or "Test" in fiche:
            print("✅ Test 5 - Gestion données incomplètes réussie")
        else:
            print("❌ Test 5 - Échec gestion données incomplètes")
    except Exception as e:
        print(f"❌ Test 5 - Erreur: {e}")
    
    print("=" * 50)
    print("📊 Résultat des tests de correction")

if __name__ == "__main__":
    test_correction()