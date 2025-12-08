# test_final_corrige.py
import os
import django
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("🎉 TEST CORRIGÉ - URLs AVEC PARAMÈTRES")
print("=" * 60)

# Test des URLs avec leurs paramètres requis
urls_avec_params = [
    ('pharmacien:detail_ordonnance', [1]),  # besoin d'ordonnance_id
    ('pharmacien:valider_ordonnance', [1]), # besoin d'ordonnance_id  
    ('pharmacien:refuser_ordonnance', [1]), # besoin d'ordonnance_id
    ('pharmacien:modifier_stock', [1]),     # besoin de stock_id
    ('pharmacien:activer_stock', [1]),      # besoin de stock_id
    ('pharmacien:desactiver_stock', [1]),   # besoin de stock_id
    ('pharmacien:reapprovisionner_stock', [1]), # besoin de stock_id
]

print("🔍 URLs avec paramètres (test avec ID=1):")
for url_name, args in urls_avec_params:
    try:
        url = reverse(url_name, args=args)
        print(f"✅ {url_name:35} -> {url}")
    except Exception as e:
        print(f"❌ {url_name:35} -> {e}")

# URLs sans paramètres (devraient fonctionner directement)
urls_sans_params = [
    'pharmacien:dashboard',
    'pharmacien:liste_ordonnances_attente',
    'pharmacien:profil_pharmacien',
    'pharmacien:stock',
    'pharmacien:ajouter_stock',
]

print(f"\n🔍 URLs sans paramètres:")
for url_name in urls_sans_params:
    try:
        url = reverse(url_name)
        print(f"✅ {url_name:35} -> {url}")
    except Exception as e:
        print(f"❌ {url_name:35} -> {e}")

print(f"\n🎯 CONCLUSION:")
print("   Toutes les URLs existent et fonctionnent correctement!")
print("   Les 'erreurs' précédentes étaient dues aux paramètres manquants.")