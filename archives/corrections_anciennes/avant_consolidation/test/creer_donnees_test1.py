import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from membres.models import Membre
from medecin.models import Medecin, Consultation, SpecialiteMedicale, EtablissementMedical
from agents.models import BonSoin
from django.utils import timezone

def creer_donnees_test():
    print("🔧 Création des données de test...")
    
    # 1. Créer ou récupérer le groupe médecin
    groupe_medecin, created = Group.objects.get_or_create(name='medecin')
    
    # 2. Créer un utilisateur médecin de test (s'il n'existe pas)
    try:
        user_medecin = User.objects.get(username='test_medecin')
        print("✅ Médecin test existant trouvé")
    except User.DoesNotExist:
        user_medecin = User.objects.create_user(
            username='test_medecin',
            password='test123',
            first_name='Jean',
            last_name='Dupont',
            email='jean.dupont@clinique.com'
        )
        user_medecin.groups.add(groupe_medecin)
        user_medecin.save()
        print("✅ Médecin test créé")
    
    # 3. Créer le profil médecin
    try:
        medecin = Medecin.objects.get(user=user_medecin)
        print("✅ Profil médecin existant trouvé")
    except Medecin.DoesNotExist:
        # Créer spécialité et établissement par défaut
        specialite, _ = SpecialiteMedicale.objects.get_or_create(
            nom='Médecine Générale',
            defaults={'description': 'Médecine générale et soins primaires'}
        )
        
        etablissement, _ = EtablissementMedical.objects.get_or_create(
            nom='Clinique du Lac',
            defaults={
                'type_etablissement': 'CLINIQUE',
                'adresse': '123 Avenue de la Santé',
                'telephone': '+225 01 23 45 67 89',
                'ville': 'Abidjan'
            }
        )
        
        medecin = Medecin.objects.create(
            user=user_medecin,
            numero_ordre='MED123456',
            specialite=specialite,
            etablissement=etablissement,
            telephone_pro='+225 07 89 45 12 36',
            email_pro='jean.dupont@clinique.com',
            tarif_consultation=15000,
            annees_experience=10
        )
        print("✅ Profil médecin créé")
    
    # 4. Créer des patients (membres) de test
    patients_data = [
        {'prenom': 'Marie', 'nom': 'Koné', 'telephone': '+225 01 23 45 67 90'},
        {'prenom': 'Pierre', 'nom': 'Kouadio', 'telephone': '+225 01 23 45 67 91'},
        {'prenom': 'Aïcha', 'nom': 'Traoré', 'telephone': '+225 01 23 45 67 92'},
        {'prenom': 'Mohamed', 'nom': 'Diop', 'telephone': '+225 01 23 45 67 93'},
    ]
    
    patients = []
    for i, data in enumerate(patients_data, 1):
        try:
            # Créer l'utilisateur patient
            user_patient, created = User.objects.get_or_create(
                username=f'patient{i}',
                defaults={
                    'first_name': data['prenom'],
                    'last_name': data['nom'],
                    'email': f"{data['prenom'].lower()}.{data['nom'].lower()}@email.com"
                }
            )
            if created:
                user_patient.set_password('patient123')
                user_patient.save()
            
            # Créer le membre
            membre, m_created = Membre.objects.get_or_create(
                user=user_patient,
                defaults={
                    'numero_unique': f'MEM{1000 + i}',
                    'telephone': data['telephone'],
                    'date_naissance': timezone.now() - timedelta(days=365*30),
                    'sexe': 'F' if data['prenom'] in ['Marie', 'Aïcha'] else 'M'
                }
            )
            
            if m_created:
                patients.append(membre)
                print(f"✅ Patient {data['prenom']} {data['nom']} créé")
            else:
                patients.append(membre)
                print(f"✅ Patient {data['prenom']} {data['nom']} existant")
                
        except Exception as e:
            print(f"❌ Erreur création patient {data['prenom']}: {e}")
    
    # 5. Créer des consultations de test
    statuts = ['PLANIFIEE', 'EN_COURS', 'TERMINEE', 'ANNULEE']
    types_consultation = ['GENERALE', 'SPECIALISEE', 'SUIVI', 'URGENCE']
    
    consultations_creees = 0
    for i in range(10):  # Créer 10 consultations
        try:
            patient = patients[i % len(patients)]  # Répartir entre les patients
            
            consultation = Consultation.objects.create(
                medecin=medecin,
                membre=patient,
                date_consultation=timezone.now().date() + timedelta(days=i-5),  # Dates variées
                heure_consultation=datetime.strptime(f"{(9 + i % 6):02d}:00", "%H:%M").time(),
                type_consultation=types_consultation[i % len(types_consultation)],
                statut=statuts[i % len(statuts)],
                symptomes="Fièvre, maux de tête" if i % 2 == 0 else "Douleurs abdominales",
                motifs="Consultation de routine" if i % 3 == 0 else "Symptômes aigus",
                duree=30
            )
            consultations_creees += 1
            print(f"✅ Consultation {i+1} créée pour {patient.user.get_full_name()}")
            
        except Exception as e:
            print(f"❌ Erreur création consultation {i+1}: {e}")
    
    # 6. Créer des bons de soin de test
    try:
        for i, patient in enumerate(patients):
            bon = BonSoin.objects.create(
                code=f"BS{timezone.now().strftime('%Y%m%d')}{i}",
                membre=patient,
                agent=user_medecin,  # Utiliser l'user comme agent
                medecin_destinataire=medecin,
                date_creation=timezone.now(),
                date_expiration=timezone.now() + timedelta(days=30),
                statut='EN_ATTENTE' if i % 2 == 0 else 'VALIDE',
                montant_max=25000 + i * 5000,
                type_soin='Consultation',
                motif_consultation="Consultation médicale standard"
            )
            print(f"✅ Bon de soin créé pour {patient.user.get_full_name()}")
    except Exception as e:
        print(f"❌ Erreur création bons de soin: {e}")
    
    print(f"\n🎉 DONNÉES DE TEST CRÉÉES AVEC SUCCÈS!")
    print(f"📊 Médecin: Dr {medecin.user.get_full_name()}")
    print(f"👥 Patients: {len(patients)} créés")
    print(f"📅 Consultations: {consultations_creees} créées")
    print(f"📋 Bons de soin: {len(patients)} créés")

if __name__ == '__main__':
    creer_donnees_test()