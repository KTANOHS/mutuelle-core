#!/usr/bin/env python3
"""
Script pour corriger les problèmes identifiés
- Fichiers vides
- Dépendances manquantes
- Structure des dossiers
"""

import os
import shutil
from pathlib import Path

class TemplateFixer:
    def __init__(self, templates_dir="templates"):
        self.templates_dir = Path(templates_dir)
        
    def fix_empty_files(self):
        """Corriger ou supprimer les fichiers vides"""
        empty_files = [
            'registration/login_ajax.html',
            'assureur/detail_paiement.html',
            'assureur/partials/_filtres_paiements.html',
            'assureur/partials/_liste_paiements.html',
            'assureur/partials/_stats_paiements.html',
            'paiements/pdf/releve_paiements.html',
            'paiements/pdf/journal_paiements.html',
            'paiements/pdf/bordereau_paiement.html',
            'paiements/pdf/etat_remboursements.html'
        ]
        
        # Créer un contenu de base pour les fichiers vides
        base_content = """{% extends "base.html" %}

{% block content %}
<div class="container">
    <div class="alert alert-info">
        <h4>Template en cours de développement</h4>
        <p>Cette page est en cours de construction.</p>
    </div>
</div>
{% endblock %}
"""
        
        for file_path in empty_files:
            full_path = self.templates_dir / file_path
            if full_path.exists() and full_path.stat().st_size < 100:
                print(f"📝 Correction de {file_path}")
                full_path.write_text(base_content, encoding='utf-8')
                
    def create_missing_dependencies(self):
        """Créer les fichiers manquants identifiés"""
        missing_files = {
            'membres/base.html': """{% extends "base.html" %}

{% block sidebar %}
    {% include "includes/sidebar_membre.html" %}
{% endblock %}

{% block content %}
{% endblock %}
""",
            'communication/partials/_nouveau_message_modal.html': """<!-- Modal Nouveau Message -->
<div class="modal fade" id="nouveauMessageModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Nouveau Message</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p>Formulaire nouveau message à implémenter</p>
            </div>
        </div>
    </div>
</div>
""",
            'communication/partials/_modal_fichier.html': """<!-- Modal Fichier -->
<div class="modal fade" id="fichierModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Gestion des Fichiers</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p>Gestion des fichiers à implémenter</p>
            </div>
        </div>
    </div>
</div>
"""
        }
        
        for file_path, content in missing_files.items():
            full_path = self.templates_dir / file_path
            if not full_path.exists():
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding='utf-8')
                print(f"✅ Créé: {file_path}")
    
    def fix_email_templates_structure(self):
        """Corriger la structure incorrecte des templates d'email"""
        # Le problème : emails.py est traité comme un dossier alors que c'est un fichier Python
        email_templates = [
            'emails.py/remboursement_demande.html',
            'emails.py/paiement_annule.html', 
            'emails.py/bordereau_paiement.html',
            'emails.py/rappel_paiement.html'
        ]
        
        # Déplacer vers le bon emplacement
        for old_path in email_templates:
            old_full_path = self.templates_dir / old_path
            if old_full_path.exists():
                # Nouveau chemin dans templates/emails/
                new_path = old_path.replace('emails.py/', 'emails/')
                new_full_path = self.templates_dir / new_path
                
                new_full_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(old_full_path), str(new_full_path))
                print(f"📧 Déplacé: {old_path} → {new_path}")
    
    def create_unified_dashboard(self):
        """Créer un dashboard unifié"""
        dashboard_content = """{% extends "base.html" %}

{% block content %}
<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <h1 class="h3 mb-4">Tableau de Bord</h1>
        </div>
    </div>
    
    <!-- Cartes de statistiques -->
    <div class="row">
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-primary shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                                Membres</div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.membres_total }}</div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-users fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Ajouter d'autres cartes selon le rôle -->
    </div>
    
    <!-- Contenu spécifique au rôle -->
    {% block dashboard_content %}
    {% endblock %}
</div>
{% endblock %}
"""
        
        unified_path = self.templates_dir / 'core' / 'dashboard_unified.html'
        unified_path.parent.mkdir(parents=True, exist_ok=True)
        unified_path.write_text(dashboard_content, encoding='utf-8')
        print(f"🎯 Dashboard unifié créé: {unified_path}")

def main():
    fixer = TemplateFixer()
    
    print("🔧 Correction des problèmes identifiés...")
    
    # 1. Créer les dépendances manquantes
    print("\n1. Création des dépendances manquantes...")
    fixer.create_missing_dependencies()
    
    # 2. Corriger la structure des emails
    print("\n2. Correction de la structure des emails...")
    fixer.fix_email_templates_structure()
    
    # 3. Corriger les fichiers vides
    print("\n3. Correction des fichiers vides...")
    fixer.fix_empty_files()
    
    # 4. Créer un dashboard unifié
    print("\n4. Création d'un dashboard unifié...")
    fixer.create_unified_dashboard()
    
    print("\n✅ Toutes les corrections ont été appliquées!")

if __name__ == "__main__":
    main()