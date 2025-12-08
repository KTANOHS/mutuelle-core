
// Intégration Messagerie - Badge de notifications
document.addEventListener('DOMContentLoaded', function() {
    // Mettre à jour le badge de notifications
    function updateNotificationBadge() {
        fetch('/communication/notifications/count/')
            .then(response => response.json())
            .then(data => {
                const badge = document.getElementById('notification-badge');
                const unreadSpan = document.getElementById('unread-messages');
                
                if (badge && data.unread_count > 0) {
                    badge.textContent = data.unread_count;
                    badge.style.display = 'inline';
                } else if (badge) {
                    badge.style.display = 'none';
                }
                
                if (unreadSpan) {
                    unreadSpan.textContent = data.unread_count || 0;
                }
            })
            .catch(error => {
                console.log('Erreur lors du chargement des notifications:', error);
            });
    }
    
    // Mettre à jour toutes les 30 secondes
    updateNotificationBadge();
    setInterval(updateNotificationBadge, 30000);
    
    // Animation pour la carte messagerie
    const messagingCard = document.querySelector('.card [href*="messagerie"]');
    if (messagingCard) {
        messagingCard.addEventListener('mouseenter', function() {
            this.closest('.card').style.transform = 'translateY(-5px)';
            this.closest('.card').style.transition = 'transform 0.3s ease';
        });
        
        messagingCard.addEventListener('mouseleave', function() {
            this.closest('.card').style.transform = 'translateY(0)';
        });
    }
    
    console.log('✅ Intégration messagerie initialisée');
});
