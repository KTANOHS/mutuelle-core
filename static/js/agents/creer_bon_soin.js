// Configuration
const config = {
    minSearchLength: 3,
    apiEndpoints: {
        searchMembers: '/membres/api/search/',
        verifyCotisation: '/agents/verifier-cotisation/',
        createBonSoin: '/agents/creer-bon-soin/',
        getMedecins: '/medecin/api/list/',
        getStats: '/agents/api/stats-quotidiens/'
    }
};

// Éléments DOM
const elements = {
    searchMember: document.getElementById('search-member'),
    searchBtn: document.getElementById('search-btn'),
    membersList: document.getElementById('members-list'),
    memberResults: document.getElementById('member-results'),
    selectedMember: document.getElementById('selected-member'),
    memberDetails: document.getElementById('member-details'),
    deselectMember: document.getElementById('deselect-member'),
    verifierCotisation: document.getElementById('verifier-cotisation'),
    cotisationStatus: document.getElementById('cotisation-status'),
    nextStep1: document.getElementById('next-step-1'),
    step1: document.getElementById('step-1'),
    step2: document.getElementById('step-2'),
    prevStep2: document.getElementById('prev-step-2'),
    medecinSelect: document.getElementById('medecin_id'),
    bonForm: document.getElementById('bon-soin-form'),
    submitBtn: document.getElementById('submit-btn')
};

// État de l'application
let state = {
    selectedMember: null,
    currentStep: 1
};

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    loadMedecins();
    updateStats();
});

function initializeEventListeners() {
    // Recherche de membres
    elements.searchBtn.addEventListener('click', searchMembers);
    elements.searchMember.addEventListener('input', function(e) {
        if (e.target.value.length >= config.minSearchLength) {
            searchMembers();
        }
    });

    // Navigation des étapes
    elements.nextStep1.addEventListener('click', nextStep);
    elements.prevStep2.addEventListener('click', prevStep);

    // Désélection du membre
    elements.deselectMember.addEventListener('click', deselectMember);

    // Vérification de cotisation
    elements.verifierCotisation.addEventListener('click', verifyCotisation);

    // Soumission du formulaire
    elements.bonForm.addEventListener('submit', submitForm);
}

// Recherche de membres
function searchMembers() {
    const query = elements.searchMember.value.trim();
    if (query.length < config.minSearchLength) {
        showAlert('Veuillez saisir au moins 3 caractères', 'warning');
        return;
    }

    showLoading(elements.membersList, 'Recherche en cours...');

    fetch(`${config.apiEndpoints.searchMembers}?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            if (data.membres && data.membres.length > 0) {
                displayMembers(data.membres);
            } else {
                showNoResults();
            }
        })
        .catch(error => {
            console.error('Erreur recherche:', error);
            showAlert('Erreur lors de la recherche', 'danger');
        });
}

// Affichage des résultats
function displayMembers(membres) {
    elements.membersList.innerHTML = '';
    
    membres.forEach(membre => {
        const memberItem = document.createElement('button');
        memberItem.type = 'button';
        memberItem.className = 'list-group-item list-group-item-action';
        memberItem.innerHTML = `
            <div class="d-flex w-100 justify-content-between align-items-start">
                <div>
                    <h6 class="mb-1">${membre.nom_complet}</h6>
                    <small class="text-muted">
                        <i class="fas fa-id-card me-1"></i>Membre #${membre.numero}<br>
                        <i class="fas fa-phone me-1"></i>${membre.telephone}<br>
                        <i class="fas fa-calendar me-1"></i>Inscrit le ${membre.date_inscription}
                    </small>
                </div>
                <span class="badge bg-primary rounded-pill">Sélectionner</span>
            </div>
        `;
        memberItem.addEventListener('click', () => selectMember(membre));
        elements.membersList.appendChild(memberItem);
    });
    
    elements.memberResults.style.display = 'block';
}

// Sélection d'un membre
function selectMember(membre) {
    state.selectedMember = membre;
    
    // Mettre à jour l'interface
    elements.searchMember.value = membre.nom_complet;
    elements.memberResults.style.display = 'none';
    elements.memberDetails.innerHTML = `
        <strong>Nom:</strong> ${membre.nom_complet}<br>
        <strong>Numéro:</strong> ${membre.numero}<br>
        <strong>Téléphone:</strong> ${membre.telephone}<br>
        <strong>Date inscription:</strong> ${membre.date_inscription}
    `;
    elements.selectedMember.style.display = 'block';
    elements.nextStep1.disabled = false;
    
    // Réinitialiser le statut de cotisation
    elements.cotisationStatus.innerHTML = '';
}

// Vérification de cotisation
function verifyCotisation() {
    if (!state.selectedMember) return;

    showLoading(elements.cotisationStatus, 'Vérification en cours...');

    fetch(`${config.apiEndpoints.verifyCotisation}${state.selectedMember.id}/`)
        .then(response => response.json())
        .then(data => {
            if (data.est_a_jour) {
                elements.cotisationStatus.innerHTML = `
                    <div class="alert alert-success mb-0">
                        <i class="fas fa-check-circle me-2"></i>
                        <strong>Membre à jour</strong> de sa cotisation
                        ${data.prochaine_echeance ? `<br><small>Prochaine échéance: ${data.prochaine_echeance}</small>` : ''}
                    </div>
                `;
            } else {
                elements.cotisationStatus.innerHTML = `
                    <div class="alert alert-danger mb-0">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        <strong>Membre non à jour</strong> de sa cotisation
                        ${data.prochaine_echeance ? `<br><small>Dernière échéance: ${data.prochaine_echeance}</small>` : ''}
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Erreur vérification:', error);
            elements.cotisationStatus.innerHTML = `
                <div class="alert alert-warning mb-0">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Erreur lors de la vérification
                </div>
            `;
        });
}

