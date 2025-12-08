# reset_complet.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def reset_complet():
    """
    Réinitialisation complète et création d'un médecin fonctionnel
    """
    print("🔄 RÉINITIALISATION COMPLÈTE")
    print("=" * 50)
    
    from django.contrib.auth import get_user_model
    from medecin.models import Medecin, SpecialiteMedicale, EtablissementMedical
    from django.utils import timezone
    
    User = get_user_model()
    
    # 1. Supprimer l'ancien utilisateur s'il existe
    try:
        user = User.objects.get(username='dr_kouame')
        print(f"✅ Utilisateur trouvé: {user.username}")
        
        # Essayer de supprimer le profil médecin d'abord
        try:
            medecin = Medecin.objects.get(user=user)
            medecin.delete()
            print("✅ Ancien profil médecin supprimé")
        except Medecin.DoesNotExist:
            print("✅ Aucun ancien profil médecin à supprimer")
        except Exception as e:
            print(f"⚠ Erreur suppression profil: {e}")
            # Forcer la suppression en utilisant SQL brut si nécessaire
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM medecin_medecin WHERE user_id = %s", [user.id])
            print("✅ Profil médecin forcément supprimé")
        
        user.delete()
        print("✅ Ancien utilisateur supprimé")
    except User.DoesNotExist:
        print("✅ Aucun ancien utilisateur à supprimer")
    
    # 2. Créer les modèles de base
    print("\n2. 🏗️ CRÉATION MODÈLES DE BASE")
    
    # Spécialité
    specialite, created = SpecialiteMedicale.objects.get_or_create(
        nom="Médecine Générale",
        defaults={'description': "Spécialité de médecine générale", 'actif': True}
    )
    print(f"✅ Spécialité: {specialite.nom}")
    
    # Établissement
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
    
    # 3. Créer l'utilisateur médecin
    print("\n3. 👤 CRÉATION UTILISATEUR MÉDECIN")
    
    user = User.objects.create_user(
        username='dr_kouame',
        password='medecin123',
        first_name='Jean',
        last_name='Kouamé',
        email='jean.kouame@chucocody.ci',
        is_active=True
    )
    print("✅ Utilisateur créé: dr_kouame / medecin123")
    
    # 4. Créer le profil médecin
    print("\n4. 🩺 CRÉATION PROFIL MÉDECIN")
    
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
    print(f"   👨‍⚕️ Dr {user.get_full_name()}")
    print(f"   🔢 {medecin.numero_ordre}")
    print(f"   🩺 {medecin.specialite.nom}")
    print(f"   🏥 {medecin.etablissement.nom}")
    
    return user

def test_final_apres_reset():
    """
    Test final après réinitialisation
    """
    print("\n" + "=" * 50)
    print("🧪 TEST FINAL APRÈS RÉINITIALISATION")
    print("=" * 50)
    
    from django.test import Client
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    client = Client()
    
    # Test connexion
    login_success = client.login(username='dr_kouame', password='medecin123')
    print(f"1. Authentification: {login_success}")
    
    if login_success:
        # Vérifier le profil
        user = User.objects.get(username='dr_kouame')
        if hasattr(user, 'medecin'):
            print(f"2. Profil médecin: ✅ PRÉSENT")
            medecin = user.medecin
            print(f"   👨‍⚕️ Dr {user.get_full_name()}")
        else:
            print("2. Profil médecin: ❌ ABSENT")
            return False
        
        # Test dashboard
        response = client.get('/medecin/dashboard/')
        print(f"3. Dashboard: Status {response.status_code}")
        
        if response.status_code == 200:
            print("🎉 SUCCÈS COMPLET! 🎉")
            print("\n📍 Application prête à l'utilisation:")
            print("   python manage.py runserver")
            print("   http://127.0.0.1:8000/medecin/login/")
            return True
        else:
            print(f"❌ Problème dashboard: {response.status_code}")
    else:
        print("❌ Échec authentification")
    
    return False

if __name__ == "__main__":
    user = reset_complet()
    success = test_final_apres_reset()
    
    if success:
        print("\n✨ Tous les problèmes sont résolus!")
        print("🚀 L'application medecin est maintenant opérationnelle!")
    else:
        print("\n❌ Problème persistant - besoin d'analyse approfondie")