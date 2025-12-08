# correction_profil_medecin_v2.py
import os
import sys
import django
from django.contrib.auth import get_user_model

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

User = get_user_model()

class CorrecteurProfilMedecinV2:
    """Corrige les problèmes de profil médecin avec gestion des spécialités"""
    
    def __init__(self):
        self.user_model = User
    
    def obtenir_ou_creer_specialite(self, nom_specialite="Médecine Générale"):
        """Obtient ou crée une spécialité médicale"""
        try:
            from medecin.models import SpecialiteMedicale
            
            # Essayer de trouver la spécialité existante
            specialite, creee = SpecialiteMedicale.objects.get_or_create(
                nom=nom_specialite,
                defaults={'description': f"Spécialité {nom_specialite}"}
            )
            
            if creee:
                print(f"✅ Spécialité créée: {specialite.nom}")
            else:
                print(f"✅ Spécialité trouvée: {specialite.nom}")
                
            return specialite
            
        except Exception as e:
            print(f"❌ Erreur spécialité: {e}")
            return None
    
    def trouver_utilisateur_medecin(self, username):
        """Trouve un utilisateur médecin par son username"""
        try:
            return self.user_model.objects.get(username=username)
        except self.user_model.DoesNotExist:
            print(f"❌ Utilisateur '{username}' non trouvé")
            return None
    
    def verifier_profil_medecin(self, user):
        """Vérifie si l'utilisateur a un profil médecin"""
        try:
            # Essayer d'accéder au profil médecin via différentes relations possibles
            if hasattr(user, 'medecin'):
                return user.medecin, 'medecin'
            elif hasattr(user, 'profile_medecin'):
                return user.profile_medecin, 'profile_medecin'
            elif hasattr(user, 'medecinprofile'):
                return user.medecinprofile, 'medecinprofile'
            else:
                return None, 'non_trouve'
        except Exception as e:
            print(f"❌ Erreur vérification profil: {e}")
            return None, 'erreur'
    
    def creer_profil_medecin(self, user):
        """Crée un profil médecin pour l'utilisateur avec spécialité"""
        try:
            from medecin.models import Medecin
            
            print("✅ Modèle Medecin trouvé dans l'app 'medecin'")
            
            # Obtenir la spécialité
            specialite = self.obtenir_ou_creer_specialite()
            if not specialite:
                print("❌ Impossible d'obtenir la spécialité")
                return None
            
            # Créer le profil médecin
            profil_medecin = Medecin.objects.create(
                user=user,
                nom_complet=user.get_full_name() or user.username,
                specialite=specialite,  # Maintenant c'est une instance, pas une string
                numero_ordre="TEST12345",
                est_actif=True
            )
            return profil_medecin
            
        except Exception as e:
            print(f"❌ Erreur création profil: {e}")
            import traceback
            traceback.print_exc()
        
        return None
    
    def tester_connexion_medecin(self, username, password):
        """Teste la connexion après correction"""
        from django.test import Client
        
        client = Client()
        print(f"\n🔐 Test de connexion pour {username}...")
        
        # Tentative de connexion
        login_success = client.login(username=username, password=password)
        
        if login_success:
            print("✅ Connexion réussie")
            
            # Test d'accès au dashboard médecin
            response = client.get('/medecin/dashboard/', follow=True)
            print(f"📊 Accès dashboard: Status {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Dashboard médecin accessible avec succès!")
                return True
            else:
                print(f"❌ Échec accès dashboard: {response.status_code}")
                # Afficher la redirection
                if hasattr(response, 'redirect_chain') and response.redirect_chain:
                    print(f"   Redirection vers: {response.redirect_chain[-1][0]}")
                return False
        else:
            print("❌ Échec de la connexion")
            return False
    
    def corriger_utilisateur(self, username, password="testpass123"):
        """Corrige un utilisateur médecin spécifique"""
        print(f"\n🔧 Correction de l'utilisateur: {username}")
        print("="*50)
        
        # 1. Trouver l'utilisateur
        user = self.trouver_utilisateur_medecin(username)
        if not user:
            return False
        
        print(f"✅ Utilisateur trouvé: {user.get_full_name()}")
        print(f"   - Email: {user.email}")
        print(f"   - Actif: {user.is_active}")
        print(f"   - Staff: {user.is_staff}")
        print(f"   - Superuser: {user.is_superuser}")
        
        # 2. Vérifier le profil médecin
        profil, relation_type = self.verifier_profil_medecin(user)
        
        if profil:
            print(f"✅ Profil médecin trouvé (relation: {relation_type})")
            print(f"   - ID Profil: {profil.id}")
            print(f"   - Nom complet: {getattr(profil, 'nom_complet', 'N/A')}")
            print(f"   - Spécialité: {getattr(profil, 'specialite', 'N/A')}")
            return True
        else:
            print(f"❌ Profil médecin manquant (relation: {relation_type})")
            
            # 3. Créer le profil médecin
            print("\n🛠️  Création du profil médecin...")
            nouveau_profil = self.creer_profil_medecin(user)
            
            if nouveau_profil:
                print("✅ Profil médecin créé avec succès!")
                print(f"   - ID: {nouveau_profil.id}")
                print(f"   - Spécialité: {nouveau_profil.specialite}")
                
                # 4. Tester la connexion
                print("\n🧪 Test de la connexion après correction...")
                return self.tester_connexion_medecin(username, password)
            else:
                print("❌ Échec création profil médecin")
                return False
    
    def corriger_tous_medecins(self):
        """Corrige tous les médecins sans profil"""
        print("\n🔄 Correction de tous les médecins sans profil...")
        
        medecins_a_corriger = [
            'test_medecin',
            'test_medecin2', 
            'test_medecin_final',
            'test_medecin_ultime'
        ]
        
        succes = 0
        echecs = 0
        
        for username in medecins_a_corriger:
            try:
                if self.corriger_utilisateur(username):
                    succes += 1
                else:
                    echecs += 1
            except Exception as e:
                print(f"❌ Erreur avec {username}: {e}")
                echecs += 1
        
        print(f"\n📊 Résultat global: {succes} succès, {echecs} échecs")
        return succes > 0

