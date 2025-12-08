# creer_donnees_necessaires.py
import os
import django
import sys
from datetime import date

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

django.setup()

from django.contrib.auth.models import User
from membres.models import Membre
from medecin.models import MaladieChronique

def creer_donnees_necessaires():
    print("🛠️ CRÉATION DES DONNÉES MANQUANTES")
    print("=" * 50)
    
    # 1. Créer des patients de test
    print("1. 👥 CRÉATION DES PATIENTS...")
    patients_data = [
        {'username': 'patient_dupont', 'first_name': 'Marie', 'last_name': 'Dupont', 'email': 'marie.dupont@test.com', 'numero': 'MEM001'},
        {'username': 'patient_martin', 'first_name': 'Pierre', 'last_name': 'Martin', 'email': 'pierre.martin@test.com', 'numero': 'MEM002'},
        {'username': 'patient_leroy', 'first_name': 'Sophie', 'last_name': 'Leroy', 'email': 'sophie.leroy@test.com', 'numero': 'MEM003'},
        {'username': 'patient_bernard', 'first_name': 'Jean', 'last_name': 'Bernard', 'email': 'jean.bernard@test.com', 'numero': 'MEM004'},
        {'username': 'patient_dubois', 'first_name': 'Alice', 'last_name': 'Dubois', 'email': 'alice.dubois@test.com', 'numero': 'MEM005'},
    ]
    
    patients_crees = 0
    for patient_data in patients_data:
        try:
            user, created = User.objects.get_or_create(
                username=patient_data['username'],
                defaults={
                    'first_name': patient_data['first_name'],
                    'last_name': patient_data['last_name'],
                    'email': patient_data['email'],
                    'is_active': True
                }
            )
            
            if created:
                user.set_password('password123')
                user.save()
                print(f"   ✅ Utilisateur créé: {user.get_full_name()}")
            
            membre, created = Membre.objects.get_or_create(
                user=user,
                defaults={
                    'numero_membre': patient_data['numero'],
                    'date_naissance': date(1980, 1, 1),
                    'telephone': '0123456789',
                    'adresse': '123 Rue Test, 75000 Paris'
                }
            )
            
            if created:
                patients_crees += 1
                print(f"   ✅ Patient créé: {membre.get_full_name()} - {membre.numero_membre}")
            else:
                print(f"   ℹ️  Patient existe déjà: {membre.get_full_name()}")
                
        except Exception as e:
            print(f"   ❌ Erreur création patient {patient_data['username']}: {e}")
    
    # 2. Créer des maladies chroniques de test
    print("\n2. 🩺 CRÉATION DES MALADIES CHRONIQUES...")
    maladies_data = [
        {'nom': 'Diabète de type 2', 'categorie': 'Métabolique', 'description': 'Trouble métabolique caractérisé par une hyperglycémie chronique'},
        {'nom': 'Hypertension artérielle', 'categorie': 'Cardiovasculaire', 'description': 'Élévation permanente de la pression artérielle'},
        {'nom': 'Asthme', 'categorie': 'Respiratoire', 'description': 'Maladie inflammatoire des bronches'},
        {'nom': 'Arthrite rhumatoïde', 'categorie': 'Rhumatologique', 'description': 'Maladie auto-immune inflammatoire chronique'},
        {'nom': 'Dépression', 'categorie': 'Psychiatrique', 'description': 'Trouble de l humeur caractérisé par une tristesse persistante'},
        {'nom': 'Bronchite chronique', 'categorie': 'Respiratoire', 'description': 'Inflammation chronique des bronches'},
        {'nom': 'Insuffisance cardiaque', 'categorie': 'Cardiovasculaire', 'description': 'Incapacité du cœur à assurer un débit sanguin normal'},
        {'nom': 'Cancer du sein', 'categorie': 'Oncologique', 'description': 'Tumeur maligne du tissu mammaire'},
        {'nom': 'Maladie de Parkinson', 'categorie': 'Neurologique', 'description': 'Maladie neurodégénérative affectant le système nerveux'},
        {'nom': 'Sclérose en plaques', 'categorie': 'Neurologique', 'description': 'Maladie auto-immune du système nerveux central'},
    ]
    
    maladies_crees = 0
    for maladie_data in maladies_data:
        try:
            maladie, created = MaladieChronique.objects.get_or_create(
                nom=maladie_data['nom'],
                defaults={
                    'categorie': maladie_data['categorie'],
                    'description': maladie_data['description']
                }
            )
            
            if created:
                maladies_crees += 1
                print(f"   ✅ Maladie créée: {maladie.nom} ({maladie.categorie})")
            else:
                print(f"   ℹ️  Maladie existe déjà: {maladie.nom}")
                
        except Exception as e:
            print(f"   ❌ Erreur création maladie {maladie_data['nom']}: {e}")
    
    # 3. Résumé final
    print(f"\n3. 📊 RÉSUMÉ FINAL:")
    print(f"   👥 Patients créés: {patients_crees}")
    print(f"   🩺 Maladies créées: {maladies_crees}")
    print(f"   📋 Total patients dans la base: {Membre.objects.count()}")
    print(f"   📋 Total maladies dans la base: {MaladieChronique.objects.count()}")
    
    if patients_crees > 0 and maladies_crees > 0:
        print("\n🎯 LES DONNÉES SONT MAINTENANT DISPONIBLES!")
        print("💡 Les filtres devraient maintenant fonctionner correctement")
        print("🌐 Testez dans le navigateur: http://127.0.0.1:8000/medecin/suivi-chronique/accompagnements/creer/")
    else:
        print("\n⚠️  Problème lors de la création des données")
        print("📋 Vérifiez les erreurs ci-dessus")

creer_donnees_necessaires()
