#!/usr/bin/env python
"""
SCRIPT AVEC NOUVEAU MODÈLE - TEST RELATION MÉDECIN
"""

import os
import sys
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre, Bon
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

def test_nouvelle_relation():
    print("🔧 TEST AVEC NOUVELLE RELATION MÉDECIN")
    print("=" * 45)
    
    try:
        medecin = User.objects.get(username='medecin_test')
        membre = Membre.objects.first()
        
        print(f"👨‍⚕️ Médecin: {medecin.username}")
        print(f"👥 Membre: {membre.nom} {membre.prenom}")
        
        # Création avec la nouvelle relation
        bon = Bon.objects.create(
            membre=membre,
            type_soin='CONSULT',
            description='Test avec relation médecin',
            medecin_traitant=medecin,  # ✅ Maintenant un objet User
            montant_total=7500,
            statut='BROUILLON'
        )
        
        print(f"\n✅ BON CRÉÉ AVEC RELATION:")
        print(f"   📋 Numéro: {bon.numero_bon}")
        print(f"   👨‍⚕️ Médecin: {bon.medecin_traitant.username}")
        print(f"   📊 Statut: {bon.statut}")
        
        # Test: Vérifier que le médecin peut voir ses bons
        print(f"\n🔍 BONS DU MÉDECIN {medecin.username}:")
        bons_medecin = Bon.objects.filter(medecin_traitant=medecin)
        print(f"   Nombre de bons: {bons_medecin.count()}")
        
        for bon_med in bons_medecin:
            print(f"   - {bon_med.numero_bon} | {bon_med.membre.nom} | {bon_med.statut}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_nouvelle_relation()
    sys.exit(0 if success else 1)