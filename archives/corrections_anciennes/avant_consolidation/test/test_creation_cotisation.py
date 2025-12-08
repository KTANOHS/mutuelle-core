# test_creation_cotisation.py
import os
import sys
import django
from datetime import datetime, timedelta

# Configuration Django
sys.path.append('/Users/koffitanohsoualiho/Documents/P FINALE AVANT SYNCHRO/pf erreur/projet 21.49.30')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from assureur.models import Cotisation
from membres.models import Membre
from decimal import Decimal
import json

class TestCreationCotisation(TestCase):
    """Tests complets pour la création de cotisations"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        print("🧪 Configuration des tests...")
        
        # Créer un utilisateur assureur
        self.assureur_user = User.objects.create_user(
            username='test_assureur',
            email='assureur@test.com',
            password='test123'
        )
        
        # Créer un membre pour les tests
        self.membre = Membre.objects.create(
            nom="Test",
            prenom="Membre",
            numero_unique="MEMTEST001",
            email="membre@test.com",
            telephone="0123456789",
            statut="actif"
        )
        
        # Client de test
        self.client = Client()
        
        print(f"✅ Utilisateur créé: {self.assureur_user.username}")
        print(f"✅ Membre créé: {self.membre.prenom} {self.membre.nom}")
    
    def test_creation_cotisation_api(self):
        """Test de l'API de création de cotisation"""
        print("\n🔍 Test 1: API de création de cotisation")
        print("="*50)
        
        # Se connecter
        self.client.login(username='test_assureur', password='test123')
        
        # URL pour créer une cotisation
        url = reverse('assureur:creer_cotisation_membre', args=[self.membre.id])
        
        # Données de test
        data = {
            'periode': '2025-12',
            'montant': '5000.00',
            'type_cotisation': 'normale',
            'notes': 'Cotisation de test API'
        }
        
        # Envoyer la requête POST
        response = self.client.post(url, data, follow=True)
        
        print(f"📤 URL: {url}")
        print(f"📝 Données: {data}")
        print(f"📥 Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Requête réussie (status 200)")
            
            # Vérifier les messages
            messages = list(response.context['messages']) if response.context else []
            for message in messages:
                print(f"📨 Message: {message}")
        elif response.status_code == 302:
            print("🔄 Redirection détectée")
            print(f"📎 Redirection vers: {response.url}")
        else:
            print(f"❌ Échec: Status {response.status_code}")
            print(f"📄 Réponse: {response.content[:500]}")
        
        # Vérifier si la cotisation a été créée
        cotisations_count = Cotisation.objects.filter(membre=self.membre).count()
        print(f"📊 Nombre de cotisations pour le membre: {cotisations_count}")
        
        if cotisations_count > 0:
            dernière_cotisation = Cotisation.objects.filter(membre=self.membre).latest('created_at')
            print(f"🎉 Dernière cotisation créée:")
            print(f"   - Référence: {dernière_cotisation.reference}")
            print(f"   - Période: {dernière_cotisation.periode}")
            print(f"   - Montant: {dernière_cotisation.montant}")
            print(f"   - Statut: {dernière_cotisation.statut}")
        
        return response.status_code
    
    def test_creation_cotisation_directe(self):
        """Test de création directe via ORM"""
        print("\n🔍 Test 2: Création directe via ORM")
        print("="*50)
        
        try:
            # Créer une cotisation directement
            cotisation = Cotisation.objects.create(
                membre=self.membre,
                periode='2025-12',
                montant=Decimal('5000.00'),
                type_cotisation='normale',
                date_emission=datetime.now().date(),
                date_echeance=(datetime.now() + timedelta(days=30)).date(),
                statut='due',
                reference=f'COT-TEST-{datetime.now().strftime("%Y%m%d%H%M%S")}',
                enregistre_par=self.assureur_user,
                notes='Test création directe'
            )
            
            print("✅ Cotisation créée avec succès")
            print(f"📝 Détails:")
            print(f"   - ID: {cotisation.id}")
            print(f"   - Référence: {cotisation.reference}")
            print(f"   - Membre: {cotisation.membre.prenom} {cotisation.membre.nom}")
            print(f"   - Période: {cotisation.periode}")
            print(f"   - Montant: {cotisation.montant}")
            print(f"   - Statut: {cotisation.statut}")
            print(f"   - Créé par: {cotisation.enregistre_par.username}")
            
            # Vérifier les champs
            print(f"\n🔍 Vérification des champs:")
            expected_fields = [
                'membre', 'periode', 'montant', 'type_cotisation',
                'date_emission', 'date_echeance', 'statut', 'reference',
                'enregistre_par', 'notes', 'created_at', 'updated_at'
            ]
            
            for field in expected_fields:
                if hasattr(cotisation, field):
                    print(f"   ✅ {field}: {getattr(cotisation, field)}")
                else:
                    print(f"   ❌ {field}: NON DISPONIBLE")
            
            # Vérifier qu'il n'y a pas les champs problématiques
            problem_fields = ['montant_clinique', 'montant_pharmacie', 'montant_charges_mutuelle']
            for field in problem_fields:
                if hasattr(cotisation, field):
                    print(f"   ⚠️  {field}: EXISTE (ne devrait pas être là)")
                else:
                    print(f"   ✅ {field}: N'EXISTE PAS (correct)")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la création: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_formulaire_web(self):
        """Test d'accès au formulaire web"""
        print("\n🔍 Test 3: Accès au formulaire web")
        print("="*50)
        
        # Se connecter
        self.client.login(username='test_assureur', password='test123')
        
        # URL du formulaire
        url = reverse('assureur:creer_cotisation_membre', args=[self.membre.id])
        
        # Accéder au formulaire (GET)
        response = self.client.get(url)
        
        print(f"🌐 URL: {url}")
        print(f"📥 Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Formulaire accessible")
            
            # Vérifier le contenu
            content = response.content.decode('utf-8')
            
            # Vérifier les éléments importants
            checks = [
                ('Période (Mois)', 'Champ période présent'),
                ('Montant (FCFA)', 'Champ montant présent'),
                ('Type de cotisation', 'Champ type présent'),
                ('Notes', 'Champ notes présent'),
                ('Créer la cotisation', 'Bouton de soumission présent')
            ]
            
            for text, description in checks:
                if text in content:
                    print(f"   ✅ {description}")
                else:
                    print(f"   ❌ {description} - NON TROUVÉ")
            
            # Vérifier que les champs problématiques ne sont pas dans le formulaire
            problem_texts = ['montant_clinique', 'montant_pharmacie', 'montant_charges_mutuelle']
            for text in problem_texts:
                if text in content.lower():
                    print(f"   ⚠️  Champ problématique '{text}' présent dans le formulaire")
                else:
                    print(f"   ✅ Champ problématique '{text}' absent du formulaire")
        
        else:
            print(f"❌ Impossible d'accéder au formulaire")
            print(f"📄 Réponse: {response.content[:500]}")
        
        return response.status_code
    
    def test_liste_cotisations(self):
        """Test d'accès à la liste des cotisations"""
        print("\n🔍 Test 4: Liste des cotisations")
        print("="*50)
        
        # Se connecter
        self.client.login(username='test_assureur', password='test123')
        
        # URL de la liste
        url = reverse('assureur:liste_cotisations')
        
        # Accéder à la liste
        response = self.client.get(url)
        
        print(f"📋 URL: {url}")
        print(f"📥 Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Liste accessible")
            
            # Vérifier si des cotisations sont affichées
            content = response.content.decode('utf-8')
            
            # Vérifier les éléments
            if 'Cotisations' in content:
                print("   ✅ Titre 'Cotisations' présent")
            
            if 'Aucune cotisation' in content:
                print("   ℹ️  Aucune cotisation trouvée")
            else:
                # Chercher des lignes de tableau
                import re
                table_rows = re.findall(r'<tr[^>]*>.*?</tr>', content, re.DOTALL)
                if len(table_rows) > 1:  # Plus que l'en-tête
                    print(f"   📊 {len(table_rows)-1} ligne(s) de cotisation(s) affichée(s)")
        
        return response.status_code
    
    def test_workflow_complet(self):
        """Test du workflow complet de création"""
        print("\n🔍 Test 5: Workflow complet")
        print("="*50)
        
        # 1. Accéder à la liste des membres
        self.client.login(username='test_assureur', password='test123')
        url_membres = reverse('assureur:liste_membres')
        response = self.client.get(url_membres)
        
        if response.status_code == 200:
            print("✅ 1. Liste des membres accessible")
            
            # Vérifier si notre membre est dans la liste
            content = response.content.decode('utf-8')
            if self.membre.nom in content and self.membre.prenom in content:
                print(f"   ✅ Membre {self.membre.prenom} {self.membre.nom} trouvé")
            else:
                print(f"   ❌ Membre non trouvé dans la liste")
        
        # 2. Accéder à la page détail du membre
        url_detail = reverse('assureur:detail_membre', args=[self.membre.id])
        response = self.client.get(url_detail)
        
        if response.status_code == 200:
            print("✅ 2. Détail membre accessible")
            
            # Vérifier le bouton "Créer une cotisation"
            content = response.content.decode('utf-8')
            if 'Créer une cotisation' in content:
                print("   ✅ Bouton 'Créer une cotisation' présent")
            else:
                print("   ❌ Bouton 'Créer une cotisation' absent")
        
        # 3. Créer une cotisation via le formulaire
        url_creer = reverse('assureur:creer_cotisation_membre', args=[self.membre.id])
        
        # D'abord récupérer le formulaire pour avoir le CSRF token
        response = self.client.get(url_creer)
        if response.status_code == 200:
            print("✅ 3. Formulaire de création accessible")
            
            # Extraire le CSRF token
            import re
            csrf_match = re.search(r'name=["\']csrfmiddlewaretoken["\'] value=["\']([^"\']+)["\']', response.content.decode('utf-8'))
            
            if csrf_match:
                csrf_token = csrf_match.group(1)
                print("   ✅ CSRF token trouvé")
                
                # Données du formulaire
                data = {
                    'csrfmiddlewaretoken': csrf_token,
                    'periode': '2025-12',
                    'montant': '7500.00',
                    'type_cotisation': 'femme_enceinte',
                    'statut': 'due',
                    'notes': 'Test workflow complet'
                }
                
                # Soumettre le formulaire
                response = self.client.post(url_creer, data, follow=True)
                
                if response.status_code in [200, 302]:
                    print("✅ 4. Formulaire soumis avec succès")
                    
                    # Vérifier la redirection
                    if len(response.redirect_chain) > 0:
                        print(f"   🔄 Redirection vers: {response.redirect_chain[-1][0]}")
                    
                    # Vérifier les messages
                    messages = list(response.context['messages']) if response.context else []
                    if messages:
                        for message in messages:
                            print(f"   📨 Message: {message}")
                    else:
                        print("   ℹ️  Aucun message affiché")
                    
                    # Vérifier que la cotisation a été créée
                    nouvelle_cotisation = Cotisation.objects.filter(
                        membre=self.membre,
                        periode='2025-12',
                        montant=Decimal('7500.00')
                    ).first()
                    
                    if nouvelle_cotisation:
                        print(f"✅ 5. Cotisation créée avec succès: {nouvelle_cotisation.reference}")
                    else:
                        print("❌ 5. Cotisation non trouvée dans la base de données")
                else:
                    print(f"❌ 4. Échec de soumission: {response.status_code}")
            else:
                print("❌ CSRF token non trouvé")
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        print("🚀 LANCEMENT DE TOUS LES TESTS")
        print("="*60)
        
        results = []
        
        # Test 1
        print("\n1️⃣  Test API création...")
        result1 = self.test_creation_cotisation_api()
        results.append(('API création', result1))
        
        # Test 2
        print("\n2️⃣  Test création directe...")
        result2 = self.test_creation_cotisation_directe()
        results.append(('Création directe', result2))
        
        # Test 3
        print("\n3️⃣  Test formulaire web...")
        result3 = self.test_formulaire_web()
        results.append(('Formulaire web', result3))
        
        # Test 4
        print("\n4️⃣  Test liste cotisations...")
        result4 = self.test_liste_cotisations()
        results.append(('Liste cotisations', result4))
        
        # Test 5
        print("\n5️⃣  Test workflow complet...")
        self.test_workflow_complet()
        results.append(('Workflow complet', 'Exécuté'))
        
        # Résumé
        print("\n" + "="*60)
        print("📊 RÉSUMUM DES TESTS")
        print("="*60)
        
        for test_name, result in results:
            if isinstance(result, bool):
                status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
            elif isinstance(result, int):
                status = "✅ PASSÉ" if result in [200, 302] else f"❌ ÉCHOUÉ (code: {result})"
            else:
                status = "ℹ️  EXÉCUTÉ"
            
            print(f"{test_name:20} : {status}")
        
        print("\n🎯 Tests terminés !")

