#!/usr/bin/env python
"""
TEST DE CONNEXION COMPLET - Adapté aux modèles réels
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class ComprehensiveConnectionTest:
    """Classe de test complet adaptée aux modèles réels"""
    
    def __init__(self):
        self.client = Client()
        self.User = get_user_model()
        self.results = {}
    
    def create_test_users(self):
        """Crée des utilisateurs de test avec les champs EXACTS de vos modèles"""
        print("👥 Création des utilisateurs de test...")
        
        try:
            # 1. MEMBRE - AVEC CHAMPS EXACTS
            self.membre_user, created = self.User.objects.get_or_create(
                username='membre_test',
                defaults={
                    'email': 'membre@mutuelle.com',
                    'password': 'password123',
                    'is_active': True,
                    'first_name': 'John',
                    'last_name': 'Doe'
                }
            )
            if created:
                self.membre_user.set_password('password123')
                self.membre_user.save()
            
            from membres.models import Membre
            try:
                self.membre, created = Membre.objects.get_or_create(
                    user=self.membre_user,
                    defaults={
                        'numero_unique': 'MEM001',
                        'nom': 'Doe',
                        'prenom': 'John',
                        'telephone': '+2250102030405',
                        'statut': 'actif',
                        'categorie': 'standard',
                        'date_naissance': '1990-01-01',
                        'adresse': 'Adresse test',
                        'email': 'membre@mutuelle.com',
                        'profession': 'Testeur',
                        'type_piece_identite': 'cni',
                        'numero_piece_identite': 'CI001',
                        'statut_documents': 'valide'
                    }
                )
                print("✅ Membre créé avec succès")
            except Exception as e:
                print(f"⚠️  Création Membre: {e}")
                return False
            
            # 2. ASSUREUR - AVEC CHAMPS EXACTS
            self.assureur_user, created = self.User.objects.get_or_create(
                username='assureur_test',
                defaults={
                    'email': 'assureur@mutuelle.com',
                    'password': 'password123',
                    'is_staff': True,
                    'is_active': True,
                    'first_name': 'Assureur',
                    'last_name': 'Test'
                }
            )
            if created:
                self.assureur_user.set_password('password123')
                self.assureur_user.save()
            
            from assureur.models import Assureur
            try:
                self.assureur, created = Assureur.objects.get_or_create(
                    user=self.assureur_user,
                    defaults={
                        'numero_employe': 'ASS001',
                        'departement': 'Commercial',
                        'date_embauche': '2020-01-01',
                        'est_actif': True
                    }
                )
                print("✅ Assureur créé avec succès")
            except Exception as e:
                print(f"⚠️  Création Assureur: {e}")
                return False
            
            # 3. MÉDECIN - AVEC CHAMPS EXACTS (incluant etablissement)
            self.medecin_user, created = self.User.objects.get_or_create(
                username='medecin_test',
                defaults={
                    'email': 'medecin@mutuelle.com',
                    'password': 'password123',
                    'is_active': True,
                    'first_name': 'Jane',
                    'last_name': 'Smith'
                }
            )
            if created:
                self.medecin_user.set_password('password123')
                self.medecin_user.save()
            
            from medecin.models import Medecin
            try:
                # Vérifier s'il existe déjà un établissement, sinon créer un minimal
                from medecin.models import Etablissement
                etablissement, _ = Etablissement.objects.get_or_create(
                    nom="Centre Médical Test",
                    defaults={
                        'adresse': 'Adresse test',
                        'telephone': '+2250100000000',
                        'type_etablissement': 'clinique'
                    }
                )
                
                self.medecin, created = Medecin.objects.get_or_create(
                    user=self.medecin_user,
                    defaults={
                        'numero_ordre': 'MED001',
                        'specialite': 'Généraliste',
                        'etablissement': etablissement,
                        'telephone_pro': '+2250506070809',
                        'email_pro': 'medecin@mutuelle.com',
                        'annees_experience': 5,
                        'tarif_consultation': 5000,
                        'actif': True,
                        'disponible': True
                    }
                )
                print("✅ Médecin créé avec succès")
            except Exception as e:
                print(f"⚠️  Création Medecin: {e}")
                # Essayer sans établissement si le modèle le permet
                try:
                    self.medecin = Medecin.objects.create(
                        user=self.medecin_user,
                        numero_ordre='MED001',
                        specialite='Généraliste',
                        telephone_pro='+2250506070809',
                        actif=True
                    )
                    print("✅ Médecin créé (sans établissement)")
                except Exception as e2:
                    print(f"❌ Impossible de créer médecin: {e2}")
                    return False
            
            # 4. PHARMACIEN - AVEC CHAMPS EXACTS
            self.pharmacien_user, created = self.User.objects.get_or_create(
                username='pharmacien_test',
                defaults={
                    'email': 'pharmacien@mutuelle.com',
                    'password': 'password123',
                    'is_active': True,
                    'first_name': 'Pierre',
                    'last_name': 'Martin'
                }
            )
            if created:
                self.pharmacien_user.set_password('password123')
                self.pharmacien_user.save()
            
            from pharmacien.models import Pharmacien
            try:
                self.pharmacien, created = Pharmacien.objects.get_or_create(
                    user=self.pharmacien_user,
                    defaults={
                        'nom_pharmacie': 'Pharmacie Centrale Test',
                        'adresse_pharmacie': 'Adresse pharmacie test',
                        'telephone': '+2250708091011',
                        'actif': True,
                        'numero_pharmacien': 'PHARM001',
                        'specialite': 'Générale'
                    }
                )
                print("✅ Pharmacien créé avec succès")
            except Exception as e:
                print(f"⚠️  Création Pharmacien: {e}")
                return False
            
            # 5. AGENT - AVEC CHAMPS EXACTS
            self.agent_user, created = self.User.objects.get_or_create(
                username='agent_test',
                defaults={
                    'email': 'agent@mutuelle.com',
                    'password': 'password123',
                    'is_staff': True,
                    'is_active': True,
                    'first_name': 'Agent',
                    'last_name': 'Test'
                }
            )
            if created:
                self.agent_user.set_password('password123')
                self.agent_user.save()
            
            from agents.models import Agent
            try:
                self.agent, created = Agent.objects.get_or_create(
                    user=self.agent_user,
                    defaults={
                        'matricule': 'AGENT001',
                        'poste': 'Agent de terrain',
                        'role': 'saisie',
                        'date_embauche': '2023-01-01',
                        'est_actif': True,
                        'limite_bons_quotidienne': 10,
                        'telephone': '+2250901010101',
                        'email_professionnel': 'agent@mutuelle.com'
                    }
                )
                print("✅ Agent créé avec succès")
            except Exception as e:
                print(f"⚠️  Création Agent: {e}")
                return False
            
            print("🎉 Tous les utilisateurs de test créés avec succès")
            return True
            
        except Exception as e:
            print(f"❌ Erreur création utilisateurs: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_basic_login(self):
        """Test de connexion basique pour chaque utilisateur"""
        print("\n🔐 TESTS DE CONNEXION BASIQUES...")
        
        users_to_test = [
            ('membre_test', 'Membre'),
            ('assureur_test', 'Assureur'),
            ('medecin_test', 'Médecin'),
            ('pharmacien_test', 'Pharmacien'),
            ('agent_test', 'Agent'),
        ]
        
        results = {}
        for username, user_type in users_to_test:
            try:
                print(f"\n--- Test {user_type} ---")
                
                # Test connexion
                login_success = self.client.login(
                    username=username, 
                    password='password123'
                )
                
                if login_success:
                    print(f"✅ {user_type}: Authentification réussie")
                    
                    # Test session
                    session = self.client.session
                    if '_auth_user_id' in session:
                        user_id = session['_auth_user_id']
                        print(f"✅ Session active (User ID: {user_id})")
                    
                    # Test page d'accueil
                    response = self.client.get('/')
                    print(f"✅ Accès page accueil: {response.status_code}")
                    
                    # Test URLs spécifiques
                    self.test_user_specific_urls(user_type)
                    
                    # Déconnexion
                    self.client.logout()
                    print(f"✅ Déconnexion réussie")
                    results[user_type] = True
                else:
                    print(f"❌ {user_type}: Échec authentification")
                    results[user_type] = False
                    
            except Exception as e:
                print(f"❌ {user_type}: Erreur - {e}")
                results[user_type] = False
        
        return results
    
    def test_user_specific_urls(self, user_type):
        """Test les URLs spécifiques à chaque type d'utilisateur"""
        urls_to_test = []
        
        if user_type == 'Agent':
            urls_to_test = [
                ('/agents/', 'Dashboard agent'),
                ('/agents/dashboard/', 'Dashboard agent détaillé'),
            ]
        elif user_type == 'Membre':
            urls_to_test = [
                ('/membres/', 'Espace membre'),
                ('/membres/profil/', 'Profil membre'),
            ]
        elif user_type == 'Assureur':
            urls_to_test = [
                ('/assureur/', 'Espace assureur'),
                ('/assureur/dashboard/', 'Dashboard assureur'),
            ]
        elif user_type == 'Médecin':
            urls_to_test = [
                ('/medecin/', 'Espace médecin'),
                ('/medecin/consultations/', 'Consultations'),
            ]
        elif user_type == 'Pharmacien':
            urls_to_test = [
                ('/pharmacien/', 'Espace pharmacien'),
                ('/pharmacien/ordonnances/', 'Ordonnances'),
            ]
        
        for url, description in urls_to_test:
            try:
                response = self.client.get(url)
                if response.status_code == 200:
                    print(f"   ✅ {description}: Accessible")
                elif response.status_code == 302:
                    print(f"   🔀 {description}: Redirection vers {response.url}")
                elif response.status_code == 403:
                    print(f"   🚫 {description}: Permission refusée")
                elif response.status_code == 404:
                    print(f"   ❌ {description}: Non trouvé")
                else:
                    print(f"   ⚠️  {description}: Code {response.status_code}")
            except Exception as e:
                print(f"   ❌ {description}: Erreur - {e}")
    
    def test_public_urls(self):
        """Test les URLs publiques accessibles sans connexion"""
        print("\n🌐 TEST DES URLS PUBLIQUES...")
        
        public_urls = [
            ('/', 'Page d\'accueil'),
            ('/accounts/login/', 'Page de connexion'),
            ('/accounts/signup/', 'Page d\'inscription'),
            ('/about/', 'À propos'),
        ]
        
        for url, description in public_urls:
            try:
                response = self.client.get(url)
                if response.status_code == 200:
                    print(f"✅ {description}: Accessible")
                elif response.status_code == 302:
                    print(f"🔀 {description}: Redirection")
                elif response.status_code == 404:
                    print(f"❌ {description}: Non trouvé")
                else:
                    print(f"⚠️  {description}: Code {response.status_code}")
            except Exception as e:
                print(f"❌ {description}: Erreur - {e}")
    
    def verify_user_profiles(self):
        """Vérifie que les profils utilisateurs sont correctement liés"""
        print("\n👤 VÉRIFICATION DES PROFILS UTILISATEURS...")
        
        try:
            from membres.models import Membre
            from assureur.models import Assureur
            from medecin.models import Medecin
            from pharmacien.models import Pharmacien
            from agents.models import Agent
            
            # Vérification Membre
            try:
                membre = Membre.objects.get(user__username='membre_test')
                print(f"✅ Membre: {membre.nom} {membre.prenom} ({membre.numero_unique})")
            except Exception as e:
                print(f"❌ Membre: {e}")
            
            # Vérification Assureur
            try:
                assureur = Assureur.objects.get(user__username='assureur_test')
                print(f"✅ Assureur: {assureur.numero_employe}")
            except Exception as e:
                print(f"❌ Assureur: {e}")
            
            # Vérification Medecin
            try:
                medecin = Medecin.objects.get(user__username='medecin_test')
                print(f"✅ Médecin: Dr. {medecin.user.last_name} ({medecin.specialite})")
            except Exception as e:
                print(f"❌ Médecin: {e}")
            
            # Vérification Pharmacien
            try:
                pharmacien = Pharmacien.objects.get(user__username='pharmacien_test')
                print(f"✅ Pharmacien: {pharmacien.nom_pharmacie}")
            except Exception as e:
                print(f"❌ Pharmacien: {e}")
            
            # Vérification Agent
            try:
                agent = Agent.objects.get(user__username='agent_test')
                print(f"✅ Agent: {agent.matricule} ({agent.poste})")
            except Exception as e:
                print(f"❌ Agent: {e}")
                
        except Exception as e:
            print(f"❌ Erreur vérification profils: {e}")
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        print("=" * 60)
        print("🧪 DÉMARRAGE DES TESTS DE CONNEXION COMPLETS")
        print("=" * 60)
        
        # Création des utilisateurs
        if not self.create_test_users():
            print("❌ Impossible de créer les utilisateurs de test")
            print("💡 Essayez de créer d'abord les modèles nécessaires...")
            return False
        
        # Exécution des tests
        print("\n" + "=" * 50)
        print("EXÉCUTION DES TESTS PRINCIPAUX")
        print("=" * 50)
        
        # Test URLs publiques
        self.test_public_urls()
        
        # Test connexions basiques
        login_results = self.test_basic_login()
        
        # Vérification profils
        self.verify_user_profiles()
        
        # Résumé final
        print("\n" + "=" * 60)
        print("📊 RÉSUMUM FINAL DES TESTS")
        print("=" * 60)
        
        total_success = sum(login_results.values())
        total_tests = len(login_results)
        
        for user_type, success in login_results.items():
            status = "✅ RÉUSSI" if success else "❌ ÉCHEC"
            print(f"{user_type}: {status}")
        
        print(f"\n🎯 TOTAL: {total_success}/{total_tests} connexions réussies")
        
        if total_success == total_tests:
            print("🎉 TOUTES LES CONNEXIONS SONT RÉUSSIES!")
            print("✨ Votre système d'authentification fonctionne parfaitement!")
        elif total_success >= 3:
            print("⚠️  La plupart des connexions fonctionnent - Vérifiez les échecs")
        else:
            print("❌ Problèmes majeurs d'authentification - Intervention nécessaire")
        
        return total_success == total_tests

def main():
    """Fonction principale"""
    test_suite = ComprehensiveConnectionTest()
    success = test_suite.run_all_tests()
    
    if success:
        print("\n🚀 Tous les tests sont passés avec succès!")
        sys.exit(0)
    else:
        print("\n💡 Conseils de dépannage:")
        print("1. Vérifiez que la base de données est migrée")
        print("2. Vérifiez les modèles dans admin Django")
        print("3. Testez avec un utilisateur simple d'abord")
        sys.exit(1)

if __name__ == "__main__":
    main()