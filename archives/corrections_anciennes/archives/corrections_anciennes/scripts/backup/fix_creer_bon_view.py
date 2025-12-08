#!/usr/bin/env python
"""
CORRECTION DE LA VUE CREER_BON
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def create_simple_creer_bon_view():
    """Crée une vue creer_bon simplifiée et fonctionnelle"""
    print("🔧 Création d'une vue creer_bon simplifiée...")
    
    views_content = '''
@login_required
@assureur_required
def creer_bon(request, numero_membre):
    """Création simplifiée d'un bon pour un membre"""
    membre = get_object_or_404(Membre, numero_unique=numero_membre)
    
    # Vérifier que le membre est à jour
    if not getattr(membre, 'est_a_jour', True):
        messages.error(request, f"Le membre {membre.nom} n'est pas à jour de cotisation")
        return redirect('assureur:detail_membre', numero_membre=numero_membre)
    
    if request.method == 'POST':
        type_soin = request.POST.get('type_soin', '').strip()
        description = request.POST.get('description', '').strip()
        
        if not type_soin:
            messages.error(request, "Le type de soin est obligatoire")
            return render(request, 'assureur/creer_bon.html', {'membre': membre})
        
        try:
            # Générer un numéro de bon unique
            dernier_bon = Bon.objects.order_by('-id').first()
            nouveau_numero = f"BON{timezone.now().strftime('%Y%m%d')}{dernier_bon.id + 1 if dernier_bon else 1:04d}"
            
            # Créer le bon
            bon = Bon.objects.create(
                membre=membre,
                numero_bon=nouveau_numero,
                type_soin=type_soin,
                description=description,
                montant_total=0,  # À définir ultérieurement
                statut='ATTENTE'
            )
            
            messages.success(request, f"Bon {nouveau_numero} créé avec succès !")
            return redirect('assureur:detail_membre', numero_membre=numero_membre)
            
        except Exception as e:
            messages.error(request, f"Erreur lors de la création : {e}")
    
    # Types de soins disponibles
    types_soins = getattr(Bon, 'TYPE_SOIN_CHOICES', [
        ('CONSULT', 'Consultation'),
        ('MEDIC', 'Médicaments'),
        ('ANALYSE', 'Analyses'),
    ])
    
    return render(request, 'assureur/creer_bon.html', {
        'membre': membre,
        'types_soins': types_soins
    })
'''
    
    # Ajouter cette vue à assureur/views.py
    views_path = BASE_DIR / 'assureur' / 'views.py'
    
    with open(views_path, 'r') as f:
        content = f.read()
    
    # Vérifier si la vue existe déjà
    if 'def creer_bon(' in content:
        print("✅ Vue creer_bon existe déjà")
        return
    
    # Ajouter la vue à la fin du fichier
    with open(views_path, 'a') as f:
        f.write('\n\n' + views_content)
    
    print("✅ Vue creer_bon créée")

def create_simple_template():
    """Crée un template simplifié pour creer_bon"""
    print("📁 Création du template creer_bon.html...")
    
    template_content = '''{% extends 'base.html' %}

{% block title %}Créer un Bon - {{ membre.nom }} {{ membre.prenom }}{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>
            <i class="fas fa-file-medical"></i> 
            Créer un Bon pour {{ membre.nom }} {{ membre.prenom }}
        </h1>
        <a href="{% url 'assureur:detail_membre' membre.numero_unique %}" class="btn btn-outline-primary">
            <i class="fas fa-arrow-left"></i> Retour au membre
        </a>
    </div>

    <div class="row">
        <div class="col-md-8">
            <div class="card shadow-sm">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Nouveau Bon de Soins</h5>
                </div>
                <div class="card-body">
                    {% if messages %}
                        {% for message in messages %}
                            <div class="alert alert-{{ message.tags }}">{{ message }}</div>
                        {% endfor %}
                    {% endif %}
                    
                    <form method="post">
                        {% csrf_token %}
                        
                        <div class="mb-3">
                            <label for="type_soin" class="form-label">Type de Soin *</label>
                            <select name="type_soin" id="type_soin" class="form-select" required>
                                <option value="">Sélectionnez un type de soin</option>
                                {% for code, libelle in types_soins %}
                                    <option value="{{ code }}">{{ libelle }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        
                        <div class="mb-3">
                            <label for="description" class="form-label">Description</label>
                            <textarea name="description" id="description" class="form-control" 
                                      rows="3" placeholder="Description des soins..."></textarea>
                        </div>
                        
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle"></i>
                            Le bon sera créé avec le statut "En attente". Le montant pourra être ajouté ultérieurement.
                        </div>
                        
                        <div class="d-flex gap-2">
                            <button type="submit" class="btn btn-success">
                                <i class="fas fa-save"></i> Créer le Bon
                            </button>
                            <a href="{% url 'assureur:detail_membre' membre.numero_unique %}" class="btn btn-secondary">
                                Annuler
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card shadow-sm">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">Informations Membre</h5>
                </div>
                <div class="card-body">
                    <p><strong>Nom:</strong> {{ membre.nom }} {{ membre.prenom }}</p>
                    <p><strong>N° Membre:</strong> {{ membre.numero_unique }}</p>
                    <p><strong>Statut:</strong> 
                        <span class="badge bg-{% if membre.est_a_jour %}success{% else %}danger{% endif %}">
                            {% if membre.est_a_jour %}À jour{% else %}En retard{% endif %}
                        </span>
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''
    
    template_path = BASE_DIR / 'templates' / 'assureur' / 'creer_bon.html'
    template_path.parent.mkdir(parents=True, exist_ok=True)
    template_path.write_text(template_content)
    print("✅ Template creer_bon.html créé")

if __name__ == "__main__":
    print("🎉 CORRECTION DE LA VUE CREER_BON")
    print("=" * 50)
    
    create_simple_creer_bon_view()
    create_simple_template()
    
    print("\n✅ VUE CREER_BON PRÊTE !")
    print("📋 Testez maintenant :")
    print("   http://127.0.0.1:8000/assureur/bons/creer/MEM001/")