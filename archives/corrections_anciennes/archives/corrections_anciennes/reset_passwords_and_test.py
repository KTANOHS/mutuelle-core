# reset_passwords_and_test.py
import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class PasswordResetTester:
    """Réinitialise les mots de passe et teste les connexions"""
    
    def __init__(self):
        self.default_password = "mutuelle2024"
        self.results = {}
    
    def reset_all_passwords(self):
        """Réinitialise tous les mots de passe"""
        print("🔄 RÉINITIALISATION DES MOTS DE PASSE")
        print("-" * 50)
        
        users = User.objects.all()
        results = []
        
        for user in users:
            try:
                # Sauvegarder l'ancien mot de passe (pour info)
                old_password = user.password
                
                # Définir le nouveau mot de passe
                user.password = make_password(self.default_password)
                user.save()
                
                results.append(f"✅ {user.username}: Mot de passe réinitialisé → '{self.default_password}'")
                
            except Exception as e:
                results.append(f"❌ {user.username}: Erreur réinitialisation - {e}")
        
        self.results['reset_passwords'] = results
        return results
    
    def verify_password_reset(self):
        """Vérifie que la réinitialisation a fonctionné"""
        print("\n🔍 VÉRIFICATION DES MOTS DE PASSE RÉINITIALISÉS")
        print("-" * 50)
        
        from django.contrib.auth import authenticate
        
        users = User.objects.all()
        results = []
        
        for user in users:
            # Tester l'authentification avec le nouveau mot de passe
            auth_user = authenticate(username=user.username, password=self.default_password)
            
            if auth_user and auth_user.is_authenticated:
                results.append(f"✅ {user.username}: Authentification réussie avec nouveau mot de passe")
            else:
                # Essayer avec l'ancienne méthode
                try:
                    if user.check_password(self.default_password):
                        results.append(f"✅ {user.username}: Vérification mot de passe réussie")
                    else:
                        results.append(f"❌ {user.username}: Échec vérification mot de passe")
                except Exception as e:
                    results.append(f"❌ {user.username}: Erreur vérification - {e}")
        
        self.results['verify_reset'] = results
        return results
    
    def test_connexions_apres_reset(self):
        """Teste les connexions après réinitialisation"""
        print("\n🚀 TEST DES CONNEXIONS APRÈS RÉINITIALISATION")
        print("-" * 50)
        
        from django.test import Client
        from django.contrib.auth import authenticate
        
        # Acteurs à tester
        actors = {
            'admin': User.objects.filter(is_superuser=True).first(),
            'agent': User.objects.filter(username__icontains='agent').first(),
            'medecin': User.objects.filter(username__icontains='medecin').first(),
            'membre': User.objects.exclude(
                username__icontains='agent'
            ).exclude(
                username__icontains='medecin'
            ).exclude(
                username__icontains='admin'
            ).exclude(
                username__icontains='technicien'
            ).exclude(
                username__icontains='superviseur'
            ).first()
        }
        
        results = []
        
        for role, user in actors.items():
            if not user:
                results.append(f"❌ {role}: Utilisateur non trouvé")
                continue
            
            # Test 1: Authentification Django
            auth_user = authenticate(username=user.username, password=self.default_password)
            if auth_user:
                results.append(f"✅ {role} ({user.username}): Authentification Django réussie")
            else:
                results.append(f"❌ {role} ({user.username}): Échec authentification Django")
                continue
            
            # Test 2: Connexion web
            client = Client()
            try:
                response = client.post('/accounts/login/', {
                    'username': user.username,
                    'password': self.default_password
                }, follow=True)
                
                if response.status_code == 200 and response.wsgi_request.user.is_authenticated:
                    results.append(f"✅ {role}: Connexion web réussie")
                    
                    # Test 3: Accès page d'accueil
                    response_home = client.get('/', follow=True)
                    if response_home.status_code == 200:
                        results.append(f"✅ {role}: Accès page d'accueil réussi")
                    else:
                        results.append(f"⚠️  {role}: Accès page d'accueil échoué (status: {response_home.status_code})")
                    
                    # Test 4: Déconnexion
                    response_logout = client.get('/accounts/logout/', follow=True)
                    if not response_logout.wsgi_request.user.is_authenticated:
                        results.append(f"✅ {role}: Déconnexion réussie")
                    else:
                        results.append(f"❌ {role}: Échec déconnexion")
                        
                else:
                    results.append(f"❌ {role}: Échec connexion web")
                    
            except Exception as e:
                results.append(f"❌ {role}: Erreur connexion web - {e}")
        
        self.results['test_connexions'] = results
        return results
    
    def create_test_pharmacien(self):
        """Crée un utilisateur pharmacien pour tests complets"""
        print("\n💊 CRÉATION D'UN UTILISATEUR PHARMACIEN")
        print("-" * 50)
        
        results = []
        
        try:
            # Vérifier si un pharmacien existe déjà
            existing_pharmacien = User.objects.filter(username__icontains='pharmacien').first()
            if existing_pharmacien:
                results.append(f"✅ Pharmacien existe déjà: {existing_pharmacien.username}")
                return results
            
            # Créer un nouvel utilisateur pharmacien
            pharmacien_user = User.objects.create_user(
                username='pharmacien_test',
                email='pharmacien@mutuelle.com',
                password=self.default_password,
                first_name='Pharmacien',
                last_name='Test',
                is_active=True
            )
            
            results.append(f"✅ Pharmacien créé: {pharmacien_user.username}")
            results.append(f"   📧 Email: {pharmacien_user.email}")
            results.append(f"   🔑 Mot de passe: '{self.default_password}'")
            
            # Créer l'instance Pharmacien si le modèle existe
            try:
                from pharmacien.models import Pharmacien
                pharmacien = Pharmacien.objects.create(
                    user=pharmacien_user,
                    nom_pharmacie='Pharmacie Centrale de Test',
                    nom='Pharmacien',
                    prenom='Test'
                )
                results.append(f"✅ Instance Pharmacien créée: {pharmacien}")
            except Exception as e:
                results.append(f"⚠️  Impossible de créer l'instance Pharmacien: {e}")
            
        except Exception as e:
            results.append(f"❌ Erreur création pharmacien: {e}")
        
        self.results['create_pharmacien'] = results
        return results
    
    def generate_password_report(self):
        """Génère un rapport des mots de passe"""
        print("\n📋 RAPPORT DES MOTS DE PASSE")
        print("-" * 50)
        
        users = User.objects.all()
        
        print(f"👥 Nombre total d'utilisateurs: {users.count()}")
        print("\n🔐 MOTS DE PASSE RÉINITIALISÉS:")
        print(f"   Le mot de passe par défaut est: '{self.default_password}'")
        print("\n📝 LISTE DES UTILISATEURS:")
        
        for user in users:
            status = "✅" if user.is_active else "❌"
            roles = []
            if user.is_superuser:
                roles.append("Superuser")
            if user.is_staff:
                roles.append("Staff")
            
            role_str = ", ".join(roles) if roles else "Utilisateur standard"
            
            print(f"   {status} {user.username:<20} | {user.email:<30} | {role_str}")
    
    def run_complete_test(self):
        """Exécute le test complet"""
        print("🚀 LANCEMENT DU TEST COMPLET DE RÉINITIALISATION")
        print("=" * 80)
        
        # 1. Réinitialiser les mots de passe
        self.reset_all_passwords()
        
        # 2. Vérifier la réinitialisation
        self.verify_password_reset()
        
        # 3. Créer un pharmacien manquant
        self.create_test_pharmacien()
        
        # 4. Tester les connexions
        self.test_connexions_apres_reset()
        
        # 5. Générer le rapport
        self.generate_final_report()
    
    def generate_final_report(self):
        """Génère le rapport final"""
        print("\n" + "=" * 80)
        print("📊 RAPPORT FINAL - RÉINITIALISATION MOTS DE PASSE")
        print("=" * 80)
        
        # Afficher tous les résultats
        for etape, resultats in self.results.items():
            titre = etape.replace('_', ' ').title()
            print(f"\n🎯 {titre}:")
            for resultat in resultats:
                print(f"   {resultat}")
        
        # Générer le rapport des mots de passe
        self.generate_password_report()
        
        print(f"\n💡 INSTRUCTIONS POUR LES TESTS:")
        print(f"   1. Utilisez le mot de passe: '{self.default_password}'")
        print(f"   2. Tous les utilisateurs ont le même mot de passe")
        print(f"   3. Exécutez à nouveau: python test_connexions_acteurs.py")
        print(f"   4. Les connexions devraient maintenant fonctionner")

