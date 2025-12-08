# debug_creation_ordonnance.py
import os
import django
import sys

# Configuration Django
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')  # Remplacez par le vrai nom
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth.models import User
from medecin.models import Medecin, Patient, Medicament, Ordonnance
from medecin.forms import OrdonnanceForm
from django.contrib.messages import get_messages

def debug_creation():
    print("🐛 DEBUG CRÉATION ORDONNANCE")
    print("================================================")
    
    # Utiliser Client pour une meilleure simulation
    client = Client()
    
    # Créer ou récupérer un utilisateur médecin
    try:
        user = User.objects.get(username='test_medecin')
    except User.DoesNotExist:
        user = User.objects.create_user('test_medecin', 'test@example.com', 'password')
        user.save()
    
    # Créer un profil médecin si nécessaire
    try:
        medecin = user.medecin
    except:
        medecin = Medecin.objects.create(
            user=user,
            nom="Test",
            prenom="Docteur",
            specialite="Generaliste"
        )
    
    # Créer un patient de test
    patient = Patient.objects.create(
        nom="Patient",
        prenom="Test",
        date_naissance="1990-01-01",
        numero_securite_sociale="1234567890123"
    )
    
    # Créer un médicament de test
    medicament = Medicament.objects.create(
        nom="Paracetamol",
        dci="Paracetamol",
        forme_galenique="Comprimé",
        dosage="500mg"
    )
    
    # Se connecter
    client.force_login(user)
    
    print("📋 Données de test créées:")
    print(f"   - Médecin: {medecin}")
    print(f"   - Patient: {patient}")
    print(f"   - Médicament: {medicament}")
    
    # Test GET d'abord
    print("\n🔍 Test GET de la page...")
    response_get = client.get('/medecin/ordonnances/nouvelle/')
    print(f"   Statut: {response_get.status_code}")
    
    if response_get.status_code == 200:
        print("✅ Page accessible")
        
        # Vérifier le contexte
        if 'form' in response_get.context:
            form = response_get.context['form']
            print(f"✅ Formulaire dans le contexte: {type(form)}")
            print(f"   Champs du formulaire: {list(form.fields.keys())}")
        else:
            print("❌ Formulaire manquant dans le contexte")
    
    # Test POST avec données complètes
    print("\n📤 Test POST avec données complètes...")
    
    data = {
        'patient': patient.id,
        'notes': 'Ordonnance de test',
        'medicaments-TOTAL_FORMS': '1',
        'medicaments-INITIAL_FORMS': '0',
        'medicaments-MIN_NUM_FORMS': '0',
        'medicaments-MAX_NUM_FORMS': '1000',
        'medicaments-0-medicament': medicament.id,
        'medicaments-0-posologie': '1 comprimé 3 fois par jour',
        'medicaments-0-duree_traitement': 7,
        'medicaments-0-quantite_prescrite': 21
    }
    
    response_post = client.post('/medecin/ordonnances/nouvelle/', data)
    print(f"   Statut POST: {response_post.status_code}")
    
    # Analyser la réponse
    if response_post.status_code == 302:
        print("✅ SUCCÈS ! Redirection détectée")
        print(f"   URL de redirection: {response_post.url}")
        
        # Vérifier si l'ordonnance a été créée
        ordonnances = Ordonnance.objects.filter(patient=patient)
        print(f"   Ordonnances créées: {ordonnances.count()}")
        
        if ordonnances.exists():
            ordonnance = ordonnances.first()
            print(f"   ✅ Ordonnance créée avec ID: {ordonnance.id}")
            print(f"   📝 Notes: {ordonnance.notes}")
            print(f"   💊 Lignes: {ordonnance.lignes.count()}")
        else:
            print("❌ Aucune ordonnance créée en base")
            
    else:
        print("❌ Échec - Pas de redirection")
        
        # Afficher les erreurs du formulaire
        if 'form' in response_post.context:
            form = response_post.context['form']
            if form.errors:
                print("❌ Erreurs de validation:")
                for field, errors in form.errors.items():
                    print(f"   - {field}: {errors}")
        
        # Afficher les messages
        messages = list(get_messages(response_post.wsgi_request))
        if messages:
            print("📢 Messages:")
            for message in messages:
                print(f"   - {message}")

if __name__ == "__main__":
    debug_creation()