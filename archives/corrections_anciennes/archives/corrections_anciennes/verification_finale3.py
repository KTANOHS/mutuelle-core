# verification_finale.py
import os
import django
from django.urls import reverse, NoReverseMatch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_urls_pharmacien():
    print("🔍 VÉRIFICATION FINALE DES URLS PHARMACIEN")
    print("=" * 50)
    
    urls_a_verifier = [
        'pharmacien:dashboard',
        'pharmacien:liste_ordonnances_attente',
        'pharmacien:profil_pharmacien', 
        'pharmacien:stock',  # Celle qui posait problème
        'pharmacien:ajouter_stock',
        'pharmacien:historique_validation',
    ]
    
    for url_name in urls_a_verifier:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name:35} -> {url}")
        except NoReverseMatch as e:
            print(f"❌ {url_name:35} -> ERREUR: {e}")
    
    print("\n🎯 TEST DES URLS CRITIQUES:")
    urls_critiques = ['pharmacien:stock', 'pharmacien:profil_pharmacien']
    for url_name in urls_critiques:
        try:
            url = reverse(url_name)
            print(f"🎉 {url_name} FONCTIONNE -> {url}")
        except NoReverseMatch:
            print(f"💥 {url_name} - TOUJOURS PROBLEMATIQUE")

if __name__ == '__main__':
    verifier_urls_pharmacien()