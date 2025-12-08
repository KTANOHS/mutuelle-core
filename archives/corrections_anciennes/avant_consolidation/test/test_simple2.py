# test_simple.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

print("🔍 TEST SIMPLIFIÉ")
print("="*50)

# 1. Vérifier le template
import os
template_path = 'templates/assureur/liste_membres.html'
if os.path.exists(template_path):
    print(f"✅ Template trouvé: {template_path}")
    
    with open(template_path, 'r') as f:
        content = f.read()
        
    if 'numero_unique' in content:
        print("✅ Template utilise 'numero_unique'")
    else:
        print("❌ Template n'utilise PAS 'numero_unique'")
        
    if 'date_inscription' in content:
        print("✅ Template utilise 'date_inscription'")
    else:
        print("❌ Template n'utilise PAS 'date_inscription'")
else:
    print(f"❌ Template non trouvé: {template_path}")

# 2. Vérifier la vue
try:
    from assureur import views
    print("\n✅ Module assureur.views importé")
    
    # Vérifier la fonction liste_membres
    if hasattr(views, 'liste_membres'):
        print("✅ Fonction liste_membres() existe")
    else:
        print("❌ Fonction liste_membres() n'existe pas")
        
except Exception as e:
    print(f"❌ Erreur import: {e}")

# 3. Vérifier les URLs
try:
    from django.urls import reverse
    print("\n🔗 Test des URLs:")
    
    urls_to_test = [
        'assureur:liste_membres',
        'assureur:dashboard_assureur',
    ]
    
    for url_name in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"✅ URL '{url_name}' : {url}")
        except Exception as e:
            print(f"❌ URL '{url_name}' : NON CONFIGURÉE ({e})")
            
except Exception as e:
    print(f"❌ Erreur URLs: {e}")

print("\n" + "="*50)
print("🚀 POUR TESTER MANUELLEMENT:")
print("1. python manage.py runserver")
print("2. Ouvrir: http://127.0.0.1:8000/assureur/membres/?q=ASIA")
print("3. Vous devriez voir 2 résultats")
print("="*50)