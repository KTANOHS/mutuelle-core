# implement_communication_access.py
import os
import django
import sys
from pathlib import Path

# Configuration Django
project_path = Path(__file__).parent
sys.path.append(str(project_path))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    # Contenu des fichiers à créer/modifier
    files_content = {
        
        # 1. NAVBAR PRINCIPALE
        'navbar_updated': {
            'path': 'templates/includes/navbar.html',
            'content': '''<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
        <a class="navbar-brand" href="{% url 'home' %}">
            <i class="fas fa-heartbeat"></i> HealthApp
        </a>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarMain">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarMain">
            <!-- Navigation principale -->
            <ul class="navbar-nav me-auto">
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'core:dashboard' %}">
                        <i class="fas fa-tachometer-alt"></i> Tableau de bord
                    </a>
                </li>
                
                <!-- ACCÈS COMMUNICATION - Visible pour tous les utilisateurs connectés -->
                {% if user.is_authenticated %}
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarCommunication" role="button" data-bs-toggle="dropdown">
                        <i class="fas fa-comments"></i> Communication
                        <span class="badge bg-danger communication-badge" id="navCommBadge" style="display: none;">
                            <i class="fas fa-circle"></i>
                        </span>
                    </a>
                    <ul class="dropdown-menu">
                        <li>
                            <a class="dropdown-item" href="{% url 'communication:messagerie' %}">
                                <i class="fas fa-inbox"></i> Messagerie
                                <span class="badge bg-danger msg-count" id="navMsgCount" style="display: none;">0</span>
                            </a>
                        </li>
                        <li>
                            <a class="dropdown-item" href="{% url 'communication:notification_list' %}">
                                <i class="fas fa-bell"></i> Notifications
                                <span class="badge bg-warning notif-count" id="navNotifCount" style="display: none;">0</span>
                            </a>
                        </li>
                        <li><hr class="dropdown-divider"></li>
                        <li>
                            <a class="dropdown-item" href="{% url 'communication:liste_groupes' %}">
                                <i class="fas fa-users"></i> Groupes
                            </a>
                        </li>
                        <li>
                            <a class="dropdown-item" href="{% url 'communication:liste_fichiers' %}">
                                <i class="fas fa-file"></i> Fichiers partagés
                            </a>
                        </li>
                    </ul>
                </li>
                {% endif %}
            </ul>
            
            <!-- Menu utilisateur -->
            <ul class="navbar-nav">
                {% if user.is_authenticated %}
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarUser" role="button" data-bs-toggle="dropdown">
                        <i class="fas fa-user-circle"></i> {{ user.get_full_name|default:user.username }}
                        <span class="badge bg-danger user-msg-badge" id="userMsgBadge" style="display: none;"></span>
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li>
                            <a class="dropdown-item" href="{% url 'communication:messagerie' %}">
                                <i class="fas fa-envelope"></i> Messagerie
                                <span class="badge bg-danger msg-count-sm" id="userMsgCount" style="display: none;">0</span>
                            </a>
                        </li>
                        <li>
                            <a class="dropdown-item" href="{% url 'communication:notification_list' %}">
                                <i class="fas fa-bell"></i> Notifications
                                <span class="badge bg-warning notif-count-sm" id="userNotifCount" style="display: none;">0</span>
                            </a>
                        </li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item" href="{% url 'logout' %}"><i class="fas fa-sign-out-alt"></i> Déconnexion</a></li>
                    </ul>
                </li>
                {% else %}
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'login' %}">
                        <i class="fas fa-sign-in-alt"></i> Connexion
                    </a>
                </li>
                {% endif %}
            </ul>
        </div>
    </div>
</nav>

<!-- Script pour charger les compteurs de messages -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Charger les compteurs via AJAX
    function loadCommunicationCounts() {
        // Charger le compteur de notifications
        fetch('{% url "communication:notification_count" %}')
            .then(response => response.json())
            .then(data => {
                updateBadges('notif', data.count);
            })
            .catch(error => console.error('Error loading notification count:', error));
            
        // Charger le compteur de messages non lus
        fetch('{% url "communication:api_messages_count" %}')
            .then(response => response.json())
            .then(data => {
                updateBadges('msg', data.unread_count);
            })
            .catch(error => console.error('Error loading message count:', error));
    }
    
    function updateBadges(type, count) {
        const badges = document.querySelectorAll(`.${type}-count, .${type}-count-sm`);
        const mainBadge = document.querySelector('.communication-badge');
        const userBadge = document.querySelector('.user-msg-badge');
        
        badges.forEach(badge => {
            if (count > 0) {
                badge.textContent = count;
                badge.style.display = 'inline';
            } else {
                badge.style.display = 'none';
            }
        });
        
        // Mettre à jour le badge principal
        if (type === 'msg' && count > 0) {
            mainBadge.style.display = 'inline';
            userBadge.textContent = count;
            userBadge.style.display = 'inline';
        } else if (type === 'msg' && count === 0) {
            mainBadge.style.display = 'none';
            userBadge.style.display = 'none';
        }
    }
    
    // Charger les compteurs au chargement de la page
    loadCommunicationCounts();
    
    // Recharger toutes les 30 secondes
    setInterval(loadCommunicationCounts, 30000);
});
</script>

<style>
.communication-badge, .user-msg-badge {
    font-size: 0.6em;
    padding: 0.2em 0.4em;
    position: relative;
    top: -8px;
    left: -5px;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}

.badge.bg-danger {
    animation: pulse 2s infinite;
}
</style>'''
        },
        
        # 2. SIDEBAR COMMUNICATION
        'sidebar_communication': {
            'path': 'templates/includes/sidebar_communication.html',
            'content': '''<!-- templates/includes/sidebar_communication.html -->
<div class="card mb-4">
    <div class="card-header bg-light">
        <h6 class="mb-0">
            <i class="fas fa-comments me-2 text-primary"></i>Communication
        </h6>
    </div>
    <div class="card-body p-0">
        <div class="list-group list-group-flush">
            <a href="{% url 'communication:messagerie' %}" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                <span><i class="fas fa-inbox me-2"></i>Messagerie</span>
                <span class="badge bg-danger sidebar-msg-count" style="display: none;">0</span>
            </a>
            <a href="{% url 'communication:notification_list' %}" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                <span><i class="fas fa-bell me-2"></i>Notifications</span>
                <span class="badge bg-warning sidebar-notif-count" style="display: none;">0</span>
            </a>
            <a href="{% url 'communication:message_create' %}" class="list-group-item list-group-item-action">
                <i class="fas fa-edit me-2"></i>Nouveau message
            </a>
            <a href="{% url 'communication:liste_groupes' %}" class="list-group-item list-group-item-action">
                <i class="fas fa-users me-2"></i>Groupes de discussion
            </a>
            <a href="{% url 'communication:liste_fichiers' %}" class="list-group-item list-group-item-action">
                <i class="fas fa-file me-2"></i>Fichiers partagés
            </a>
        </div>
    </div>
</div>

<script>
// Synchroniser les badges de la sidebar
document.addEventListener('DOMContentLoaded', function() {
    function updateSidebarBadges() {
        const msgCount = document.querySelector('#navMsgCount')?.textContent || '0';
        const notifCount = document.querySelector('#navNotifCount')?.textContent || '0';
        
        const sidebarMsg = document.querySelector('.sidebar-msg-count');
        const sidebarNotif = document.querySelector('.sidebar-notif-count');
        
        if (parseInt(msgCount) > 0 && sidebarMsg) {
            sidebarMsg.textContent = msgCount;
            sidebarMsg.style.display = 'inline';
        }
        if (parseInt(notifCount) > 0 && sidebarNotif) {
            sidebarNotif.textContent = notifCount;
            sidebarNotif.style.display = 'inline';
        }
    }
    
    // Mettre à jour immédiatement et périodiquement
    updateSidebarBadges();
    setInterval(updateSidebarBadges, 30000);
});
</script>'''
        },
        
        # 3. WIDGET DASHBOARD
        'dashboard_widget': {
            'path': 'templates/includes/communication_widget.html',
            'content': '''<!-- templates/includes/communication_widget.html -->
<div class="card border-primary h-100">
    <div class="card-header bg-primary text-white">
        <div class="d-flex justify-content-between align-items-center">
            <h6 class="mb-0">
                <i class="fas fa-comments me-2"></i>Communication
            </h6>
            <div class="communication-widget-badges">
                <span class="badge bg-danger me-1 msg-widget-count" style="display: none;">0</span>
                <span class="badge bg-warning notif-widget-count" style="display: none;">0</span>
            </div>
        </div>
    </div>
    <div class="card-body">
        <div class="row g-2">
            <div class="col-6">
                <a href="{% url 'communication:messagerie' %}" class="btn btn-outline-primary w-100 h-100 p-2">
                    <i class="fas fa-inbox fa-2x mb-2 d-block"></i>
                    <small>Messagerie</small>
                </a>
            </div>
            <div class="col-6">
                <a href="{% url 'communication:notification_list' %}" class="btn btn-outline-warning w-100 h-100 p-2">
                    <i class="fas fa-bell fa-2x mb-2 d-block"></i>
                    <small>Notifications</small>
                </a>
            </div>
            <div class="col-6">
                <a href="{% url 'communication:message_create' %}" class="btn btn-outline-success w-100 h-100 p-2">
                    <i class="fas fa-edit fa-2x mb-2 d-block"></i>
                    <small>Nouveau</small>
                </a>
            </div>
            <div class="col-6">
                <a href="{% url 'communication:liste_groupes' %}" class="btn btn-outline-info w-100 h-100 p-2">
                    <i class="fas fa-users fa-2x mb-2 d-block"></i>
                    <small>Groupes</small>
                </a>
            </div>
        </div>
        
        <!-- Dernière activité -->
        <div class="mt-3 pt-2 border-top">
            <small class="text-muted">
                <i class="fas fa-clock me-1"></i>
                Dernier message: 
                <span id="last-communication-activity">Chargement...</span>
            </small>
        </div>
    </div>
</div>

<script>
// Script pour le widget communication
document.addEventListener('DOMContentLoaded', function() {
    function updateWidgetBadges() {
        const msgCount = document.querySelector('#navMsgCount')?.textContent || '0';
        const notifCount = document.querySelector('#navNotifCount')?.textContent || '0';
        
        const msgWidget = document.querySelector('.msg-widget-count');
        const notifWidget = document.querySelector('.notif-widget-count');
        
        if (parseInt(msgCount) > 0 && msgWidget) {
            msgWidget.textContent = msgCount;
            msgWidget.style.display = 'inline';
        }
        if (parseInt(notifCount) > 0 && notifWidget) {
            notifWidget.textContent = notifCount;
            notifWidget.style.display = 'inline';
        }
    }
    
    // Charger la dernière activité
    function loadLastActivity() {
        fetch('{% url "communication:api_last_activity" %}')
            .then(response => response.json())
            .then(data => {
                const activityElement = document.getElementById('last-communication-activity');
                if (data.last_activity && activityElement) {
                    const date = new Date(data.last_activity);
                    activityElement.textContent = date.toLocaleDateString('fr-FR');
                } else if (activityElement) {
                    activityElement.textContent = 'Aucun';
                }
            })
            .catch(() => {
                const activityElement = document.getElementById('last-communication-activity');
                if (activityElement) {
                    activityElement.textContent = 'Erreur';
                }
            });
    }
    
    updateWidgetBadges();
    loadLastActivity();
    setInterval(updateWidgetBadges, 30000);
});
</script>'''
        },
        
        # 4. VUES API SUPPLEMENTAIRES
        'views_api': {
            'path': 'communication/api_views.py',
            'content': '''# communication/api_views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message, Notification

@login_required
def api_messages_count(request):
    """API pour le compteur de messages non lus"""
    try:
        unread_count = request.user.messages_recus.filter(est_lu=False).count()
        return JsonResponse({'unread_count': unread_count})
    except Exception as e:
        return JsonResponse({'unread_count': 0, 'error': str(e)})

@login_required  
def api_last_activity(request):
    """API pour la dernière activité de communication"""
    try:
        last_message = Message.objects.filter(
            Q(expediteur=request.user) | Q(destinataire=request.user)
        ).order_by('-date_envoi').first()
        
        last_activity = last_message.date_envoi if last_message else None
        
        return JsonResponse({
            'last_activity': last_activity.isoformat() if last_activity else None,
            'success': True
        })
    except Exception as e:
        return JsonResponse({
            'last_activity': None,
            'success': False,
            'error': str(e)
        })

@login_required
def api_communication_stats(request):
    """API pour les statistiques de communication"""
    try:
        stats = {
            'messages_non_lus': request.user.messages_recus.filter(est_lu=False).count(),
            'messages_recus_total': request.user.messages_recus.count(),
            'notifications_non_lues': Notification.objects.filter(user=request.user, est_lue=False).count(),
            'conversations_actives': 0,  # À adapter selon votre modèle
        }
        return JsonResponse({'stats': stats, 'success': True})
    except Exception as e:
        return JsonResponse({'stats': {}, 'success': False, 'error': str(e)})'''
        },
        
        # 5. MISE A JOUR DES URLS
        'urls_update': {
            'path': 'communication/urls_api.py',
            'content': '''# communication/urls_api.py
from django.urls import path
from . import api_views

app_name = 'communication_api'

urlpatterns = [
    path('api/messages/count/', api_views.api_messages_count, name='api_messages_count'),
    path('api/last-activity/', api_views.api_last_activity, name='api_last_activity'),
    path('api/stats/', api_views.api_communication_stats, name='api_communication_stats'),
]'''
        },
        
        # 6. SCRIPT D'INTEGRATION
        'integration_script': {
            'path': 'static/js/communication-integration.js',
            'content': '''// static/js/communication-integration.js
class CommunicationIntegration {
    constructor() {
        this.initialized = false;
        this.init();
    }
    
    init() {
        if (this.initialized) return;
        
        this.loadCounts();
        this.setupEventListeners();
        this.initialized = true;
        
        console.log('Communication Integration initialized');
    }
    
    loadCounts() {
        // Charger les compteurs de notifications
        this.fetchData('{% url "communication:notification_count" %}')
            .then(data => this.updateNotificationBadges(data.count))
            .catch(error => console.error('Failed to load notification count:', error));
        
        // Charger les compteurs de messages
        this.fetchData('{% url "communication:api_messages_count" %}')
            .then(data => this.updateMessageBadges(data.unread_count))
            .catch(error => console.error('Failed to load message count:', error));
    }
    
    fetchData(url) {
        return fetch(url)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            });
    }
    
    updateNotificationBadges(count) {
        const badges = document.querySelectorAll('.notif-count, .notif-count-sm, .sidebar-notif-count, .notif-widget-count');
        badges.forEach(badge => {
            if (count > 0) {
                badge.textContent = count;
                badge.style.display = 'inline';
            } else {
                badge.style.display = 'none';
            }
        });
    }
    
    updateMessageBadges(count) {
        const badges = document.querySelectorAll('.msg-count, .msg-count-sm, .sidebar-msg-count, .msg-widget-count');
        const mainBadge = document.querySelector('.communication-badge');
        const userBadge = document.querySelector('.user-msg-badge');
        
        badges.forEach(badge => {
            if (count > 0) {
                badge.textContent = count;
                badge.style.display = 'inline';
            } else {
                badge.style.display = 'none';
            }
        });
        
        // Badge principal
        if (mainBadge) {
            mainBadge.style.display = count > 0 ? 'inline' : 'none';
        }
        if (userBadge) {
            userBadge.textContent = count;
            userBadge.style.display = count > 0 ? 'inline' : 'none';
        }
    }
    
    setupEventListeners() {
        // Recharger les compteurs toutes les 30 secondes
        setInterval(() => this.loadCounts(), 30000);
        
        // Recharger quand la page redevient visible
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.loadCounts();
            }
        });
    }
}

// Initialisation automatique
document.addEventListener('DOMContentLoaded', function() {
    window.communicationIntegration = new CommunicationIntegration();
});'''
        }
    }
    
    # Instructions d'implémentation
    instructions = '''
# INSTRUCTIONS D'IMPLÉMENTATION - ACCÈS COMMUNICATION

## ÉTAPE 1: Sauvegardes
cp templates/includes/navbar.html templates/includes/navbar.html.backup

## ÉTAPE 2: Création des fichiers

### 2.1. Mettre à jour la navbar
- Remplacez le contenu de templates/includes/navbar.html par le contenu fourni

### 2.2. Créer les nouveaux fichiers:
- templates/includes/sidebar_communication.html
- templates/includes/communication_widget.html
- communication/api_views.py
- communication/urls_api.py
- static/js/communication-integration.js

## ÉTAPE 3: Intégration dans les dashboards

### 3.1. Dans core/dashboard.html:
Ajoutez ce code dans la section principale:
{% include "includes/communication_widget.html" %}

### 3.2. Dans chaque sidebar spécifique:
Ajoutez après le menu principal:
{% include "includes/sidebar_communication.html" %}

## ÉTAPE 4: Mise à jour des URLs principales

Dans communication/urls.py, ajoutez:
from .urls_api import urlpatterns as api_urls
urlpatterns += api_urls

## ÉTAPE 5: Vérifications

1. Vérifiez que les URLs existent:
   - communication:notification_count
   - communication:api_messages_count
   - communication:api_last_activity

2. Testez l\'accès:
   - Connectez-vous
   - Vérifiez la navbar
   - Testez les liens

## ÉTAPE 6: Personnalisation (optionnel)

Adaptez les couleurs et styles dans le CSS selon votre thème.

## RÉSULTAT ATTENDU:
✅ Menu Communication dans la navbar
✅ Badges dynamiques pour messages non lus
✅ Widget communication dans les dashboards
✅ Sidebar communication dans toutes les pages
✅ Actualisation automatique toutes les 30s
'''

    # Affichage des contenus
    print("=" * 80)
    print("SCRIPT D'IMPLÉMENTATION - ACCÈS COMMUNICATION UNIVERSEL")
    print("=" * 80)
    
    for file_name, file_info in files_content.items():
        print(f"\n{file_name.upper()}:")
        print("=" * 40)
        print(f"Fichier: {file_info['path']}")
        print("-" * 40)
        print(file_info['content'])
        print("\n" + "=" * 40)
    
    print("\nINSTRUCTIONS:")
    print("=" * 40)
    print(instructions)
    
    # Script de déploiement automatique
    deploy_script = '''#!/bin/bash
# deploy_communication_access.sh

echo "Déploiement de l'accès communication..."

# Sauvegardes
echo "✓ Création des sauvegardes..."
cp templates/includes/navbar.html templates/includes/navbar.html.backup.$(date +%Y%m%d_%H%M%S)

# Création des fichiers
echo "✓ Création des nouveaux fichiers..."

# Sidebar communication
cat > templates/includes/sidebar_communication.html << 'EOF'
''' + files_content['sidebar_communication']['content'] + '''
EOF

# Widget dashboard
cat > templates/includes/communication_widget.html << 'EOF'
''' + files_content['dashboard_widget']['content'] + '''
EOF

# API Views
cat > communication/api_views.py << 'EOF'
''' + files_content['views_api']['content'] + '''
EOF

# URLs API
cat > communication/urls_api.py << 'EOF'
''' + files_content['urls_update']['content'] + '''
EOF

# Script JS
cat > static/js/communication-integration.js << 'EOF'
''' + files_content['integration_script']['content'] + '''
EOF

# Mise à jour de la navbar
cat > templates/includes/navbar.html << 'EOF'
''' + files_content['navbar_updated']['content'] + '''
EOF

echo "✓ Fichiers créés avec succès!"
echo ""
echo "NEXT STEPS:"
echo "1. Intégrez le widget dans vos dashboards"
echo "2. Ajoutez la sidebar dans vos templates"
echo "3. Mettez à jour les URLs dans communication/urls.py"
echo "4. Testez l'accès: python manage.py runserver"
echo ""
echo "Déploiement terminé! 🎉"
'''

    print("\nSCRIPT DE DÉPLOIEMENT AUTOMATIQUE:")
    print("=" * 40)
    print(deploy_script)

except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Assurez-vous que Django est configuré correctement")
except Exception as e:
    print(f"Erreur: {e}")