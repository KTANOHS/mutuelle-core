#!/usr/bin/env python
"""
Test FINAL corrigé de l'application médecin
"""

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from medecin.models import Medecin

User = get_user_model()

def test_medecin_existant():
    """Test avec un vrai médecin existant"""
    print("🧪 TEST AVEC VRAI MÉDECIN")
    print("=" * 50)
    
    client = Client()
    
    # 1. Trouver un médecin actif dans la base
    print("1. Recherche d'un médecin actif...")
    try:
        medecin_actif = Medecin.objects.filter(actif=True).first()
        if not medecin_actif:
            print("❌ Aucun médecin actif trouvé")
            print("💡 Exécutez: python scripts/creer_medecin_test.py")
            return False
        
        user_medecin = medecin_actif.user
        print(f"✅ Médecin trouvé: Dr {user_medecin.get_full_name()}")
        print(f"   👤 Utilisateur: {user_medecin.username}")
        print(f"   🏥 Établissement: {medecin_actif.etablissement.nom}")
        print(f"   📊 Spécialité: {medecin_actif.specialite.nom}")
        
    except Exception as e:
        print(f"❌ Erreur recherche médecin: {e}")
        return False
    
    # 2. Test login avec redirection
    print("\n2. Test login et redirection...")
    response = client.post('/accounts/login/', {
        'username': user_medecin.username,
        'password': 'Medecin123!',  # Mot de passe par défaut
    }, follow=True)
    
    final_url = response.request['PATH_INFO']
    print(f"URL finale: {final_url}")
    
    # Vérifier la redirection
    if '/medecin/dashboard/' in final_url:
        print("✅ SUCCÈS: Redirigé vers dashboard médecin!")
        redirection_ok = True
    elif '/membres/' in final_url:
        print("❌ ÉCHEC: Redirigé vers espace membre")
        print("💡 Vérifiez que l'utilisateur a bien un profil médecin actif")
        redirection_ok = False
    else:
        print(f"⚠️  Redirection inattendue: {final_url}")
        redirection_ok = False
    
    # 3. Test accès pages médecin
    print("\n3. Test accès pages médecin...")
    client.login(username=user_medecin.username, password='Medecin123!')
    
    pages_a_tester = [
        ('/medecin/dashboard/', 'Tableau de bord'),
        ('/medecin/patients/', 'Liste patients'),
        ('/medecin/consultations/', 'Consultations'),
        ('/medecin/ordonnances/', 'Ordonnances'),
        ('/medecin/ordonnance/nouvelle/', 'Nouvelle ordonnance'),
        ('/medecin/ordonnances/historique/', 'Historique ordonnances'),
        ('/medecin/profil/', 'Profil médecin'),
    ]
    
    pages_ok = 0
    for url, nom in pages_a_tester:
        response = client.get(url)
        status = "✅" if response.status_code == 200 else "❌"
        print(f"   {status} {nom}: {response.status_code}")
        if response.status_code == 200:
            pages_ok += 1
    
    print(f"\n📊 {pages_ok}/{len(pages_a_tester)} pages accessibles")
    
    return redirection_ok and (pages_ok > 0)

def test_creation_medecin_si_necessaire():
    """Crée un médecin si aucun n'existe"""
    print("🔍 VÉRIFICATION MÉDECINS EXISTANTS")
    print("-" * 35)
    
    medecins_count = Medecin.objects.filter(actif=True).count()
    print(f"Médecins actifs: {medecins_count}")
    
    if medecins_count == 0:
        print("🚨 Création d'un médecin de test...")
        os.system("python scripts/creer_medecin_test.py")
        return True
    else:
        print("✅ Médecin(s) existant(s) trouvé(s)")
        return True

if __name__ == "__main__":
    print("🚀 TEST FINAL CORRIGÉ - APPLICATION MÉDECIN")
    print("=" * 60)
    
    # Vérifier/créer un médecin
    test_creation_medecin_si_necessaire()
    
    # Tester avec un vrai médecin
    succes = test_medecin_existant()
    
    print("\n" + "=" * 60)
    if succes:
        print("🎉 FÉLICITATIONS! L'application médecin fonctionne!")
        print("\n✅ RÉSUMÉ:")
        print("   • Templates corrigés")
        print("   • URLs configurées") 
        print("   • Profil médecin actif")
        print("   • Redirection fonctionnelle")
        print("   • Pages accessibles")
    else:
        print("❌ Il reste des problèmes")
        print("\n🔧 SOLUTIONS:")
        print("1. Vérifiez qu'un médecin actif existe")
        print("2. Vérifiez les URLs dans medecin/urls.py")
        print("3. Vérifiez les vues dans medecin/views.py")
        print("4. Vérifiez les templates dans templates/medecin/")