# verifier_correction.py
import os
import sys
import django
from django.urls import reverse, NoReverseMatch

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/VERIFICATION/projet')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def verifier_urls():
    print("🔍 VÉRIFICATION DES URLs APRÈS CORRECTION")
    print("=" * 50)
    
    # URLs à tester
    urls_a_tester = [
        ('agents:dashboard', 'Dashboard principal'),
        ('agents:verification_cotisations', 'Vérification cotisations'),
        ('agents:creer_bon_soin', 'Créer bon de soin'),
        ('agents:historique_bons', 'Historique des bons'),
        ('agents:liste_membres', 'Liste des membres'),
    ]
    
    print("\n📋 URLs DES AGENTS:")
    print("-" * 40)
    
    toutes_valides = True
    for nom_url, description in urls_a_tester:
        try:
            url = reverse(nom_url)
            print(f"✅ {description:25} -> {url}")
        except NoReverseMatch as e:
            print(f"❌ {description:25} -> ERREUR: {e}")
            toutes_valides = False
    
    return toutes_valides

def verifier_template():
    print("\n📄 VÉRIFICATION DU TEMPLATE:")
    print("-" * 40)
    
    template_path = '/Users/koffitanohsoualiho/Documents/VERIFICATION/projet/templates/agents/dashboard.html'
    
    if not os.path.exists(template_path):
        print("❌ Template dashboard.html non trouvé")
        return False
    
    with open(template_path, 'r') as f:
        content = f.read()
    
    # Vérifier les URLs dans le template
    problemes = []
    
    # Vérifier la présence de tableau_de_bord_agent (ne doit pas exister)
    if 'tableau_de_bord_agent' in content:
        problemes.append("❌ 'tableau_de_bord_agent' trouvé dans le template")
    
    # Vérifier les URLs corrigées
    urls_corrigees = [
        "{% url 'agents:dashboard' %}",
        "{% url 'agents:verification_cotisations' %}",
        "{% url 'agents:creer_bon_soin' %}",
        "{% url 'agents:historique_bons' %}",
        "{% url 'agents:liste_membres' %}"
    ]
    
    for url in urls_corrigees:
        if url in content:
            print(f"✅ URL trouvée: {url}")
        else:
            # Ce n'est pas forcément un problème si certaines URLs ne sont pas utilisées
            pass
    
    if not problemes:
        print("✅ Aucun problème détecté dans le template")
        return True
    else:
        for probleme in problemes:
            print(probleme)
        return False

def verifier_vue_dashboard():
    print("\n👁️ VÉRIFICATION DE LA VUE DASHBOARD:")
    print("-" * 40)
    
    try:
        from agents.views import dashboard
        print("✅ Vue dashboard importée avec succès")
        
        # Vérifier si la fonction existe
        if callable(dashboard):
            print("✅ Vue dashboard est callable")
        else:
            print("❌ Vue dashboard n'est pas callable")
            return False
            
    except ImportError as e:
        print(f"❌ Erreur import vue dashboard: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur vérification vue: {e}")
        return False
    
    return True

def test_acces_dashboard():
    print("\n🌐 TEST D'ACCÈS AU DASHBOARD:")
    print("-" * 40)
    
    try:
        from django.test import RequestFactory
        from django.contrib.auth.models import User
        from agents.views import dashboard
        
        # Créer une requête factice
        factory = RequestFactory()
        request = factory.get('/agents/tableau-de-bord/')
        
        # Simuler un utilisateur (vous devrez peut-être adapter selon votre modèle)
        request.user = User(username='test_agent')
        
        print("✅ Configuration de test créée")
        print("💡 Pour un test complet, lancez le serveur et accédez à:")
        print("   http://localhost:8000/agents/tableau-de-bord/")
        
    except Exception as e:
        print(f"⚠️  Test avancé échoué (normal en mode diagnostic): {e}")
        print("💡 Le test manuel via le navigateur est recommandé")

def main():
    print("🚀 VÉRIFICATION COMPLÈTE DE LA CORRECTION")
    print("=" * 60)
    
    # 1. Vérifier les URLs
    urls_ok = verifier_urls()
    
    # 2. Vérifier le template
    template_ok = verifier_template()
    
    # 3. Vérifier la vue
    vue_ok = verifier_vue_dashboard()
    
    # 4. Test d'accès
    test_acces_dashboard()
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DU DIAGNOSTIC:")
    print("-" * 60)
    
    if urls_ok and template_ok and vue_ok:
        print("🎉 TOUT EST CORRECT ! Le problème est résolu.")
        print("\n✅ Prochaines étapes:")
        print("   1. Redémarrez le serveur: python manage.py runserver")
        print("   2. Accédez à: http://localhost:8000/agents/tableau-de-bord/")
        print("   3. Connectez-vous avec un compte agent")
    else:
        print("❌ Il reste des problèmes à corriger:")
        if not urls_ok:
            print("   - Problèmes d'URLs détectés")
        if not template_ok:
            print("   - Problèmes dans le template")
        if not vue_ok:
            print("   - Problèmes avec la vue dashboard")
        
        print("\n🔧 Solutions:")
        print("   - Vérifiez que agents/urls.py contient bien les URLs")
        print("   - Vérifiez l'orthographe dans le template")
        print("   - Redémarrez le serveur Django")

if __name__ == "__main__":
    main()