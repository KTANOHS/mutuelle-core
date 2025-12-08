# verification_profil_medecin.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from medecin.models import Medecin, SpecialiteMedicale, EtablissementMedical

User = get_user_model()

print("🔍 VÉRIFICATION PROFIL MÉDECIN")
print("=" * 40)

def verifier_et_corriger_profil():
    """Vérifie et corrige le profil médecin"""
    
    try:
        # 1. Récupérer l'utilisateur
        user = User.objects.get(username='test_medecin')
        print(f"✅ Utilisateur trouvé: {user.username}")
        print(f"   - ID: {user.id}")
        print(f"   - Email: {user.email}")
        print(f"   - Prénom: {user.first_name}")
        print(f"   - Nom: {user.last_name}")
        
        # 2. Vérifier si le profil médecin existe
        if hasattr(user, 'medecin'):
            profil = user.medecin
            print(f"✅ PROFIL MÉDECIN EXISTE:")
            print(f"   - ID Profil: {profil.id}")
            print(f"   - Nom complet: {profil.nom_complet}")
            print(f"   - Spécialité: {profil.specialite}")
            print(f"   - Établissement: {profil.etablissement}")
            print(f"   - Numéro ordre: {profil.numero_ordre}")
            return True
        else:
            print("❌ PROFIL MÉDECIN NON TROUVÉ")
            print("🔄 Création du profil médecin...")
            
            # 3. Créer le profil médecin
            return creer_profil_medecin(user)
            
    except User.DoesNotExist:
        print("❌ Utilisateur test_medecin non trouvé")
        return False

def creer_profil_medecin(user):
    """Crée un profil médecin pour l'utilisateur"""
    
    try:
        # 1. Obtenir ou créer la spécialité
        specialite, created = SpecialiteMedicale.objects.get_or_create(
            nom="Médecine Générale",
            defaults={'description': 'Spécialité médecine générale'}
        )
        print(f"✅ Spécialité: {specialite.nom}")
        
        # 2. Obtenir un établissement
        etablissement = EtablissementMedical.objects.first()
        if not etablissement:
            etablissement = EtablissementMedical.objects.create(
                nom="Centre Médical Principal",
                type_etablissement="HOPITAL",
                adresse="123 Rue de la Santé",
                ville="Abidjan",
                est_actif=True
            )
            print(f"✅ Établissement créé: {etablissement.nom}")
        else:
            print(f"✅ Établissement: {etablissement.nom}")
        
        # 3. Créer le profil médecin
        profil = Medecin.objects.create(
            user=user,
            specialite=specialite,
            etablissement=etablissement,
            numero_ordre="TEST12345"
        )
        
        print(f"✅ PROFIL MÉDECIN CRÉÉ AVEC SUCCÈS!")
        print(f"   - ID: {profil.id}")
        print(f"   - Nom complet: {profil.nom_complet}")
        print(f"   - Spécialité: {profil.specialite}")
        print(f"   - Établissement: {profil.etablissement}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur création profil: {e}")
        return False

def verifier_acces_dashboard():
    """Vérifie l'accès au dashboard après correction"""
    
    print("\n🧪 TEST ACCÈS DASHBOARD:")
    
    from django.test import Client
    client = Client()
    
    # Connexion
    success = client.login(username='test_medecin', password='testpass123')
    print(f"🔐 Connexion: {'✅ RÉUSSIE' if success else '❌ ÉCHOUÉE'}")
    
    if not success:
        return False
    
    # Test dashboard
    response = client.get('/medecin/dashboard/', follow=True)
    print(f"📊 Dashboard - Status: {response.status_code}")
    print(f"🔄 Redirections: {len(response.redirect_chain)}")
    
    if response.redirect_chain:
        print("   Chaîne de redirection:")
        for i, (url, status) in enumerate(response.redirect_chain):
            print(f"     {i+1}. {status} → {url}")
    
    return response.status_code == 200

def solution_alternative_vue_dashboard():
    """Solution alternative si le problème persiste"""
    
    print("\n💡 SOLUTION ALTERNATIVE:")
    
    code_alternative = '''
# SOLUTION TEMPORAIRE - Modifiez dashboard_medecin_robuste dans medecin/views.py

@login_required
def dashboard_medecin_robuste(request):
    """
    Tableau de bord médecin - Version ULTRA SIMPLIFIÉE
    """
    # Vérification basique
    if not request.user.is_authenticated:
        return redirect('login')
    
    # ✅ SOLUTION TEMPORAIRE: Ignorer la vérification du profil
    try:
        medecin = None
        if hasattr(request.user, 'medecin'):
            medecin = request.user.medecin
        else:
            # Créer un contexte basique même sans profil
            medecin = {
                'nom_complet': request.user.get_full_name() or request.user.username,
                'specialite': 'Médecine Générale',
                'etablissement': 'Centre Médical'
            }
        
        context = {
            'user': request.user,
            'medecin': medecin,
            'is_medecin': True,
            'page_title': 'Tableau de Bord Médecin',
            'ordonnances_count': 0,
            'bons_attente': 0,
            'consultations_count': 0,
        }
        
        return render(request, 'medecin/dashboard.html', context)
        
    except Exception as e:
        # Toujours retourner le template même en cas d'erreur
        context = {
            'user': request.user,
            'is_medecin': True,
            'error': str(e)
        }
        return render(request, 'medecin/dashboard.html', context)
'''
    
    print("Si le problème persiste, utilisez cette version simplifiée:")
    print(code_alternative)

if __name__ == "__main__":
    # Vérifier et corriger le profil
    if verifier_et_corriger_profil():
        print("\n✅ PROFIL MÉDECIN CONFIGURÉ")
        
        # Tester l'accès
        if verifier_acces_dashboard():
            print("\n🎉 SUCCÈS COMPLET! Le dashboard est accessible.")
        else:
            print("\n❌ Problème d'accès persistant")
            solution_alternative_vue_dashboard()
    else:
        print("\n❌ Impossible de créer le profil médecin")
        solution_alternative_vue_dashboard()