def test_simple_creation():
    """Test simple sans framework de test"""
    print("🧪 Test simple de création de cotisation")
    print("="*50)
    
    try:
        # Récupérer un utilisateur et un membre
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            user = User.objects.first()
        
        membre = Membre.objects.first()
        
        if not user or not membre:
            print("❌ Utilisateur ou membre non trouvé")
            return
        
        print(f"👤 Utilisateur: {user.username}")
        print(f"👤 Membre: {membre.prenom} {membre.nom}")
        
        # Créer une cotisation
        cotisation = Cotisation.objects.create(
            membre=membre,
            periode='2025-12',
            montant=Decimal('5000.00'),
            type_cotisation='normale',
            date_emission=datetime.now().date(),
            date_echeance=(datetime.now() + timedelta(days=30)).date(),
            statut='due',
            reference=f'COT-SIMPLE-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            enregistre_par=user,
            notes='Test simple création'
        )
        
        print(f"✅ Cotisation créée avec succès!")
        print(f"📝 Référence: {cotisation.reference}")
        print(f"💰 Montant: {cotisation.montant} FCFA")
        print(f"📅 Période: {cotisation.periode}")
        print(f"📊 Statut: {cotisation.statut}")
        
        # Vérifier la liste
        count = Cotisation.objects.count()
        print(f"\n📊 Total cotisations en base: {count}")
        
        # Supprimer la cotisation test
        cotisation.delete()
        print("🧹 Cotisation test supprimée")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 SCRIPT DE TEST CRÉATION COTISATION")
    print("="*60)
    
    # Option 1: Tests unitaires complets
    print("\nOption 1: Tests unitaires complets")
    print("-" * 40)
    
    try:
        test_suite = TestCreationCotisation()
        test_suite.setUp()
        test_suite.run_all_tests()
    except Exception as e:
        print(f"❌ Erreur lors des tests unitaires: {e}")
    
    # Option 2: Test simple
    print("\n" + "="*60)
    print("\nOption 2: Test simple de création")
    print("-" * 40)
    
    test_simple_creation()
    
    # Option 3: Test via le shell Django
    print("\n" + "="*60)
    print("\nOption 3: Commande pour tester via shell")
    print("-" * 40)
    
    print("""
Pour tester manuellement via le shell Django:
    
    python manage.py shell
    
    from assureur.models import Cotisation
    from membres.models import Membre
    from django.contrib.auth.models import User
    from decimal import Decimal
    
    # Récupérer un utilisateur et un membre
    user = User.objects.first()
    membre = Membre.objects.first()
    
    # Créer une cotisation
    cotisation = Cotisation.objects.create(
        membre=membre,
        periode='2025-12',
        montant=Decimal('5000.00'),
        type_cotisation='normale',
        statut='due',
        reference='COT-TEST-12345',
        enregistre_par=user
    )
    
    print(f"Créée: {cotisation.reference}")
    """)
    
    print("\n" + "="*60)
    print("📋 Pour tester via l'interface web:")
    print("1. Lancez le serveur: python manage.py runserver")
    print("2. Accédez à: http://localhost:8000/assureur/membres/")
    print("3. Cliquez sur un membre")
    print("4. Cliquez sur 'Créer une cotisation'")
    print("5. Remplissez le formulaire et soumettez")
    print("="*60)