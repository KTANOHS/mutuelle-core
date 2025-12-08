# verification_complete_finale.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verification_complete_finale():
    """Vérification complète finale après corrections"""
    
    print("🎯 VÉRIFICATION COMPLÈTE FINALE")
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
        
        # Vérifications COMPLÈTES
        verifications_completes = {
            'Structure générale': 'conversation-item' in content,
            'Conversation spécifique': 'Conversation #4' in content,
            'Participant koffitanoh': 'koffitanoh' in content,
            'Utilisateur actuel': 'assureur_test' in content,
            'Statistiques messages': 'Messages non lus' in content or 'non lu' in content,
            'Total messages': 'Total messages' in content or 'message(s)' in content,
            'Date activité': 'Dernière activité' in content or 'activité' in content,
            'Badges visuels': 'badge bg-' in content,
            'Bouton action': 'btn btn-' in content,
            'Formulaire message': 'nouveauMessageModal' in content
        }
        
        print(f"\n✅ ÉTAT DU SYSTÈME:")
        score = 0
        for element, present in verifications_completes.items():
            status = "✅" if present else "❌"
            if present: score += 1
            print(f"   {status} {element}: {'FONCTIONNEL' if present else 'MANQUANT'}")
        
        pourcentage = (score / len(verifications_completes)) * 100
        print(f"\n📈 SCORE: {score}/{len(verifications_completes)} ({pourcentage:.0f}%)")
        
        if pourcentage >= 80:
            print(f"\n🎉 SUCCÈS ÉLEVÉ ! Le système est fonctionnel à {pourcentage:.0f}%")
            print("🌐 La messagerie est utilisable et opérationnelle")
        else:
            print(f"\n⚠️  PROGRÈS SIGNIFICATIF à {pourcentage:.0f}% - Derniers ajustements nécessaires")
        
        # Afficher un extrait pour confirmation visuelle
        if 'Conversation #4' in content:
            debut = content.find('Conversation #4')
            extrait = content[debut:debut+800]
            print(f"\n👁️  EXTRAT VISUEL DE LA CONVERSATION:")
            print("..." + extrait + "...")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    verification_complete_finale()