# mapping_medecin.py
import os
import django
from django.urls import reverse, NoReverseMatch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def mapping_urls_medecin():
    """
    Crée un mapping complet des URLs medecin existantes vs manquantes
    """
    print("MAPPING COMPLET MEDECIN")
    print("=" * 60)
    
    # URLs attendues vs URLs existantes
    urls_attendues = {
        'Authentification': [
            'medecin:login',
            'medecin:logout', 
        ],
        'Profil': [
            'medecin:profil',
            'medecin:profil_medecin',
        ],
        'Tableau de bord': [
            'medecin:dashboard',
        ],
        'Consultations': [
            'medecin:consultations',
            'medecin:detail_consultation',
            'medecin:modifier_consultation',
            'medecin:creer_consultation',
        ],
        'Ordonnances': [
            'medecin:ordonnances',
            'medecin:detail_ordonnance',
            'medecin:modifier_ordonnance',
            'medecin:creer_ordonnance',
            'medecin:liste_ordonnances',
            'medecin:historique_ordonnances',
        ],
        'Bons de soins': [
            'medecin:liste_bons',
            'medecin:liste_bons_attente',
            'medecin:bons_attente',
            'medecin:detail_bon',
            'medecin:valider_bon',
            'medecin:refuser_bon',
        ],
        'Rendez-vous': [
            'medecin:mes_rendez_vous',
            'medecin:creer_rendez_vous',
            'medecin:modifier_statut_rdv',
        ],
        'Disponibilités': [
            'medecin:disponibilites',
            'medecin:creer_disponibilite',
            'medecin:modifier_disponibilite',
        ],
        'Recherche & Stats': [
            'medecin:rechercher_patient',
            'medecin:statistiques',
            'medecin:historique',
            'medecin:api_statistiques',
            'medecin:api_toggle_disponibilite',
            'medecin:ajouter_medicament',
        ]
    }
    
    print("\nSTATUT DES URLs PAR CATÉGORIE:")
    print("=" * 60)
    
    for categorie, urls in urls_attendues.items():
        print(f"\n{categorie.upper()}:")
        print("-" * 40)
        
        for url_name in urls:
            try:
                url = reverse(url_name)
                statut = "✓ EXISTE"
                url_affichage = url
            except NoReverseMatch:
                statut = "✗ MANQUANTE"
                url_affichage = ""
            
            print(f"  {statut:<10} {url_name:<35} {url_affichage}")
    
    # Recommandations spécifiques
    print("\n" + "=" * 60)
    print("RECOMMANDATIONS:")
    print("=" * 60)
    
    print("\n1. URLs CRITIQUES MANQUANTES:")
    urls_critiques_manquantes = [
        'medecin:login', 'medecin:logout', 'medecin:profil',
        'medecin:consultations', 'medecin:ordonnances'
    ]
    
    for url_name in urls_critiques_manquantes:
        try:
            reverse(url_name)
        except NoReverseMatch:
            print(f"  - {url_name}")
    
    print("\n2. SOLUTIONS:")
    print("   - Ajouter les URLs manquantes dans medecin/urls.py")
    print("   - Créer les vues correspondantes dans medecin/views.py") 
    print("   - Vérifier que les templates existent")
    print("   - Tester chaque URL après correction")

if __name__ == "__main__":
    mapping_urls_medecin()