#!/usr/bin/env python3
"""
ANALYSE URGENTE - Problème de chemin et vérification complète
"""

import os
import re
import sys

def analyse_urgence():
    print("🔍 ANALYSE URGENTE - Problème de chemin détecté")
    print("=" * 60)
    
    # 1. Vérifier la structure exacte
    print("📁 STRUCTURE DES DOSSIERS:")
    for root, dirs, files in os.walk('.'):
        if 'dashboard.html' in files:
            print(f"✅ dashboard.html trouvé dans: {root}/")
        if 'agents' in dirs:
            print(f"✅ Dossier agents trouvé dans: {root}/")
    
    # 2. Vérifier le template spécifique
    template_path = 'templates/agents/dashboard.html'
    print(f"\n🎯 ANALYSE DU TEMPLATE: {template_path}")
    
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ Template existe - Analyse du contenu...")
        
        # Rechercher TOUTES les occurrences du calcul de pourcentage
        patterns = [
            (r'stats\.membres_a_jour', "Référence à membres_a_jour"),
            (r'stats\.membres_actifs', "Référence à membres_actifs"), 
            (r'pourcentage_conformite', "Référence à pourcentage_conformite"),
            (r'\|\s*\(\(.*\*.*100\)', "Calcul avec multiplication"),
            (r'\|\|', "Double pipe"),
            (r'\{\{\s*\|', "Pipe au début d'expression"),
        ]
        
        print("\n🔎 PATTERNS TROUVÉS DANS LE TEMPLATE:")
        for pattern, description in patterns:
            matches = list(re.finditer(pattern, content))
            if matches:
                print(f"📌 {description}: {len(matches)} occurrence(s)")
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    context_start = max(0, match.start() - 30)
                    context_end = min(len(content), match.end() + 30)
                    context = content[context_start:context_end].replace('\n', ' ')
                    print(f"   Ligne {line_num}: ...{context}...")
            else:
                print(f"❌ {description}: AUCUNE")
        
        # Vérifier spécifiquement la section du taux de conformité
        print("\n📊 SECTION TAUX DE CONFORMITÉ:")
        if 'Taux conformité' in content:
            # Trouver la section autour de "Taux conformité"
            start_idx = content.find('Taux conformité')
            if start_idx != -1:
                section_start = max(0, start_idx - 200)
                section_end = min(len(content), start_idx + 500)
                section = content[section_start:section_end]
                
                # Extraire les lignes pertinentes
                lines = section.split('\n')
                for i, line in enumerate(lines):
                    if 'Taux conformité' in line or '%' in line or 'pourcentage' in line.lower():
                        print(f"   Ligne {i}: {line.strip()}")
        
    else:
        print(f"❌ Template non trouvé: {template_path}")
    
    # 3. Vérifier la vue Django
    print(f"\n🐍 VÉRIFICATION DE LA VUE:")
    views_path = 'agents/views.py'
    if os.path.exists(views_path):
        with open(views_path, 'r', encoding='utf-8') as f:
            views_content = f.read()
        
        # Vérifier la fonction dashboard
        if 'def dashboard(' in views_content:
            print("✅ Fonction dashboard() trouvée")
            
            # Extraire la fonction
            start = views_content.find('def dashboard(')
            end = views_content.find('def ', start + 1)
            if end == -1:
                end = len(views_content)
            
            dashboard_func = views_content[start:end]
            
            # Vérifier les variables critiques
            critical_vars = {
                'pourcentage_conformite': "Variable pourcentage dans stats",
                'membres_a_jour': "Variable membres à jour", 
                'membres_actifs': "Variable membres actifs",
                'stats.pourcentage_conformite': "Assignation correcte",
            }
            
            for var, desc in critical_vars.items():
                if var in dashboard_func:
                    print(f"✅ {desc}: PRÉSENTE")
                else:
                    print(f"❌ {desc}: ABSENTE")
        
        else:
            print("❌ Fonction dashboard() non trouvée!")
    else:
        print(f"❌ Fichier views.py non trouvé: {views_path}")
    
    # 4. Vérifier le cache Django
    print(f"\n🗑️  VÉRIFICATION CACHE:")
    cache_dirs = [
        '__pycache__',
        'templates/__pycache__', 
        'agents/__pycache__',
        'venv'
    ]
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            print(f"⚠️  Cache présent: {cache_dir}")
        else:
            print(f"✅ Cache absent: {cache_dir}")

def solution_definitive():
    print("\n🔧 SOLUTION DÉFINITIVE")
    print("=" * 50)
    
    print("1. FORCER LE RECHARGEMENT DU TEMPLATE:")
    print("   python manage.py collectstatic --noinput")
    print("   python manage.py compress --force")
    print("")
    
    print("2. VIDER LE CACHE DJANGO:")
    print("   rm -rf __pycache__")
    print("   rm -rf templates/__pycache__")
    print("   rm -rf agents/__pycache__")
    print("   find . -name '*.pyc' -delete")
    print("")
    
    print("3. REDÉMARRER COMPLÈTEMENT:")
    print("   pkill -f 'python manage.py runserver'")
    print("   python manage.py runserver")
    print("")
    
    print("4. VÉRIFIER LE TEMPLATE EN LIGNE:")
    print("   Ouvrez http://localhost:8000/agents/tableau-de-bord/")
    print("   Vérifiez le code source de la page")

def creer_template_corrige():
    """Crée une version 100% corrigée du template"""
    print("\n🛠️  CRÉATION D'UN TEMPLATE 100% CORRIGÉ")
    
    template_content = """{% extends 'agents/base_agent.html' %}
{% load static %}

{% block title %}Tableau de bord - Agent{% endblock %}
{% block page_icon %}tachometer-alt{% endblock %}
{% block page_title %}Tableau de bord{% endblock %}

{% block content %}
<div class="row">
    <!-- Statistiques -->
    <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-primary shadow h-100 py-2">
            <div class="card-body">
                <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                        <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                            Vérifications aujourd'hui
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">
                            {{ stats.verifications_jour|default:"0" }}
                        </div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-check-circle fa-2x text-gray-300"></i>
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
                            Membres à jour
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">
                            {{ stats.membres_a_jour|default:"0" }}
                        </div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-user-check fa-2x text-gray-300"></i>
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
                            En retard
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">
                            {{ stats.membres_retard|default:"0" }}
                        </div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-exclamation-triangle fa-2x text-gray-300"></i>
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
                            Taux conformité
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">
                            {{ stats.pourcentage_conformite|default:0|floatformat:0 }}%
                        </div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-percent fa-2x text-gray-300"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Le reste de votre template existant -->
<div class="row">
    <div class="col-lg-8">
        <!-- Votre contenu existant -->
    </div>
</div>
{% endblock %}
"""
    
    template_path = 'templates/agents/dashboard_corrige.html'
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    print(f"✅ Template 100% corrigé créé: {template_path}")
    print("💡 Testez avec cette URL: /agents/tableau-de-bord/?template=corrige")

if __name__ == "__main__":
    analyse_urgence()
    solution_definitive()
    creer_template_corrige()