# diagnostic_rapide.py
import os
import django
from django.urls import reverse, NoReverseMatch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnostic_rapide():
    print("🔍 DIAGNOSTIC RAPIDE - communication:liste_notifications")
    print("=" * 60)
    
    # Test direct
    try:
        url = reverse('communication:liste_notifications')
        print(f"✅ URL TROUVÉE: {url}")
        return True
    except NoReverseMatch as e:
        print(f"❌ ERREUR: {e}")
        print("\n🔧 SOLUTIONS IMMÉDIATES:")
        print("1. Vérifiez que communication/urls.py contient:")
        print('   path("notifications/", views.XXX, name="liste_notifications")')
        print("\n2. Vérifiez que l'app communication est dans INSTALLED_APPS")
        print("\n3. Vérifiez l'inclusion dans urls.py principal:")
        print('   path("communication/", include("communication.urls"))')
        return False

# Test alternatif
def tester_variantes():
    print("\n🔄 TEST DES VARIANTES:")
    variantes = [
        'communication:liste_notifications',
        'communication:notification_list', 
        'liste_notifications',
    ]
    
    for var in variantes:
        try:
            url = reverse(var)
            print(f"✅ {var} -> {url}")
        except:
            print(f"❌ {var} -> NON TROUVÉE")

if __name__ == "__main__":
    if diagnostic_rapide():
        print("\n🎉 Le problème semble résolu!")
    else:
        print("\n🔴 Le problème persiste. Lancer le diagnostic complet.")
        tester_variantes()