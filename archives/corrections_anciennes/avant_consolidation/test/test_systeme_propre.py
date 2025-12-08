#!/usr/bin/env python
"""
TEST FINAL - SYSTÈME PROPRE
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

def test_systeme_propre():
    print("🎯 TEST SYSTÈME PROPRE")
    print("=" * 40)
    
    try:
        # 1. Vérifier les utilisateurs
        medecin = User.objects.get(username='medecin_test')
        agent = User.objects.get(username='test_agent')
        membre = Membre.objects.first()
        
        print(f"👨‍⚕️ Médecin: {medecin.username}")
        print(f"👤 Agent: {agent.username}")
        print(f"👥 Membre: {membre.nom} {membre.prenom}")
        
        # 2. Créer un bon avec la nouvelle structure
        bon = Bon.objects.create(
            membre=membre,
            type_soin='CONSULT',
            description='Test système propre - consultation générale',
            lieu_soins='Centre Médical Principal',
            date_soins=timezone.now().date(),
            medecin_traitant=medecin,  # ✅ ForeignKey fonctionnelle
            montant_total=12500,
            statut='BROUILLON'
        )
        
        print(f"\n✅ BON CRÉÉ:")
        print(f"   📋 Numéro: {bon.numero_bon}")
        print(f"   👨‍⚕️ Médecin: {bon.medecin_traitant.username}")
        print(f"   💰 Montant: {bon.montant_total} FCFA")
        print(f"   📊 Statut: {bon.statut}")
        
        # 3. Test de filtrage par médecin
        print(f"\n🔍 TEST FILTRAGE MÉDECIN:")
        bons_medecin = Bon.objects.filter(medecin_traitant=medecin)
        print(f"   Bons trouvés: {bons_medecin.count()}")
        
        for bon_med in bons_medecin:
            print(f"   - {bon_med.numero_bon} | {bon_med.membre.nom} | {bon_med.statut}")
        
        # 4. Validation
        print(f"\n✅ VALIDATION:")
        bon.statut = 'VALIDE'
        bon.valide_par = medecin
        bon.date_validation = timezone.now()
        bon.montant_rembourse = bon.montant_a_rembourser
        bon.save()
        
        print(f"   📋 {bon.numero_bon} → VALIDÉ")
        print(f"   👨‍⚕️ Validé par: {bon.valide_par.username}")
        print(f"   💰 Remboursement: {bon.montant_rembourse} FCFA")
        print(f"   📅 Date: {bon.date_validation}")
        
        # 5. Vérification finale
        print(f"\n📊 ÉTAT FINAL:")
        total_bons = Bon.objects.count()
        bons_valides = Bon.objects.filter(statut='VALIDE').count()
        print(f"   Total bons: {total_bons}")
        print(f"   Bons validés: {bons_valides}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_systeme_propre()
    if success:
        print("\n🎉 SYSTÈME FONCTIONNEL! Le médecin peut maintenant voir ses bons.")
    sys.exit(0 if success else 1)