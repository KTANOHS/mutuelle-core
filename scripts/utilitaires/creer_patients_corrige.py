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

def obtenir_choix_champs():
    """Récupère les choix valides pour les champs du modèle Membre"""
    print("🔍 RECHERCHE DES CHOIX VALIDES...")
    
    # Inspecter le modèle Membre pour trouver les choix
    champ_type_piece = Membre._meta.get_field('type_piece_identite')
    champ_statut_docs = Membre._meta.get_field('statut_documents')
    
    print(f"   📋 Type pièce identité: {getattr(champ_type_piece, 'choices', 'Aucun choix défini')}")
    print(f"   📋 Statut documents: {getattr(champ_statut_docs, 'choices', 'Aucun choix défini')}")
    
    # Retourner les premiers choix disponibles ou des valeurs par défaut
    return {
        'type_piece_identite': 'CNI',  # Essayer avec majuscules
        'statut_documents': 'VALIDATED'  # Essayer avec statut en anglais
    }

def creer_patients_corrige():
    print("👥 CRÉATION DES PATIENTS AVEC CHOIX CORRECTS")
    print("==============================================")
    
    # Obtenir les choix valides
    choix = obtenir_choix_champs()
    
    patients_data = [
        {"username": "marie_dupont", "first_name": "Marie", "last_name": "Dupont", "email": "marie@example.com"},
        {"username": "pierre_martin", "first_name": "Pierre", "last_name": "Martin", "email": "pierre@example.com"},
        {"username": "sophie_leroy", "first_name": "Sophie", "last_name": "Leroy", "email": "sophie@example.com"},
        {"username": "jean_bernard", "first_name": "Jean", "last_name": "Bernard", "email": "jean@example.com"},
        {"username": "alice_dubois", "first_name": "Alice", "last_name": "Dubois", "email": "alice@example.com"},
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
            numero_piece = f"CI2024{str(i).zfill(6)}"
            
            # Créer le membre avec les CHOIX VALIDES
            membre = Membre.objects.create(
                user=user,
                nom=data['last_name'],
                prenom=data['first_name'],
                telephone=f"+22501{str(i).zfill(8)}",
                numero_urgence=f"+22507{str(i).zfill(8)}",
                date_inscription=timezone.now(),
                statut="ACTIVE",  # Essayer en majuscules
                categorie="STANDARD",  # Essayer en majuscules
                cmu_option=False,
                date_naissance=date(1980 + i, 1, 1),  # Dates différentes
                adresse=f"Abidjan, Plateau {i}",
                email=data['email'],
                profession="Employé",
                date_derniere_cotisation=date.today(),
                prochain_paiement_le=date.today() + timedelta(days=365),
                est_femme_enceinte=False,
                avance_payee=0,
                carte_adhesion_payee=0,
                taux_couverture=70.0,
                type_piece_identite=choix['type_piece_identite'],
                numero_piece_identite=numero_piece,  # Unique pour chaque
                statut_documents=choix['statut_documents']
            )
            
            patients_crees.append(membre)
            print(f"   ✅ Patient créé: {membre.prenom} {membre.nom} (PI: {numero_piece})")
            
        except Exception as e:
            print(f"   ❌ Erreur création patient {data['username']}: {e}")
    
    print(f"\n📊 Total patients créés: {len(patients_crees)}")
    print(f"📋 Total patients dans la base: {Membre.objects.count()}")

if __name__ == "__main__":
    creer_patients_corrige()