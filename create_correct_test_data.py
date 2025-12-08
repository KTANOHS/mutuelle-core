import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
import django
django.setup()

from django.contrib.auth.models import User, Group
from membres.models import Membre
from assureur.models import Bon, ConfigurationAssurance, Paiement
from django.utils import timezone
from datetime import timedelta
import random
import string

print("=== CRÉATION DE DONNÉES DE TEST CORRIGÉE ===")

# 1. Vérifier que DOUA est dans le bon groupe
doua = User.objects.get(username='DOUA')
assureur_group = Group.objects.get(name='Assureur')
print(f"✓ DOUA dans groupe: {assureur_group.name}")

# 2. Générer un numéro unique pour chaque membre
def generer_numero_membre():
    date_part = timezone.now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"MEM-{date_part}-{random_part}"

# 3. Créer quelques membres avec le bon champ (numero_unique au lieu de matricule)
membres_data = [
    {'nom': 'KOUADIO', 'prenom': 'Jean', 'telephone': '07000001'},
    {'nom': 'KONE', 'prenom': 'Marie', 'telephone': '07000002'},
    {'nom': 'DIAKITE', 'prenom': 'Paul', 'telephone': '07000003'},
]

for data in membres_data:
    # Générer un numéro unique
    numero_unique = generer_numero_membre()
    
    # Vérifier si un membre avec ce numéro existe déjà
    if not Membre.objects.filter(numero_unique=numero_unique).exists():
        membre = Membre.objects.create(
            numero_unique=numero_unique,
            nom=data['nom'],
            prenom=data['prenom'],
            telephone=data['telephone'],
            date_inscription=timezone.now() - timedelta(days=random.randint(30, 365)),
            statut='actif',
            email=f"{data['prenom'].lower()}.{data['nom'].lower()}@example.com",
            date_naissance=timezone.now() - timedelta(days=random.randint(20*365, 60*365)),  # Âge entre 20 et 60 ans
            type_piece_identite='CNI',
            numero_piece_identite=f'CI{random.randint(1000000, 9999999)}',
            date_expiration_piece=timezone.now() + timedelta(days=random.randint(365, 1825)),  # 1 à 5 ans
            adresse=f"{random.randint(1, 100)} Rue des Manguiers, Abidjan",
            profession=random.choice(['Enseignant', 'Commerçant', 'Fonctionnaire', 'Agriculteur']),
            taux_couverture=random.uniform(60, 90),
        )
        print(f"✓ Membre créé: {membre.nom_complet} - Numéro: {membre.numero_unique}")
    else:
        print(f"⚠️ Membre avec numéro {numero_unique} existe déjà")

# 4. Créer quelques bons de soin
membres = Membre.objects.all()
if membres.exists():
    types_soin = ['consultation', 'hospitalisation', 'pharmacie']
    statuts = ['en_attente', 'valide', 'rejete']

    for i in range(5):
        bon = Bon.objects.create(
            numero=f"BS{2024}{i+1:04d}",
            membre=random.choice(membres),
            type_soin=random.choice(types_soin),
            montant_total=random.uniform(5000, 20000),
            taux_couverture=random.uniform(50, 80),
            montant_remboursable=0,
            date_emission=timezone.now().date() - timedelta(days=random.randint(1, 30)),
            date_expiration=timezone.now().date() + timedelta(days=random.randint(30, 90)),
            statut=random.choice(statuts),
        )
        bon.montant_remboursable = bon.montant_total * (bon.taux_couverture / 100)
        bon.save()
        print(f"✓ Bon créé: {bon.numero} - {bon.montant_remboursable:.2f} FCFA")
else:
    print("⚠️ Aucun membre disponible pour créer des bons")

# 5. Créer la configuration
config, created = ConfigurationAssurance.objects.get_or_create(
    nom_assureur="Mutuelle Santé Plus",
    defaults={
        'taux_couverture_defaut': 70.0,
        'delai_validite_bon': 30,
    }
)
if created:
    print(f"✓ Configuration créée: {config.nom_assureur}")

print(f"\n📊 RÉSUMÉ:")
print(f"Membres: {Membre.objects.count()}")
print(f"Bons de soin: {Bon.objects.count()}")
print(f"Configuration: {ConfigurationAssurance.objects.count()}")

print("\n🔑 Identifiants de test:")
print("   Interface assureur:")
print("   - Utilisateur: DOUA")
print("   - Mot de passe: (celui que vous avez défini)")
print("\n   Pour réinitialiser le mot de passe de DOUA:")
print("   python manage.py shell -c \"")
print("   from django.contrib.auth.models import User")
print("   user = User.objects.get(username='DOUA')")
print("   user.set_password('doua123')")
print("   user.save()")
print("   print('Mot de passe réinitialisé à: doua123')")
print("   \"")