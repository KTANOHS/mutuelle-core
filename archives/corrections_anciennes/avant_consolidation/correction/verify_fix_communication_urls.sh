#!/bin/bash

echo "🔍 VÉRIFICATION DES URLS COMMUNICATION"
echo "======================================"

# 1. Vérifier la vue communication_home dans views.py
echo ""
echo "1. Vérification de la vue communication_home:"
if grep -n "def communication_home" communication/views.py; then
    echo "✅ Vue trouvée dans views.py"
else
    echo "❌ Vue NON TROUVÉE dans views.py"
    echo "   Exécutez d'abord le script de correction des vues !"
    exit 1
fi

# 2. Vérifier l'URL racine
echo ""
echo "2. Vérification de l'URL racine (/communication/):"
ROOT_URL=$(grep -n "path(''," communication/urls.py | head -1)
if echo "$ROOT_URL" | grep -q "communication_home"; then
    echo "✅ URL racine correctement configurée (pointe vers communication_home)"
    echo "   Ligne: $ROOT_URL"
else
    echo "❌ URL racine INCORRECTE !"
    echo "   Actuel: $ROOT_URL"
    echo "   Doit pointer vers: views.communication_home"
fi

# 3. Lister toutes les URLs
echo ""
echo "3. Liste de toutes les URLs configurées:"
python -c "
import sys
sys.path.insert(0, '.')
try:
    from communication import urls
    print('📋 URLs du module communication:')
    print('=' * 50)
    
    for pattern in urls.urlpatterns:
        if hasattr(pattern, 'name') and pattern.name:
            name = pattern.name
        else:
            name = 'SANS_NOM'
        
        print(f'• {pattern.pattern:<40} → {name}')
    
    print('=' * 50)
    print(f'Total: {len(urls.urlpatterns)} URLs configurées')
    
except Exception as e:
    print(f'❌ Erreur: {e}')
"

# 4. Tester les URLs critiques
echo ""
echo "4. Test des URLs critiques:"
CRITICAL_URLS=(
    "'' communication_home"
    "'messagerie/' messagerie"
    "'notifications/' notification_list"
    "'messages/' message_list"
    "'conversations/' conversations"
)

for url_pattern in "${CRITICAL_URLS[@]}"; do
    url=$(echo $url_pattern | cut -d' ' -f1)
    name=$(echo $url_pattern | cut -d' ' -f2)
    
    if grep -q "name='$name'" communication/urls.py; then
        echo "✅ $name → OK"
    else
        echo "❌ $name → MANQUANT"
    fi
done

# 5. Tester la résolution d'URL
echo ""
echo "5. Test de résolution d'URL:"
python -c "
import sys
sys.path.insert(0, '.')
from django.urls import reverse, NoReverseMatch

URLS_A_TESTER = [
    'communication:communication_home',
    'communication:messagerie',
    'communication:notification_list',
    'communication:message_list',
    'communication:conversations',
]

print('🧪 Test de résolution des URLs:')
for url_name in URLS_A_TESTER:
    try:
        url = reverse(url_name)
        print(f'✅ {url_name:<35} → {url}')
    except NoReverseMatch as e:
        print(f'❌ {url_name:<35} → ERREUR: {e}')
    except Exception as e:
        print(f'⚠️  {url_name:<35} → AUTRE ERREUR: {e}')
"

# 6. Vérifier les templates
echo ""
echo "6. Vérification des templates:"
TEMPLATES=(
    "accueil.html"
    "messagerie.html"
    "notification_list.html"
    "message_list.html"
    "conversations.html"
)

for template in "${TEMPLATES[@]}"; do
    if [ -f "communication/templates/communication/$template" ]; then
        echo "✅ $template → EXISTE"
    else
        echo "❌ $template → MANQUANT"
    fi
done

echo ""
echo "📊 RÉSUMÉ:"
echo "Pour que le module communication fonctionne:"
echo "1. URL racine (/communication/) doit pointer vers communication_home"
echo "2. La vue communication_home doit exister dans views.py"
echo "3. Le template communication/accueil.html doit exister"
echo ""
echo "🔧 Pour corriger automatiquement:"
echo "   ./fix_communication_urls.sh"
