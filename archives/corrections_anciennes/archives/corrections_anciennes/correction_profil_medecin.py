# correction_profil_medecin.py
import os
import sys
import django
from django.contrib.auth import get_user_model

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

User = get_user_model()

class CorrecteurProfilMedecin:
    """Corrige les problèmes de profil médecin manquant"""
    
    def __init__(self):
        self.user_model = User
    
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
        """Crée un profil médecin pour l'utilisateur"""
        try:
            # Essayer d'importer le modèle Medecin
            from medecin.models import Medecin
            print("✅ Modèle Medecin trouvé dans l'app 'medecin'")
            
            # Créer le profil médecin
            profil_medecin = Medecin.objects.create(
                user=user,
                nom_complet=user.get_full_name() or user.username,
                specialite="Médecine Générale",
                numero_ordre="TEST12345",
                est_actif=True
            )
            return profil_medecin
            
        except ImportError:
            print("❌ Modèle Medecin non trouvé dans 'medecin.models'")
        except Exception as e:
            print(f"❌ Erreur création profil: {e}")
        
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
    
    def lister_utilisateurs_medecins(self):
        """Liste tous les utilisateurs potentiellement médecins"""
        print("\n📋 Liste des utilisateurs (potentiels médecins):")
        print("-" * 40)
        
        # Chercher des utilisateurs avec "medecin" dans le username
        medecins_potentiels = self.user_model.objects.filter(
            username__icontains='medecin'
        ) | self.user_model.objects.filter(
            email__icontains='medecin'
        ) | self.user_model.objects.filter(
            first_name__icontains='medecin'
        ) | self.user_model.objects.filter(
            last_name__icontains='medecin'
        )
        
        for user in medecins_potentiels:
            profil, relation_type = self.verifier_profil_medecin(user)
            statut = "✅ AVEC PROFIL" if profil else "❌ SANS PROFIL"
            print(f"👤 {user.username:20} | {user.get_full_name():25} | {statut:15} | Relation: {relation_type}")
        
        return medecins_potentiels.count()
    
    def verifier_structure_modeles(self):
        """Vérifie la structure des modèles"""
        print("\n🏗️  Vérification structure des modèles:")
        print("-" * 40)
        
        try:
            # Vérifier l'app medecin
            from django.apps import apps
            modeles_medecin = [m for m in apps.get_app_config('medecin').get_models()]
            print(f"✅ App 'medecin' trouvée avec {len(modeles_medecin)} modèles")
            
            for modele in modeles_medecin:
                print(f"   - {modele.__name__}")
                # Vérifier les champs
                for champ in modele._meta.get_fields():
                    if hasattr(champ, 'related_model') and champ.related_model == User:
                        print(f"     → Relation avec User: {champ.name}")
                        
        except LookupError:
            print("❌ App 'medecin' non trouvée")
        
        # Vérifier d'autres apps potentielles
        apps_potentielles = ['membres', 'core', 'agents']
        for app in apps_potentielles:
            try:
                modeles = [m for m in apps.get_app_config(app).get_models()]
                print(f"ℹ️  App '{app}' a {len(modeles)} modèles")
            except LookupError:
                pass

# Script principal
if __name__ == "__main__":
    correcteur = CorrecteurProfilMedecin()
    
    print("🚀 CORRECTEUR PROFIL MÉDECIN")
    print("=" * 60)
    
    # 1. Vérifier la structure
    correcteur.verifier_structure_modeles()
    
    # 2. Lister les médecins
    count = correcteur.lister_utilisateurs_medecins()
    print(f"\n📊 Total médecins potentiels: {count}")
    
    # 3. Corriger l'utilisateur test_medecin
    if count > 0:
        print(f"\n🎯 Correction ciblée sur 'test_medecin'...")
        success = correcteur.corriger_utilisateur("test_medecin")
        
        if success:
            print("\n🎉 CORRECTION TERMINÉE AVEC SUCCÈS!")
        else:
            print("\n💥 LA CORRECTION A ÉCHOUÉ!")
            
            # Suggestions de dépannage
            print("\n💡 SUGGESTIONS:")
            print("1. Vérifiez que le modèle Medecin existe dans medecin/models.py")
            print("2. Vérifiez la relation OneToOne avec User")
            print("3. Créez manuellement le profil via: python manage.py shell")
            print("""
from django.contrib.auth import get_user_model
from medecin.models import Medecin

User = get_user_model()
user = User.objects.get(username='test_medecin')
Medecin.objects.create(user=user, nom_complet='Medecin Test', specialite='Médecine Générale')
            """)
    else:
        print("\n❌ Aucun médecin trouvé à corriger")