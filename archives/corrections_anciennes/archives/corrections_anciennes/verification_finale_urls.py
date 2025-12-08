# verification_finale_urls.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.urls import reverse, NoReverseMatch

def verification_finale():
    print("🔗 VÉRIFICATION FINALE DES URLs")
    print("=" * 50)
    
    urls_medecin = [
        'dashboard',
        'mes_rendez_vous',
        'creer_rendez_vous', 
        'modifier_statut_rdv',
        'detail_consultation',
        'liste_bons',
        'liste_bons_attente',
        'bons_attente',  # ✅ Celle-ci doit maintenant exister
        'detail_bon',
        'valider_bon',
        'refuser_bon',
        'creer_ordonnance',
        'historique_ordonnances',
        'detail_ordonnance',
        'profil_medecin',
        'statistiques',
        'api_statistiques',
        'api_toggle_disponibilite',
        'ajouter_medicament',
    ]
    
    print("📋 URLs de l'application medecin:")
    toutes_ok = True
    
    for url_name in urls_medecin:
        full_name = f'medecin:{url_name}'
        try:
            url = reverse(full_name)
            print(f"   ✅ {full_name} -> {url}")
        except NoReverseMatch:
            print(f"   ❌ {full_name} -> NON TROUVÉE")
            toutes_ok = False
    
    return toutes_ok

if __name__ == "__main__":
    if verification_finale():
        print("\n🎉 TOUTES LES URLs MEDECIN SONT CONFIGURÉES !")
        print("💡 L'application medecin est complètement fonctionnelle")
    else:
        print("\n💡 Certaines URLs manquent encore")