def check_current_passwords():
    """Vérifie les mots de passe actuels"""
    print("🔍 VÉRIFICATION DES MOTS DE PASSE ACTUELS")
    print("-" * 50)
    
    from django.contrib.auth import authenticate
    
    User = get_user_model()
    users = User.objects.all()[:5]  # Vérifier les 5 premiers
    
    common_passwords = [
        'password123', 'password', '123456', 'admin', 'test',
        'mutuelle', 'mutuelle2024', 'secret', 'pass'
    ]
    
    print("🧪 Test des mots de passe courants...")
    
    for user in users:
        print(f"\n🔍 Testing: {user.username}")
        password_found = False
        
        for password in common_passwords:
            # Méthode 1: Authentification Django
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                print(f"   ✅ MOT DE PASSE TROUVÉ: '{password}' (via authenticate)")
                password_found = True
                break
            
            # Méthode 2: Vérification directe
            try:
                if user.check_password(password):
                    print(f"   ✅ MOT DE PASSE TROUVÉ: '{password}' (via check_password)")
                    password_found = True
                    break
            except:
                continue
        
        if not password_found:
            print(f"   ❌ Aucun mot de passe commun ne fonctionne")

if __name__ == "__main__":
    print("🚀 DIAGNOSTIC ET RÉINITIALISATION DES MOTS DE PASSE")
    print("=" * 80)
    
    # Vérifier d'abord les mots de passe actuels
    check_current_passwords()
    
    print("\n" + "=" * 80)
    print("🔄 LANCEMENT DE LA RÉINITIALISATION...")
    print("=" * 80)
    
    # Lancer la réinitialisation complète
    tester = PasswordResetTester()
    tester.run_complete_test()
    
    print("\n🎉 RÉINITIALISATION TERMINÉE!")
    print("=" * 80)