// Navigation entre les étapes
function nextStep() {
    if (!state.selectedMember) {
        showAlert('Veuillez sélectionner un membre', 'warning');
        return;
    }
    
    elements.step1.style.display = 'none';
    elements.step2.style.display = 'block';
    state.currentStep = 2;
}

function prevStep() {
    elements.step2.style.display = 'none';
    elements.step1.style.display = 'block';
    state.currentStep = 1;
}

// Chargement des médecins
function loadMedecins() {
    fetch(config.apiEndpoints.getMedecins)
        .then(response => response.json())
        .then(data => {
            elements.medecinSelect.innerHTML = '<option value="">Sélectionner un médecin...</option>';
            
            if (data.medecins && data.medecins.length > 0) {
                data.medecins.forEach(medecin => {
                    const option = document.createElement('option');
                    option.value = medecin.id;
                    option.textContent = `Dr. ${medecin.nom} - ${medecin.specialite}`;
                    elements.medecinSelect.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error('Erreur chargement médecins:', error);
        });
}

// Soumission du formulaire
function submitForm(e) {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    const formData = {
        membre_id: state.selectedMember.id,
        montant_max: document.getElementById('montant_max').value,
        motif: document.getElementById('motif').value,
        medecin_id: elements.medecinSelect.value
    };

    // Désactiver le bouton de soumission
    elements.submitBtn.disabled = true;
    elements.submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Création...';

    fetch(config.apiEndpoints.createBonSoin, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccessModal(data.bon_soin);
            updateStats();
        } else {
            showAlert('Erreur: ' + data.message, 'danger');
            elements.submitBtn.disabled = false;
            elements.submitBtn.innerHTML = '<i class="fas fa-save me-1"></i>Créer le Bon de Soin';
        }
    })
    .catch(error => {
        console.error('Erreur soumission:', error);
        showAlert('Erreur lors de la création du bon', 'danger');
        elements.submitBtn.disabled = false;
        elements.submitBtn.innerHTML = '<i class="fas fa-save me-1"></i>Créer le Bon de Soin';
    });
}

// Validation du formulaire
function validateForm() {
    const montantMax = document.getElementById('montant_max').value;
    const motif = document.getElementById('motif').value;
    const medecinId = elements.medecinSelect.value;

    if (!montantMax || montantMax <= 0) {
        showAlert('Veuillez saisir un montant maximum valide', 'warning');
        return false;
    }

    if (!motif.trim()) {
        showAlert('Veuillez décrire le motif de consultation', 'warning');
        return false;
    }

    if (!medecinId) {
        showAlert('Veuillez sélectionner un médecin', 'warning');
        return false;
    }

    return true;
}

// Affichage du modal de succès
function showSuccessModal(bonSoin) {
    document.getElementById('bon-code').textContent = bonSoin.code;
    document.getElementById('bon-expiration').textContent = bonSoin.date_expiration;
    document.getElementById('bon-montant').textContent = bonSoin.montant_max;
    document.getElementById('bon-medecin').textContent = 
        elements.medecinSelect.options[elements.medecinSelect.selectedIndex].text;
    
    const modal = new bootstrap.Modal(document.getElementById('bonCreatedModal'));
    modal.show();
}

// Utilitaires
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insérer au début du formulaire
    elements.bonForm.prepend(alertDiv);
    
    // Supprimer automatiquement après 5 secondes
    setTimeout(() => {
        if (alertDiv.parentElement) {
            alertDiv.remove();
        }
    }, 5000);
}

function showLoading(element, message = 'Chargement...') {
    element.innerHTML = `
        <div class="text-center text-muted">
            <i class="fas fa-spinner fa-spin me-2"></i>
            ${message}
        </div>
    `;
}

function showNoResults() {
    elements.membersList.innerHTML = `
        <div class="text-center text-muted py-3">
            <i class="fas fa-search me-2"></i>
            Aucun membre trouvé
        </div>
    `;
    elements.memberResults.style.display = 'block';
}

function deselectMember() {
    state.selectedMember = null;
    elements.selectedMember.style.display = 'none';
    elements.nextStep1.disabled = true;
    elements.searchMember.value = '';
    elements.cotisationStatus.innerHTML = '';
}

function updateStats() {
    fetch(config.apiEndpoints.getStats)
        .then(response => response.json())
        .then(data => {
            document.getElementById('today-count').textContent = data.bons_du_jour;
            document.getElementById('remaining-count').textContent = data.limite_restante;
        });
}

// Fonctions globales pour les boutons du modal
function imprimerBon() {
    window.print();
}

function creerNouveauBon() {
    // Réinitialiser le formulaire
    elements.bonForm.reset();
    deselectMember();
    prevStep();
    
    // Fermer le modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('bonCreatedModal'));
    modal.hide();
    
    // Remettre le focus sur la recherche
    elements.searchMember.focus();
}