#!/bin/bash
echo "🔍 DIAGNOSTIC COMPLET - MODULE COMMUNICATION"
echo "=" * 60

echo "1. 📁 Structure des fichiers :"
ls -la communication/ 2>/dev/null || echo "❌ Répertoire communication/ non trouvé"

echo ""
echo "2. 🐍 Fichier views.py :"
if [ -f "communication/views.py" ]; then
    echo "✅ Fichier existant"
    echo "   - Vue communication_home : $(grep -c "def communication_home" communication/views.py)"
    echo "   - Taille : $(wc -l < communication/views.py) lignes"
else
    echo "❌ Fichier views.py manquant"
fi

echo ""
echo "3. 📄 Fichier urls.py :"
if [ -f "communication/urls.py" ]; then
    echo "✅ Fichier existant"
    echo "   - Contenu :"
    grep -n "communication_home\|accueil" communication/urls.py || echo "   ⚠️  URL non trouvée"
else
    echo "❌ Fichier urls.py manquant"
fi

echo ""
echo "4. 🎨 Templates :"
if [ -d "communication/templates/communication" ]; then
    echo "✅ Répertoire templates existant"
    ls -la communication/templates/communication/ | head -10
else
    echo "❌ Répertoire templates manquant"
fi

echo ""
echo "5. 🔗 URLs principales :"
echo "   - /communication/ → communication_home"
echo "   - /communication/messagerie/ → messagerie"
echo "   - /communication/notifications/ → notification_list"

echo ""
echo "🌐 Pour tester :"
echo "   1. Redémarrez : python manage.py runserver"
echo "   2. Accédez à : http://127.0.0.1:8000/communication/"
echo "   3. Connectez-vous avec GLORIA1 (pharmacien123)"
