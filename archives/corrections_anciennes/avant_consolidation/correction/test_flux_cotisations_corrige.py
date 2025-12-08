# test_flux_cotisations_corrige.py
import os
import sys
import django
from pathlib import Path
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

print("🧪 TEST DU FLUX COTISATIONS - VERSION CORRIGÉE")
print("=" * 50)

class TestFluxCotisationsCorrige:
    def __init__(self):
        self.resultats = []
    
    def tester_modeles_disponibles(self):
        """Teste les modèles réellement disponibles"""
        print("1. 🔧 TEST MODÈLES DISPONIBLES...")
        
        from django.apps import apps
        
        modeles_a_tester = [
            'membres.Membre',
            'assureur.Assureur', 
            'agents.Agent',
            'agents.VerificationCotisation'
        ]
        
        for modele_path in modeles_a_tester:
            try:
                modele = apps.get_model(modele_path)
                count = modele.objects.count()
                self.resultats.append((modele_path, f'✅ DISPONIBLE ({count} enregistrements)'))
                print(f"   ✅ {modele_path}: {count} enregistrements")
            except Exception as e:
                self.resultats.append((modele_path, f'❌ {e}'))
                print(f"   ❌ {modele_path}: {e}")
    
    def tester_creation_agent(self):
        """Teste la création d'un agent avec tous les champs requis"""
        print("\n2. 👨‍💼 TEST CRÉATION AGENT...")
        
        try:
            from agents.models import Agent
            from django.contrib.auth.models import User
            
            # Créer un user pour l'agent
            user, created = User.objects.get_or_create(
                username='agent_test_cotisation',
                defaults={
                    'email': 'agent_cotisation@mutuelle.com',
                    'password': 'test123',
                    'first_name': 'Agent',
                    'last_name': 'TestCotisation'
                }
            )
            
            # Créer l'agent avec tous les champs requis
            agent, created = Agent.objects.get_or_create(
                user=user,
                defaults={
                    'matricule': 'AGENT_COTIS001',
                    'date_embauche': datetime.now().date(),  # Champ requis
                    'telephone': '+2250102030405',
                    'est_actif': True
                }
            )
            
            if created:
                self.resultats.append(('Agent test', '✅ Créé avec succès'))
                print("   ✅ Agent test créé avec tous les champs requis")
            else:
                self.resultats.append(('Agent test', '✅ Existant'))
                print("   ✅ Agent test existant")
                
            return agent
            
        except Exception as e:
            self.resultats.append(('Agent test', f'❌ {e}'))
            print(f"   ❌ Création agent: {e}")
            return None
    
    def tester_creation_verification(self):
        """Teste la création d'une vérification de cotisation"""
        print("\n3. 🔍 TEST CRÉATION VÉRIFICATION...")
        
        try:
            from membres.models import Membre
            from agents.models import VerificationCotisation
            from django.contrib.auth.models import User
            
            # Récupérer ou créer un membre
            membre, created = Membre.objects.get_or_create(
                numero_unique='TEST_COTIS001',
                defaults={
                    'prenom': 'Test',
                    'nom': 'Cotisation',
                    'telephone': '+2250100000001'
                }
            )
            
            if created:
                self.resultats.append(('Membre test', '✅ Créé'))
                print("   ✅ Membre test créé")
            else:
                self.resultats.append(('Membre test', '✅ Existant'))
                print("   ✅ Membre test existant")
            
            # Récupérer l'agent créé précédemment
            from agents.models import Agent
            agent = Agent.objects.filter(matricule='AGENT_COTIS001').first()
            
            if not agent:
                self.resultats.append(('Vérification test', '❌ Agent non trouvé'))
                print("   ❌ Agent test non trouvé")
                return
            
            # Créer la vérification avec les champs disponibles
            verification_data = {
                'membre': membre,
                'agent': agent,
                'date_verification': datetime.now().date(),
            }
            
            # Ajouter les champs conditionnels
            if hasattr(VerificationCotisation, 'statut_cotisation'):
                verification_data['statut_cotisation'] = 'VALIDE'
            if hasattr(VerificationCotisation, 'montant_dette'):
                verification_data['montant_dette'] = 0
            if hasattr(VerificationCotisation, 'jours_retard'):
                verification_data['jours_retard'] = 0
            
            verification, created = VerificationCotisation.objects.get_or_create(
                membre=membre,
                agent=agent,
                defaults=verification_data
            )
            
            if created:
                self.resultats.append(('Vérification test', '✅ Créée avec succès'))
                print("   ✅ Vérification test créée")
            else:
                self.resultats.append(('Vérification test', '✅ Existant'))
                print("   ✅ Vérification test existante")
                
        except Exception as e:
            self.resultats.append(('Vérification test', f'❌ {e}'))
            print(f"   ❌ Création vérification: {e}")
    
    def tester_flux_complet(self):
        """Teste le flux complet avec les données réelles"""
        print("\n4. 🔄 TEST FLUX COMPLET...")
        
        try:
            from membres.models import Membre
            from agents.models import VerificationCotisation
            
            # Vérifier le flux pour le membre test
            membre_test = Membre.objects.filter(numero_unique='TEST_COTIS001').first()
            
            if membre_test:
                # Vérifier les vérifications
                verifications = VerificationCotisation.objects.filter(membre=membre_test)
                self.resultats.append(('Vérifications membre', f'✅ {verifications.count()} trouvée(s)'))
                print(f"   ✅ Vérifications: {verifications.count()} trouvée(s)")
                
                # Vérifier la cohérence
                if verifications.exists():
                    verification = verifications.first()
                    agent_info = f"Agent: {verification.agent.user.username}" if verification.agent else "Sans agent"
                    date_info = f"Date: {verification.date_verification}" if verification.date_verification else "Sans date"
                    
                    self.resultats.append(('Flux cohérent', f'✅ {agent_info}, {date_info}'))
                    print(f"   ✅ Flux cohérent: {agent_info}, {date_info}")
                else:
                    self.resultats.append(('Flux incomplet', '⚠️  Aucune vérification trouvée'))
                    print("   ⚠️  Flux incomplet: aucune vérification trouvée")
                    
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
        elif tests_reussis >= total_tests * 0.7:
            print("⚠️  FLUX FONCTIONNEL AVEC QUELQUES PROBLEMES")
        else:
            print("🔴 PROBLEMES MAJEURS DÉTECTÉS DANS LE FLUX")

# Exécution
if __name__ == "__main__":
    testeur = TestFluxCotisationsCorrige()
    testeur.tester_modeles_disponibles()
    testeur.tester_creation_agent()
    testeur.tester_creation_verification()
    testeur.tester_flux_complet()
    testeur.afficher_resultats()