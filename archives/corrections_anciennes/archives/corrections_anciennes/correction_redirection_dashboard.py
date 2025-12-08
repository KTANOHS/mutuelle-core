# correction_redirection_dashboard.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
import inspect
from medecin import views

print("🔧 CORRECTION REDIRECTION DASHBOARD VERS PROFIL")
print("=" * 60)

def examiner_vue_dashboard_actuelle():
    """Examine le code actuel de la vue dashboard"""
    
    print("1. 🔍 EXAMEN DU CODE DASHBOARD ACTUEL")
    print("-" * 40)
    
    try:
        if hasattr(views, 'dashboard_medecin_robuste'):
            source = inspect.getsource(views.dashboard_medecin_robuste)
            print("📝 Code de dashboard_medecin_robuste:")
            print("=" * 50)
            
            # Afficher les parties problématiques
            lines = source.split('\n')
            for i, line in enumerate(lines):
                if 'redirect' in line or 'profil' in line.lower():
                    print(f"{i+1:3}: {line}")
            
            # Vérifier les redirections
            if 'redirect' in source and 'profil' in source.lower():
                print("\n🚨 PROBLEME: La vue dashboard redirige vers le profil!")
                
        else:
            print("❌ dashboard_medecin_robuste non trouvée")
            
    except Exception as e:
        print(f"❌ Erreur examen: {e}")

def corriger_vue_dashboard():
    """Fournit la vue dashboard corrigée sans redirection"""
    
    print("\n2. 🎯 CODE DASHBOARD CORRIGÉ")
    print("-" * 40)
    
    code_corrige = '''
@login_required
def dashboard_medecin_robuste(request):
    """
    Tableau de bord médecin - VERSION CORRIGÉE SANS REDIRECTION
    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    medecin = None
    warning = None
    
    # RECHERCHE DU PROFIL (sans redirection)
    try:
        # Méthode 1: Relation Django
        if hasattr(request.user, 'medecin'):
            medecin = request.user.medecin
        
        else:
            # Méthode 2: Recherche directe
            try:
                medecin = Medecin.objects.get(user_id=request.user.id)
                warning = "Profil chargé directement depuis la base"
                
            except Medecin.DoesNotExist:
                # Méthode 3: Profil temporaire (PAS DE REDIRECTION)
                class ProfilTemporaire:
                    def __init__(self, user):
                        self.nom_complet = user.get_full_name() or user.username
                        self.specialite = "Médecine Générale"
                        self.etablissement = "Établissement à configurer"
                        self.numero_ordre = "EN_ATTENTE"
                        self.est_actif = True
                        self.id = None
                
                medecin = ProfilTemporaire(request.user)
                warning = "Profil temporaire - Configuration requise"
                
    except Exception as e:
        # Fallback sans redirection
        class ProfilFallback:
            nom_complet = request.user.get_full_name() or "Médecin"
            specialite = "Médecine Générale"
            etablissement = "Centre Médical"
            numero_ordre = "CONFIGURATION"
            est_actif = True
            id = None
        
        medecin = ProfilFallback()
        warning = f"Mode dégradé: {str(e)}"
    
    # STATISTIQUES
    try:
        ordonnances_count = Ordonnance.objects.filter(medecin_id=request.user.id).count()
    except:
        ordonnances_count = 0
        
    try:
        bons_attente = BonDeSoin.objects.filter(statut='EN_ATTENTE').count()
    except:
        bons_attente = 0
        
    try:
        consultations_count = Consultation.objects.filter(medecin__user_id=request.user.id).count()
    except:
        consultations_count = 0
    
    # CONTEXTE ET RENDER (IMPORTANT: pas de redirect!)
    context = {
        'user': request.user,
        'medecin': medecin,
        'is_medecin': True,
        'page_title': 'Tableau de Bord Médecin',
        'ordonnances_count': ordonnances_count,
        'bons_attente': bons_attente,
        'consultations_count': consultations_count,
        'warning': warning,
    }
    
    # TOUJOURS utiliser render() pour le dashboard
    return render(request, 'medecin/dashboard.html', context)
'''
    
    print("Remplacez la fonction dashboard_medecin_robuste par ce code:")
    print(code_corrige)

def verifier_redirection_middleware():
    """Vérifie si un middleware cause la redirection"""
    
    print("\n3. 🔍 VÉRIFICATION MIDDLEWARE")
    print("-" * 40)
    
    from django.conf import settings
    
    print("Middleware actif:")
    for middleware in settings.MIDDLEWARE:
        if 'redirect' in middleware.lower() or 'auth' in middleware.lower():
            print(f"   - {middleware}")

def test_redirection_specifique():
    """Test spécifique de la redirection"""
    
    print("\n4. 🧪 TEST REDIRECTION SPÉCIFIQUE")
    print("-" * 40)
    
    client = Client()
    client.login(username='test_medecin', password='testpass123')
    
    # Test avec follow=False pour voir la première redirection
    response = client.get('/medecin/dashboard/', follow=False)
    print(f"Dashboard sans follow: Status {response.status_code}")
    
    if response.status_code == 302:
        print(f"Redirection vers: {response.url}")
        
        # Vérifier l'URL de redirection
        if 'profil' in response.url:
            print("🚨 CONFIRMÉ: Dashboard redirige vers profil!")
        else:
            print(f"Redirection vers: {response.url}")

def solution_contournement_immediate():
    """Solution de contournement immédiate"""
    
    print("\n5. 🚀 SOLUTION DE CONTOURNEMENT IMMÉDIATE")
    print("-" * 40)
    
    solution = '''
# SOLUTION TEMPORAIRE - Créer une vue dashboard alternative

@login_required
def dashboard_fixe(request):
    """Dashboard fixe sans redirection"""
    # Charger le profil directement
    try:
        medecin = Medecin.objects.get(user_id=request.user.id)
    except Medecin.DoesNotExist:
        medecin = None
    
    context = {
        'user': request.user,
        'medecin': medecin,
        'is_medecin': True,
        'page_title': 'Tableau de Bord',
    }
    
    return render(request, 'medecin/dashboard.html', context)

# Dans urls.py, utiliser cette vue temporairement:
# path('dashboard/', views.dashboard_fixe, name='dashboard'),
'''
    
    print("Pour une solution immédiate, créez cette vue temporaire:")
    print(solution)

if __name__ == "__main__":
    examiner_vue_dashboard_actuelle()
    corriger_vue_dashboard()
    verifier_redirection_middleware()
    test_redirection_specifique()
    solution_contournement_immediate()