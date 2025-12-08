# medecin/quick_check.py
def check_views_quick():
    """Vérification rapide des vues"""
    print("🔍 VÉRIFICATION RAPIDE DES VUES MÉDECIN")
    print("=" * 50)
    
    # Test direct des URLs
    urls_to_test = [
        ('medecin:dashboard', 'Dashboard'),
        ('medecin:liste_bons_attente', 'Bons en attente'),
        ('medecin:historique_ordonnances', 'Historique ordonnances'),
        ('medecin:mes_rendez_vous', 'Rendez-vous'),
        ('medecin:profil_medecin', 'Profil'),
        ('medecin:statistiques', 'Statistiques'),
    ]
    
    from django.urls import reverse, NoReverseMatch
    
    for url_name, description in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"✅ {description:25} -> {url}")
        except NoReverseMatch:
            print(f"❌ {description:25} -> URL NON TROUVÉE")
        except Exception as e:
            print(f"❌ {description:25} -> ERREUR: {e}")

# Exécution:
# python manage.py shell
# >>> from medecin.quick_check import check_views_quick
# >>> check_views_quick()