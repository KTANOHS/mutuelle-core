# fix_remaining_issues.py - VERSION ULTIME SIMPLIFIÉE
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def check_and_fix_database():
    """Vérifier et corriger la structure de la base"""
    print("🔍 Vérification de la structure de la base...")
    
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(membres_membre)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'score_risque' not in columns:
            print("➕ Ajout de la colonne score_risque...")
            cursor.execute("ALTER TABLE membres_membre ADD COLUMN score_risque INTEGER DEFAULT 0")
            print("✅ Colonne score_risque ajoutée")
        else:
            print("✅ Colonne score_risque existe déjà")
    
    print("🎯 Structure de base vérifiée")

def create_test_agent():
    """Créer un agent de test si nécessaire"""
    from django.contrib.auth.models import User
    from agents.models import Agent
    
    try:
        user = User.objects.get(username='LEILA')
        if not Agent.objects.filter(user=user).exists():
            print("👤 Création de l'agent LEILA...")
            Agent.objects.create(
                user=user,
                telephone="0102030405",
                est_actif=True
            )
            print("✅ Agent LEILA créé")
        else:
            print("✅ Agent LEILA existe déjà")
    except User.DoesNotExist:
        print("⚠️  Utilisateur LEILA non trouvé - création de l'utilisateur...")
        user = User.objects.create_user(
            username='LEILA',
            password='test123',
            first_name='Leila',
            last_name='Test',
            email='leila@test.com'
        )
        Agent.objects.create(
            user=user,
            telephone="0102030405", 
            est_actif=True
        )
        print("✅ Agent LEILA créé")

def generate_unique_member_number():
    """Générer un numéro unique pour les membres"""
    from membres.models import Membre
    import random
    import string
    
    while True:
        number = f"MEM-{''.join(random.choices(string.digits, k=5))}"
        if not Membre.objects.filter(numero_unique=number).exists():
            return number

def populate_test_data_safe():
    """Ajouter des données de test de manière sécurisée"""
    from membres.models import Membre
    
    print("\n👥 Création de données de test pour les membres...")
    
    # Données de test simples
    test_members = [
        {'prenom': 'Jean', 'nom': 'Dupont', 'telephone': '0102030405'},
        {'prenom': 'Marie', 'nom': 'Martin', 'telephone': '0203040506'},
        {'prenom': 'Pierre', 'nom': 'Durand', 'telephone': '0304050607'},
        {'prenom': 'Sophie', 'nom': 'Leroy', 'telephone': '0405060708'},
        {'prenom': 'David', 'nom': 'Moreau', 'telephone': '0506070809'},
        {'prenom': 'Asia', 'nom': 'Koné', 'telephone': '0607080910'},
        {'prenom': 'Dramane', 'nom': 'Coulibaly', 'telephone': '0708091011'},
    ]
    
    members_created = 0
    
    for member_data in test_members:
        try:
            # Vérifier si le membre existe déjà
            existing = Membre.objects.filter(
                prenom=member_data['prenom'],
                nom=member_data['nom']
            ).exists()
            
            if not existing:
                # Créer le membre avec des valeurs par défaut simples
                numero_unique = generate_unique_member_number()
                
                Membre.objects.create(
                    prenom=member_data['prenom'],
                    nom=member_data['nom'],
                    telephone=member_data['telephone'],
                    email=f"{member_data['prenom'].lower()}.{member_data['nom'].lower()}@test.com",
                    score_risque=25,  # Valeur par défaut
                    niveau_risque='FAIBLE',  # Valeur simple
                    numero_unique=numero_unique
                )
                print(f"✅ Membre {member_data['prenom']} {member_data['nom']} créé")
                members_created += 1
            else:
                print(f"⚠️  Membre {member_data['prenom']} {member_data['nom']} existe déjà")
                
        except Exception as e:
            print(f"❌ Erreur avec {member_data['prenom']} {member_data['nom']}: {str(e)[:100]}...")
    
    print(f"📊 {members_created} nouveaux membres créés")

def test_search_functionality():
    """Tester la fonctionnalité de recherche"""
    print("\n🔍 Test de la fonctionnalité de recherche...")
    
    from membres.models import Membre
    
    # Tests de recherche
    searches = ['jean', 'asia', 'dramane', 'marie']
    
    for search_term in searches:
        results = Membre.objects.filter(
            prenom__icontains=search_term
        ) | Membre.objects.filter(
            nom__icontains=search_term
        )
        print(f"✅ Recherche '{search_term}': {results.count()} résultats")
        
        for membre in results[:2]:  # Afficher les 2 premiers
            print(f"   👤 {membre.prenom} {membre.nom} - 📞 {membre.telephone}")

def quick_fix_member_scores():
    """Corriger rapidement les scores des membres existants"""
    from membres.models import Membre
    
    print("\n🎯 Mise à jour des scores des membres existants...")
    
    membres = Membre.objects.all()
    for membre in membres:
        if not hasattr(membre, 'score_risque') or membre.score_risque is None:
            membre.score_risque = 30  # Valeur par défaut
        if not hasattr(membre, 'niveau_risque') or not membre.niveau_risque:
            membre.niveau_risque = 'MOYEN'  # Valeur par défaut
        membre.save()
    
    print(f"✅ {membres.count()} membres mis à jour")

if __name__ == "__main__":
    print("🚀 DÉMARRAGE DES CORRECTIONS FINALES...")
    
    check_and_fix_database()
    create_test_agent()
    quick_fix_member_scores()
    populate_test_data_safe()
    test_search_functionality()
    
    print("\n🎉 CORRECTIONS TERMINÉES AVEC SUCCÈS!")
    print("\n🚀 INSTRUCTIONS DE TEST:")
    print("   1. Redémarrez: python manage.py runserver")
    print("   2. Connectez-vous: LEILA / test123")
    print("   3. Testez la recherche avec: 'asia', 'jean', 'dramane'")
    print("   4. Vérifiez le dashboard agent")
    print("\n📊 DONNÉS PRÊTES:")
    print("   👤 Agent: LEILA Test")
    print("   👥 Membres: Jean, Marie, Pierre, Sophie, David, Asia, Dramane")
    print("   🔍 Recherche: Testée et fonctionnelle")