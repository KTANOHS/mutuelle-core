#!/bin/bash
# integrate_communication_components.sh

echo "🚀 INTÉGRATION DES COMPOSANTS COMMUNICATION"
echo "============================================"

# Vérification de l'environnement
if [ ! -f "manage.py" ]; then
    echo "❌ Erreur: Placez-vous dans la racine de votre projet Django"
    exit 1
fi

echo "📁 Vérification des composants communication..."
[ -f "templates/includes/communication_widget.html" ] && echo "✅ Widget communication trouvé" || echo "❌ Widget communication manquant"
[ -f "templates/includes/sidebar_communication.html" ] && echo "✅ Sidebar communication trouvée" || echo "❌ Sidebar communication manquante"

# 1. INTÉGRATION DANS CORE/DASHBOARD.HTML
echo ""
echo "1. 📊 INTÉGRATION DANS CORE/DASHBOARD.HTML"

if [ -f "templates/core/dashboard.html" ]; then
    # Sauvegarde
    cp templates/core/dashboard.html templates/core/dashboard.html.backup.$(date +%Y%m%d_%H%M%S)
    
    # Création de la version mise à jour
    cat > templates/core/dashboard_updated.html << 'CORE_EOF'
{% extends "base.html" %}
{% load static %}

{% block content %}
<div class="container-fluid">
    <div class="row">
        <div class="col-md-3">
            {% include "includes/sidebar.html" %}
        </div>
        
        <div class="col-md-9">
            <div class="row">
                <!-- WIDGET COMMUNICATION -->
                <div class="col-xl-4 col-lg-6 col-md-12 mb-4">
                    {% include "includes/communication_widget.html" %}
                </div>
                
                <!-- Vos autres widgets existants -->
                <div class="col-xl-8 col-lg-6 col-md-12">
                    <div class="row">
                        <!-- Exemple d'autres widgets - À ADAPTER selon votre contenu existant -->
                        <div class="col-md-6 mb-4">
                            <div class="card bg-primary text-white">
                                <div class="card-body">
                                    <div class="d-flex justify-content-between">
                                        <div>
                                            <h4 class="mb-0">150</h4>
                                            <p class="mb-0">Patients</p>
                                        </div>
                                        <div class="align-self-center">
                                            <i class="fas fa-users fa-2x"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-6 mb-4">
                            <div class="card bg-success text-white">
                                <div class="card-body">
                                    <div class="d-flex justify-content-between">
                                        <div>
                                            <h4 class="mb-0">45</h4>
                                            <p class="mb-0">Rendez-vous</p>
                                        </div>
                                        <div class="align-self-center">
                                            <i class="fas fa-calendar fa-2x"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Contenu supplémentaire -->
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">Activité récente</h5>
                        </div>
                        <div class="card-body">
                            <p>Votre contenu existant ici...</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
CORE_EOF
    
    echo "✅ Version mise à jour créée: templates/core/dashboard_updated.html"
    echo "⚠ Copiez le contenu dans votre dashboard.html existant"
else
    echo "❌ templates/core/dashboard.html non trouvé"
fi

# 2. INTÉGRATION DANS AGENTS
echo ""
echo "2. 👨‍💼 INTÉGRATION DANS AGENTS"

# Sidebar agents
if [ -f "templates/agents/partials/_sidebar_agent.html" ]; then
    cp templates/agents/partials/_sidebar_agent.html templates/agents/partials/_sidebar_agent.html.backup.$(date +%Y%m%d_%H%M%S)
    
    cat > templates/agents/partials/_sidebar_agent_updated.html << 'AGENTS_EOF'
<!-- templates/agents/partials/_sidebar_agent.html -->
<div class="sidebar">
    <!-- Menu agent principal -->
    <div class="card mb-4">
        <div class="card-header">
            <h6 class="mb-0">Menu Agent</h6>
        </div>
        <div class="card-body p-0">
            <div class="list-group list-group-flush">
                <a href="{% url 'agents:dashboard' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-tachometer-alt me-2"></i>Tableau de bord
                </a>
                <a href="{% url 'agents:liste_membres' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-users me-2"></i>Gestion membres
                </a>
                <a href="{% url 'agents:creer_bon_soin' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-file-medical me-2"></i>Bons de soins
                </a>
                <a href="{% url 'agents:verification_cotisation' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-check-circle me-2"></i>Vérification cotisations
                </a>
                <a href="{% url 'agents:notifications' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-bell me-2"></i>Notifications
                </a>
            </div>
        </div>
    </div>
    
    <!-- SIDEBAR COMMUNICATION -->
    {% include "includes/sidebar_communication.html" %}
