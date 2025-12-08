// Gestion de la liste des membres
class ListeMembresManager {
    constructor() {
        this.membres = [];
        this.currentPage = 1;
        this.itemsPerPage = 10;
        this.filters = {};
        this.selectedMembres = new Set();
    }

    // Méthodes d'initialisation et de gestion...
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    window.membresManager = new ListeMembresManager();
    window.membresManager.loadMembres();
});