# verification_finale_vues.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_toutes_les_vues():
    """Vérifie que toutes les vues existent maintenant"""
    print("✅ VÉRIFICATION FINALE - TOUTES LES VUES")
    print("=" * 50)
    
    try:
        from mutuelle_core import views
        
        vues_requises = [
            'creer_bon', 'creer_paiement', 'detail_bon', 'detail_membre',
            'detail_paiement', 'detail_soin', 'liste_bons', 'liste_paiements', 'liste_soins'
        ]
        
        print("Vérification des vues précédemment manquantes:")
        for vue in vues_requises:
            if hasattr(views, vue):
                print(f"  ✅ {vue} - EXISTE MAINTENANT")
            else:
                print(f"  ❌ {vue} - TOUJOURS MANQUANTE")
        
        print("\n🎉 VÉRIFICATION TERMINÉE!")
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")

if __name__ == '__main__':
    verifier_toutes_les_vues()