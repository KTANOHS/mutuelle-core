# correction_finale_urls.sh
#!/bin/bash

echo "🔧 CORRECTION FINALE DE communication/urls.py"

# Afficher le contenu actuel pour diagnostic
echo "📄 Contenu actuel de communication/urls.py:"
head -20 communication/urls.py

# Créer la version corrigée
cat > communication/urls_corrige.py << 'URLS_EOF'
from django.urls import path, include
from . import views
from .urls_api import urlpatterns as api_urls

app_name = 'communication'

urlpatterns = [
    path('', views.messagerie, name='messagerie'),
    path('messages/', views.MessageListView.as_view(), name='message_list'),
    path('messages/nouveau/', views.MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('messages/envoyer/', views.envoyer_message, name='envoyer_message'),
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
    path('notifications/count/', views.notification_non_lue_count, name='notification_count'),
    path('fichiers/', views.liste_fichiers, name='liste_fichiers'),
    path('groupes/', views.liste_groupes, name='liste_groupes'),
    path('groupes/creer/', views.creer_groupe, name='creer_groupe'),
    path('stats/', views.stats_communication, name='stats_communication'),
    
    # Inclure les URLs API
    path('', include((api_urls, 'communication_api'))),
]
URLS_EOF

# Appliquer la correction
cp communication/urls.py communication/urls.py.backup.final
cp communication/urls_corrige.py communication/urls.py
rm communication/urls_corrige.py

echo "✅ communication/urls.py corrigé avec succès!"
echo "💡 Ancienne version sauvegardée dans: communication/urls.py.backup.final"

# Vérification
echo ""
echo "🧪 Vérification finale..."
python manage.py check

echo ""
echo "🚀 Test du serveur..."
python manage.py runserver
URLS_EOF


