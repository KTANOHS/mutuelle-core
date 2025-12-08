# correctif_groupe_medecin.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model

User = get_user_model()

print("🚀 CORRECTION GROUPE MÉDECIN")
print("=" * 40)

def corriger_groupe_medecin():
    """Ajoute l'utilisateur test_medecin au groupe Medecin"""
    
    try:
        # 1. Récupérer l'utilisateur
        user = User.objects.get(username='test_medecin')
        print(f"✅ Utilisateur trouvé: {user.username}")
        
        # 2. Récupérer ou créer le groupe Medecin
        groupe_medecin, created = Group.objects.get_or_create(name='Medecin')
        if created:
            print("✅ Groupe 'Medecin' créé")
        else:
            print("✅ Groupe 'Medecin' existe déjà")
        
        # 3. Ajouter l'utilisateur au groupe
        user.groups.add(groupe_medecin)
        user.save()
        
        # 4. Vérifier
        est_dans_groupe = user.groups.filter(name='Medecin').exists()
        print(f"🔍 Vérification groupe: {'✅ DANS LE GROUPE' if est_dans_groupe else '❌ PAS DANS LE GROUPE'}")
        
        # 5. Afficher tous les groupes de l'utilisateur
        groupes = user.groups.all()
        print(f"📋 Groupes de {user.username}: {[g.name for g in groupes]}")
        
        return True
        
    except User.DoesNotExist:
        print("❌ Utilisateur test_medecin non trouvé")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def verifier_et_corriger_vue_dashboard():
    """Vérifie et corrige la vue dashboard si nécessaire"""
    
    print("\n🔧 VÉRIFICATION VUE DASHBOARD:")
    
    # Code de correction pour la vue
    code_correction = '''
# DANS medecin/views.py - REMPLACEZ la condition problématique
if not request.user.groups.filter(name='Medecin').exists():
    # AU LIEU de redirect('home'), utiliser:
    messages.error(request, "Accès réservé aux médecins")
    return redirect('medecin:login')  # Ou une autre page safe
'''
    
    print("💡 Si le problème persiste, modifiez la condition dans dashboard_medecin_robuste:")
    print(code_correction)

def test_apres_correction():
    """Test après correction"""
    
    print("\n🧪 TEST APRÈS CORRECTION:")
    
    from django.test import Client
    client = Client()
    
    # Connexion
    success = client.login(username='test_medecin', password='testpass123')
    print(f"🔐 Connexion: {'✅ RÉUSSIE' if success else '❌ ÉCHOUÉE'}")
    
    if success:
        # Test dashboard
        response = client.get('/medecin/dashboard/', follow=True)
        print(f"📊 Dashboard - Status: {response.status_code}")
        print(f"🔄 Redirections: {len(response.redirect_chain)}")
        
        if response.status_code == 200:
            print("🎉 SUCCÈS! La boucle est résolue!")
        else:
            print("❌ Le problème persiste - vérifiez la vue dashboard")

if __name__ == "__main__":
    # Appliquer la correction
    if corriger_groupe_medecin():
        test_apres_correction()
    else:
        print("❌ Impossible d'appliquer la correction")
    
    verifier_et_corriger_vue_dashboard()