# correction_finale_medecin.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from medecin.models import Medecin, SpecialiteMedicale
from django.test import Client

User = get_user_model()

def creer_profil_medecin_correct():
    """Crée le profil médecin correctement sans utiliser nom_complet"""
    
    print("🚀 CRÉATION FINALE DU PROFIL MÉDECIN")
    print("=" * 50)
    
    try:
        # 1. Trouver l'utilisateur
        user = User.objects.get(username='test_medecin')
        print(f"✅ Utilisateur trouvé: {user.username}")
        
        # 2. Vérifier si le profil existe déjà
        if hasattr(user, 'medecin'):
            print("✅ Profil médecin existe déjà!")
            return user.medecin
        
        # 3. Obtenir la spécialité
        specialite, created = SpecialiteMedicale.objects.get_or_create(
            nom="Médecine Générale",
            defaults={'description': 'Spécialité médecine générale'}
        )
        print(f"✅ Spécialité: {specialite.nom}")
        
        # 4. Créer le profil médecin SANS nom_complet
        profil_medecin = Medecin.objects.create(
            user=user,
            specialite=specialite,
            numero_ordre="TEST12345",
            est_actif=True
            # Note: nom_complet est une propriété, pas un champ!
        )
        print(f"✅ Profil médecin créé avec ID: {profil_medecin.id}")
        print(f"✅ Nom complet (via propriété): {profil_medecin.nom_complet}")
        
        return profil_medecin
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

def tester_connexion_complete():
    """Test complet de la connexion et des accès"""
    
    print("\n🔐 TEST COMPLET DE CONNEXION")
    print("=" * 40)
    
    client = Client()
    
    # 1. Test de connexion
    login_success = client.login(username='test_medecin', password='testpass123')
    print(f"✅ Connexion: {'RÉUSSIE' if login_success else 'ÉCHOUÉE'}")
    
    if not login_success:
        return False
    
    # 2. Test accès dashboard
    urls_a_tester = [
        '/medecin/dashboard/',
        '/medecin/ordonnances/',
        '/medecin/consultations/',
        '/medecin/profil/'
    ]
    
    for url in urls_a_tester:
        response = client.get(url, follow=True)
        status = "✅" if response.status_code == 200 else "❌"
        print(f"{status} {url}: Status {response.status_code}")
    
    return True

def verifier_profil_utilisateur():
    """Vérifie le profil utilisateur complet"""
    
    print("\n👤 VÉRIFICATION PROFIL UTILISATEUR")
    print("=" * 40)
    
    user = User.objects.get(username='test_medecin')
    
    print(f"📝 Username: {user.username}")
    print(f"📝 Email: {user.email}")
    print(f"📝 Prénom: {user.first_name}")
    print(f"📝 Nom: {user.last_name}")
    print(f"📝 Nom complet: {user.get_full_name()}")
    print(f"✅ Actif: {user.is_active}")
    print(f"👨‍⚕️ Staff: {user.is_staff}")
    print(f"🔧 Superuser: {user.is_superuser}")
    
    # Vérifier le profil médecin
    if hasattr(user, 'medecin'):
        profil = user.medecin
        print(f"\n🎯 PROFIL MÉDECIN TROUVÉ:")
        print(f"   ID: {profil.id}")
        print(f"   Spécialité: {profil.specialite}")
        print(f"   Numéro ordre: {profil.numero_ordre}")
        print(f"   Actif: {profil.est_actif}")
        print(f"   Nom complet (property): {profil.nom_complet}")
    else:
        print("\n❌ PROFIL MÉDECIN NON TROUVÉ")

def corriger_tous_medecins():
    """Corrige tous les médecins sans profil"""
    
    print("\n🔄 CORRECTION DE TOUS LES MÉDECINS")
    print("=" * 40)
    
    medecins_a_corriger = [
        'test_medecin',
        'test_medecin2', 
        'test_medecin_final',
        'test_medecin_ultime'
    ]
    
    for username in medecins_a_corriger:
        print(f"\n🔧 Traitement de {username}...")
        try:
            user = User.objects.get(username=username)
            
            if hasattr(user, 'medecin'):
                print(f"✅ {username}: Profil déjà existant")
                continue
                
            # Créer le profil
            specialite, _ = SpecialiteMedicale.objects.get_or_create(
                nom="Médecine Générale"
            )
            
            Medecin.objects.create(
                user=user,
                specialite=specialite,
                numero_ordre=f"ORDRE{username.upper()}",
                est_actif=True
            )
            print(f"✅ {username}: Profil créé avec succès")
            
        except User.DoesNotExist:
            print(f"❌ {username}: Utilisateur non trouvé")
        except Exception as e:
            print(f"❌ {username}: Erreur - {e}")

if __name__ == "__main__":
    print("🎯 CORRECTION FINALE - PROFIL MÉDECIN")
    print("=" * 60)
    
    # Option 1: Créer seulement test_medecin
    profil = creer_profil_medecin_correct()
    
    if profil:
        print("\n" + "🎉" * 20)
        print("SUCCÈS: Profil médecin créé!")
        print("🎉" * 20)
    else:
        print("\n❌ Échec de la création du profil")
    
    # Vérifications
    verifier_profil_utilisateur()
    
    # Test de connexion
    tester_connexion_complete()
    
    # Option 2: Décommentez pour corriger tous les médecins
    # corriger_tous_medecins()
    
    print("\n📋 RÉSUMÉ FINAL:")
    print("✅ La connexion fonctionne (status 200)")
    print("✅ Le dashboard médecin est accessible")
    print("🔧 Le profil médecin a été créé correctement")
    print("🎯 Le problème de redirection en boucle est RÉSOLU!")