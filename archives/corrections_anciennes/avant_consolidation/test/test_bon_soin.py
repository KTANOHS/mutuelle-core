# test_bon_soin.py
import os
import sys
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

try:
    django.setup()
    
    from membres.models import Membre
    from soins.models import BonDeSoin
    from django.contrib.auth.models import User
from django.utils import timezone
    
    def test_creation_bon_soin():
        print("🧪 TEST DE CRÉATION DE BON DE SOIN")
        print("-" * 50)
        
        # 1. Vérifier qu'il y a des membres
        membres = Membre.objects.all()[:5]
        if not membres:
            print("❌ Aucun membre trouvé dans la base de données")
            return
            
        print(f"✅ {len(membres)} membre(s) disponible(s)")
        
        # 2. Tester avec chaque membre
        for i, membre in enumerate(membres, 1):
            print(f"\n--- Test {i} avec {membre.prenom} {membre.nom} ---")
            
            try:
                # Essayer de créer un bon de soin
                bon = BonDeSoin.objects.create(
                    patient=membre,
                    date_soin=timezone.now().date(),
                    symptomes="Toux et fièvre",
                    diagnostic="Infection respiratoire",
                    montant=75.50,
                    statut='attente'
                )
                print(f"✅ SUCCÈS - Bon créé (ID: {bon.id})")
                
                # Afficher les détails du bon créé
                print(f"   Détails:")
                print(f"   - Patient: {bon.patient.prenom} {bon.patient.nom}")
                print(f"   - Montant: {bon.montant}")
                print(f"   - Statut: {bon.statut}")
                print(f"   - Date: {bon.date_soin}")
                
                # Nettoyer
                bon.delete()
                print("   ✅ Bon supprimé (nettoyage)")
                
            except Exception as e:
                print(f"❌ ÉCHEC: {e}")
                print(f"   Type: {type(e).__name__}")
                
                # Analyse détaillée de l'erreur
                error_str = str(e).lower()
                
                if "patient" in error_str:
                    print("   → Problème: Relation avec le patient")
                elif "montant" in error_str:
                    print("   → Problème: Champ montant")
                    # Tester avec différentes valeurs
                    test_montants = [100, 100.0, "100", "100.0"]
                    for test_montant in test_montants:
                        try:
                            bon_test = BonDeSoin(
                                patient=membre,
                                date_soin=timezone.now().date(),
                                montant=test_montant,
                                statut='attente'
                            )
                            bon_test.full_clean()
                            print(f"   ✅ Montant '{test_montant}' ({type(test_montant)}) valide")
                        except Exception as e2:
                            print(f"   ❌ Montant '{test_montant}' invalide: {e2}")
                            
                elif "null" in error_str:
                    print("   → Problème: Champ obligatoire manquant")
                    # Lister les champs obligatoires
                    required_fields = []
                    for field in BonDeSoin._meta.get_fields():
                        if not field.null and not field.blank and hasattr(field, 'name'):
                            required_fields.append(field.name)
                    print(f"   Champs obligatoires: {', '.join(required_fields)}")
                    
                elif "foreign key" in error_str:
                    print("   → Problème: Clé étrangère invalide")
                    
        print("\n" + "=" * 50)
        print("TESTS TERMINÉS")
        
    # Exécuter le test
    test_creation_bon_soin()
    
except Exception as e:
    print(f"❌ ERREUR: {e}")