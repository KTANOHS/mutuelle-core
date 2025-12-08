#!/usr/bin/env python
"""
SCRIPT SIMPLIFIÉ DE TEST PAIEMENT
=================================
Usage: python manage.py shell < test_paiement_simple.py
"""

import sys
import os
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User, Group
from django.utils import timezone
from decimal import Decimal
from assureur.models import Assureur, Paiement
from agents.models import Membre
from assureur.models import Soin

def test_paiement_simple():
    """Test simplifié de création de paiement"""
    print("🔧 Test simplifié de paiement")
    print("=" * 40)
    
    try:
        # 1. Créer/obtenir un utilisateur assureur
        user, created = User.objects.get_or_create(
            username='test_simple',
            defaults={
                'email': 'test@example.com',
                'password': 'test123',
                'is_active': True
            }
        )
        if created:
            user.set_password('test123')
            user.save()
        
        # 2. Ajouter au groupe ASSUREUR
        groupe, _ = Group.objects.get_or_create(name='assureur')
        user.groups.add(groupe)
        
        # 3. Créer un profil assureur
        Assureur.objects.get_or_create(
            user=user,
            defaults={
                'nom': 'Test Simple',
                'email': 'test@example.com'
            }
        )
        
        # 4. Créer un membre de test
        membre, _ = Membre.objects.get_or_create(
            numero_unique='SIMPLE001',
            defaults={
                'nom': 'Simple',
                'prenom': 'Test',
                'statut': 'actif'
            }
        )
        
        # 5. Créer un soin de test
        soin, _ = Soin.objects.get_or_create(
            code='SIMPLE-SOIN',
            defaults={
                'membre': membre,
                'type_soin': 'consultation',
                'montant_facture': Decimal('3000.00'),
                'statut': 'valide'
            }
        )
        
        # 6. Créer un paiement de test
        paiement = Paiement.objects.create(
            membre=membre,
            soin=soin,
            montant=Decimal('3000.00'),
            mode_paiement='espece',
            date_paiement=timezone.now().date(),
            statut='valide',
            reference=f'PAY-SIMPLE-{timezone.now().strftime("%Y%m%d%H%M%S")}',
            notes='Paiement de test simplifié',
            created_by=user,
            valide_par=user,
            date_validation=timezone.now()
        )
        
        print(f"✅ Paiement créé avec succès:")
        print(f"   Référence: {paiement.reference}")
        print(f"   Membre: {paiement.membre.nom} {paiement.membre.prenom}")
        print(f"   Montant: {paiement.montant} FCFA")
        print(f"   Statut: {paiement.statut}")
        
        # 7. Vérifier la présence en base
        paiements_count = Paiement.objects.filter(reference__contains='SIMPLE').count()
        print(f"📊 Nombre de paiements 'SIMPLE': {paiements_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_paiement_simple()
    
    if success:
        print("\n✅ Test réussi !")
        sys.exit(0)
    else:
        print("\n❌ Test échoué !")
        sys.exit(1)