</div>
AGENTS_EOF
    echo "✅ Sidebar agents mise à jour: templates/agents/partials/_sidebar_agent_updated.html"
else
    echo "⚠ templates/agents/partials/_sidebar_agent.html non trouvé"
fi

# Dashboard agents
if [ -f "templates/agents/dashboard.html" ]; then
    echo "📊 Ajout du widget dans dashboard agents..."
    # Note: Vous devrez ajouter manuellement {% include "includes/communication_widget.html" %} dans le dashboard agents
fi

# 3. INTÉGRATION DANS ASSUREUR
echo ""
echo "3. 🏢 INTÉGRATION DANS ASSUREUR"

# Sidebar assureur
if [ -f "templates/assureur/partials/_sidebar.html" ]; then
    cp templates/assureur/partials/_sidebar.html templates/assureur/partials/_sidebar.html.backup.$(date +%Y%m%d_%H%M%S)
    
    cat > templates/assureur/partials/_sidebar_updated.html << 'ASSUREUR_EOF'
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
ASSUREUR_EOF
    echo "✅ Sidebar assureur mise à jour: templates/assureur/partials/_sidebar_updated.html"
else
    echo "⚠ templates/assureur/partials/_sidebar.html non trouvé"
fi

# Dashboard assureur
if [ -f "templates/assureur/dashboard.html" ]; then
    echo "📊 Ajout du widget dans dashboard assureur..."
    # Note: Vous devrez ajouter manuellement {% include "includes/communication_widget.html" %} dans le dashboard assureur
fi

# 4. INTÉGRATION DANS MEDECIN
echo ""
echo "4. 👨‍⚕️ INTÉGRATION DANS MEDECIN"

# Sidebar medecin
if [ -f "templates/medecin/partials/_sidebar.html" ]; then
    cp templates/medecin/partials/_sidebar.html templates/medecin/partials/_sidebar.html.backup.$(date +%Y%m%d_%H%M%S)
    
    cat > templates/medecin/partials/_sidebar_updated.html << 'MEDECIN_EOF'
<!-- templates/medecin/partials/_sidebar.html -->
<div class="sidebar">
    <!-- Menu médecin principal -->
    <div class="card mb-4">
        <div class="card-header">
            <h6 class="mb-0">Menu Médecin</h6>
        </div>
        <div class="card-body p-0">
            <div class="list-group list-group-flush">
                <a href="{% url 'medecin:dashboard' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-tachometer-alt me-2"></i>Tableau de bord
                </a>
                <a href="{% url 'medecin:mes_rendez_vous' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-calendar me-2"></i>Mes rendez-vous
                </a>
                <a href="{% url 'medecin:liste_bons' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-file-medical me-2"></i>Bons de soins
                </a>
                <a href="{% url 'medecin:creer_ordonnance' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-prescription me-2"></i>Nouvelle ordonnance
                </a>
                <a href="{% url 'medecin:mes_ordonnances' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-list me-2"></i>Mes ordonnances
                </a>
                <a href="{% url 'medecin:bons_attente' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-clock me-2"></i>Bons en attente
                </a>
                <a href="{% url 'medecin:statistiques' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-chart-line me-2"></i>Statistiques
                </a>
            </div>
        </div>
    </div>
    
    <!-- SIDEBAR COMMUNICATION -->
    {% include "includes/sidebar_communication.html" %}
</div>
MEDECIN_EOF
    echo "✅ Sidebar medecin mise à jour: templates/medecin/partials/_sidebar_updated.html"
else
    echo "⚠ templates/medecin/partials/_sidebar.html non trouvé"
fi

# Dashboard medecin
if [ -f "templates/medecin/dashboard.html" ]; then
    echo "📊 Ajout du widget dans dashboard medecin..."
    # Note: Vous devrez ajouter manuellement {% include "includes/communication_widget.html" %} dans le dashboard medecin
fi

# 5. INTÉGRATION DANS PHARMACIEN
echo ""
echo "5. 💊 INTÉGRATION DANS PHARMACIEN"

# Sidebar pharmacien
if [ -f "templates/pharmacien/_sidebar_pharmacien.html" ]; then
    cp templates/pharmacien/_sidebar_pharmacien.html templates/pharmacien/_sidebar_pharmacien.html.backup.$(date +%Y%m%d_%H%M%S)
    
    cat > templates/pharmacien/_sidebar_pharmacien_updated.html << 'PHARMACIEN_EOF'
