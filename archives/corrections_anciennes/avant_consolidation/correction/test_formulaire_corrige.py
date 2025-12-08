import os
import django
import sys
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate
from soins.models import BonDeSoin
from membres.models import Membre
import json

def test_formulaire_complet():
    """Test complet du formulaire de création"""
    print("🧪 TEST FORMULAIRE COMPLET")
    print("===========================")
    
    client = Client()
    user = authenticate(username='koffitanoh', password='nouveau_mot_de_passe')
    
    if not user:
        print("❌ Authentification échouée")
        return False
    
    client.force_login(user)
    print("✅ Authentification réussie")
    
    # 1. Accéder à la page de création pour obtenir le CSRF token
    print("\n1. 🔄 OBTENTION CSRF TOKEN")
    response = client.get('/agents/creer-bon-soin/')
    
    if response.status_code != 200:
        print(f"❌ Impossible d'accéder à la page: {response.status_code}")
        return False
    
    # Extraire le CSRF token du cookie
    csrf_token = client.cookies.get('csrftoken')
    if csrf_token:
        print(f"✅ CSRF token obtenu")
    else:
        print("⚠️  CSRF token non trouvé")
    
    # 2. Préparer les données du formulaire
    print("\n2. 📝 PRÉPARATION DONNÉES")
    membre = Membre.objects.first()
    
    data = {
        'patient': membre.id,
        'date_soin': datetime.now().strftime('%Y-%m-%d'),
        'symptomes': 'Douleurs thoraciques et essoufflement',
        'diagnostic': 'Suspicion de problèmes cardiaques',
        'statut': 'EN_ATTENTE',
        'montant': '25000.00',
    }
    
    print(f"   Données: {data}")
    
    # 3. Soumettre le formulaire
    print("\n3. 📤 SOUMISSION FORMULAIRE")
    
    # Utiliser le format multipart/form-data comme un vrai navigateur
    response = client.post(
        '/agents/creer-bon-soin/',
        data=data,
        HTTP_X_REQUESTED_WITH='XMLHttpRequest' if csrf_token else None,
        follow=True  # Suivre les redirections
    )
    
    print(f"   Statut: {response.status_code}")
    
    # 4. Analyser la réponse
    if response.status_code == 200:
        print("   ✅ Formulaire traité")
        
        # Vérifier si la création a réussi
        nouveau_total = BonDeSoin.objects.count()
        print(f"   📊 Bons après soumission: {nouveau_total}")
        
        # Vérifier le contenu de la réponse
        content = response.content.decode('utf-8')
        if 'succès' in content.lower() or 'success' in content.lower():
            print("   🎉 Message de succès détecté")
        if 'erreur' in content.lower() or 'error' in content.lower():
            print("   ❌ Erreur détectée dans la réponse")
            
    elif response.status_code == 302:
        print("   🔄 Redirection détectée")
        if response.url:
            print(f"   Vers: {response.url}")
            
        # Vérifier si un bon a été créé malgré la redirection
        nouveau_total = BonDeSoin.objects.count()
        print(f"   📊 Bons après redirection: {nouveau_total}")
        
    else:
        print(f"   ❌ Statut inattendu: {response.status_code}")
    
    # 5. Vérification finale
    print("\n4. 📋 VÉRIFICATION FINALE")
    bons_apres_test = BonDeSoin.objects.count()
    print(f"   📈 Total bons de soin: {bons_apres_test}")
    
    # Vérifier le dernier bon créé
    dernier_bon = BonDeSoin.objects.last()
    if dernier_bon:
        print(f"   🆕 Dernier bon créé:")
        print(f"      ID: {dernier_bon.id}")
        print(f"      Patient: {dernier_bon.patient.nom_complet}")
        print(f"      Date: {dernier_bon.date_soin}")
        print(f"      Statut: {dernier_bon.statut}")
    
    return True

if __name__ == "__main__":
    success = test_formulaire_complet()
    
    if success:
        print("\n🎉 TEST FORMULAIRE TERMINÉ!")
    else:
        print("\n⚠️  TEST FORMULAIRE ÉCHOUÉ")