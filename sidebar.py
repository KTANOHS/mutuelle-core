
<!-- templates/assureur/partials/_sidebar.html -->
<div class="sidebar">
    <!-- Menu assureur principal -->
    <div class="card mb-4">
        <div class="card-header">
            <h6 class="mb-0">Menu Assureur</h6>
        </div>
        <div class="card-body p-0">
            <div class="list-group list-group-flush">
                <a href="{% url 'assureur:dashboard' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-tachometer-alt me-2"></i>Tableau de bord
                </a>
                <a href="{% url 'assureur:liste_membres' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-users me-2"></i>Membres
                </a>
                <a href="{% url 'assureur:liste_bons' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-file-invoice me-2"></i>Bons de soins
                </a>
                <a href="{% url 'assureur:liste_paiements' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-money-bill-wave me-2"></i>Paiements
                </a>
                <a href="{% url 'assureur:liste_soins' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-stethoscope me-2"></i>Soins médicaux
                </a>
                <a href="{% url 'assureur:rapports' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-chart-bar me-2"></i>Rapports
                </a>
            </div>
        </div>
    </div>
    
    <!-- SIDEBAR COMMUNICATION -->
    {% include "includes/sidebar_communication.html" %}
</div>
