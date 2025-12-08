# fix_migration_issues.py
import os
import re

def fix_template_extends(filepath, target_base):
    """Corrige l'extends d'un template spécifique"""
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return False
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Cas 1: Template a déjà un extends
    extends_pattern = r'\{%\s*extends\s*[\'"]([^\'"]*)[\'"]\s*%\}'
    match = re.search(extends_pattern, content)
    
    if match:
        current_extends = match.group(1)
        if target_base not in current_extends:
            # Remplacer l'extends existant
            new_extends = f'{{% extends "{target_base}" %}}'
            content = re.sub(extends_pattern, new_extends, content)
            print(f"✅ Corrigé: {filepath}")
            print(f"   {current_extends} → {target_base}")
    else:
        # Cas 2: Template sans extends - on l'ajoute
        # Chercher le doctype ou le début du html
        if '<!DOCTYPE html>' in content or '<html' in content:
            # Template autonome - on ne modifie pas
            print(f"ℹ️  Template autonome: {filepath}")
            return False
        else:
            # Template fragment - on ajoute l'extends au début
            new_content = f'{{% extends "{target_base}" %}}\n\n{content}'
            content = new_content
            print(f"✅ Extends ajouté: {filepath} → {target_base}")
    
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    
    return False

def fix_specific_issues():
    """Corrige les problèmes spécifiques identifiés"""
    
    issues = {
        'assureur/export_bons_pdf.html': 'assureur/base_assureur.html',
        'medecin/detail_bon.html': 'medecin/base_medecin.html',
        'medecin/bons_attente.html': 'medecin/base_medecin.html', 
        'medecin/creer_ordonnance.html': 'medecin/base_medecin.html',
        'medecin/historique.html': 'medecin/base_medecin.html',
        'registration/login_ajax.html': 'registration/base_auth.html',
        'registration/logout.html': 'registration/base_auth.html'
    }
    
    print("🔧 CORRECTION DES PROBLÈMES DE MIGRATION")
    print("=" * 50)
    
    fixed_count = 0
    for template_path, base_template in issues.items():
        full_path = f'templates/{template_path}'
        if os.path.exists(full_path):
            if fix_template_extends(full_path, base_template):
                fixed_count += 1
        else:
            print(f"❌ Fichier non trouvé: {template_path}")
    
    print(f"\n✅ {fixed_count} templates corrigés")

def analyze_problematic_templates():
    """Analyse les templates problématiques"""
    print("\n🔍 ANALYSE DES TEMPLATES NON MIGRÉS")
    print("=" * 40)
    
    problematic = [
        'templates/assureur/export_bons_pdf.html',
        'templates/medecin/detail_bon.html',
        'templates/medecin/bons_attente.html',
        'templates/medecin/creer_ordonnance.html', 
        'templates/medecin/historique.html',
        'templates/registration/login_ajax.html',
        'templates/registration/logout.html'
    ]
    
    for template in problematic:
        if os.path.exists(template):
            size = os.path.getsize(template)
            with open(template, 'r') as f:
                content = f.read()
            
            print(f"\n📄 {template} ({size} octets)")
            
            # Vérifier le contenu
            if size == 0:
                print("   ⚠️  FICHIER VIDE")
            elif '{% extends' in content:
                extends_match = re.search(r'{% extends [\'"]([^\'"]*)[\'"] %}', content)
                if extends_match:
                    print(f"   ➤ Étend: {extends_match.group(1)}")
            elif '<!DOCTYPE' in content:
                print("   ➤ TEMPLATE AUTONOME (DOCTYPE trouvé)")
            else:
                print("   ➤ FRAGMENT DE TEMPLATE (sans DOCTYPE)")
                
            # Afficher les premières lignes
            lines = content.split('\n')[:3]
            for i, line in enumerate(lines):
                if line.strip():
                    print(f"   Ligne {i+1}: {line.strip()[:50]}...")

def create_missing_templates():
    """Crée les templates manquants ou vides"""
    print("\n📝 CRÉATION DES TEMPLATES MANQUANTS")
    print("=" * 40)
    
    # Templates médecin vides à compléter
    medecin_templates = {
        'medecin/detail_bon.html': """{% extends "medecin/base_medecin.html" %}
{% load static %}

{% block title %}Détail du Bon - Médecin{% endblock %}

{% block content %}
<div class="container mt-4">
    <h2>Détail du Bon de Soins</h2>
    <p>Template à développer - Détails du bon de soins</p>
</div>
{% endblock %}
""",
        
        'medecin/bons_attente.html': """{% extends "medecin/base_medecin.html" %}
{% load static %}

{% block title %}Bons en Attente - Médecin{% endblock %}

{% block content %}
<div class="container mt-4">
    <h2>Bons de Soins en Attente</h2>
    <p>Template à développer - Liste des bons en attente de traitement</p>
</div>
{% endblock %}
""",
        
        'medecin/creer_ordonnance.html': """{% extends "medecin/base_medecin.html" %}
{% load static %}

{% block title %}Créer Ordonnance - Médecin{% endblock %}

{% block content %}
<div class="container mt-4">
    <h2>Créer une Nouvelle Ordonnance</h2>
    <p>Template à développer - Formulaire de création d'ordonnance</p>
</div>
{% endblock %}
""",
        
        'medecin/historique.html': """{% extends "medecin/base_medecin.html" %}
{% load static %}

{% block title %}Historique - Médecin{% endblock %}

{% block content %}
<div class="container mt-4">
    <h2>Historique des Ordonnances</h2>
    <p>Template à développer - Historique des ordonnances créées</p>
</div>
{% endblock %}
"""
    }
    
    created_count = 0
    for template_path, content in medecin_templates.items():
        full_path = f'templates/{template_path}'
        if os.path.exists(full_path) and os.path.getsize(full_path) == 0:
            with open(full_path, 'w') as f:
                f.write(content)
            print(f"✅ Template vide complété: {template_path}")
            created_count += 1
        elif not os.path.exists(full_path):
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
            print(f"✅ Template créé: {template_path}")
            created_count += 1
    
    print(f"📊 {created_count} templates créés/complétés")

if __name__ == "__main__":
    analyze_problematic_templates()
    create_missing_templates() 
    fix_specific_issues()
    
    print("\n🎯 EXÉCUTEZ À NOUVEAU LA VÉRIFICATION:")
    print("python verify_migration.py")