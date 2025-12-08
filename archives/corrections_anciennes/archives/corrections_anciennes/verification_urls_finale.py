# verification_urls_finale.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verification_urls_pharmacien_finale():
    """Vérification finale de toutes les URLs pharmacien"""
    print("✅ VÉRIFICATION FINALE DES URLs PHARMACIEN")
    print("=" * 50)
    
    from django.urls import reverse, NoReverseMatch
    
    # Toutes les URLs pharmacien qui devraient exister
    urls_pharmacien = [
        'pharmacien:dashboard_pharmacien',
        'pharmacien:liste_ordonnances_attente',
        'pharmacien:detail_ordonnance',
        'pharmacien:valider_ordonnance', 
        'pharmacien:historique_validation',
        'pharmacien:api_statistiques',
        'pharmacien:api_ordonnances_attente',
        'pharmacien:api_statistiques_temps_reel',
        'pharmacien:rechercher_ordonnances',
        'pharmacien:filtrer_ordonnances',
        'pharmacien:export_historique',
    ]
    
    print("URLs définies dans pharmacien/urls.py:")
    for url_name in urls_pharmacien:
        try:
            url = reverse(url_name)
            print(f"  ✅ {url_name:40} -> {url}")
        except NoReverseMatch as e:
            print(f"  ❌ {url_name:40} -> ERREUR: {e}")
    
    # Vérifier les URLs problématiques spécifiques
    print("\n🔍 URLs PROBLÉMATIQUES (qui causent des erreurs):")
    urls_problematiques = [
        'pharmacien:historique_validations',  # L'ancienne URL qui cause l'erreur
        'pharmacien:dashboard',               # L'ancien nom
    ]
    
    for url_name in urls_problematiques:
        try:
            url = reverse(url_name)
            print(f"  ⚠️  {url_name:40} -> {url} (EXISTE MAIS NE DEVRAIT PAS)")
        except NoReverseMatch:
            print(f"  ✅ {url_name:40} -> N'EXISTE PAS (C'EST NORMAL)")

if __name__ == '__main__':
    verification_urls_pharmacien_finale()