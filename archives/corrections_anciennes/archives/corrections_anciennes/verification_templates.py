# verification_templates.py
import os

def verifier_tous_les_templates():
    """Vérifie que tous les templates nécessaires existent"""
    print("🔍 VÉRIFICATION DE TOUS LES TEMPLATES")
    print("=" * 50)
    
    templates_necessaires = {
        'pharmacien': [
            'base_pharmacien.html',
            'dashboard.html', 
            'liste_ordonnances.html',
            'detail_ordonnance.html',
            'historique_validation.html'
        ],
        'medecin': [
            'base_medecin.html',
            'dashboard.html',
            'liste_bons.html',
            'detail_bon.html',
            'creer_ordonnance.html',
            'historique_ordonnances.html',
            'mes_rendez_vous.html',
            'profil_medecin.html',
            'statistiques.html'
        ],
        'assureur': [
            'base_assureur.html',
            'dashboard.html',
            'liste_membres.html',
            'creer_membre.html',
            'detail_membre.html',
            'liste_bons.html',
            'creer_bon.html',
            'detail_bon.html',
            'liste_paiements.html',
            'creer_paiement.html',
            'detail_paiement.html',
            'liste_soins.html',
            'detail_soin.html',
            'rapports.html',
            'rapport_statistiques.html'
        ],
        'membres': [
            'dashboard.html',
            'liste_membres.html',
            'creer_membre.html',
            'detail_membre.html',
            'selection_membre.html'
        ]
    }
    
    for app, templates in templates_necessaires.items():
        print(f"\n📁 {app.upper()}:")
        for template in templates:
            chemin = f'templates/{app}/{template}'
            if os.path.exists(chemin):
                print(f"  ✅ {template}")
            else:
                print(f"  ❌ {template} - MANQUANT")
    
    print("\n💡 Les templates marqués ❌ doivent être créés")

if __name__ == '__main__':
    verifier_tous_les_templates()