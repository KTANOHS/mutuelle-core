# verification_finale.py
import os
import django
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verification_finale():
    print("🎯 VÉRIFICATION FINALE - TOUTES LES URLS")
    print("=" * 60)
    
    urls_a_verifier = [
        # Communication
        'communication:liste_notifications',
        'communication:messagerie',
        
        # Médecin
        'medecin:dashboard',           # Nom principal
        'medecin:dashboard_medecin',   # Alias de compatibilité
        'medecin:liste_bons',
        'medecin:mes_ordonnances',
        
        # URLs de base
        'medecin:dashboard_root',
    ]
    
    for url_name in urls_a_verifier:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name:35} -> {url}")
        except Exception as e:
            print(f"❌ {url_name:35} -> ERREUR: {e}")

if __name__ == "__main__":
    verification_finale()
    print("\n🎉 VÉRIFICATION TERMINÉE !")