import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    from django.contrib.auth.models import User
    from medecin.models import Medecin, SpecialiteMedicale
    
    def creer_medecin_corrige():
        print("🛠️ CRÉATION MÉDECIN CORRIGÉE")
        print("=" * 40)
        
        # 1. Vérifier/Créer une spécialité médicale
        print("1. 🔍 Vérification spécialité médicale...")
        try:
            specialite = SpecialiteMedicale.objects.get(nom="Généraliste")
            print(f"   ✅ Spécialité trouvée: {specialite}")
        except SpecialiteMedicale.DoesNotExist:
            # Créer la spécialité
            specialite = SpecialiteMedicale.objects.create(
                nom="Généraliste",
                description="Médecine générale"
            )
            print("   ✅ Spécialité 'Généraliste' créée")
        
        # 2. Vérifier/Créer l'utilisateur
        print("2. 👤 Vérification utilisateur...")
        try:
            user = User.objects.get(username='medecin_test')
            print("   ✅ Utilisateur medecin_test trouvé")
        except User.DoesNotExist:
            user = User.objects.create_user(
                username='medecin_test',
                email='medecin@test.com',
                password='password123',
                first_name='Docteur',
                last_name='Test'
            )
            print("   ✅ Utilisateur medecin_test créé")
        
        # 3. Vérifier/Créer le médecin
        print("3. 🩺 Vérification médecin...")
        try:
            medecin = Medecin.objects.get(user=user)
            print(f"   ✅ Médecin trouvé: {medecin}")
        except Medecin.DoesNotExist:
            medecin = Medecin.objects.create(
                user=user,
                nom="Test",
                prenom="Docteur",
                specialite=specialite,  # Utiliser l'instance, pas une string
                numero_ordre="123456",
                telephone="0123456789",
                email="medecin@test.com"
            )
            print("   ✅ Profil médecin créé avec succès")
            print(f"   📋 Détails: Dr {medecin.prenom} {medecin.nom} - {medecin.specialite.nom}")
        
        # 4. Vérifier les permissions
        print("4. 🔐 Vérification permissions...")
        print(f"   User is_active: {user.is_active}")
        print(f"   User is_staff: {user.is_staff}")
        print(f"   Médecin actif: {medecin.est_actif}")
        
        return user, medecin
    
    user, medecin = creer_medecin_corrige()
    
    print("\n🎯 MÉDECIN PRÊT POUR LES TESTS!")
    print(f"   Identifiant: {user.username}")
    print(f"   Mot de passe: password123")
    print(f"   Médecin: {medecin}")
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()