# Script principal
if __name__ == "__main__":
    correcteur = CorrecteurProfilMedecinV2()
    
    print("🚀 CORRECTEUR PROFIL MÉDECIN V2")
    print("=" * 60)
    
    # Option 1: Corriger un utilisateur spécifique
    success = correcteur.corriger_utilisateur("test_medecin")
    
    # Option 2: Décommentez la ligne suivante pour corriger tous les médecins
    # success = correcteur.corriger_tous_medecins()
    
    if success:
        print("\n🎉 CORRECTION TERMINÉE AVEC SUCCÈS!")
        print("\n🔍 Vérification finale avec diagnostic...")
        
        # Relancer un diagnostic rapide
        from django.test import Client
        client = Client()
        client.login(username='test_medecin', password='testpass123')
        response = client.get('/medecin/dashboard/', follow=True)
        
        print(f"🎯 Statut final dashboard: {response.status_code}")
        if response.status_code == 200:
            print("✅ ✅ ✅ TOUT FONCTIONNE PARFAITEMENT!")
        else:
            print("❌ Il reste un problème de redirection")
            
    else:
        print("\n💥 LA CORRECTION A ÉCHOUÉ!")
        print("\n🛠️  Solution manuelle alternative:")
        print("""
# Dans le shell Django:
from django.contrib.auth import get_user_model
from medecin.models import Medecin, SpecialiteMedicale

User = get_user_model()
user = User.objects.get(username='test_medecin')

# Obtenir ou créer la spécialité
specialite, created = SpecialiteMedicale.objects.get_or_create(
    nom="Médecine Générale",
    defaults={'description': 'Spécialité médecine générale'}
)

# Créer le profil médecin
Medecin.objects.create(
    user=user,
    nom_complet='Medecin Test',
    specialite=specialite,
    numero_ordre='TEST12345',
    est_actif=True
)
        """)