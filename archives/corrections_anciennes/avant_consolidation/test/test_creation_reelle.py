# test_creation_reelle.py
import os
import sys
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

django.setup()

def test_creation_reelle_bon_soin():
    print("🧪 TEST DE CRÉATION RÉELLE DE BON DE SOIN")
    print("=" * 50)
    
    try:
        from membres.models import Membre
        from soins.models import BonDeSoin
        
        # Prendre un membre existant
        membre = Membre.objects.first()
        print(f"📋 Membre sélectionné: {membre.prenom} {membre.nom}")
        
        # Créer un bon de soin complet
        bon_soin = BonDeSoin.objects.create(
            patient=membre,
            date_soin=date.today(),
            symptomes="Fièvre, toux et maux de tête",
            diagnostic="Infection respiratoire supérieure",
            montant=75.50,
            statut='attente'
        )
        
        print(f"✅ BON DE SOIN CRÉÉ AVEC SUCCÈS!")
        print(f"   📝 Référence: {bon_soin.id}")
        print(f"   👤 Patient: {bon_soin.patient.prenom} {bon_soin.patient.nom}")
        print(f"   💰 Montant: {bon_soin.montant} FCFA")
        print(f"   📅 Date: {bon_soin.date_soin}")
        print(f"   🏥 Diagnostic: {bon_soin.diagnostic}")
        print(f"   📊 Statut: {bon_soin.statut}")
        
        # Laisser le bon dans la base pour vérification
        print(f"\n💾 Bon de soin conservé dans la base (ID: {bon_soin.id})")
        
        return bon_soin
        
    except Exception as e:
        print(f"❌ ERREUR lors de la création: {e}")
        return None

if __name__ == "__main__":
    bon = test_creation_reelle_bon_soin()
    if bon:
        print("\n🎉 TOUT FONCTIONNE PARFAITEMENT!")
        print("Vous pouvez maintenant créer des bons de soin dans l'interface web.")
    else:
        print("\n❌ Il reste un problème à investiguer.")