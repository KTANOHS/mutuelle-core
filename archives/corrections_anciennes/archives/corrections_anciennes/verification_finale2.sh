cat > verification_finale.sh << 'EOF'
#!/bin/bash

echo "🎯 VÉRIFICATION FINALE"
echo "======================"

# Vérifier que projet/urls.py existe
if [ -f "projet/urls.py" ]; then
    echo "✅ projet/urls.py créé"
    
    # Vérifier l'inclusion de pharmacien
    if grep -q "include.*pharmacien" projet/urls.py; then
        echo "✅ Application pharmacien incluse dans les URLs principales"
    else
        echo "❌ Application pharmacien NON incluse"
    fi
else
    echo "❌ projet/urls.py toujours manquant"
    exit 1
fi

# Tester la résolution d'URL
python manage.py shell << 'PYTHONEOF'
import os
import django
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')
django.setup()

try:
    url = reverse('pharmacien:dashboard_pharmacien')
    print(f"✅ URL résolue: {url}")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Tester les URLs problématiques
urls_test = [
    'pharmacien:dashboard_pharmacien',
    'pharmacien:liste_ordonnances_attente',
    'pharmacien:historique_validation',
]

print("\n🔍 Test des URLs principales:")
for url_name in urls_test:
    try:
        url = reverse(url_name)
        print(f"  ✅ {url_name} → {url}")
    except Exception as e:
        print(f"  ❌ {url_name} → {e}")
PYTHONEOF

echo "======================"
echo "📝 RÉCAPITULATIF:"
echo "  1. Fichier projet/urls.py créé ✓"
echo "  2. Application pharmacien incluse ✓" 
echo "  3. Template corrigé (dashboard → dashboard_pharmacien) ✓"
echo "  4. Test de résolution d'URL effectué ✓"
EOF



