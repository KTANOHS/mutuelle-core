# check_pharmacien_views.py
import os
import django
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_vues_pharmacien():
    print("🔍 VÉRIFICATION DES VUES PHARMACIEN")
    print("=" * 50)
    
    try:
        from pharmacien import views
        
        # Liste des vues attendues
        vues_attendues = [
            'dashboard_pharmacien',
            'liste_ordonnances_attente',
            'detail_ordonnance', 
            'valider_ordonnance',
            'historique_validations',
            'api_ordonnances_attente'
        ]
        
        print("📋 VUES DISPONIBLES:")
        vues_trouvees = []
        
        for vue_name in vues_attendues:
            if hasattr(views, vue_name):
                vues_trouvees.append(vue_name)
                print(f"   ✅ {vue_name}")
            else:
                print(f"   ❌ {vue_name} - MANQUANTE")
        
        print(f"\n📊 RÉSULTAT: {len(vues_trouvees)}/{len(vues_attendues)} vues trouvées")
        
        # Vérifier les modèles nécessaires
        print(f"\n🏷️ MODÈLES NÉCESSAIRES:")
        try:
            from pharmacien.models import Ordonnance
            print("   ✅ Modèle Ordonnance trouvé")
            
            # Vérifier les champs disponibles
            fields = [f.name for f in Ordonnance._meta.get_fields()]
            print(f"   📋 Champs Ordonnance: {', '.join(fields)}")
            
        except ImportError as e:
            print(f"   ❌ Modèle Ordonnance non trouvé: {e}")
            
    except Exception as e:
        print(f"❌ Erreur import views: {e}")

def tester_urls_pharmacien():
    print(f"\n🔗 TEST DES URLs PHARMACIEN:")
    print("=" * 35)
    
    try:
        from django.urls import reverse
        
        urls_a_tester = [
            'pharmacien:dashboard',
            'pharmacien:liste_ordonnances_attente',
            'pharmacien:historique_validations',
            'pharmacien:api_ordonnances_attente'
        ]
        
        for url_name in urls_a_tester:
            try:
                url = reverse(url_name)
                print(f"   ✅ {url_name}: {url}")
            except Exception as e:
                print(f"   ❌ {url_name}: {e}")
                
    except Exception as e:
        print(f"   ❌ Erreur test URLs: {e}")

if __name__ == "__main__":
    verifier_vues_pharmacien()
    tester_urls_pharmacien()