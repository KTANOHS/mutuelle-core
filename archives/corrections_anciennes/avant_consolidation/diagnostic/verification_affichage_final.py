# verification_affichage_final.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verification_affichage_final():
    """Vérifier exactement ce qui s'affiche dans la messagerie"""
    
    print("🔍 VÉRIFICATION AFFICHAGE FINAL")
    print("=" * 50)
    
    from django.test import Client
    from django.contrib.auth.models import User
    
    try:
        # Tester avec assureur_test
        user = User.objects.get(username='assureur_test')
        client = Client()
        client.force_login(user)
        
        # Faire une requête
        response = client.get('/communication/')
        content = response.content.decode('utf-8')
        
        print(f"📊 Statut: {response.status_code}")
        
        # Chercher la section des conversations
        if 'conversation-item' in content:
            print("✅ Section conversations trouvée")
            
            # Extraire la partie HTML des conversations
            debut = content.find('conversation-item')
            fin = content.find('</div>', debut) + 1000  # Prendre un extrait
            extrait_conversation = content[debut:fin] if debut != -1 else "Non trouvé"
            
            print(f"\n📄 EXTRAT DE LA CONVERSATION:")
            print(extrait_conversation[:500] + "..." if len(extrait_conversation) > 500 else extrait_conversation)
        
        # Vérifications détaillées
        verifications = {
            'Conversation #4': 'Conversation #4' in content,
            'koffitanoh': 'koffitanoh' in content,
            'assureur_test': 'assureur_test' in content,
            'Messages non lus': 'Messages non lus' in content or 'non lu' in content,
            'Total messages': 'Total messages' in content or 'message(s)' in content,
            'Dernière activité': 'Dernière activité' in content or 'activité' in content,
            'Badge messages': 'badge bg-info' in content or 'badge bg-danger' in content
        }
        
        print(f"\n✅ DÉTAILS AFFICHÉS:")
        for element, present in verifications.items():
            status = "✅" if present else "❌"
            print(f"   {status} {element}: {'PRÉSENT' if present else 'ABSENT'}")
        
        if all(verifications.values()):
            print(f"\n🎉 SUCCÈS COMPLET ! Tous les éléments s'affichent correctement.")
        else:
            print(f"\n⚠️  Certains éléments manquent encore dans l'affichage.")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    verification_affichage_final()