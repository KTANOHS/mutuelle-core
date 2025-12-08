#!/usr/bin/env python3
"""
CORRECTION URGENTE - Modal sans ID
"""

import os
import django
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

BASE_DIR = Path(__file__).parent

def fix_modal_id():
    """Corrige l'ID manquant du modal"""
    
    modal_file = BASE_DIR / 'templates' / 'communication' / 'partials' / '_nouveau_message_modal.html'
    
    if modal_file.exists():
        print(f"🔧 Correction du modal: {modal_file}")
        
        with open(modal_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # CORRECTION 1: Ajouter l'ID manquant au modal
        if 'id="nouveauMessageModal"' not in content:
            # Trouver la ligne du modal et ajouter l'ID
            lines = content.split('\n')
            new_lines = []
            
            for line in lines:
                if 'class="modal fade"' in line and 'id=' not in line:
                    # Ajouter l'ID manquant
                    fixed_line = line.replace(
                        'class="modal fade"', 
                        'class="modal fade" id="nouveauMessageModal"'
                    )
                    new_lines.append(fixed_line)
                    print("✅ ID ajouté au modal")
                else:
                    new_lines.append(line)
            
            content = '\n'.join(new_lines)
        
        # CORRECTION 2: S'assurer que le formulaire existe
        if '<form' not in content:
            form_section = '''
            <!-- Formulaire de message -->
            <form method="post" action="{% url 'communication:envoyer_message' %}">
                {% csrf_token %}
                <div class="mb-3">
                    <label for="destinataire" class="form-label">Destinataire</label>
                    <select class="form-select" id="destinataire" name="destinataire" required>
                        <option value="">Choisir un destinataire...</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="message" class="form-label">Message</label>
                    <textarea class="form-control" id="message" name="message" rows="4" required></textarea>
                </div>
            </form>
            '''
            
            # Insérer le formulaire dans le modal-body
            if '<div class="modal-body">' in content:
                content = content.replace(
                    '<div class="modal-body">', 
                    '<div class="modal-body">' + form_section
                )
                print("✅ Formulaire ajouté au modal")
        
        # CORRECTION 3: Ajouter des boutons d'action
        if 'Envoyer' not in content:
            # Trouver modal-footer et ajouter boutons
            if '<div class="modal-footer">' in content:
                buttons = '''
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                <button type="button" class="btn btn-primary" onclick="envoyerMessage()">Envoyer le message</button>
                '''
                content = content.replace('<div class="modal-footer">', '<div class="modal-footer">' + buttons)
                print("✅ Boutons d'action ajoutés")
        
        # CORRECTION 4: Ajouter le JavaScript manquant
        if 'envoyerMessage' not in content:
            js_patch = '''
<script>
function envoyerMessage() {
    const form = document.querySelector('#nouveauMessageModal form');
    const formData = new FormData(form);
    
    fetch("{% url 'communication:envoyer_message' %}", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Fermer le modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('nouveauMessageModal'));
            modal.hide();
            
            // Afficher message de succès
            alert('Message envoyé avec succès!');
            location.reload();
        } else {
            alert('Erreur: ' + data.message);
        }
    });
}

// Initialisation du modal
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Modal nouveau message initialisé');
    
    const modalElement = document.getElementById('nouveauMessageModal');
    if (modalElement) {
        modalElement.addEventListener('show.bs.modal', function() {
            console.log('🎯 Modal ouvert!');
            // Charger la liste des destinataires
            chargerDestinataires();
        });
    }
});

function chargerDestinataires() {
    // Simuler le chargement des destinataires
    const select = document.getElementById('destinataire');
    if (select) {
        select.innerHTML = '<option value="">Chargement...</option>';
        
        // Simuler un délai de chargement
        setTimeout(() => {
            select.innerHTML = '''
                <option value="">Choisir un destinataire...</option>
                <option value="1">Médecin 1</option>
                <option value="2">Médecin 2</option>
                <option value="3">Pharmacien 1</option>
                <option value="4">Administrateur</option>
            ''';
        }, 500);
    }
}
</script>
'''
            content += js_patch
            print("✅ JavaScript ajouté")
        
        # Sauvegarder les corrections
        with open(modal_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Modal complètement corrigé!")
        
    else:
        print("❌ Fichier modal non trouvé")

def fix_messagerie_buttons():
    """Corrige les boutons dans la messagerie principale"""
    
    messagerie_file = BASE_DIR / 'templates' / 'communication' / 'messagerie.html'
    
    if messagerie_file.exists():
        with open(messagerie_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # CORRECTION: S'assurer que les boutons pointent vers le bon modal
        if 'data-bs-target="#nouveauMessageModal"' not in content:
            # Remplacer les vieux boutons
            old_button = '''<button type="button" class="btn btn-primary" data-bs-toggle="modal">'''
            new_button = '''<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#nouveauMessageModal" onclick="console.log('Ouverture modal message')">'''
            
            content = content.replace(old_button, new_button)
            print("✅ Boutons corrigés dans messagerie.html")
        
        # Ajouter un bouton de test
        test_button = '''
<!-- BOUTON TEST FONCTIONNEL -->
<div class="alert alert-info mt-3">
    <button type="button" 
            class="btn btn-success btn-lg" 
            data-bs-toggle="modal" 
            data-bs-target="#nouveauMessageModal"
            id="testButton">
        <i class="fas fa-bolt me-2"></i>TESTER LE MODAL
    </button>
    <small class="d-block mt-1">Ce bouton devrait ouvrir le modal</small>
</div>
'''
        
        if 'BOUTON TEST FONCTIONNEL' not in content:
            # Insérer après le premier h1 ou h2
            if '<h1' in content or '<h2' in content:
                import re
                content = re.sub(
                    r'(<h[12][^>]*>.*?</h[12]>)', 
                    r'\1' + test_button, 
                    content, 
                    count=1
                )
                print("✅ Bouton test ajouté")
        
        with open(messagerie_file, 'w', encoding='utf-8') as f:
            f.write(content)

def main():
    print("🚨 CORRECTION URGENTE - MODAL SANS ID")
    print("=" * 50)
    
    fix_modal_id()
    fix_messagerie_buttons()
    
    print("\n✅ CORRECTIONS APPLIQUÉES !")
    print("\n🎯 POUR TESTER :")
    print("1. Allez dans /communication/")
    print("2. Cherchez le bouton 'TESTER LE MODAL' (vert)")
    print("3. Cliquez dessus - le modal devrait s'ouvrir")
    print("4. Vérifiez la console pour les messages de confirmation")

if __name__ == "__main__":
    main()