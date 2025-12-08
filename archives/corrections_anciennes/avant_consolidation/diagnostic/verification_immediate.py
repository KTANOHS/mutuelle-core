# verification_immediate.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verification_immediate():
    """Vérification immédiate après correction du template"""
    
    print("🔍 VÉRIFICATION IMMÉDIATE APRÈS CORRECTION")
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
        
        # Vérifications CRITIQUES du nouveau template
        verifications_critiques = {
            'Template complet chargé': 'container-fluid' in content,
            'Structure conversation-item': 'conversation-item' in content,
            'Badges Bootstrap': 'badge bg-' in content,
            'Modal nouveau message': 'nouveauMessageModal' in content,
            'Date activité': 'Dernière activité' in content,
            'Statistiques section': 'Statistiques:' in content,
            'Bouton action présent': 'btn btn-primary' in content,
            'En-tête messagerie': 'Messagerie' in content and 'fa-comments' in content
        }
        
        print(f"\n✅ ÉLÉMENTS CRITIQUES:")
        score = 0
        for element, present in verifications_critiques.items():
            status = "✅" if present else "❌"
            if present: score += 1
            print(f"   {status} {element}: {'PRÉSENT' if present else 'ABSENT'}")
        
        pourcentage = (score / len(verifications_critiques)) * 100
        print(f"\n📈 SCORE: {score}/{len(verifications_critiques)} ({pourcentage:.0f}%)")
        
        if pourcentage >= 80:
            print(f"\n🎉 SUCCÈS COMPLET ! Template appliqué avec succès")
            print("🌐 La messagerie a maintenant une interface professionnelle")
        else:
            print(f"\n⚠️  Problème d'application du template")
        
        # Afficher un extrait pour confirmation
        if 'conversation-item' in content:
            debut = content.find('conversation-item')
            extrait = content[debut:debut+1500]
            print(f"\n👁️  APERÇU DU NOUVEAU TEMPLATE:")
            print("..." + extrait + "...")
        else:
            print(f"\n❌ Le template complet n'a pas été appliqué correctement")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    verification_immediate()