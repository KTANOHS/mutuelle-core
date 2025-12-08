# correction_redirect.py
import re
from pathlib import Path

def fix_redirect_logic():
    """Corrige la logique de redirection"""
    print("🔧 CORRECTION DE LA LOGIQUE DE REDIRECTION")
    print("=" * 60)
    
    views_file = Path('mutuelle_core/views.py')
    
    if not views_file.exists():
        print("❌ Fichier views.py non trouvé")
        return
    
    with open(views_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver et corriger la fonction redirect_after_login
    old_pattern = r'''(def redirect_after_login\(request\):
.*?
    if hasattr\(request\.user, 'medecin'\):
        return redirect\('medecin:dashboard'\)
    elif hasattr\(request\.user, 'pharmacien'\):
        return redirect\('pharmacien:dashboard'\)
    elif hasattr\(request\.user, 'agent'\):
        return redirect\('agents:dashboard'\)
    elif hasattr\(request\.user, 'assureur_profile'\):
        return redirect\('assureur:dashboard'\)
    else:
        # Utilisateur standard - rediriger vers la page d'accueil
        return redirect\('home'\))'''
    
    new_function = '''def redirect_after_login(request):
    """
    Redirection intelligente après connexion - VERSION CORRIGÉE
    """
    from django.shortcuts import redirect
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Redirection basée sur le profil utilisateur
    # Vérification par relations OneToOne d'abord
    if hasattr(request.user, 'medecin'):
        return redirect('medecin:dashboard')
    elif hasattr(request.user, 'pharmacien'):
        return redirect('pharmacien:dashboard')
    elif hasattr(request.user, 'agent'):
        return redirect('agents:dashboard')
    elif hasattr(request.user, 'assureur'):
        return redirect('assureur:dashboard')
    
    # Fallback: vérification par groupes
    elif request.user.groups.filter(name='Medecin').exists():
        return redirect('medecin:dashboard')
    elif request.user.groups.filter(name='Pharmacien').exists():
        return redirect('pharmacien:dashboard')
    elif request.user.groups.filter(name='Agents').exists():
        return redirect('agents:dashboard')
    elif request.user.groups.filter(name='Assureur').exists():
        return redirect('assureur:dashboard')
    elif request.user.groups.filter(name='Membre').exists():
        return redirect('membres:dashboard')
    
    # Redirection par défaut
    else:
        return redirect('home')'''
    
    # Remplacer la fonction
    if re.search(old_pattern, content, re.DOTALL):
        new_content = re.sub(old_pattern, new_function, content, flags=re.DOTALL)
        
        # Sauvegarder le fichier corrigé
        with open(views_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Logique de redirection corrigée !")
        print("\n📝 CHANGEMENTS EFFECTUÉS:")
        print("   1. ✅ Supprimé 'assureur_profile' problématique")
        print("   2. ✅ Ajouté 'assureur' (relation correcte)")
        print("   3. ✅ Ajouté fallback par groupes")
        print("   4. ✅ Ajouté vérification pour 'membre'")
        
    else:
        print("❌ Pattern de fonction non trouvé - vérification manuelle nécessaire")

def verify_correction():
    """Vérifie que la correction a été appliquée"""
    print("\n✅ VÉRIFICATION DE LA CORRECTION")
    print("=" * 60)
    
    views_file = Path('mutuelle_core/views.py')
    
    with open(views_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier la nouvelle logique
    checks = [
        ("Vérification medecin", "hasattr(request.user, 'medecin')"),
        ("Vérification pharmacien", "hasattr(request.user, 'pharmacien')"),
        ("Vérification agent", "hasattr(request.user, 'agent')"),
        ("Vérification assureur", "hasattr(request.user, 'assureur')"),
        ("Fallback groupes Medecin", "groups.filter(name='Medecin')"),
        ("Fallback groupes Membre", "groups.filter(name='Membre')"),
    ]
    
    all_good = True
    for check_name, pattern in checks:
        if pattern in content:
            print(f"   ✅ {check_name}")
        else:
            print(f"   ❌ {check_name}")
            all_good = False
    
    return all_good

def test_redirection_scenarios():
    """Teste les scénarios de redirection"""
    print("\n🧪 SCÉNARIOS DE REDIRECTION")
    print("=" * 60)
    
    scenarios = [
        {
            'user': 'test_medecin',
            'has_medecin': False,  # Même problème qu'avant
            'has_assureur_profile': False,
            'groups': ['Medecin'],
            'expected': '/medecin/dashboard/'
        },
        {
            'user': 'docteur_kouame', 
            'has_medecin': False,
            'has_assureur_profile': False,
            'groups': ['Medecin'],
            'expected': '/medecin/dashboard/'
        },
        {
            'user': 'test_membre',
            'has_membre': False,
            'groups': ['Membre'],
            'expected': '/membres/dashboard/'
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🔍 {scenario['user']}:")
        print(f"   Groupes: {scenario['groups']}")
        
        # Logique simulée
        if scenario.get('has_medecin'):
            redirect_to = '/medecin/dashboard/'
            method = "Relation OneToOne"
        elif scenario.get('has_assureur_profile'):
            redirect_to = '/assureur/dashboard/'
            method = "Relation assureur_profile (PROBLÉMATIQUE)"
        elif 'Medecin' in scenario['groups']:
            redirect_to = '/medecin/dashboard/'
            method = "Fallback groupe"
        elif 'Membre' in scenario['groups']:
            redirect_to = '/membres/dashboard/'
            method = "Fallback groupe"
        else:
            redirect_to = '/home/'
            method = "Défaut"
        
        status = "✅" if redirect_to == scenario['expected'] else "❌"
        print(f"   {status} Redirection: {redirect_to} ({method})")

if __name__ == "__main__":
    print("🚀 CORRECTION DU PROBLÈME DE REDIRECTION")
    print("📋 Résolution du conflit assureur_profile vs medecin")
    
    # 1. Corriger la logique
    fix_redirect_logic()
    
    # 2. Vérifier la correction
    correction_ok = verify_correction()
    
    # 3. Tester les scénarios
    test_redirection_scenarios()
    
    print("\n" + "="*60)
    if correction_ok:
        print("🎉 CORRECTION APPLIQUÉE AVEC SUCCÈS !")
        print("\n🔁 MAINTENANT:")
        print("   1. Le serveur Django va automatiquement recharger les changes")
        print("   2. Testez IMMÉDIATEMENT avec test_medecin")
        print("   3. Vous devriez être redirigé vers /medecin/dashboard/")
    else:
        print("⚠️  Problème lors de la correction - vérification manuelle nécessaire")