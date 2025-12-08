
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

print("=== CRÉATION DE DONNÉES DE TEST SIMPLES ===")

# 1. Vérifier que DOUA est dans le bon groupe
doua = User.objects.get(username='DOUA')
assureur_group = Group.objects.get(name='Assureur')
print(f"✓ DOUA dans groupe: {assureur_group.name}")

# 2. Créer quelques membres
membres_data = [
    {'nom': 'KOUADIO', 'prenom': 'Jean', 'matricule': 'MEM001', 'telephone': '07000001'},
    {'nom': 'KONE', 'prenom': 'Marie', 'matricule': 'MEM002', 'telephone': '07000002'},
    {'nom': 'DIAKITE', 'prenom': 'Paul', 'matricule': 'MEM003', 'telephone': '07000003'},
]

for data in membres_data:
    membre, created = Membre.objects.get_or_create(
        matricule=data['matricule'],
        defaults={
            'nom': data['nom'],
            'prenom': data['prenom'],
            'telephone': data['telephone'],
            'date_inscription': timezone.now() - timedelta(days=random.randint(30, 365)),
            'statut': 'actif',
            'email': f"{data['prenom'].lower()}.{data['nom'].lower()}@example.com",
        }
    )
    if created:
        print(f"✓ Membre créé: {membre.nom_complet}")

# 3. Créer quelques bons de soin
membres = Membre.objects.all()
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

# 4. Créer la configuration
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
print("\n   Interface admin:")
print("   - Utilisateur: admin")
print("   - Mot de passe: admin123")

