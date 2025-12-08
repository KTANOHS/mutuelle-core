#!/bin/bash
# verification_urls_notifications.sh

echo "🔍 VÉRIFICATION DES URLs DE NOTIFICATIONS"

echo "1. URLs de notifications disponibles :"
python manage.py show_urls | grep notifications

echo "2. Test de résolution d'URL :"
python manage.py shell << EOF
from django.urls import reverse
try:
    url = reverse('communication:marquer_toutes_notifications_lues')
    print(f"✅ URL marquer_toutes_notifications_lues trouvée: {url}")
except Exception as e:
    print(f"❌ Erreur: {e}")

try:
    url = reverse('communication:notification_list')
    print(f"✅ URL notification_list trouvée: {url}")
except Exception as e:
    print(f"❌ Erreur: {e}")
EOF