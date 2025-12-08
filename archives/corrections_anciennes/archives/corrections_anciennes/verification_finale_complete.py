# verification_finale_complete.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verification_finale_complete():
    """Vérification finale que tout fonctionne"""
    print("🎯 VÉRIFICATION FINALE COMPLÈTE")
    print("=" * 50)
    
    from django.urls import reverse, NoReverseMatch
    from django.template.loader import get_template
    from django.template import TemplateDoesNotExist
    
    # 1. Vérification des URLs
    print("1. 🔗 VÉRIFICATION DES URLs:")
    print("-" * 30)
    
    urls_critiques = [
        ('home', []),
        ('dashboard', []),
        ('pharmacien:dashboard_pharmacien', []),
        ('pharmacien:liste_ordonnances_attente', []),
        ('pharmacien:detail_ordonnance', [1]),
        ('pharmacien:valider_ordonnance', [1]),
        ('pharmacien:historique_validation', []),
        ('medecin:dashboard', []),
        ('assureur:dashboard', []),
        ('membres:dashboard', []),
    ]
    
    succes_urls = 0
    for url_name, args in urls_critiques:
        try:
            if args:
                url = reverse(url_name, args=args)
            else:
                url = reverse(url_name)
            print(f"   ✅ {url_name:35} -> {url}")
            succes_urls += 1
        except NoReverseMatch:
            print(f"   ❌ {url_name:35} -> ERREUR")
    
    # 2. Vérification des templates
    print("\n2. 📄 VÉRIFICATION DES TEMPLATES:")
    print("-" * 30)
    
    templates_critiques = [
        'pharmacien/base_pharmacien.html',
        'pharmacien/dashboard.html',
        'pharmacien/liste_ordonnances.html',
        'pharmacien/detail_ordonnance.html',
        'pharmacien/historique_validation.html',
        'assureur/detail_soin.html',
        'membres/detail_membre.html',
        'base.html',
        'home.html',
    ]
    
    succes_templates = 0
    for template_name in templates_critiques:
        try:
            template = get_template(template_name)
            print(f"   ✅ {template_name:35} -> EXISTE")
            succes_templates += 1
        except TemplateDoesNotExist:
            print(f"   ❌ {template_name:35} -> MANQUANT")
    
    # 3. Résumé
    print(f"\n3. 📊 RÉSUMÉ FINAL:")
    print("-" * 30)
    print(f"   URLs:     {succes_urls}/{len(urls_critiques)} ✅")
    print(f"   Templates: {succes_templates}/{len(templates_critiques)} ✅")
    
    if succes_urls == len(urls_critiques) and succes_templates == len(templates_critiques):
        print("\n🎉 TOUT EST PRÊT !")
        print("💡 Votre application devrait fonctionner parfaitement")
    else:
        print("\n⚠️  Il reste quelques éléments à corriger")

if __name__ == '__main__':
    verification_finale_complete()