# verification_structure_corrigee.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_structure_corrigee():
    """Vérifier que la structure corrigée fonctionne"""
    
    print("🔍 VÉRIFICATION DE LA STRUCTURE CORRIGÉE")
    print("=" * 50)
    
    from django.test import Client
    from django.contrib.auth.models import User
    
    try:
        # Se connecter
        pharmacien = User.objects.get(username='test_pharmacien')
        client = Client()
        client.force_login(pharmacien)
        
        # Faire une requête
        response = client.get('/communication/')
        content = response.content.decode('utf-8')
        
        print(f"📊 Statut: {response.status_code}")
        
        # Vérifications CRITIQUES
        checks = {
            'Template Corrigé - Mode Debug': 'Template Corrigé' in content,
            'Conversations dans base': 'conversation(s) trouvée(s)' in content,
            'test_agent visible': 'test_agent' in content,
            'test_medecin visible': 'test_medecin' in content,
            'Conversation #7': 'Conversation #7' in content,
            'Conversation #6': 'Conversation #6' in content,
            'Statistiques affichées': 'Statistiques:' in content,
            'Bouton Nouveau Message': 'Nouveau Message' in content
        }
        
        print("\n✅ VÉRIFICATIONS CRITIQUES:")
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"   {status} {check}: {'TROUVÉ' if result else 'NON TROUVÉ'}")
        
        # Compter les occurrences
        count_agent = content.count('test_agent')
        count_medecin = content.count('test_medecin')
        count_conversations = content.count('Conversation #')
        
        print(f"\n🔢 COMPTAGE DES OCCURRENCES:")
        print(f"   - test_agent: {count_agent}")
        print(f"   - test_medecin: {count_medecin}") 
        print(f"   - Conversation #: {count_conversations}")
        
        if count_agent > 0 and count_medecin > 0 and count_conversations >= 2:
            print("\n🎉 SUCCÈS TOTAL ! La structure est corrigée et les données s'affichent.")
            print("🌐 Ouvrez: http://127.0.0.1:8000/communication/")
        else:
            print("\n❌ PROBLEME - Les données ne s'affichent pas correctement.")
            
            # Afficher un extrait pour debug
            if 'Conversation #' in content:
                index = content.find('Conversation #')
                extrait = content[index:index+1000]
                print(f"\n📄 EXTRAT DU CONTENU:")
                print(extrait)
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verifier_structure_corrigee()