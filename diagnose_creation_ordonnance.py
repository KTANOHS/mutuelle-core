# diagnose_creation_ordonnance.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from medecin.models import Ordonnance
import json

def diagnose_creation():
    print("🔍 DIAGNOSTIC CRÉATION ORDONNANCE")
    print("=" * 50)
    
    client = Client()
    user = User.objects.get(username='test_medecin')
    client.force_login(user)
    
    from membres.models import Membre
    patient = Membre.objects.first()
    
    # Test 1: Données minimales
    print("\n🧪 TEST 1 - Données minimales")
    data_minimal = {
        'patient': patient.id,
        'type_ordonnance': 'STANDARD',
        'diagnostic': 'Test diagnostic minimal',
    }
    
    response = client.post(reverse('medecin:creer_ordonnance'), data_minimal)
    print(f"   Statut: {response.status_code}")
    
    if response.status_code == 302:
        print("   ✅ SUCCÈS avec données minimales")
        # Nettoyer
        Ordonnance.objects.filter(medecin=user, diagnostic='Test diagnostic minimal').delete()
    else:
        print("   ❌ ÉCHEC avec données minimales")
        if hasattr(response, 'context') and 'form' in response.context:
            form = response.context['form']
            if form.errors:
                print(f"   Erreurs formulaire: {form.errors}")
    
    # Test 2: Données complètes
    print("\n🧪 TEST 2 - Données complètes")
    data_complet = {
        'patient': patient.id,
        'type_ordonnance': 'STANDARD',
        'diagnostic': 'Test diagnostic complet',
        'medicaments': json.dumps([
            {'nom': 'Test Médicament', 'posologie': '1 comprimé', 'duree': '5 jours'}
        ]),
        'duree_traitement': 5,
        'renouvelable': 'on',
        'nombre_renouvellements': 1,
    }
    
    response = client.post(reverse('medecin:creer_ordonnance'), data_complet)
    print(f"   Statut: {response.status_code}")
    
    if response.status_code == 302:
        print("   ✅ SUCCÈS avec données complètes")
        # Nettoyer
        Ordonnance.objects.filter(medecin=user, diagnostic='Test diagnostic complet').delete()
    else:
        print("   ❌ ÉCHEC avec données complètes")
        if hasattr(response, 'context') and 'form' in response.context:
            form = response.context['form']
            if form.errors:
                print(f"   Erreurs formulaire: {form.errors}")
    
    # Test 3: Format médicaments array
    print("\n🧪 TEST 3 - Format array médicaments")
    data_array = {
        'patient': patient.id,
        'type_ordonnance': 'STANDARD',
        'diagnostic': 'Test format array',
        'medicaments[]': ['Médicament A', 'Médicament B'],
        'posologie[]': ['1 comprimé', '2 comprimés'],
        'duree_traitement[]': ['5 jours', '7 jours'],
    }
    
    response = client.post(reverse('medecin:creer_ordonnance'), data_array)
    print(f"   Statut: {response.status_code}")
    
    if response.status_code == 302:
        print("   ✅ SUCCÈS avec format array")
        # Nettoyer
        Ordonnance.objects.filter(medecin=user, diagnostic='Test format array').delete()
    else:
        print("   ❌ ÉCHEC avec format array")
        if hasattr(response, 'context') and 'form' in response.context:
            form = response.context['form']
            if form.errors:
                print(f"   Erreurs formulaire: {form.errors}")
    
    # Test 4: Vérification nombre d'ordonnances
    print(f"\n📊 Ordonnances en base: {Ordonnance.objects.filter(medecin=user).count()}")

if __name__ == "__main__":
    diagnose_creation()