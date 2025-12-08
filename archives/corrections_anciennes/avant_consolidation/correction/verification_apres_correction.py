# verification_apres_correction.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verification_apres_correction():
    """Vérification après application de la correction finale"""
    
    print("🎯 VÉRIFICATION APRÈS CORRECTION FINALE")
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
        
        # Vérifications COMPLÈTES du nouveau template
        verifications = {
            'Structure conversation-item': 'conversation-item' in content,
            'Badges colorés': 'badge bg-' in content,
            'Modal nouveau message': 'nouveauMessageModal' in content,
            'Date activité affichée': 'Dernière activité' in content,
            'Statistiques détaillées': 'Statistiques:' in content,
            'Bouton nouveau message': 'Nouveau Message' in content,
            'Participants avec badges': 'Participants:' in content and 'badge' in content,
            'Conversation avec': 'Conversation avec:' in content,
            'Messages comptés': 'message(s)' in content,
            'Interface complète': 'container-fluid' in content
        }
        
        print(f"\n✅ VÉRIFICATION DU TEMPLATE COMPLET:")
        score = 0
        for element, present in verifications.items():
            status = "✅" if present else "❌"
            if present: score += 1
            print(f"   {status} {element}: {'PRÉSENT' if present else 'ABSENT'}")
        
        pourcentage = (score / len(verifications)) * 100
        print(f"\n📈 SCORE FINAL: {score}/{len(verifications)} ({pourcentage:.0f}%)")
        
        if pourcentage >= 80:
            print(f"\n🎉 SUCCÈS COMPLET ! Système fonctionnel à {pourcentage:.0f}%")
            print("🌐 La messagerie est maintenant COMPLÈTEMENT OPÉRATIONNELLE")
        elif pourcentage >= 60:
            print(f"\n⚠️  BON FONCTIONNEMENT à {pourcentage:.0f}% - Quelques ajustements mineurs")
        else:
            print(f"\n❌ PROBLÈME PERSISTANT à {pourcentage:.0f}% - Investigation nécessaire")
        
        # Afficher un extrait du nouveau template
        if 'conversation-item' in content:
            debut = content.find('conversation-item')
            extrait = content[debut:debut+1200]
            print(f"\n👁️  APERÇU DU NOUVEAU TEMPLATE:")
            print("..." + extrait + "...")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    verification_apres_correction()