# verifier_affichage_noms.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_affichage_noms():
    """Vérifier que les noms des participants s'affichent dans le HTML"""
    
    print("🔍 VÉRIFICATION DE L'AFFICHAGE DES NOMS")
    print("=" * 50)
    
    from django.test import Client
    from django.contrib.auth.models import User
    
    try:
        # Se connecter en tant que pharmacien
        pharmacien = User.objects.get(username='test_pharmacien')
        client = Client()
        client.force_login(pharmacien)
        
        # Faire une requête
        response = client.get('/communication/')
        content = response.content.decode('utf-8')
        
        print(f"📊 Statut: {response.status_code}")
        
        # Vérifier l'affichage des noms
        noms_a_verifier = ['test_agent', 'test_medecin']
        
        print("\n🔍 RECHERCHE DES NOMS DANS LE HTML:")
        for nom in noms_a_verifier:
            if nom in content:
                print(f"✅ {nom}: TROUVÉ dans le HTML")
                # Afficher le contexte autour du nom
                index = content.find(nom)
                contexte = content[max(0, index-50):min(len(content), index+50)]
                print(f"   Contexte: ...{contexte}...")
            else:
                print(f"❌ {nom}: NON TROUVÉ dans le HTML")
        
        # Vérifier la structure des conversations
        if 'list-group-item' in content:
            print("✅ Structure des conversations trouvée")
        else:
            print("❌ Structure des conversations manquante")
            
        # Vérifier les badges de messages non lus
        if 'badge bg-danger' in content or 'badge bg-primary' in content:
            print("✅ Badges de messages non lus trouvés")
        else:
            print("❌ Badges de messages non lus manquants")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    verifier_affichage_noms()