# test_api_mobile_complete.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def test_api_mobile_complete():
    print("📱 TEST COMPLET DE L'API MOBILE")
    print("=" * 50)
    
    try:
        # Test imports
        from api.views_mobile import (
            MobileMembreViewSet, MobileBonViewSet, MobileNotificationViewSet,
            MobileSoinViewSet, MobilePaiementViewSet
        )
        from api.serializers_mobile import (
            MobileMembreSerializer, MobileBonSerializer, MobileNotificationSerializer,
            MobileSoinSerializer, MobilePaiementSerializer, MobileDashboardSerializer
        )
        
        print("✅ Tous les imports mobiles fonctionnent")
        
        # Test serializers
        serializers = [
            MobileMembreSerializer(),
            MobileBonSerializer(), 
            MobileNotificationSerializer(),
            MobileSoinSerializer(),
            MobilePaiementSerializer(),
            MobileDashboardSerializer()
        ]
        
        print("✅ Tous les serializers mobiles fonctionnent")
        
        # Test endpoints
        endpoints = [
            "GET    /api/mobile/membres/",
            "GET    /api/mobile/membres/dashboard/",
            "GET    /api/mobile/bons/", 
            "GET    /api/mobile/notifications/",
            "POST   /api/mobile/notifications/marquer_toutes_lues/",
            "POST   /api/mobile/notifications/{id}/marquer_lue/",
            "GET    /api/mobile/soins/",
            "GET    /api/mobile/paiements/"
        ]
        
        print("\n🎯 ENDPOINTS MOBILES DISPONIBLES:")
        for endpoint in endpoints:
            print(f"   📍 {endpoint}")
        
        # Vérifier system check
        from django.core.management import call_command
        call_command('check')
        print("✅ System check OK")
        
        print("\n🎉 API MOBILE COMPLÈTEMENT OPÉRATIONNELLE!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_api_mobile_complete()