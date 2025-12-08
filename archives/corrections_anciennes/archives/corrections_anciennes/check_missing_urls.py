# check_missing_urls.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.urls import reverse, NoReverseMatch

def check_urls():
    print("🔗 VÉRIFICATION DES URLs MANQUANTES")
    print("=" * 50)
    
    urls_to_check = [
        'bons_attente',
        'medecin:bons_attente', 
        'medecin:creer_ordonnance',
        'medecin:dashboard',
        'medecin:mes_rendez_vous',
        'medecin:liste_bons',
        'medecin:historique_ordonnances',
        'medecin:profil_medecin',
    ]
    
    for url_name in urls_to_check:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name} -> {url}")
        except NoReverseMatch:
            print(f"❌ {url_name} -> NON TROUVÉ")

if __name__ == "__main__":
    check_urls()