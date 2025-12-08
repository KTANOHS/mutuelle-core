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

def creer_donnees_test():
    print("🛠️ CRÉATION DES DONNÉES AVEC CHAMPS CORRECTS")
    print("================================================")
    
    # 1. Création des patients
    print("1. 👥 CRÉATION DES PATIENTS...")
    
    patients_data = [
        {"username": "marie_dupont", "first_name": "Marie", "last_name": "Dupont", "email": "marie@example.com"},
        {"username": "pierre_martin", "first_name": "Pierre", "last_name": "Martin", "email": "pierre@example.com"},
        {"username": "sophie_leroy", "first_name": "Sophie", "last_name": "Leroy", "email": "sophie@example.com"},
        {"username": "jean_bernard", "first_name": "Jean", "last_name": "Bernard", "email": "jean@example.com"},
        {"username": "alice_dubois", "first_name": "Alice", "last_name": "Dubois", "email": "alice@example.com"},
    ]
    
    patients_crees = []
    
    for data in patients_data:
        try:
            # Créer l'utilisateur
            user = User.objects.create_user(
                username=data['username'],
                password='password123',
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email']
            )
            
            # Créer le membre avec les CHAMPS EXISTANTS du modèle
            membre = Membre.objects.create(
                user=user,
                nom=data['last_name'],
                prenom=data['first_name'],
                telephone="+2250102030405",
                numero_urgence="+2250506070809",
                date_inscription=timezone.now(),
                statut="actif",
                categorie="standard",
                cmu_option=False,
                date_naissance=date(1980, 1, 1),
                adresse="Abidjan, Côte d'Ivoire",
                email=data['email'],
                profession="Employé",
                date_derniere_cotisation=date.today(),
                prochain_paiement_le=date.today() + timedelta(days=365),
                est_femme_enceinte=False,
                avance_payee=0,
                carte_adhesion_payee=0,
                taux_couverture=70.0,
                type_piece_identite="cni",
                numero_piece_identite="123456789",
                statut_documents="valide"
            )
            
            patients_crees.append(membre)
            print(f"   ✅ Patient créé: {membre.prenom} {membre.nom}")
            
        except Exception as e:
            print(f"   ❌ Erreur création patient {data['username']}: {e}")
    
    # 2. Essayer d'importer et créer des maladies chroniques
    print("\n2. 🩺 TENTATIVE DE CRÉATION DES MALADIES CHRONIQUES...")
    
    try:
        # Essayer différents noms d'application possibles
        try:
            from maladies_chroniques.models import MaladieChronique
            app_name = "maladies_chroniques"
        except ImportError:
            try:
                from maladie_chronique.models import MaladieChronique
                app_name = "maladie_chronique"
            except ImportError:
                try:
                    from sante.models import MaladieChronique
                    app_name = "sante"
                except ImportError:
                    try:
                        from medical.models import MaladieChronique
                        app_name = "medical"
                    except ImportError:
                        print("   ❌ Impossible de trouver le modèle MaladieChronique")
                        raise ImportError("Modèle MaladieChronique non trouvé")
        
        print(f"   ✅ Modèle MaladieChronique trouvé dans l'application: {app_name}")
        
        maladies_data = [
            {"nom": "Diabète de type 2", "code_cim": "E11", "description": "Diabète sucré de type 2"},
            {"nom": "Hypertension artérielle", "code_cim": "I10", "description": "Hypertension artérielle essentielle"},
            {"nom": "Asthme", "code_cim": "J45", "description": "Asthme bronchique"},
            {"nom": "Arthrite rhumatoïde", "code_cim": "M05", "description": "Arthrite rhumatoïde séropositive"},
            {"nom": "Dépression", "code_cim": "F32", "description": "Épisode dépressif"},
        ]
        
        maladies_crees = []
        
        for data in maladies_data:
            try:
                maladie = MaladieChronique.objects.create(
                    nom=data['nom'],
                    code_cim=data['code_cim'],
                    description=data['description'],
                    recommandations_generales="Suivi médical régulier requis",
                    actif=True
                )
                
                maladies_crees.append(maladie)
                print(f"   ✅ Maladie créée: {maladie.nom}")
                
            except Exception as e:
                print(f"   ❌ Erreur création maladie {data['nom']}: {e}")
                
    except Exception as e:
        print(f"   ⚠️  Impossible de créer les maladies: {e}")
        print("   💡 Création des patients uniquement...")
        maladies_crees = []
    
    # 3. Résumé final
    print("\n3. 📊 RÉSUMÉ FINAL:")
    print(f"   👥 Patients créés: {len(patients_crees)}")
    print(f"   🩺 Maladies créées: {len(maladies_crees)}")
    print(f"   📋 Total patients dans la base: {Membre.objects.count()}")
    
    try:
        from maladies_chroniques.models import MaladieChronique
        print(f"   📋 Total maladies dans la base: {MaladieChronique.objects.count()}")
    except:
        print("   📋 Total maladies dans la base: Modèle non accessible")
    
    if len(patients_crees) > 0:
        print("\n✅ Patients créés avec succès! Les filtres devraient maintenant fonctionner.")
    else:
        print("\n⚠️  Problème lors de la création des données")

if __name__ == "__main__":
    creer_donnees_test()