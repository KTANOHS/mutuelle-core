import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    from django.contrib.auth.models import User
    from membres.models import Medecin
    
    def verifier_medecin():
        print("🔍 VÉRIFICATION MÉDECIN:")
        print("=" * 40)
        
        # Vérifier si l'utilisateur médecin existe
        try:
            user = User.objects.get(username='medecin_test')
            print(f"✅ Utilisateur trouvé: {user.username}")
            
            # Vérifier si c'est un médecin
            try:
                medecin = Medecin.objects.get(user=user)
                print(f"✅ Médecin trouvé: {medecin.prenom} {medecin.nom}")
                print(f"   Specialité: {medecin.specialite}")
                print(f"   ID: {medecin.id}")
                
                # Vérifier les permissions
                print(f"   User is_active: {user.is_active}")
                print(f"   User is_staff: {user.is_staff}")
                print(f"   User is_superuser: {user.is_superuser}")
                
            except Medecin.DoesNotExist:
                print("❌ L'utilisateur n'est pas associé à un médecin")
                # Créer le médecin
                medecin = Medecin.objects.create(
                    user=user,
                    nom="Docteur",
                    prenom="Test", 
                    specialite="Generaliste"
                )
                print("✅ Médecin créé automatiquement")
                
        except User.DoesNotExist:
            print("❌ Utilisateur médecin_test non trouvé")
            # Créer l'utilisateur et le médecin
            user = User.objects.create_user(
                username='medecin_test',
                email='medecin@test.com',
                password='password123'
            )
            medecin = Medecin.objects.create(
                user=user,
                nom="Docteur",
                prenom="Test",
                specialite="Generaliste"
            )
            print("✅ Utilisateur et médecin créés automatiquement")
    
    verifier_medecin()
    
except Exception as e:
    print(f"❌ ERREUR: {e}")