# test_flux_cotisations.py
import os
import sys
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

print("🧪 TEST DU FLUX COTISATIONS ASSUREUR → AGENT")
print("=" * 50)

class TestFluxCotisations:
    def __init__(self):
        self.resultats = []
    
    def tester_import_modeles(self):
        """Teste l'importation des modèles nécessaires"""
        print("1. 🔧 TEST IMPORT MODÈLES...")
        
        try:
            from membres.models import Membre
            self.resultats.append(('Membre', '✅ Importé'))
            print("   ✅ Membre importé")
        except ImportError as e:
            self.resultats.append(('Membre', f'❌ {e}'))
            print(f"   ❌ Membre: {e}")
        
        try:
            from membres.models import Cotisation
            self.resultats.append(('Cotisation', '✅ Importé'))
            print("   ✅ Cotisation importé")
        except ImportError as e:
            self.resultats.append(('Cotisation', f'❌ {e}'))
            print(f"   ❌ Cotisation: {e}")
        
        try:
            from assureur.models import Assureur
            self.resultats.append(('Assureur', '✅ Importé'))
            print("   ✅ Assureur importé")
        except ImportError as e:
            self.resultats.append(('Assureur', f'❌ {e}'))
            print(f"   ❌ Assureur: {e}")
        
        try:
            from agents.models import Agent, VerificationCotisation
            self.resultats.append(('Agent', '✅ Importé'))
            self.resultats.append(('VerificationCotisation', '✅ Importé'))
            print("   ✅ Agent et VerificationCotisation importés")
        except ImportError as e:
            self.resultats.append(('Agent', f'❌ {e}'))
            print(f"   ❌ Agent/Verification: {e}")
    
    def tester_creation_donnees_test(self):
        """Teste la création de données de test"""
        print("\n2. 🧪 CRÉATION DONNÉES TEST...")
        
        try:
            from membres.models import Membre
            from django.contrib.auth.models import User
            
            # Créer un user test
            user, created = User.objects.get_or_create(
                username='test_flux_cotisation',
                defaults={
                    'email': 'test_flux@mutuelle.com',
                    'password': 'test123'
                }
            )
            
            # Créer un membre test
            membre, created = Membre.objects.get_or_create(
                user=user,
                defaults={
                    'numero_unique': 'TEST_FLUX001',
                    'prenom': 'Test',
                    'nom': 'FluxCotisation'
                }
            )
            
            if created:
                self.resultats.append(('Membre test', '✅ Créé'))
                print("   ✅ Membre test créé")
            else:
                self.resultats.append(('Membre test', '✅ Existant'))
                print("   ✅ Membre test existant")
            
            # Tester la création de cotisation
            try:
                from membres.models import Cotisation
                cotisation, created = Cotisation.objects.get_or_create(
                    membre=membre,
                    defaults={
                        'montant': 10000,
                        'statut': 'PAYEE',
                        'date_paiement': '2025-11-27'
                    }
                )
                
                if created:
                    self.resultats.append(('Cotisation test', '✅ Créée'))
                    print("   ✅ Cotisation test créée")
                else:
                    self.resultats.append(('Cotisation test', '✅ Existant'))
                    print("   ✅ Cotisation test existante")
                    
            except Exception as e:
                self.resultats.append(('Cotisation test', f'❌ {e}'))
                print(f"   ❌ Cotisation test: {e}")
            
            # Tester la création de vérification
            try:
                from agents.models import Agent, VerificationCotisation
                
                # Créer un agent test
                agent_user, created = User.objects.get_or_create(
                    username='agent_test_flux',
                    defaults={
                        'email': 'agent_flux@mutuelle.com',
                        'password': 'test123',
                        'first_name': 'Agent',
                        'last_name': 'TestFlux'
                    }
                )
                
                agent, created = Agent.objects.get_or_create(
                    user=agent_user,
                    defaults={
                        'matricule': 'AGENT_FLUX001'
                    }
                )
                
                # Créer vérification
                verification, created = VerificationCotisation.objects.get_or_create(
                    membre=membre,
                    agent=agent,
                    defaults={
                        'statut': 'VALIDE',
                        'date_verification': '2025-11-27'
                    }
                )
                
                if created:
                    self.resultats.append(('Vérification test', '✅ Créée'))
                    print("   ✅ Vérification test créée")
                else:
                    self.resultats.append(('Vérification test', '✅ Existant'))
                    print("   ✅ Vérification test existante")
                    
            except Exception as e:
                self.resultats.append(('Vérification test', f'❌ {e}'))
                print(f"   ❌ Vérification test: {e}")
                
        except Exception as e:
            self.resultats.append(('Données test', f'❌ {e}'))
            print(f"   ❌ Création données test: {e}")
    
    def tester_flux_complet(self):
        """Teste le flux complet assureur → agent"""
        print("\n3. 🔄 TEST FLUX COMPLET...")
        
        try:
            from membres.models import Membre, Cotisation
            from agents.models import VerificationCotisation
            
            # Vérifier le flux pour un membre
            membre_test = Membre.objects.filter(numero_unique='TEST_FLUX001').first()
            
            if membre_test:
                # Vérifier les cotisations
                cotisations = Cotisation.objects.filter(membre=membre_test)
                self.resultats.append(('Cotisations membre', f'✅ {cotisations.count()} trouvée(s)'))
                print(f"   ✅ Cotisations: {cotisations.count()} trouvée(s)")
                
                # Vérifier les vérifications
                verifications = VerificationCotisation.objects.filter(membre=membre_test)
                self.resultats.append(('Vérifications membre', f'✅ {verifications.count()} trouvée(s)'))
                print(f"   ✅ Vérifications: {verifications.count()} trouvée(s)")
                
                # Vérifier la cohérence
                if cotisations.exists() and verifications.exists():
                    self.resultats.append(('Flux cohérent', '✅ OK'))
                    print("   ✅ Flux cohérent: cotisation → vérification")
                else:
                    self.resultats.append(('Flux incomplet', '⚠️  Cotisation ou vérification manquante'))
                    print("   ⚠️  Flux incomplet")
                    
            else:
                self.resultats.append(('Membre test', '❌ Non trouvé'))
                print("   ❌ Membre test non trouvé")
                
        except Exception as e:
            self.resultats.append(('Test flux', f'❌ {e}'))
            print(f"   ❌ Test flux: {e}")
    
    def afficher_resultats(self):
        """Affiche les résultats des tests"""
        print("\n" + "="*50)
        print("📊 RÉSULTATS DES TESTS FLUX COTISATIONS")
        print("="*50)
        
        for test, resultat in self.resultats:
            print(f"{resultat} {test}")
        
        # Résumé
        tests_reussis = sum(1 for _, r in self.resultats if '✅' in r)
        total_tests = len(self.resultats)
        
        print(f"\n🎯 RÉSUMÉ: {tests_reussis}/{total_tests} tests réussis")
        
        if tests_reussis == total_tests:
            print("🚀 FLUX COTISATIONS OPÉRATIONNEL!")
        else:
            print("⚠️  PROBLEMES DÉTECTÉS DANS LE FLUX")

# Exécution
if __name__ == "__main__":
    testeur = TestFluxCotisations()
    testeur.tester_import_modeles()
    testeur.tester_creation_donnees_test()
    testeur.tester_flux_complet()
    testeur.afficher_resultats()