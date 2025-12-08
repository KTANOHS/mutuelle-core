# test_generation_fixed.py
import os
import django
from datetime import datetime
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("=== TEST AVEC LES BONNES VALEURS ===")

from assureur.models import Membre, Cotisation
from django.contrib.auth.models import User

# Créer un utilisateur test
user = User.objects.create_user('test_user', 'test@test.com', 'test123')

# Prendre un membre existant
membre = Membre.objects.filter(statut='actif').first()
if not membre:
    print("❌ Aucun membre actif trouvé")
    exit()

print(f"Membre test: {membre.nom} {membre.prenom}")

# Tester la création d'une cotisation avec les bonnes valeurs
try:
    # Période au bon format
    periode = '2025-01'
    
    # Dates
    date_emission = datetime.now().date()
    date_echeance = datetime(2025, 1, 31).date()
    
    # Déterminer type et montant
    if membre.est_femme_enceinte:
        type_cotisation = 'femme_enceinte'
        montant = Decimal('7500.00')
    else:
        type_cotisation = 'normale'
        montant = Decimal('5000.00')
    
    # Créer la référence
    reference = f"COT-{membre.numero_membre}-202501"
    
    # Créer la cotisation
    cotisation = Cotisation(
        membre=membre,
        periode=periode,
        montant=montant,
        statut='due',
        date_emission=date_emission,
        date_echeance=date_echeance,
        type_cotisation=type_cotisation,
        reference=reference,
        enregistre_par=user,
        notes='Test unitaire',
        montant_clinique=Decimal('0.00'),
        montant_pharmacie=Decimal('0.00'),
        montant_charges_mutuelle=Decimal('0.00'),
    )
    
    # Valider
    cotisation.full_clean()
    print("✅ Validation réussie!")
    
    # Sauvegarder
    cotisation.save()
    print("✅ Sauvegarde réussie!")
    print(f"   Référence: {cotisation.reference}")
    print(f"   Type: {cotisation.type_cotisation}")
    print(f"   Statut: {cotisation.statut}")
    print(f"   Montant: {cotisation.montant}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()