# test_reel_dashboard.py
import os
import sys
import django
from django.urls import reverse, NoReverseMatch

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/VERIFICATION/projet')

try:
    django.setup()
    print("✅ Django configuré")
except Exception as e:
    print(f"❌ Erreur Django: {e}")
    sys.exit(1)

def test_urls_reelles():
    print("🌐 TEST DES URLs RÉELLES")
    print("=" * 40)
    
    urls_a_tester = [
        ('agents:dashboard', 'Dashboard agent'),
        ('agents:creer_bon_soin', 'Créer bon de soin'),
        ('agents:liste_membres', 'Liste membres'),
        ('agents:historique_bons', 'Historique bons'),
        ('agents:verification_cotisations', 'Vérification cotisations')
    ]
    
    toutes_valides = True
    
    for url_name, description in urls_a_tester:
        try:
            url = reverse(url_name)
            print(f"✅ {description:25} -> {url}")
        except NoReverseMatch as e:
            print(f"❌ {description:25} -> ERREUR: {e}")
            toutes_valides = False
    
    return toutes_valides

def test_vue_dashboard():
    print("\n👁️ TEST DE LA VUE DASHBOARD")
    print("-" * 30)
    
    try:
        from agents.views import dashboard
        print("✅ Vue dashboard importée")
        
        # Vérifier que c'est une fonction callable
        if callable(dashboard):
            print("✅ Vue dashboard est callable")
        else:
            print("❌ Vue dashboard n'est pas callable")
            return False
            
        return True
    except ImportError as e:
        print(f"❌ Erreur import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_template_dashboard():
    print("\n📄 TEST DU TEMPLATE DASHBOARD")
    print("-" * 30)
    
    template_path = '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/agents/dashboard.html'
    
    if not os.path.exists(template_path):
        print("❌ Template dashboard non trouvé")
        return False
    
    with open(template_path, 'r') as f:
        content = f.read()
    
    # Vérifier les problèmes
    problemes = []
    
    if 'tableau_de_bord_agent' in content:
        problemes.append("Contient 'tableau_de_bord_agent'")
    
    if "{% url 'agents:dashboard' %}" not in content and '{% url "agents:dashboard" %}' not in content:
        problemes.append("URL dashboard non trouvée")
    
    if not problemes:
        print("✅ Template dashboard valide")
        return True
    else:
        print(f"❌ Problèmes: {', '.join(problemes)}")
        return False

def main():
    print("🚀 TEST RÉEL DU DASHBOARD")
    print("=" * 50)
    
    # Test 1: URLs
    urls_ok = test_urls_reelles()
    
    # Test 2: Vue
    vue_ok = test_vue_dashboard()
    
    # Test 3: Template
    template_ok = test_template_dashboard()
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DU TEST:")
    print("-" * 50)
    
    if urls_ok and vue_ok and template_ok:
        print("🎉 TOUT EST FONCTIONNEL !")
        print("\n✅ Le dashboard devrait maintenant fonctionner")
        print("💡 Accédez à: http://localhost:8000/agents/tableau-de-bord/")
    else:
        print("❌ Problèmes détectés:")
        if not urls_ok:
            print("   - URLs non valides")
        if not vue_ok:
            print("   - Problème avec la vue dashboard")
        if not template_ok:
            print("   - Problème avec le template")

if __name__ == "__main__":
    main()