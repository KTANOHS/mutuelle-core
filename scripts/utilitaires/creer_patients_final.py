import os
import django
import sys
from datetime import date, timedelta
from django.utils import timezone

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User
from membres.models import Membre

def creer_patients_final():
    print("👥 CRÉATION DES PATIENTS AVEC NOMS UNIQUES")
    print("============================================")
    
    patients_data = [
        {"username": "patient_martin_001", "first_name": "Pierre", "last_name": "Martin", "email": "pierre.martin@example.com"},
        {"username": "patient_leroy_002", "first_name": "Sophie", "last_name": "Leroy", "email": "sophie.leroy@example.com"},
        {"username": "patient_bernard_003", "first_name": "Jean", "last_name": "Bernard", "email": "jean.bernard@example.com"},
        {"username": "patient_dubois_004", "first_name": "Alice", "last_name": "Dubois", "email": "alice.dubois@example.com"},
        {"username": "patient_moreau_005", "first_name": "Luc", "last_name": "Moreau", "email": "luc.moreau@example.com"},
        {"username": "patient_girard_006", "first_name": "Emma", "last_name": "Girard", "email": "emma.girard@example.com"},
        {"username": "patient_robert_007", "first_name": "Thomas", "last_name": "Robert", "email": "thomas.robert@example.com"},
        {"username": "patient_laurent_008", "first_name": "Camille", "last_name": "Laurent", "email": "camille.laurent@example.com"},
        {"username": "patient_simon_009", "first_name": "Antoine", "last_name": "Simon", "email": "antoine.simon@example.com"},
        {"username": "patient_leroux_010", "first_name": "Julie", "last_name": "Leroux", "email": "julie.leroux@example.com"},
    ]
    
    patients_crees = []
    
    for i, data in enumerate(patients_data, 1):
        try:
            # Vérifier si l'utilisateur existe déjà
            if User.objects.filter(username=data['username']).exists():
                print(f"   ⚠️  Utilisateur {data['username']} existe déjà, passage au suivant")
                continue
            
            # Créer l'utilisateur
            user = User.objects.create_user(
                username=data['username'],
                password='password123',
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email']
            )
            
            # Numéro de pièce d'identité unique
            numero_piece = f"CI2024P{str(i).zfill(6)}"
            
            # Créer le membre avec les CHOIX EXACTS
            membre = Membre.objects.create(
                user=user,
                nom=data['last_name'],
                prenom=data['first_name'],
                telephone=f"+22501{str(1000000 + i).zfill(7)}",
                numero_urgence=f"+22507{str(2000000 + i).zfill(7)}",
                date_inscription=timezone.now(),
                statut="actif",
                categorie="standard",
                cmu_option=False,
                date_naissance=date(1980 + (i % 20), (i % 12) + 1, (i % 28) + 1),
                adresse=f"Abidjan, Quartier {i}",
                email=data['email'],
                profession=["Employé", "Commerçant", "Fonctionnaire", "Enseignant", "Infirmier"][i % 5],
                date_derniere_cotisation=date.today() - timedelta(days=30),
                prochain_paiement_le=date.today() + timedelta(days=335),
                est_femme_enceinte=(i % 3 == 0),
                avance_payee=0,
                carte_adhesion_payee=5000 if i % 2 == 0 else 0,
                taux_couverture=60.0 + (i * 2),
                type_piece_identite="CNI",
                numero_piece_identite=numero_piece,
                statut_documents="VALIDE"
            )
            
            patients_crees.append(membre)
            print(f"   ✅ Patient créé: {membre.prenom} {membre.nom} (PI: {numero_piece})")
            
        except Exception as e:
            print(f"   ❌ Erreur création patient {data['username']}: {e}")
    
    print(f"\n📊 RÉSUMÉ FINAL:")
    print(f"   👥 Nouveaux patients créés: {len(patients_crees)}")
    print(f"   📋 Total patients dans la base: {Membre.objects.count()}")

if __name__ == "__main__":
    creer_patients_final()