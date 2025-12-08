# verifier_urls.py
import os
import sys
import django
from django.urls import reverse, NoReverseMatch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append('/Users/koffitanohsoualiho/Documents/projet')

django.setup()

def verifier_urls_agents():
    print("🔗 VÉRIFICATION DES URLS AGENTS")
    print("=" * 50)
    
    urls_a_verifier = [
        'agents:tableau_de_bord_agent',
        'agents:verification_cotisations', 
        'agents:rapport_performance',
        'agents:creer_bon_soin',
        'agents:creer_bon_soin_membre',
        'agents:confirmation_bon_soin',
        'agents:historique_bons',
        'agents:recherche_membres_api',
        'agents:verifier_cotisation_api',
        # URL problématique
        'agents:dashboard_agent'
    ]
    
    for url_name in urls_a_verifier:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name:35} -> {url}")
        except NoReverseMatch:
            print(f"❌ {url_name:35} -> NON TROUVÉE")
    
    print("\n💡 RECOMMANDATIONS:")
    print("   - Vérifiez que agents/urls.py est correctement configuré")
    print("   - Assurez-vous que l'application 'agents' est dans INSTALLED_APPS")
    print("   - Vérifiez l'include dans le urls.py principal")

if __name__ == "__main__":
    verifier_urls_agents()