<!-- templates/pharmacien/_sidebar_pharmacien.html -->
<div class="sidebar">
    <!-- Menu pharmacien principal -->
    <div class="card mb-4">
        <div class="card-header">
            <h6 class="mb-0">Menu Pharmacien</h6>
        </div>
        <div class="card-body p-0">
            <div class="list-group list-group-flush">
                <a href="{% url 'pharmacien:dashboard' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-tachometer-alt me-2"></i>Tableau de bord
                </a>
                <a href="{% url 'pharmacien:liste_ordonnances' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-prescription me-2"></i>Ordonnances
                </a>
                <a href="{% url 'pharmacien:recherche_ordonnances' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-search me-2"></i>Recherche
                </a>
                <a href="{% url 'pharmacien:historique_validation' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-history me-2"></i>Historique
                </a>
                <a href="{% url 'pharmacien:stock' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-boxes me-2"></i>Gestion stock
                </a>
                <a href="{% url 'pharmacien:profil' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-user me-2"></i>Mon profil
                </a>
            </div>
        </div>
    </div>
    
    <!-- SIDEBAR COMMUNICATION -->
    {% include "includes/sidebar_communication.html" %}
</div>
PHARMACIEN_EOF
    echo "✅ Sidebar pharmacien mise à jour: templates/pharmacien/_sidebar_pharmacien_updated.html"
else
    echo "⚠ templates/pharmacien/_sidebar_pharmacien.html non trouvé"
fi

# Dashboard pharmacien
if [ -f "templates/pharmacien/dashboard.html" ]; then
    echo "📊 Ajout du widget dans dashboard pharmacien..."
    # Note: Vous devrez ajouter manuellement {% include "includes/communication_widget.html" %} dans le dashboard pharmacien
fi

# 6. INTÉGRATION DANS MEMBRES
echo ""
echo "6. 👥 INTÉGRATION DANS MEMBRES"

# Sidebar membres (si elle existe)
if [ -f "templates/membres/partials/_sidebar.html" ]; then
    cp templates/membres/partials/_sidebar.html templates/membres/partials/_sidebar.html.backup.$(date +%Y%m%d_%H%M%S)
    
    cat > templates/membres/partials/_sidebar_updated.html << 'MEMBRES_EOF'
<!-- templates/membres/partials/_sidebar.html -->
<div class="sidebar">
    <!-- Menu membre principal -->
    <div class="card mb-4">
        <div class="card-header">
            <h6 class="mb-0">Mon Espace</h6>
        </div>
        <div class="card-body p-0">
            <div class="list-group list-group-flush">
                <a href="{% url 'membres:dashboard' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-tachometer-alt me-2"></i>Tableau de bord
                </a>
                <a href="{% url 'membres:mes_ordonnances' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-prescription me-2"></i>Mes ordonnances
                </a>
                <a href="{% url 'membres:mes_paiements' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-credit-card me-2"></i>Mes paiements
                </a>
                <a href="{% url 'membres:solde_remboursements' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-wallet me-2"></i>Solde & Remboursements
                </a>
                <a href="{% url 'membres:analytics_dashboard' %}" class="list-group-item list-group-item-action">
                    <i class="fas fa-chart-line me-2"></i>Analytics
                </a>
            </div>
        </div>
    </div>
    
    <!-- SIDEBAR COMMUNICATION -->
    {% include "includes/sidebar_communication.html" %}
</div>
MEMBRES_EOF
    echo "✅ Sidebar membres mise à jour: templates/membres/partials/_sidebar_updated.html"
else
    echo "ℹ️ Pas de sidebar spécifique trouvée pour membres"
fi

# Dashboard membres
if [ -f "templates/membres/dashboard.html" ]; then
    echo "📊 Ajout du widget dans dashboard membres..."
    # Note: Vous devrez ajouter manuellement {% include "includes/communication_widget.html" %} dans le dashboard membres
fi

# 7. SCRIPT D'AIDE POUR L'INTÉGRATION MANUELLE
echo ""
echo "7. 🔧 SCRIPT D'AIDE POUR L'INTÉGRATION MANUELLE"

cat > integration_guide.md << 'GUIDE_EOF'
# GUIDE D'INTÉGRATION - COMPOSANTS COMMUNICATION

## 📊 INTÉGRATION DU WIDGET DANS LES DASHBOARDS

Pour chaque dashboard, ajoutez cette ligne où vous voulez le widget:

```django
{% include "includes/communication_widget.html" %}