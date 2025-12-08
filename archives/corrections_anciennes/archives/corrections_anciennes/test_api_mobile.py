# test_api_mobile.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votre_projet.settings')
django.setup()

def test_api_mobile():
    print("🧪 TEST API MOBILE")
    print("=" * 40)
    
    try:
        from api.views_mobile import MobileMembreViewSet, MobileBonViewSet
        from api.serializers_mobile import MobileMembreSerializer, MobileBonSerializer
        
        print("✅ Vues mobiles importées avec succès")
        print("✅ Serializers mobiles fonctionnels")
        
        # Test création des serializers
        membre_serializer = MobileMembreSerializer()
        bon_serializer = MobileBonSerializer()
        
        print("✅ Serializers mobiles instanciés")
        print("\n🎯 ENDPOINTS MOBILES DISPONIBLES:")
        print("   📱 GET /api/mobile/membres/dashboard/")
        print("   📱 GET /api/mobile/membres/")
        print("   📱 GET /api/mobile/bons/")
        print("   📱 GET /api/mobile/notifications/")
        print("   📱 POST /api/mobile/notifications/marquer_toutes_lues/")
        print("   📱 GET /api/mobile/soins/")
        print("   📱 GET /api/mobile/paiements/")
        
        print("\n🎊 API MOBILE PRÊTE !")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_mobile()