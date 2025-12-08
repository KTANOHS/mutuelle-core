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

def creer_patients_avec_choix_corrects():
    print("👥 CRÉATION DES PATIENTS AVEC CHOIX CORRECTS")
    print("==============================================")
    
    patients_data = [
        {"username": "pierre_martin", "first_name": "Pierre", "last_name": "Martin", "email": "pierre@example.com"},
        {"username": "sophie_leroy", "first_name": "Sophie", "last_name": "Leroy", "email": "sophie@example.com"},
        {"username": "jean_bernard", "first_name": "Jean", "last_name": "Bernard", "email": "jean@example.com"},
        {"username": "alice_dubois", "first_name": "Alice", "last_name": "Dubois", "email": "alice@example.com"},
        {"username": "luc_moreau", "first_name": "Luc", "last_name": "Moreau", "email": "luc@example.com"},
    ]
    
    patients_crees = []
    
    for i, data in enumerate(patients_data, 1):
        try:
            # Créer l'utilisateur
            user = User.objects.create_user(
                username=data['username'],
                password='password123',
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email']
            )
            
            # Numéro de pièce d'identité unique pour chaque patient
            numero_piece = f"CI2024{str(i+1).zfill(6)}"  # Commencer à 2 pour éviter les doublons
            
            # Créer le membre avec les CHOIX EXACTS
            membre = Membre.objects.create(
                user=user,
                nom=data['last_name'],
                prenom=data['first_name'],
                telephone=f"+22501{str(i+10).zfill(8)}",  # Numéros uniques
                numero_urgence=f"+22507{str(i+10).zfill(8)}",
                date_inscription=timezone.now(),
                statut="actif",  # ✅ Choix exact: 'actif'
                categorie="standard",  # ✅ Choix exact: 'standard'
                cmu_option=False,
                date_naissance=date(1980 + i, i, 15),  # Dates différentes
                adresse=f"Abidjan, Plateau {i}",
                email=data['email'],
                profession="Employé",
                date_derniere_cotisation=date.today(),
                prochain_paiement_le=date.today() + timedelta(days=365),
                est_femme_enceinte=False,
                avance_payee=0,
                carte_adhesion_payee=0,
                taux_couverture=70.0 + i,  # Légère variation
                type_piece_identite="CNI",  # ✅ Choix exact: 'CNI'
                numero_piece_identite=numero_piece,  # Unique pour chaque
                statut_documents="VALIDE"  # ✅ Choix exact: 'VALIDE'
            )
            
            patients_crees.append(membre)
            print(f"   ✅ Patient créé: {membre.prenom} {membre.nom} (PI: {numero_piece})")
            
        except Exception as e:
            print(f"   ❌ Erreur création patient {data['username']}: {e}")
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"   👥 Patients créés: {len(patients_crees)}")
    print(f"   📋 Total patients dans la base: {Membre.objects.count()}")

if __name__ == "__main__":
    creer_patients_avec_choix_corrects()