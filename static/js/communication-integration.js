// static/js/communication-integration.js
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
});
