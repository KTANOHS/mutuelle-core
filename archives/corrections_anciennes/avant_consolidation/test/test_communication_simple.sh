#!/bin/bash

echo "🧪 TEST SIMPLE DU MODULE COMMUNICATION"
echo "======================================"

# Arrêter tout serveur existant
echo "🛑 Arrêt des serveurs existants..."
pkill -f "python manage.py runserver" 2>/dev/null
sleep 2

# Vérifier les vues
echo ""
echo "🔍 VÉRIFICATION DES VUES:"
python -c "
import sys
sys.path.insert(0, '.')
try:
    import communication.views as v
    
    print('📋 Vues disponibles (messagerie_*):')
    views = [attr for attr in dir(v) if 'messagerie' in attr.lower() and callable(getattr(v, attr))]
    
    for view in sorted(views):
        print(f'   ✅ {view}')
    
    print(f'\\n📊 Total: {len(views)} vues messagerie')
    
    # Vérifier les vues critiques
    critical_views = ['messagerie_pharmacien', 'messagerie', 'communication_home']
    for cv in critical_views:
        if hasattr(v, cv):
            print(f'   ✅ {cv} → OK')
        else:
            print(f'   ❌ {cv} → MANQUANTE')
            
except Exception as e:
    print(f'❌ Erreur: {e}')
"

# Démarrer le serveur
echo ""
echo "🚀 Démarrage du serveur..."
python manage.py runserver 0.0.0.0:8000 > /tmp/django_com_test.log 2>&1 &
SERVER_PID=$!
echo "✅ Serveur démarré (PID: $SERVER_PID)"

# Attendre
echo "⏳ Attente du démarrage..."
sleep 5

# Test rapide
echo ""
echo "🔗 TEST DES URLS PRINCIPALES:"

test_url() {
    local url=$1
    local description=$2
    local status=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:8000${url}")
    
    if [ "$status" = "200" ]; then
        echo "   ✅ $description → HTTP 200 (SUCCÈS)"
    elif [ "$status" = "302" ]; then
        echo "   🔄 $description → HTTP 302 (REDIRECTION - normal si non connecté)"
    else
        echo "   ❌ $description → HTTP $status"
    fi
}

test_url "/communication/" "Accueil communication"
test_url "/communication/pharmacien/" "Messagerie pharmacien"
test_url "/communication/messagerie/" "Messagerie générale"
test_url "/communication/notifications/" "Notifications"

# Arrêter le serveur
echo ""
echo "🛑 Arrêt du serveur..."
kill $SERVER_PID 2>/dev/null

echo ""
echo "🎉 TEST TERMINÉ !"
echo ""
echo "📌 POUR UTILISER LE MODULE:"
echo "1. Démarrez le serveur: python manage.py runserver"
echo "2. Accédez à: http://127.0.0.1:8000/communication/"
echo "3. Connectez-vous avec: GLORIA1 / pharmacien123"
echo ""
echo "📋 URLs DISPONIBLES:"
echo "   • http://127.0.0.1:8000/communication/          (Accueil)"
echo "   • http://127.0.0.1:8000/communication/pharmacien/ (Pharmacien)"
echo "   • http://127.0.0.1:8000/communication/messagerie/ (Messagerie)"
echo "   • http://127.0.0.1:8000/communication/notifications/ (Notifications)"
