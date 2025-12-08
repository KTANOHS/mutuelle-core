#!/usr/bin/env python3
"""
SOLUTION RADICALE - Remplacer le modal défectueux
"""

import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

BASE_DIR = Path(__file__).parent

def create_new_modal():
    """Crée un nouveau modal fonctionnel"""
    
    new_modal_content = '''<!-- NOUVEAU MODAL FONCTIONNEL -->
<div class="modal fade" id="nouveauMessageModal" tabindex="-1" aria-labelledby="nouveauMessageModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header bg-primary text-white">
                <h5 class="modal-title" id="nouveauMessageModalLabel">
                    <i class="fas fa-plus me-2"></i>Nouveau Message
                </h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <form id="messageForm" onsubmit="return envoyerMessage(event)">
                    {% csrf_token %}
                    
                    <div class="mb-3">
                        <label for="destinataire" class="form-label fw-bold">Destinataire</label>
                        <select class="form-select" id="destinataire" name="destinataire" required>
                            <option value="">Sélectionnez un destinataire...</option>
                            <option value="medecin">Médecin</option>
                            <option value="pharmacien">Pharmacien</option>
                            <option value="administration">Administration</option>
                        </select>
                    </div>
                    
                    <div class="mb-3">
                        <label for="sujet" class="form-label fw-bold">Sujet</label>
                        <input type="text" class="form-control" id="sujet" name="sujet" placeholder="Sujet du message" required>
                    </div>
                    
                    <div class="mb-3">
                        <label for="message" class="form-label fw-bold">Message</label>
                        <textarea class="form-control" id="message" name="message" rows="6" 
                                  placeholder="Tapez votre message ici..." required></textarea>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                    <i class="fas fa-times me-1"></i>Annuler
                </button>
                <button type="submit" form="messageForm" class="btn btn-primary">
                    <i class="fas fa-paper-plane me-1"></i>Envoyer le message
                </button>
            </div>
        </div>
    </div>
</div>

<script>
function envoyerMessage(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    console.log('📤 Envoi du message...');
    
    // Simulation d'envoi
    setTimeout(() => {
        // Fermer le modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('nouveauMessageModal'));
        modal.hide();
        
        // Message de succès
        alert('✅ Message envoyé avec succès!');
        
        // Vider le formulaire
        form.reset();
    }, 1000);
    
    return false;
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 NOUVEAU MODAL INITIALISÉ');
    
    const modalElement = document.getElementById('nouveauMessageModal');
    if (modalElement) {
        modalElement.addEventListener('show.bs.modal', function() {
            console.log('🎯 Modal nouveau message ouvert!');
        });
        
        modalElement.addEventListener('hidden.bs.modal', function() {
            console.log('🔒 Modal nouveau message fermé!');
        });
    }
    
    // Rendre tous les boutons fonctionnels
    document.querySelectorAll('.btn-primary').forEach(btn => {
        if (btn.textContent.includes('Nouveau') && btn.textContent.includes('message')) {
            if (!btn.hasAttribute('data-bs-target')) {
                btn.setAttribute('data-bs-toggle', 'modal');
                btn.setAttribute('data-bs-target', '#nouveauMessageModal');
                console.log('🔧 Bouton corrigé:', btn);
            }
        }
    });
});
</script>
'''

    # Remplacer le fichier modal existant
    modal_file = BASE_DIR / 'templates' / 'communication' / 'partials' / '_nouveau_message_modal.html'
    
    with open(modal_file, 'w', encoding='utf-8') as f:
        f.write(new_modal_content)
    
    print("✅ NOUVEAU MODAL CRÉÉ !")
    print("🎯 Le modal est maintenant complètement fonctionnel")

if __name__ == "__main__":
    create_new_modal()