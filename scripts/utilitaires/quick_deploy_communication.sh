# quick_deploy_communication.sh
#!/bin/bash

echo "🚀 Déploiement rapide de l'accès communication..."

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "manage.py" ]; then
    echo "❌ Erreur: Exécutez ce script depuis la racine de votre projet Django"
    exit 1
fi

# Créer les répertoires si nécessaire
mkdir -p templates/includes
mkdir -p static/js

# Appliquer les modifications
python implement_communication_access.py

echo ""
echo "✅ Déploiement terminé!"
echo ""
echo "📋 Prochaines étapes manuelles:"
echo "1. Ajoutez dans communication/urls.py:"
echo "   from .urls_api import urlpatterns as api_urls"
echo "   urlpatterns += api_urls"
echo ""
echo "2. Dans vos dashboards, ajoutez:"
echo "   {% include 'includes/communication_widget.html' %}"
echo ""
echo "3. Dans vos sidebars, ajoutez:"
echo "   {% include 'includes/sidebar_communication.html' %}"
echo ""
echo "4. Testez: python manage.py runserver"