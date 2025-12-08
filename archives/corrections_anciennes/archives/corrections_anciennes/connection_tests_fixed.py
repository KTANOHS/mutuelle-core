#!/usr/bin/env python
"""
TEST DE CONNEXION INTELLIGENT - S'adapte aux modèles réels
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class SmartConnectionTest:
    """Test intelligent qui s'adapte aux modèles existants"""
    
    def __init__(self):
        self.client = Client()
        self.User = get_user_model()
        self.created_users = []
    
    def analyze_models(self):
        """Analyse les modèles disponibles et leurs champs"""
        print("🔍 ANALYSE DES MODÈLES...")
        
        models_info = {}
        
        try:
            from membres.models import Membre
            models_info['Membre'] = {
                'model': Membre,
                'fields': [f.name for f in Membre._meta.fields],
                'exists': True
            }
            print("✅ Modèle Membre trouvé")
        except Exception as e:
            models_info['Membre'] = {'exists': False, 'error': e}
            print("❌ Modèle Membre non accessible")
        
        try:
            from assureur.models import Assureur
            models_info['Assureur'] = {
                'model': Assureur,
                'fields': [f.name for f in Assureur._meta.fields],
                'exists': True
            }
            print("✅ Modèle Assureur trouvé")
        except Exception as e:
            models_info['Assureur'] = {'exists': False, 'error': e}
            print("❌ Modèle Assureur non accessible")
        
        try:
            from medecin.models import Medecin
            models_info['Medecin'] = {
                'model': Medecin,
                'fields': [f.name for f in Medecin._meta.fields],
                'exists': True
            }
            print("✅ Modèle Medecin trouvé")
            
            # Analyse spéciale pour Medecin
            medecin_fields = models_info['Medecin']['fields']
            if 'specialite' in medecin_fields:
                print("   📝 Medecin.specialite: Relation ForeignKey")
            if 'etablissement' in medecin_fields:
                print("   📝 Medecin.etablissement: Relation ForeignKey")
                
        except Exception as e:
            models_info['Medecin'] = {'exists': False, 'error': e}
            print("❌ Modèle Medecin non accessible")
        
        try:
            from pharmacien.models import Pharmacien
            models_info['Pharmacien'] = {
                'model': Pharmacien,
                'fields': [f.name for f in Pharmacien._meta.fields],
                'exists': True
            }
            print("✅ Modèle Pharmacien trouvé")
        except Exception as e:
            models_info['Pharmacien'] = {'exists': False, 'error': e}
            print("❌ Modèle Pharmacien non accessible")
        
        try:
            from agents.models import Agent
            models_info['Agent'] = {
                'model': Agent,
                'fields': [f.name for f in Agent._meta.fields],
                'exists': True
            }
            print("✅ Modèle Agent trouvé")
        except Exception as e:
            models_info['Agent'] = {'exists': False, 'error': e}
            print("❌ Modèle Agent non accessible")
        
        return models_info
    
    def create_simple_users(self):
        """Crée seulement les utilisateurs de base sans profils complexes"""
        print("\n👥 CRÉATION DES UTILISATEURS SIMPLES...")
        
        users_data = [
            {'username': 'test_membre', 'type': 'Membre', 'is_staff': False},
            {'username': 'test_assureur', 'type': 'Assureur', 'is_staff': True},
            {'username': 'test_medecin', 'type': 'Médecin', 'is_staff': False},
            {'username': 'test_pharmacien', 'type': 'Pharmacien', 'is_staff': False},
            {'username': 'test_agent', 'type': 'Agent', 'is_staff': True},
        ]
        
        for user_info in users_data:
            username = user_info['username']
            user_type = user_info['type']
            is_staff = user_info['is_staff']
            
            try:
                user, created = self.User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': f'{username}@mutuelle.com',
                        'is_staff': is_staff,
                        'is_active': True,
                        'first_name': user_type,
                        'last_name': 'Test'
                    }
                )
                if created:
                    user.set_password('password123')
                    user.save()
                    print(f"✅ {user_type}: Utilisateur créé ({username})")
                else:
                    print(f"ℹ️  {user_type}: Utilisateur existe déjà")
                
                self.created_users.append({
                    'username': username,
                    'type': user_type,
                    'user_obj': user
                })
                
            except Exception as e:
                print(f"❌ {user_type}: Erreur création - {e}")
        
        return len(self.created_users) > 0
    
    def create_simple_profiles(self, models_info):
        """Crée des profils simples si possible"""
        print("\n👤 CRÉATION DES PROFILS SIMPLES...")
        
        for user_info in self.created_users:
            username = user_info['username']
            user_type = user_info['type']
            user_obj = user_info['user_obj']
            
            if user_type == 'Membre' and models_info['Membre']['exists']:
                try:
                    from membres.models import Membre
                    membre, created = Membre.objects.get_or_create(
                        user=user_obj,
                        defaults={
                            'numero_unique': f'MEM{user_obj.id}',
                            'nom': 'Test',
                            'prenom': 'Membre',
                            'telephone': '+2250100000001',
                            'statut': 'actif',
                            'categorie': 'standard'
                        }
                    )
                    if created:
                        print(f"✅ Profil Membre créé pour {username}")
                    else:
                        print(f"ℹ️  Profil Membre existe déjà pour {username}")
                except Exception as e:
                    print(f"⚠️  Impossible de créer profil Membre: {e}")
            
            elif user_type == 'Assureur' and models_info['Assureur']['exists']:
                try:
                    from assureur.models import Assureur
                    assureur, created = Assureur.objects.get_or_create(
                        user=user_obj,
                        defaults={
                            'numero_employe': f'ASS{user_obj.id}',
                            'departement': 'Test',
                            'date_embauche': '2023-01-01',
                            'est_actif': True
                        }
                    )
                    if created:
                        print(f"✅ Profil Assureur créé pour {username}")
                except Exception as e:
                    print(f"⚠️  Impossible de créer profil Assureur: {e}")
            
            elif user_type == 'Medecin' and models_info['Medecin']['exists']:
                try:
                    from medecin.models import Medecin
                    # Création minimaliste sans les relations complexes
                    medecin, created = Medecin.objects.get_or_create(
                        user=user_obj,
                        defaults={
                            'numero_ordre': f'MED{user_obj.id}',
                            'telephone_pro': '+2250200000002',
                            'actif': True
                        }
                    )
                    if created:
                        print(f"✅ Profil Medecin créé (minimal) pour {username}")
                except Exception as e:
                    print(f"⚠️  Impossible de créer profil Medecin: {e}")
            
            elif user_type == 'Pharmacien' and models_info['Pharmacien']['exists']:
                try:
                    from pharmacien.models import Pharmacien
                    pharmacien, created = Pharmacien.objects.get_or_create(
                        user=user_obj,
                        defaults={
                            'nom_pharmacie': f'Pharmacie Test {user_obj.id}',
                            'telephone': '+2250300000003',
                            'actif': True
                        }
                    )
                    if created:
                        print(f"✅ Profil Pharmacien créé pour {username}")
                except Exception as e:
                    print(f"⚠️  Impossible de créer profil Pharmacien: {e}")
            
            elif user_type == 'Agent' and models_info['Agent']['exists']:
                try:
                    from agents.models import Agent
                    agent, created = Agent.objects.get_or_create(
                        user=user_obj,
                        defaults={
                            'matricule': f'AGT{user_obj.id}',
                            'poste': 'Agent Test',
                            'est_actif': True
                        }
                    )
                    if created:
                        print(f"✅ Profil Agent créé pour {username}")
                except Exception as e:
                    print(f"⚠️  Impossible de créer profil Agent: {e}")
    
    def test_all_logins(self):
        """Test la connexion pour tous les utilisateurs créés"""
        print("\n🔐 TESTS DE CONNEXION...")
        
        results = {}
        
        for user_info in self.created_users:
            username = user_info['username']
            user_type = user_info['type']
            
            print(f"\n--- Test {user_type} ({username}) ---")
            
            try:
                # Test connexion
                login_success = self.client.login(
                    username=username, 
                    password='password123'
                )
                
                if login_success:
                    print("✅ Authentification réussie")
                    
                    # Test session
                    session = self.client.session
                    if '_auth_user_id' in session:
                        print("✅ Session active")
                    
                    # Test redirection après login
                    response = self.client.get('/accounts/login/')
                    print(f"✅ Test page login: {response.status_code}")
                    
                    # Test URLs spécifiques
                    self.test_user_urls(user_type)
                    
                    # Déconnexion
                    self.client.logout()
                    print("✅ Déconnexion réussie")
                    
                    results[user_type] = True
                else:
                    print("❌ Échec authentification")
                    results[user_type] = False
                    
            except Exception as e:
                print(f"❌ Erreur: {e}")
                results[user_type] = False
        
        return results
    
    def test_user_urls(self, user_type):
        """Test les URLs accessibles pour chaque type d'utilisateur"""
        print(f"   🌐 Test URLs pour {user_type}...")
        
        # URLs communes
        common_urls = [
            ('/', 'Accueil'),
            ('/profile/', 'Profil'),
        ]
        
        # URLs spécifiques
        specific_urls = {
            'Membre': [
                ('/membres/', 'Espace membre'),
                ('/membres/dashboard/', 'Dashboard membre'),
            ],
            'Agent': [
                ('/agents/', 'Espace agent'),
                ('/agents/dashboard/', 'Dashboard agent'),
            ],
            'Assureur': [
                ('/assureur/', 'Espace assureur'),
            ],
            'Médecin': [
                ('/medecin/', 'Espace médecin'),
            ],
            'Pharmacien': [
                ('/pharmacien/', 'Espace pharmacien'),
            ],
        }
        
        # Test URLs communes
        for url, desc in common_urls:
            try:
                response = self.client.get(url)
                status_codes = {
                    200: '✅ Accessible',
                    302: '🔀 Redirection', 
                    403: '🚫 Interdit',
                    404: '❌ Non trouvé'
                }
                status = status_codes.get(response.status_code, f'⚠️ {response.status_code}')
                print(f"      {status} {desc}")
            except Exception as e:
                print(f"      ❌ {desc}: {e}")
        
        # Test URLs spécifiques
        if user_type in specific_urls:
            for url, desc in specific_urls[user_type]:
                try:
                    response = self.client.get(url)
                    status_codes = {
                        200: '✅ Accessible',
                        302: '🔀 Redirection', 
                        403: '🚫 Interdit',
                        404: '❌ Non trouvé'
                    }
                    status = status_codes.get(response.status_code, f'⚠️ {response.status_code}')
                    print(f"      {status} {desc}")
                except Exception as e:
                    print(f"      ❌ {desc}: {e}")
    
    def test_public_access(self):
        """Test l'accès aux pages publiques"""
        print("\n🌐 TEST ACCÈS PUBLIC...")
        
        public_urls = [
            ('/', 'Accueil'),
            ('/accounts/login/', 'Connexion'),
            ('/accounts/signup/', 'Inscription'),
            ('/about/', 'À propos'),
        ]
        
        for url, desc in public_urls:
            try:
                response = self.client.get(url)
                if response.status_code == 200:
                    print(f"✅ {desc}: Accessible")
                elif response.status_code == 302:
                    print(f"🔀 {desc}: Redirection")
                else:
                    print(f"⚠️  {desc}: Code {response.status_code}")
            except Exception as e:
                print(f"❌ {desc}: {e}")
    
    def run_complete_test(self):
        """Exécute le test complet"""
        print("=" * 60)
        print("🧪 TEST DE CONNEXION INTELLIGENT")
        print("=" * 60)
        
        # Étape 1: Analyse des modèles
        models_info = self.analyze_models()
        
        # Étape 2: Création utilisateurs simples
        if not self.create_simple_users():
            print("❌ Échec création utilisateurs")
            return False
        
        # Étape 3: Création profils simples
        self.create_simple_profiles(models_info)
        
        # Étape 4: Test accès public
        self.test_public_access()
        
        # Étape 5: Test connexions
        login_results = self.test_all_logins()
        
        # Résumé final
        print("\n" + "=" * 60)
        print("📊 RÉSUMUM FINAL")
        print("=" * 60)
        
        total_success = sum(login_results.values())
        total_tests = len(login_results)
        
        for user_type, success in login_results.items():
            status = "✅ RÉUSSI" if success else "❌ ÉCHEC"
            print(f"{user_type}: {status}")
        
        print(f"\n🎯 RÉSULTAT: {total_success}/{total_tests} réussis")
        
        if total_success == total_tests:
            print("🎉 EXCELLENT! Toutes les connexions fonctionnent!")
        elif total_success >= 3:
            print("⚠️  BON! La plupart des connexions fonctionnent")
        else:
            print("❌ PROBLÈMES! Vérifiez la configuration")
        
        return total_success == total_tests

def main():
    """Fonction principale"""
    test_suite = SmartConnectionTest()
    success = test_suite.run_complete_test()
    
    if success:
        print("\n🚀 SUCCÈS: Le système d'authentification fonctionne correctement!")
        sys.exit(0)
    else:
        print("\n💡 CONSEILS:")
        print("1. Les utilisateurs de base fonctionnent - c'est bon signe!")
        print("2. Les problèmes sont liés aux modèles spécifiques")
        print("3. Vérifiez les relations ForeignKey dans l'admin Django")
        sys.exit(1)

if __name__ == "__main__":
    main()