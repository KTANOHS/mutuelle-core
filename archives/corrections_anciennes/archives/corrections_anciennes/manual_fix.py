#!/usr/bin/env python3
"""
Correcteur manuel pour les URLs résiduelles - VERSION FINALE
"""

from pathlib import Path

def manual_fix_remaining_issues():
    dashboard_path = Path("templates/agents/dashboard.html")
    
    if not dashboard_path.exists():
        print("❌ Dashboard non trouvé")
        return
    
    content = dashboard_path.read_text()
    original_content = content
    
    print("🛠️ CORRECTION MANUELLE DES PROBLÈMES RÉSIDUELS")
    print("=" * 50)
    
    # LISTE EXHAUSTIVE DES CORRECTIONS NÉCESSAIRES
    corrections = [
        # Ajouter les guillemets de fermeture manquants
        ('''href="{% url 'agents:creer_bon_soin' %}''', '''href="{% url 'agents:creer_bon_soin' %}"'''),
        ('''href="{% url 'agents:liste_membres' %}''', '''href="{% url 'agents:liste_membres' %}"'''),
        ('''href="{% url 'agents:historique_bons' %}''', '''href="{% url 'agents:historique_bons' %}"'''),
        ('''href="{% url 'agents:notifications' %}''', '''href="{% url 'agents:notifications' %}"'''),
        ('''href="{% url 'agents:verification_cotisation' %}''', '''href="{% url 'agents:verification_cotisation' %}"'''),
        
        # Corrections pour les URLs avec paramètres
        ('''href="{% url 'agents:historique_bons' %}?q={{ bon.code }}''', '''href="{% url 'agents:historique_bons' %}?q={{ bon.code }}"'''),
        
        # Fermer les balises <a>
        ('''<a href="{% url 'agents:creer_bon_soin' %}''', '''<a href="{% url 'agents:creer_bon_soin' %}">'''),
        ('''<a href="{% url 'agents:liste_membres' %}''', '''<a href="{% url 'agents:liste_membres' %}">'''),
    ]
    
    corrections_applied = 0
    for wrong, correct in corrections:
        if wrong in content:
            content = content.replace(wrong, correct)
            corrections_applied += 1
            print(f"✅ Correction: {wrong} → {correct}")
    
    if content != original_content:
        # Sauvegarde
        backup_path = dashboard_path.with_suffix('.html.manual_fix_backup')
        Path(backup_path).write_text(original_content)
        
        # Écrire la version corrigée
        dashboard_path.write_text(content)
        print(f"\n🎯 RÉSULTAT:")
        print(f"✅ {corrections_applied} corrections manuelles appliquées")
        print(f"📦 Backup sauvegardé: {backup_path}")
    else:
        print("ℹ️  Aucune correction manuelle nécessaire")

def create_verified_dashboard():
    """Créer une version vérifiée du dashboard"""
    print(f"\n🔒 CRÉATION D'UNE VERSION VÉRIFIÉE")
    print("=" * 40)
    
    verified_content = """{% extends "agents/base_agent.html" %}
{% load static %}

{% block title %}Tableau de Bord Agent{% endblock %}

{% block agent_content %}
<div class="container-fluid">
    <!-- En-tête -->
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">Tableau de Bord</h1>
    </div>

    <!-- Cartes de statistiques -->
    {% include "agents/partials/_stats_cards.html" %}

    <!-- Actions rapides -->
    {% include "agents/partials/_quick_actions.html" %}

    <!-- Section récente -->
    <div class="row">
        <div class="col-lg-6 mb-4">
            <div class="card shadow mb-4">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">Actions Rapides</h6>
                </div>
                <div class="card-body">
                    <div class="list-group">
                        <a href="{% url 'agents:creer_bon_soin' %}" class="list-group-item list-group-item-action">
                            <i class="fas fa-plus-circle text-success mr-2"></i>
                            Créer un nouveau bon de soin
                        </a>
                        <a href="{% url 'agents:liste_membres' %}" class="list-group-item list-group-item-action">
                            <i class="fas fa-users text-info mr-2"></i>
                            Gérer les membres
                        </a>
                        <a href="{% url 'agents:verification_cotisation' %}" class="list-group-item list-group-item-action">
                            <i class="fas fa-check-circle text-warning mr-2"></i>
                            Vérifier les cotisations
                        </a>
                        <a href="{% url 'agents:notifications' %}" class="list-group-item list-group-item-action">
                            <i class="fas fa-bell text-primary mr-2"></i>
                            Voir les notifications
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-lg-6 mb-4">
            <div class="card shadow mb-4">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">Dernières Activités</h6>
                </div>
                <div class="card-body">
                    <p>Vos activités récentes apparaîtront ici.</p>
                    <a href="{% url 'agents:historique_bons' %}" class="btn btn-primary btn-sm">
                        Voir l'historique complet
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
    
    verified_path = Path("templates/agents/dashboard_verified.html")
    verified_path.write_text(verified_content)
    print(f"✅ Dashboard vérifié créé: {verified_path}")

if __name__ == "__main__":
    manual_fix_remaining_issues()
    create_verified_dashboard()
    
    print(f"\n🎉 CORRECTIONS TERMINÉES!")
    print("📋 Prochaines étapes:")
    print("   1. Testez le dashboard original")
    print("   2. Si ça ne marche pas, utilisez dashboard_verified.html")
    print("   3. Exécutez: python diagnose_dashboard_urls.py pour vérifier")