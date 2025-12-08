# test_final_complet.py
import os
import sys
import django
from django.urls import reverse, NoReverseMatch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/VERIFICATION/projet')

django.setup()

def test_complet():
    print("🧪 TEST FINAL COMPLET")
    print("=" * 40)
    
    # Test des URLs
    print("\n📋 TEST DES URLs:")
    print("-" * 20)
    
    urls_a_tester = [
        'agents:dashboard',
        'agents:verification_cotisations', 
        'agents:creer_bon_soin',
        'agents:historique_bons',
        'agents:liste_membres'
    ]
    
    toutes_valides = True
    for url_name in urls_a_tester:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name:30} -> {url}")
        except NoReverseMatch:
            print(f"❌ {url_name:30} -> NON TROUVÉ")
            toutes_valides = False
    
    # Test de l'accès dashboard
    print("\n🌐 TEST ACCÈS DASHBOARD:")
    print("-" * 25)
    
    try:
        from agents.views import dashboard
        print("✅ Vue dashboard importable")
        
        # Vérifier que la fonction existe
        if hasattr(dashboard, '__call__'):
            print("✅ Vue dashboard est callable")
        else:
            print("❌ Vue dashboard n'est pas callable")
            toutes_valides = False
            
    except Exception as e:
        print(f"❌ Erreur import dashboard: {e}")
        toutes_valides = False
    
    # Vérifier le template
    print("\n📄 VÉRIFICATION TEMPLATE:")
    print("-" * 25)
    
    template_path = '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/agents/dashboard.html'
    if os.path.exists(template_path):
        with open(template_path, 'r') as f:
            content = f.read()
        
        if 'tableau_de_bord_agent' in content:
            print("❌ 'tableau_de_bord_agent' trouvé dans le template")
            toutes_valides = False
        else:
            print("✅ Aucune occurrence problématique")
        
        # Vérifier les URLs corrigées
        if "{% url 'agents:dashboard' %}" in content:
            print("✅ URLs corrigées présentes")
        else:
            print("⚠️  URLs corrigées non trouvées")
    else:
        print("❌ Template non trouvé")
        toutes_valides = False
    
    # Résumé
    print("\n" + "=" * 40)
    if toutes_valides:
        print("🎉 TOUT EST FONCTIONNEL !")
        print("\n✅ Prochaines étapes:")
        print("   1. Redémarrez le serveur: python manage.py runserver")
        print("   2. Accédez à: http://localhost:8000/agents/tableau-de-bord/")
        print("   3. Testez la navigation")
    else:
        print("❌ Problèmes détectés - utilisez les scripts de correction")

if __name__ == "__main__":
    test_complet()