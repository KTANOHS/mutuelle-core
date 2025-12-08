#!/usr/bin/env python
"""
SCRIPT DE TEST POUR LES PAIEMENTS
=================================
Ce script teste les fonctionnalités de paiement de l'assureur.
Exécution : python manage.py shell < test_paiement.py
"""

import os
import sys
import django
from django.test import RequestFactory, Client
from django.contrib.auth.models import User, Group
from django.utils import timezone
from decimal import Decimal

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

# Import des modèles après configuration
from assureur.models import Assureur, Paiement, Soin, Bon
from agents.models import Membre
from assureur.views import creer_paiement, liste_paiements
from assureur.forms import PaiementForm

class TestPaiementAssureur:
    """Classe de test pour les fonctionnalités de paiement"""
    
    def __init__(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.assureur_user = None
        self.membre_test = None
        self.soin_test = None
        
    def setup_test_data(self):
        """Création des données de test"""
        print("🔧 Configuration des données de test...")
        
        try:
            # 1. Créer un utilisateur assureur
            self.assureur_user, created = User.objects.get_or_create(
                username='test_assureur',
                defaults={
                    'email': 'assureur@test.com',
                    'first_name': 'Test',
                    'last_name': 'Assureur',
                    'is_active': True,
                    'is_staff': True
                }
            )
            if created:
                self.assureur_user.set_password('test123')
                self.assureur_user.save()
                print(f"✅ Utilisateur assureur créé: {self.assureur_user.username}")
            
            # 2. Ajouter au groupe ASSUREUR
            groupe_assureur, _ = Group.objects.get_or_create(name='assureur')
            self.assureur_user.groups.add(groupe_assureur)
            
            # 3. Créer un profil Assureur
            assureur_profile, _ = Assureur.objects.get_or_create(
                user=self.assureur_user,
                defaults={
                    'nom': 'Test Assureur',
                    'email': 'assureur@test.com',
                    'telephone': '0123456789',
                    'adresse': '123 Rue de Test',
                    'est_actif': True
                }
            )
            print(f"✅ Profil assureur créé: {assureur_profile}")
            
            # 4. Créer un membre de test
            self.membre_test, created = Membre.objects.get_or_create(
                numero_unique='TEST001',
                defaults={
                    'nom': 'Doe',
                    'prenom': 'John',
                    'email': 'john.doe@test.com',
                    'telephone': '0987654321',
                    'statut': 'actif',
                    'date_inscription': timezone.now()
                }
            )
            print(f"✅ Membre de test créé: {self.membre_test}")
            
            # 5. Créer un soin de test
            self.soin_test, created = Soin.objects.get_or_create(
                membre=self.membre_test,
                defaults={
                    'code': 'SOIN-TEST-001',
                    'type_soin': 'consultation',
                    'montant_facture': Decimal('5000.00'),
                    'montant_rembourse': Decimal('4000.00'),
                    'statut': 'valide',
                    'date_soin': timezone.now().date()
                }
            )
            print(f"✅ Soin de test créé: {self.soin_test}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la configuration: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_connexion_assureur(self):
        """Test de connexion de l'assureur"""
        print("\n🔐 Test de connexion...")
        
        try:
            # Tentative de connexion
            login_success = self.client.login(
                username='test_assureur',
                password='test123'
            )
            
            if login_success:
                print("✅ Connexion réussie")
                return True
            else:
                print("❌ Échec de connexion")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de la connexion: {e}")
            return False
    
    def test_liste_paiements(self):
        """Test d'accès à la liste des paiements"""
        print("\n📋 Test de la liste des paiements...")
        
        try:
            # Créer une requête simulée
            request = self.factory.get('/assureur/paiements/')
            request.user = self.assureur_user
            
            # Appeler la vue
            response = liste_paiements(request)
            
            if response.status_code == 200:
                print("✅ Liste des paiements accessible")
                return True
            else:
                print(f"❌ Erreur HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors du test liste: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_formulaire_paiement(self):
        """Test du formulaire de paiement"""
        print("\n📝 Test du formulaire de paiement...")
        
        try:
            # Créer une requête POST simulée
            data = {
                'membre': self.membre_test.id,
                'soin': self.soin_test.id,
                'montant': '5000.00',
                'date_paiement': timezone.now().date(),
                'mode_paiement': 'espece',
                'statut': 'initie',
                'reference': 'PAY-TEST-001',
                'banque': '',
                'numero_transaction': 'TX001',
                'numero_compte': '',
                'notes': 'Paiement de test'
            }
            
            form = PaiementForm(data=data)
            
            if form.is_valid():
                print("✅ Formulaire valide")
                print(f"   Données nettoyées: {form.cleaned_data}")
                return True, form
            else:
                print("❌ Formulaire invalide")
                print(f"   Erreurs: {form.errors}")
                return False, None
                
        except Exception as e:
            print(f"❌ Erreur lors du test formulaire: {e}")
            import traceback
            traceback.print_exc()
            return False, None
    
    def test_creer_paiement_web(self):
        """Test de création de paiement via requête web"""
        print("\n🌐 Test de création de paiement via web...")
        
        try:
            # Connecter le client
            self.client.login(username='test_assureur', password='test123')
            
            # Données du formulaire
            data = {
                'membre': self.membre_test.id,
                'soin': self.soin_test.id,
                'montant': '5000.00',
                'date_paiement': timezone.now().date().isoformat(),
                'mode_paiement': 'espece',
                'statut': 'initie',
                'reference': 'PAY-TEST-WEB-001',
                'banque': '',
                'numero_transaction': 'TX-WEB-001',
                'numero_compte': '',
                'notes': 'Paiement web de test',
                'csrfmiddlewaretoken': 'test_token'  # Généralement géré automatiquement
            }
            
            # Envoyer la requête POST
            response = self.client.post('/assureur/paiements/creer/', data, follow=True)
            
            print(f"   Code de statut: {response.status_code}")
            print(f"   Redirection: {len(response.redirect_chain)} redirection(s)")
            
            if response.status_code in [200, 302]:
                print("✅ Requête web réussie")
                return True
            else:
                print("❌ Échec de la requête web")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors du test web: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_api_soins_par_membre(self):
        """Test de l'API pour récupérer les soins par membre"""
        print("\n🔗 Test de l'API soins par membre...")
        
        try:
            self.client.login(username='test_assureur', password='test123')
            
            response = self.client.get(f'/api/soins-par-membre/{self.membre_test.id}/')
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API accessible, {len(data)} soin(s) retourné(s)")
                return True
            else:
                print(f"❌ Erreur API: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors du test API: {e}")
            return False
    
    def test_paiements_existants(self):
        """Vérification des paiements existants en base"""
        print("\n📊 Vérification des paiements en base...")
        
        try:
            paiements_count = Paiement.objects.count()
            print(f"   Total paiements en base: {paiements_count}")
            
            if paiements_count > 0:
                # Afficher les 5 derniers paiements
                derniers_paiements = Paiement.objects.select_related(
                    'membre', 'soin'
                ).order_by('-date_paiement')[:5]
                
                print(f"   Derniers paiements ({len(derniers_paiements)}):")
                for p in derniers_paiements:
                    print(f"     - {p.reference}: {p.montant} FCFA ({p.statut})")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la vérification: {e}")
            return False
    
    def cleanup(self):
        """Nettoyage des données de test"""
        print("\n🧹 Nettoyage des données de test...")
        
        try:
            # Supprimer les données de test
            deleted_count = Paiement.objects.filter(reference__contains='TEST').delete()
            if deleted_count[0] > 0:
                print(f"✅ {deleted_count[0]} paiement(s) de test supprimé(s)")
            
            # Ne pas supprimer l'utilisateur de test pour les futurs tests
            print("✅ Données temporaires nettoyées")
            return True
            
        except Exception as e:
            print(f"⚠️ Erreur lors du nettoyage: {e}")
            return False
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        print("=" * 60)
        print("SCRIPT DE TEST PAIEMENT ASSUREUR")
        print("=" * 60)
        
        results = []
        
        # Configuration initiale
        if not self.setup_test_data():
            print("❌ Configuration des données de test échouée")
            return False
        
        # Exécution des tests
        tests = [
            ("Connexion assureur", self.test_connexion_assureur),
            ("Liste paiements", self.test_liste_paiements),
            ("Formulaire paiement", lambda: self.test_formulaire_paiement()[0]),
            ("Création web paiement", self.test_creer_paiement_web),
            ("API soins par membre", self.test_api_soins_par_membre),
            ("Vérification paiements", self.test_paiements_existants),
        ]
        
        for test_name, test_func in tests:
            print(f"\n▶️  Exécution: {test_name}")
            try:
                result = test_func()
                results.append((test_name, result))
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"   Résultat: {status}")
            except Exception as e:
                print(f"   ⚠️ ERREUR: {e}")
                results.append((test_name, False))
        
        # Résumé
        print("\n" + "=" * 60)
        print("RÉSUMÉ DES TESTS")
        print("=" * 60)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test_name}")
        
        print(f"\n📈 Score: {passed}/{total} tests réussis ({passed/total*100:.0f}%)")
        
        # Nettoyage
        self.cleanup()
        
        return passed == total

# Script exécutable directement
if __name__ == "__main__":
    # Méthode 1: Exécution via manage.py shell
    print("""
Instructions d'exécution:
=======================

Option 1: Exécuter dans le shell Django
   python manage.py shell < test_paiement.py

Option 2: Exécuter comme script Python (avec les imports configurés)
   python test_paiement.py

Option 3: Exécuter via la console Django
   >>> exec(open('test_paiement.py').read())
    """)
    
    # Si exécuté directement, tenter de lancer les tests
    tester = TestPaiementAssureur()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 Tous les tests ont réussi !")
        sys.exit(0)
    else:
        print("\n⚠️  Certains tests ont échoué. Vérifiez les logs ci-dessus.")
        sys.exit(1)