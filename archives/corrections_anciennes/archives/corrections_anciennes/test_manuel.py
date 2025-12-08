import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_est_valide():
    """Test manuel de est_valide"""
    from medecin.models import Ordonnance
    from django.utils import timezone
    
    print("🧪 TEST MANUEL - est_valide")
    print("=" * 50)
    
    ordonnance = Ordonnance.objects.first()
    if ordonnance:
        print(f"Ordonnance ID: {ordonnance.id}")
        print(f"Date prescription: {ordonnance.date_prescription}")
        print(f"Type date_prescription: {type(ordonnance.date_prescription)}")
        print(f"Est valide: {ordonnance.est_valide}")
        print(f"Type est_valide: {type(ordonnance.est_valide)}")
        print(f"Date maintenant: {timezone.now().date()}")
    else:
        print("❌ Aucune ordonnance trouvée")

def test_nom_complet():
    """Test manuel de nom_complet"""
    from membres.models import Membre
    
    print("\n🧪 TEST MANUEL - nom_complet")
    print("=" * 50)
    
    membre = Membre.objects.first()
    if membre:
        print(f"Membre ID: {membre.id}")
        print(f"User: {membre.user}")
        print(f"First name: '{membre.user.first_name}'")
        print(f"Last name: '{membre.user.last_name}'")
        print(f"Nom complet: '{membre.nom_complet}'")
    else:
        print("❌ Aucun membre trouvé")

def test_vue_ordonnances():
    """Test manuel de la vue mes_ordonnances"""
    from django.test import RequestFactory
    from membres.views import mes_ordonnances
    from django.contrib.auth.models import User
    
    print("\n🧪 TEST MANUEL - Vue mes_ordonnances")
    print("=" * 50)
    
    factory = RequestFactory()
    request = factory.get('/membres/mes_ordonnances/')
    
    # Trouver un utilisateur membre
    membre_user = User.objects.filter(groups__name='Membres').first()
    if membre_user:
        request.user = membre_user
        print(f"Utilisateur test: {membre_user}")
        
        response = mes_ordonnances(request)
        print(f"Status code: {response.status_code}")
        
        ordonnances = response.context_data.get('ordonnances', [])
        print(f"Ordonnances dans contexte: {len(ordonnances)}")
        
        for ord in ordonnances:
            print(f"  - Ordonnance {ord.id}: {ord.diagnostic}")
    else:
        print("❌ Aucun utilisateur membre trouvé")

if __name__ == "__main__":
    test_est_valide()
    test_nom_complet() 
    test_vue_ordonnances()
    print("\n🎉 TESTS MANUELS TERMINÉS")
