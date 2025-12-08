"""
TEST SIMPLE DU FORMULAIRE PAIEMENT
python manage.py shell < test_formulaire_paiement.py
"""

from django.contrib.auth.models import User
from assureur.forms import PaiementForm
from agents.models import Membre
from django.utils import timezone

print("🔧 TEST DU FORMULAIRE PAIEMENT")
print("=" * 40)

try:
    # 1. Récupérer un utilisateur
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.first()
    print(f"Utilisateur: {user.username}")
    
    # 2. Récupérer un membre
    membre = Membre.objects.filter(statut='actif').first()
    if not membre:
        print("❌ Aucun membre actif trouvé")
    else:
        print(f"Membre: {membre.nom} {membre.prenom}")
        
        # 3. Tester le formulaire avec des données simples
        data = {
            'membre': membre.id,
            'montant': '10000.00',
            'mode_paiement': 'espece',
            'date_paiement': timezone.now().date(),
            'statut': 'initie',
            'reference': 'PAY-TEST-FORM',
            'notes': 'Test formulaire'
        }
        
        form = PaiementForm(data=data)
        
        if form.is_valid():
            print("✅ Formulaire valide !")
            
            # Sauvegarder le paiement
            paiement = form.save(commit=False)
            paiement.created_by = user
            
            # Si le statut est 'valide', définir les infos de validation
            if paiement.statut == 'valide':
                paiement.valide_par = user
                paiement.date_validation = timezone.now()
            
            paiement.save()
            
            print(f"\n✅ Paiement créé avec succès:")
            print(f"   Référence: {paiement.reference}")
            print(f"   Montant: {paiement.montant} FCFA")
            print(f"   Statut: {paiement.statut}")
            print(f"   Créé par: {paiement.created_by}")
            
        else:
            print("❌ Formulaire invalide")
            print(f"   Erreurs: {form.errors}")
    
except Exception as e:
    print(f"\n❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Test terminé")