# verification_finale_medecin.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_et_corriger_medecin():
    """
    Vérifie et corrige les derniers problèmes du médecin
    """
    print("🔍 VÉRIFICATION ET CORRECTION FINALE MÉDECIN")
    print("=" * 60)
    
    from django.contrib.auth import get_user_model
    from medecin.models import Medecin, SpecialiteMedicale, EtablissementMedical
    
    User = get_user_model()
    
    # 1. Vérifier l'utilisateur dr_kouame
    print("\n1. 👤 VÉRIFICATION UTILISATEUR DR_KOUAME")
    print("-" * 40)
    
    try:
        user = User.objects.get(username='dr_kouame')
        print(f"✅ Utilisateur trouvé: {user.username}")
        print(f"   Nom: {user.get_full_name()}")
        print(f"   Email: {user.email}")
        print(f"   Actif: {user.is_active}")
        
        # Vérifier le profil médecin
        if hasattr(user, 'medecin'):
            medecin = user.medecin
            print(f"✅ Profil médecin trouvé!")
            print(f"   Numéro ordre: {medecin.numero_ordre}")
            print(f"   Spécialité: {medecin.specialite.nom}")
            print(f"   Établissement: {medecin.etablissement.nom}")
        else:
            print("❌ AUCUN PROFIL MÉDECIN ASSOCIÉ!")
            print("📝 Création du profil médecin...")
            creer_profil_medecin(user)
            
    except User.DoesNotExist:
        print("❌ Utilisateur dr_kouame non trouvé")
        creer_utilisateur_et_medecin()
    except Exception as e:
        print(f"❌ Erreur: {e}")

def creer_profil_medecin(user):
    """
    Crée un profil médecin pour l'utilisateur
    """
    print("\n2. 🩺 CRÉATION PROFIL MÉDECIN")
    print("-" * 40)
    
    try:
        from medecin.models import Medecin, SpecialiteMedicale, EtablissementMedical
        from django.utils import timezone
        
        # Vérifier/créer la spécialité
        specialite, created = SpecialiteMedicale.objects.get_or_create(
            nom="Médecine Générale",
            defaults={'description': "Spécialité de médecine générale", 'actif': True}
        )
        print(f"✅ Spécialité: {specialite.nom}")
        
        # Vérifier/créer l'établissement
        etablissement, created = EtablissementMedical.objects.get_or_create(
            nom="CHU de Cocody",
            defaults={
                'type_etablissement': 'hopital',
                'adresse': "BP V 34, Abidjan",
                'telephone': "+22521252425",
                'email': "contact@chucocody.ci",
                'ville': "Abidjan", 
                'pays': "Côte d'Ivoire",
                'actif': True
            }
        )
        print(f"✅ Établissement: {etablissement.nom}")
        
        # Créer le profil médecin
        medecin = Medecin.objects.create(
            user=user,
            numero_ordre='MED2024001',
            specialite=specialite,
            etablissement=etablissement,
            telephone_pro='+2250701234567',
            email_pro='jean.kouame@chucocody.ci',
            annees_experience=12,
            tarif_consultation=15000.00,
            actif=True,
            disponible=True,
            date_inscription=timezone.now(),
            date_derniere_modif=timezone.now(),
            horaires_travail={
                'lundi': {'debut': '08:00', 'fin': '17:00'},
                'mardi': {'debut': '08:00', 'fin': '17:00'},
                'mercredi': {'debut': '08:00', 'fin': '17:00'},
                'jeudi': {'debut': '08:00', 'fin': '17:00'},
                'vendredi': {'debut': '08:00', 'fin': '16:00'}
            },
            diplome_verifie=True
        )
        
        print("✅ Profil médecin créé avec succès!")
        print(f"   Dr {user.get_full_name()}")
        print(f"   Numéro ordre: {medecin.numero_ordre}")
        
    except Exception as e:
        print(f"❌ Erreur création profil: {e}")
        import traceback
        traceback.print_exc()

def creer_utilisateur_et_medecin():
    """
    Crée l'utilisateur et le profil médecin
    """
    print("\n🆕 CRÉATION UTILISATEUR ET PROFIL MÉDECIN")
    print("-" * 40)
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Créer l'utilisateur
    user = User.objects.create_user(
        username='dr_kouame',
        password='medecin123',
        first_name='Jean',
        last_name='Kouamé',
        email='jean.kouame@chucocody.ci',
        is_active=True
    )
    print("✅ Utilisateur créé: dr_kouame / medecin123")
    
    # Créer le profil médecin
    creer_profil_medecin(user)

def tester_connexion_finale():
    """
    Test final de connexion
    """
    print("\n" + "=" * 60)
    print("🧪 TEST CONNEXION FINALE")
    print("=" * 60)
    
    from django.test import Client
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    client = Client()
    
    # 1. Connexion
    login_success = client.login(username='dr_kouame', password='medecin123')
    print(f"1. Authentification: {login_success}")
    
    if not login_success:
        print("❌ Échec authentification")
        return False
    
    # 2. Vérification profil
    user = User.objects.get(username='dr_kouame')
    if hasattr(user, 'medecin'):
        print(f"2. Profil médecin: ✅ PRÉSENT")
        medecin = user.medecin
        print(f"   👨‍⚕️ Dr {user.get_full_name()}")
        print(f"   🔢 {medecin.numero_ordre}")
        print(f"   🩺 {medecin.specialite.nom}")
    else:
        print("2. Profil médecin: ❌ ABSENT")
        return False
    
    # 3. Test dashboard
    response = client.get('/medecin/dashboard/')
    print(f"3. Accès dashboard: Status {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ DASHBOARD ACCESSIBLE!")
        return True
    else:
        print(f"   ❌ Problème: {response.status_code}")
        return False

def verifier_base_donnees():
    """
    Vérification complète de la base de données
    """
    print("\n" + "=" * 60)
    print("📊 ÉTAT BASE DE DONNÉES")
    print("=" * 60)
    
    from django.contrib.auth import get_user_model
    from medecin.models import Medecin
    
    User = get_user_model()
    
    print(f"👥 Utilisateurs totaux: {User.objects.count()}")
    print(f"👨‍⚕️ Médecins totaux: {Medecin.objects.count()}")
    
    print("\n📋 Liste des médecins:")
    for medecin in Medecin.objects.all():
        print(f"   • {medecin.user.username} - {medecin.numero_ordre}")

if __name__ == "__main__":
    verifier_et_corriger_medecin()
    success = tester_connexion_finale()
    verifier_base_donnees()
    
    if success:
        print("\n🎉 🎉 🎉 APPLICATION MEDECIN OPÉRATIONNELLE! 🎉 🎉 🎉")
        print("\n📍 Pour tester:")
        print("   python manage.py runserver")
        print("   http://127.0.0.1:8000/medecin/login/")
        print("   dr_kouame / medecin123")
    else:
        print("\n❌ Problème persistant - besoin d'analyse supplémentaire")