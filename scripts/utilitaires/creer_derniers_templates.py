# creer_derniers_templates.py
import os

def creer_derniers_templates():
    """Crée les derniers templates manquants"""
    print("🔧 CRÉATION DES DERNIERS TEMPLATES MANQUANTS")
    print("=" * 50)
    
    templates_manquants = {
        'assureur/detail_soin.html': '''{% extends "assureur/base_assureur.html" %}

{% block title %}Détail Soin - Assureur{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header bg-info text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-stethoscope me-2"></i>
                        Détail du Soin
                    </h4>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h5>Informations du Soin</h5>
                            <p><strong>ID:</strong> {{ soin.id }}</p>
                            <p><strong>Date:</strong> {{ soin.date_soin|default:"Non spécifié" }}</p>
                            <p><strong>Statut:</strong> 
                                <span class="badge bg-{% if soin.statut == 'VALIDE' %}success{% else %}warning{% endif %}">
                                    {{ soin.statut }}
                                </span>
                            </p>
                        </div>
                        <div class="col-md-6">
                            <h5>Informations Patient</h5>
                            <p><strong>Membre:</strong> {{ soin.patient.nom_complet|default:"Non spécifié" }}</p>
                            <p><strong>Numéro:</strong> {{ soin.patient.numero_membre|default:"N/A" }}</p>
                        </div>
                    </div>
                    
                    <hr>
                    
                    <h5>Détails du Traitement</h5>
                    <div class="table-responsive">
                        <table class="table table-sm">
                            <thead>
                                <tr>
                                    <th>Description</th>
                                    <th>Coût</th>
                                    <th>Remboursement</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Consultation médicale</td>
                                    <td>5 000 FCFA</td>
                                    <td>4 000 FCFA (80%)</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    
                    <div class="mt-4">
                        <a href="{% url 'assureur:liste_soins' %}" class="btn btn-secondary">
                            <i class="fas fa-arrow-left me-2"></i>Retour à la liste
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

        'membres/detail_membre.html': '''{% extends "base.html" %}

{% block title %}Détail Membre - {{ membre.nom_complet }}{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-user me-2"></i>
                        Détail du Membre: {{ membre.nom_complet }}
                    </h4>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h5>Informations Personnelles</h5>
                            <p><strong>Nom complet:</strong> {{ membre.nom_complet }}</p>
                            <p><strong>Numéro membre:</strong> {{ membre.numero_membre }}</p>
                            <p><strong>Email:</strong> {{ membre.email|default:"Non spécifié" }}</p>
                            <p><strong>Téléphone:</strong> {{ membre.telephone|default:"Non spécifié" }}</p>
                        </div>
                        <div class="col-md-6">
                            <h5>Informations de Adhésion</h5>
                            <p><strong>Date d'inscription:</strong> {{ membre.date_inscription|date:"d/m/Y" }}</p>
                            <p><strong>Statut:</strong> 
                                <span class="badge bg-{% if membre.statut == 'AC' %}success{% else %}warning{% endif %}">
                                    {{ membre.get_statut_display }}
                                </span>
                            </p>
                            <p><strong>Type de couverture:</strong> {{ membre.type_couverture|default:"Standard" }}</p>
                        </div>
                    </div>
                    
                    <hr>
                    
                    <div class="row mt-4">
                        <div class="col-md-4 text-center">
                            <div class="border rounded p-3">
                                <h3 class="text-primary">12</h3>
                                <p class="mb-0">Soins utilisés</p>
                            </div>
                        </div>
                        <div class="col-md-4 text-center">
                            <div class="border rounded p-3">
                                <h3 class="text-success">85%</h3>
                                <p class="mb-0">Taux de remboursement</p>
                            </div>
                        </div>
                        <div class="col-md-4 text-center">
                            <div class="border rounded p-3">
                                <h3 class="text-info">2</h3>
                                <p class="mb-0">Bons en attente</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mt-4">
                        <a href="{% url 'liste_membres' %}" class="btn btn-secondary">
                            <i class="fas fa-arrow-left me-2"></i>Retour à la liste
                        </a>
                        <a href="#" class="btn btn-primary">
                            <i class="fas fa-edit me-2"></i>Modifier
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    }
    
    templates_crees = []
    
    for chemin_template, contenu in templates_manquants.items():
        repertoire = os.path.dirname(f'templates/{chemin_template}')
        
        # Créer le répertoire s'il n'existe pas
        if not os.path.exists(repertoire):
            os.makedirs(repertoire)
            print(f"✅ Répertoire créé: {repertoire}")
        
        chemin_complet = f'templates/{chemin_template}'
        
        if not os.path.exists(chemin_complet):
            with open(chemin_complet, 'w', encoding='utf-8') as f:
                f.write(contenu)
            templates_crees.append(chemin_template)
            print(f"✅ Template créé: {chemin_template}")
        else:
            print(f"✅ Template existe déjà: {chemin_template}")
    
    return templates_crees

if __name__ == '__main__':
    templates_crees = creer_derniers_templates()
    
    if templates_crees:
        print(f"\n🎉 {len(templates_crees)} templates créés:")
        for template in templates_crees:
            print(f"   ✅ {template}")
    else:
        print("\n✅ Tous les templates existent déjà!")
    
    print("\n💡 Redémarrez le serveur: python manage.py runserver")