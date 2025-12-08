# creer_templates_pharmacien.py
import os

def creer_templates_pharmacien():
    """Crée tous les templates manquants pour le module pharmacien"""
    print("🔧 CRÉATION DES TEMPLATES PHARMACIEN MANQUANTS")
    print("=" * 50)
    
    templates_pharmacien = {
        'liste_ordonnances.html': '''{% extends "pharmacien/base_pharmacien.html" %}

{% block title %}Ordonnances en Attente - Pharmacien{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-file-prescription me-2"></i>
                        Ordonnances en Attente de Validation
                    </h4>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>#</th>
                                    <th>Patient</th>
                                    <th>Médecin</th>
                                    <th>Date</th>
                                    <th>Statut</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td colspan="6" class="text-center text-muted py-4">
                                        <i class="fas fa-inbox fa-3x mb-3"></i>
                                        <p>Aucune ordonnance en attente</p>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

        'detail_ordonnance.html': '''{% extends "pharmacien/base_pharmacien.html" %}

{% block title %}Détail Ordonnance - Pharmacien{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header bg-info text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-file-medical me-2"></i>
                        Détail de l'Ordonnance #{{ ordonnance.id }}
                    </h4>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h5>Informations Patient</h5>
                            <p><strong>Nom:</strong> Patient Exemple</p>
                            <p><strong>Date:</strong> {{ current_date }}</p>
                        </div>
                        <div class="col-md-6">
                            <h5>Informations Médecin</h5>
                            <p><strong>Docteur:</strong> Dr. Exemple</p>
                            <p><strong>Spécialité:</strong> Généraliste</p>
                        </div>
                    </div>
                    
                    <hr>
                    
                    <h5>Médicaments Prescrits</h5>
                    <div class="table-responsive">
                        <table class="table table-sm">
                            <thead>
                                <tr>
                                    <th>Médicament</th>
                                    <th>Posologie</th>
                                    <th>Durée</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Paracétamol</td>
                                    <td>1 comprimé 3x/jour</td>
                                    <td>7 jours</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    
                    <div class="mt-4">
                        <a href="{% url 'pharmacien:valider_ordonnance' ordonnance.id %}" class="btn btn-success">
                            <i class="fas fa-check me-2"></i>Valider l'Ordonnance
                        </a>
                        <a href="{% url 'pharmacien:liste_ordonnances_attente' %}" class="btn btn-secondary">
                            <i class="fas fa-arrow-left me-2"></i>Retour
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

        'historique_validation.html': '''{% extends "pharmacien/base_pharmacien.html" %}

{% block title %}Historique des Validations - Pharmacien{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header bg-success text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-history me-2"></i>
                        Historique des Validations
                    </h4>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>#</th>
                                    <th>Patient</th>
                                    <th>Date Validation</th>
                                    <th>Statut</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td colspan="5" class="text-center text-muted py-4">
                                        <i class="fas fa-history fa-3x mb-3"></i>
                                        <p>Aucune validation dans l'historique</p>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

        'dashboard.html': '''{% extends "pharmacien/base_pharmacien.html" %}

{% block title %}Tableau de Bord - Pharmacien{% endblock %}

{% block content %}
<div class="container-fluid">
    <!-- Statistiques -->
    <div class="row">
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-primary shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                                Ordonnances en Attente
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">0</div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-file-prescription fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-success shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                                Validations Aujourd'hui
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">0</div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-check-circle fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-info shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                                Validations Ce Mois
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">0</div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-calendar-alt fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-warning shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                                Taux de Validation
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">0%</div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-chart-line fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Actions rapides -->
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header bg-white">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-bolt me-2 text-warning"></i>Actions Rapides
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-4 mb-3">
                            <a href="{% url 'pharmacien:liste_ordonnances_attente' %}" class="btn btn-primary btn-lg w-100 py-3">
                                <i class="fas fa-file-prescription me-2"></i>
                                Voir les Ordonnances
                            </a>
                        </div>
                        <div class="col-md-4 mb-3">
                            <a href="{% url 'pharmacien:historique_validation' %}" class="btn btn-success btn-lg w-100 py-3">
                                <i class="fas fa-history me-2"></i>
                                Historique
                            </a>
                        </div>
                        <div class="col-md-4 mb-3">
                            <a href="#" class="btn btn-info btn-lg w-100 py-3">
                                <i class="fas fa-chart-bar me-2"></i>
                                Statistiques
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    }
    
    repertoire_templates = 'templates/pharmacien'
    
    # Créer le répertoire s'il n'existe pas
    if not os.path.exists(repertoire_templates):
        os.makedirs(repertoire_templates)
        print(f"✅ Répertoire créé: {repertoire_templates}")
    
    templates_crees = []
    
    for nom_template, contenu in templates_pharmacien.items():
        chemin_template = os.path.join(repertoire_templates, nom_template)
        
        if not os.path.exists(chemin_template):
            with open(chemin_template, 'w', encoding='utf-8') as f:
                f.write(contenu)
            templates_crees.append(nom_template)
            print(f"✅ Template créé: {nom_template}")
        else:
            print(f"✅ Template existe déjà: {nom_template}")
    
    return templates_crees

def verifier_templates_existants():
    """Vérifie quels templates existent déjà"""
    print("\n🔍 VÉRIFICATION DES TEMPLATES EXISTANTS")
    print("=" * 50)
    
    repertoire_templates = 'templates/pharmacien'
    
    if not os.path.exists(repertoire_templates):
        print("❌ Répertoire templates/pharmacien n'existe pas")
        return []
    
    templates_existants = []
    for fichier in os.listdir(repertoire_templates):
        if fichier.endswith('.html'):
            templates_existants.append(fichier)
    
    print("Templates existants dans templates/pharmacien/:")
    for template in sorted(templates_existants):
        print(f"  📄 {template}")
    
    return templates_existants

if __name__ == '__main__':
    templates_crees = creer_templates_pharmacien()
    templates_existants = verifier_templates_existants()
    
    if templates_crees:
        print(f"\n🎉 {len(templates_crees)} nouveaux templates créés:")
        for template in templates_crees:
            print(f"   ✅ {template}")
    else:
        print("\n✅ Tous les templates existent déjà!")
    
    print(f"\n📁 Total: {len(templates_existants)} templates disponibles")
    print("💡 Redémarrez le serveur: python manage.py runserver")