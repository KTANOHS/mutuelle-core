#!/usr/bin/env python3
"""
Nettoyage complet du cache Django et des fichiers temporaires
"""

import os
import shutil
from pathlib import Path
import subprocess

def clear_django_cache():
    """Vider le cache Django"""
    print("🗑️ NETTOYAGE DU CACHE DJANGO")
    print("=" * 40)
    
    # Vider le cache de template Django
    cache_dirs = [
        "__pycache__",
        "*/__pycache__", 
        "*/migrations/__pycache__",
        "*.pyc",
        "*.pyo",
    ]
    
    for pattern in cache_dirs:
        for path in Path(".").rglob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"✅ Supprimé: {path}")
            else:
                path.unlink()
                print(f"✅ Supprimé: {path}")
    
    # Vider le cache de la base de données SQLite si existe
    db_path = Path("db.sqlite3")
    if db_path.exists():
        # Faire une sauvegarde avant suppression
        backup_path = db_path.with_suffix('.sqlite3.backup')
        shutil.copy2(db_path, backup_path)
        print(f"📦 Base de données sauvegardée: {backup_path}")

def clear_browser_cache_instructions():
    """Instructions pour vider le cache du navigateur"""
    print(f"\n🌐 INSTRUCTIONS CACHE NAVIGATEUR")
    print("=" * 40)
    
    instructions = [
        "Chrome: Ctrl+Shift+Delete → Cochez 'Images et fichiers' → Effacer",
        "Firefox: Ctrl+Shift+Delete → Sélectionnez 'Tout' → Effacer", 
        "Safari: Cmd+Alt+E → Confirmer effacement",
        "Edge: Ctrl+Shift+Delete → Cochez 'Cache' → Effacer"
    ]
    
    for instruction in instructions:
        print(f"   💡 {instruction}")

def restart_django_server():
    """Redémarrer le serveur Django"""
    print(f"\n🔄 REDÉMARRAGE SERVEUR")
    print("=" * 40)
    
    # Trouver et tuer les processus Django existants
    try:
        result = subprocess.run(
            "pkill -f 'python manage.py runserver'",
            shell=True,
            capture_output=True,
            text=True
        )
        print("✅ Anciens processus Django terminés")
    except Exception as e:
        print(f"ℹ️  Aucun processus à terminer: {e}")
    
    print("🚀 Redémarrage du serveur...")
    print("   Exécutez: python manage.py runserver")

def create_fresh_dashboard():
    """Créer un dashboard complètement nouveau"""
    print(f"\n🆕 CRÉATION DASHBOARD FRAIS")
    print("=" * 40)
    
    fresh_content = """{% extends "agents/base_agent.html" %}
{% load static %}

{% block title %}Tableau de Bord Agent - NOUVEAU{% endblock %}

{% block agent_content %}
<div class="container-fluid">
    <div class="alert alert-success">
        <h4>🆕 NOUVEAU DASHBOARD FRAIS</h4>
        <p>Ceci est une version complètement nouvelle du dashboard.</p>
        <p>Date de création: {% now "Y-m-d H:i:s" %}</p>
    </div>

    <div class="row">
        <div class="col-12">
            <h1 class="h3 mb-4 text-gray-800">Tableau de Bord Agent</h1>
        </div>
    </div>

    <div class="row">
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-primary shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                                Test Dashboard Frais</div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">100%</div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-check fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-12">
            <div class="card shadow mb-4">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">Liens de test</h6>
                </div>
                <div class="card-body">
                    <div class="list-group">
                        <a href="{% url 'agents:creer_bon_soin' %}" class="list-group-item list-group-item-action">
                            ✅ Créer Bon de Soin
                        </a>
                        <a href="{% url 'agents:liste_membres' %}" class="list-group-item list-group-item-action">
                            ✅ Liste Membres
                        </a>
                        <a href="{% url 'agents:notifications' %}" class="list-group-item list-group-item-action">
                            ✅ Notifications
                        </a>
                        <a href="{% url 'agents:verification_cotisation' %}" class="list-group-item list-group-item-action">
                            ✅ Vérification Cotisation
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
    
    dashboard_path = Path("templates/agents/dashboard_fresh.html")
    dashboard_path.write_text(fresh_content)
    print(f"✅ Nouveau dashboard créé: {dashboard_path}")
    
    # Remplacer le dashboard actuel
    main_dashboard = Path("templates/agents/dashboard.html")
    if main_dashboard.exists():
        backup_path = main_dashboard.with_suffix('.html.old_backup')
        main_dashboard.rename(backup_path)
        print(f"📦 Ancien dashboard sauvegardé: {backup_path}")
    
    dashboard_path.rename(main_dashboard)
    print(f"🎯 Nouveau dashboard installé comme dashboard principal")

if __name__ == "__main__":
    clear_django_cache()
    clear_browser_cache_instructions()
    restart_django_server()
    create_fresh_dashboard()
    
    print(f"\n🎉 NETTOYAGE TERMINÉ!")
    print("📋 Prochaines étapes:")
    print("   1. Videz le cache de votre navigateur")
    print("   2. Redémarrez le serveur: python manage.py runserver")
    print("   3. Testez: http://127.0.0.1:8000/agents/")