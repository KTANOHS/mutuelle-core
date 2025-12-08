#!/usr/bin/env python
"""
SCRIPT DE VÉRIFICATION COMPLÈTE DE LA BASE DE DONNÉES
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth.models import User, Group
from membres.models import Membre
from medecin.models import Ordonnance
from soins.models import Soin

def verifier_etat_base():
    """Vérifie l'état complet de la base de données"""
    print("🔍 VÉRIFICATION COMPLÈTE DE LA BASE DE DONNÉES")
    print("=" * 70)
    
    # 1. Vérifier les utilisateurs
    print("\n👥 UTILISATEURS:")
    users = User.objects.all()
    print(f"Total utilisateurs: {users.count()}")
    for user in users:
        groups = ", ".join([g.name for g in user.groups.all()])
        print(f"  - {user.username} ({user.first_name} {user.last_name}) - Groupes: {groups}")
    
    # 2. Vérifier les membres
    print("\n🏥 MEMBRES:")
    membres = Membre.objects.all().order_by('id')
    print(f"Total membres: {membres.count()}")
    
    if not membres.exists():
        print("❌ AUCUN MEMBRE TROUVÉ - Création de membres de test...")
        creer_membres_test()
        membres = Membre.objects.all().order_by('id')
    
    for membre in membres:
        try:
            user_info = f"{membre.user.username}" if membre.user else "SANS USER"
            print(f"  - ID: {membre.id} | {membre.numero_unique} | {membre.nom_complet} | User: {user_info}")
        except Exception as e:
            print(f"  - ID: {membre.id} | ERREUR: {e}")
    
    # 3. Vérifier les ordonnances
    print("\n📄 ORDONNANCES:")
    ordonnances = Ordonnance.objects.all()
    print(f"Total ordonnances: {ordonnances.count()}")
    for ord in ordonnances[:5]:  # Afficher les 5 premières
        patient = ord.patient.username if ord.patient else "Aucun"
        print(f"  - ID: {ord.id} | Patient: {patient} | Diagnostic: {ord.diagnostic[:50]}...")
    
    # 4. Vérifier les soins
    print("\n💊 SOINS:")
    soins = Soin.objects.all()
    print(f"Total soins: {soins.count()}")
    for soin in soins[:5]:  # Afficher les 5 premiers
        patient = soin.patient.username if soin.patient else "Aucun"
        print(f"  - ID: {soin.id} | Patient: {patient} | Type: {soin.type_soin}")

def creer_membres_test():
    """Crée des membres de test si la base est vide"""
    print("\n🔧 CRÉATION DE MEMBRES DE TEST...")
    
    # Créer quelques utilisateurs et membres
    test_data = [
        {
            'username': 'membre_test1',
            'first_name': 'Marie',
            'last_name': 'Dubois',
            'email': 'marie.dubois@example.com',
            'membre_nom': 'Dubois',
            'membre_prenom': 'Marie',
            'membre_id': 1
        },
        {
            'username': 'membre_test2', 
            'first_name': 'Paul',
            'last_name': 'Durand',
            'email': 'paul.durand@example.com',
            'membre_nom': 'Durand',
            'membre_prenom': 'Paul',
            'membre_id': 2
        },
        {
            'username': 'membre_test5',
            'first_name': 'Jean',
            'last_name': 'Martin',
            'email': 'jean.martin@example.com',
            'membre_nom': 'Martin',
            'membre_prenom': 'Jean',
            'membre_id': 5  # Spécifiquement pour l'ID 5 manquant
        }
    ]
    
    for data in test_data:
        try:
            # Créer l'utilisateur
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                    'password': 'password123'
                }
            )
            
            # Créer le membre
            membre, created = Membre.objects.get_or_create(
                id=data['membre_id'],
                defaults={
                    'user': user,
                    'nom': data['membre_nom'],
                    'prenom': data['membre_prenom'],
                    'email': data['email'],
                    'numero_unique': f"MEM2024{data['membre_id']:04d}",
                    'statut': Membre.StatutMembre.ACTIF,
                    'telephone': f"+225 07 {data['membre_id']:02d} 00 00 00",
                    'adresse': 'Abidjan, Côte d\'Ivoire'
                }
            )
            
            if created:
                print(f"✅ Membre {data['membre_id']} créé: {data['membre_nom']} {data['membre_prenom']}")
            else:
                print(f"ℹ️  Membre {data['membre_id']} existe déjà")
                
        except Exception as e:
            print(f"❌ Erreur création membre {data['membre_id']}: {e}")

if __name__ == "__main__":
    verifier_etat_base()
    
    print("\n" + "=" * 70)
    print("🎯 PROCHAINES ÉTAPES:")
    print("1. Accédez à: http://127.0.0.1:8000/assureur/bons/creer/5/")
    print("2. Si le problème persiste, vérifiez les URLs dans mutuelle_core/urls.py")
    print("3. Vérifiez que l'utilisateur connecté a les permissions 'Assureur'")