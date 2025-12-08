class MessagerieAvancee {
    constructor() {
        this.fichiersSelectionnes = [];
        this.currentConversation = null;
        this.init();
    }

    init() {
        this.initEventListeners();
        this.initWebSocket();
        this.chargerConversations();
    }

    initEventListeners() {
        // Gestion des fichiers
        document.getElementById('btn-ajouter-fichier').addEventListener('click', () => {
            document.getElementById('fichier-input').click();
        });

        document.getElementById('fichier-input').addEventListener('change', (e) => {
            this.gererSelectionFichiers(e.target.files);
        });

        // Soumission du formulaire
        document.getElementById('message-form').addEventListener('submit', (e) => {
            this.envoyerMessage(e);
        });

        // Conversations
        document.querySelectorAll('.conversation-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                this.chargerConversation(
                    item.dataset.conversationId,
                    item.dataset.userId
                );
            });
        });
    }

    gererSelectionFichiers(files) {
        if (files.length === 0) return;

        const preview = document.getElementById('pieces-jointes-preview');
        const container = document.getElementById('fichiers-selectionnes');
        
        container.innerHTML = '';

        Array.from(files).forEach(file => {
            if (this.verifierFichier(file)) {
                this.fichiersSelectionnes.push(file);
                this.afficherFichierPreview(file, container);
            }
        });

        preview.style.display = 'block';
    }

    verifierFichier(file) {
        const maxSize = 10 * 1024 * 1024; // 10MB
        const extensionsPermises = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.jpg', '.jpeg', '.png', '.txt', '.zip'];

        if (file.size > maxSize) {
            this.afficherErreur(`Le fichier ${file.name} est trop volumineux (max 10MB)`);
            return false;
        }

        const extension = '.' + file.name.split('.').pop().toLowerCase();
        if (!extensionsPermises.includes(extension)) {
            this.afficherErreur(`Le format ${extension} n'est pas autorisé`);
            return false;
        }

        return true;
    }

    afficherFichierPreview(file, container) {
        const div = document.createElement('div');
        div.className = 'd-flex justify-content-between align-items-center mb-2 fichier-item p-2 rounded';
        
        div.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-file ${this.getFileIcon(file)} me-2 text-primary"></i>
                <div>
                    <div class="small">${file.name}</div>
                    <div class="text-muted extra-small">${this.formatTaille(file.size)}</div>
                </div>
            </div>
            <button type="button" class="btn btn-sm btn-outline-danger btn-supprimer-fichier">
                <i class="fas fa-times"></i>
            </button>
        `;

        div.querySelector('.btn-supprimer-fichier').addEventListener('click', () => {
            this.supprimerFichier(file, div);
        });

        container.appendChild(div);
    }

    getFileIcon(file) {
        const extension = '.' + file.name.split('.').pop().toLowerCase();
        const icons = {
            '.pdf': 'fa-file-pdf',
            '.doc': 'fa-file-word',
            '.docx': 'fa-file-word',
            '.xls': 'fa-file-excel',
            '.xlsx': 'fa-file-excel',
            '.jpg': 'fa-file-image',
            '.jpeg': 'fa-file-image',
            '.png': 'fa-file-image',
            '.txt': 'fa-file-alt',
            '.zip': 'fa-file-archive'
        };
        return icons[extension] || 'fa-file';
    }

    formatTaille(bytes) {
        if (bytes < 1024) return bytes + ' o';
        else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' Ko';
        else return (bytes / 1048576).toFixed(1) + ' Mo';
    }

    supprimerFichier(file, element) {
        this.fichiersSelectionnes = this.fichiersSelectionnes.filter(f => f !== file);
        element.remove();
        
        if (this.fichiersSelectionnes.length === 0) {
            document.getElementById('pieces-jointes-preview').style.display = 'none';
        }
    }

    async envoyerMessage(e) {
        e.preventDefault();

        const formData = new FormData();
        const messageText = document.getElementById('message-text').value;

        // Ajouter les données du message
        formData.append('destinataire_id', document.getElementById('destinataire_id').value);
        formData.append('titre', 'Message privé');
        formData.append('contenu', messageText);
        formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

        // Ajouter les fichiers
        this.fichiersSelectionnes.forEach(file => {
            formData.append('pieces_jointes', file);
        });

        try {
            const response = await fetch('/communication/envoyer-message/', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                this.reinitialiserFormulaire();
                this.chargerMessages(this.currentConversation);
            } else {
                this.afficherErreur('Erreur lors de l\'envoi du message');
            }
        } catch (error) {
            console.error('Erreur:', error);
            this.afficherErreur('Erreur de connexion');
        }
    }

    reinitialiserFormulaire() {
        document.getElementById('message-text').value = '';
        document.getElementById('fichier-input').value = '';
        document.getElementById('pieces-jointes-preview').style.display = 'none';
        this.fichiersSelectionnes = [];
    }

    afficherMessageAvecFichiers(message) {
        const messagesList = document.getElementById('messages-list');
        const messageDiv = document.createElement('div');
        
        messageDiv.className = `message ${message.est_expediteur ? 'message-envoye' : 'message-recu'} 
                               ${message.pieces_jointes.length > 0 ? 'message-fichier' : ''}`;
        
        let fichiersHTML = '';
        if (message.pieces_jointes && message.pieces_jointes.length > 0) {
            fichiersHTML = `
                <div class="pieces-jointes mt-2">
                    <div class="small text-muted mb-1">
                        <i class="fas fa-paperclip me-1"></i>Fichiers joints:
                    </div>
                    <div class="fichiers-list">
                        ${message.pieces_jointes.map(fichier => `
                            <div class="fichier-item d-flex align-items-center p-2 border rounded mb-1">
                                <i class="fas ${this.getFileIconFromType(fichier.type_fichier)} me-2 text-primary"></i>
                                <div class="flex-grow-1">
                                    <div class="small">${fichier.nom_original}</div>
                                    <div class="extra-small text-muted">${fichier.get_taille_lisible}</div>
                                </div>
                                <a href="/communication/telecharger/${fichier.id}/" 
                                   class="btn btn-sm btn-outline-primary" 
                                   target="_blank" 
                                   title="Télécharger">
                                    <i class="fas fa-download"></i>
                                </a>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        messageDiv.innerHTML = `
            <div class="message-header d-flex justify-content-between">
                <strong>${message.expediteur_nom}</strong>
                <small class="text-muted">${message.date_envoi}</small>
            </div>
            <div class="message-content">
                ${message.contenu}
            </div>
            ${fichiersHTML}
        `;

        messagesList.appendChild(messageDiv);
        this.scrollToBottom();
    }

    getFileIconFromType(typeFichier) {
        const icons = {
            'PDF': 'fa-file-pdf',
            'Word': 'fa-file-word',
            'Excel': 'fa-file-excel',
            'Image': 'fa-file-image',
            'Texte': 'fa-file-alt',
            'Archive': 'fa-file-archive'
        };
        return icons[typeFichier] || 'fa-file';
    }

    // ... autres méthodes existantes
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    new MessagerieAvancee();
});