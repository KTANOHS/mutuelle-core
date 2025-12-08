#!/usr/bin/env python3
"""
Script de vérification et correction des templates après mise à jour
Vérifie la compatibilité entre base.html existant et les nouvelles bases
"""

import os
import re
from pathlib import Path

def check_template_compatibility():
    """Vérifie la compatibilité des templates"""
    print("🔍 VÉRIFICATION DE LA COMPATIBILITÉ DES TEMPLATES")
    print("=" * 50)
    
    templates_dir = "templates"
    issues = []
    
    # 1. Vérifier la structure de base.html existant
    base_html_path = os.path.join(templates_dir, "base.html")
    if os.path.exists(base_html_path):
        print(f"✅ base.html trouvé: {base_html_path}")
        issues.extend(analyze_base_html(base_html_path))
    else:
        issues.append("❌ base.html introuvable")
    
    # 2. Vérifier les nouvelles bases
    new_bases = [
        "base_home.html", "base_app.html",
        "apps/assureur/base_assureur.html",
        "apps/medecin/base_medecin.html", 
        "apps/pharmacien/base_pharmacien.html",
        "apps/membres/base_membres.html",
        "apps/paiements/base_paiements.html",
        "apps/soins/base_soins.html",
        "apps/api/base_api.html"
    ]
    
    for base in new_bases:
        path = os.path.join(templates_dir, base)
        if os.path.exists(path):
            print(f"✅ {base} trouvé")
            issues.extend(check_base_structure(path, base))
        else:
            print(f"⚠️  {base} manquant")
    
    # 3. Vérifier home.html
    home_path = os.path.join(templates_dir, "home.html")
    if os.path.exists(home_path):
        issues.extend(check_home_compatibility(home_path))
    
    return issues

def analyze_base_html(filepath):
    """Analyse la structure de base.html existant"""
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier les blocs critiques
        required_blocks = [
            ('{% block title %}', 'title'),
            ('{% block content %}', 'content'), 
            ('{% block extra_css %}', 'extra_css'),
            ('{% block extra_js %}', 'extra_js')
        ]
        
        for pattern, block_name in required_blocks:
            if pattern not in content:
                issues.append(f"⚠️  base.html: bloc '{block_name}' manquant")
            else:
                print(f"   ✅ Bloc {block_name} présent")
        
        # Vérifier les inclusions
        includes_to_check = [
            ('{% include.*header.html', 'header'),
            ('{% include.*footer.html', 'footer'),
            ('{% include.*messages.html', 'messages')
        ]
        
        for pattern, include_name in includes_to_check:
            if re.search(pattern, content):
                print(f"   ✅ Inclusion {include_name} présente")
            else:
                issues.append(f"ℹ️  base.html: inclusion '{include_name}' manquante (optionnel)")
        
        return issues
        
    except Exception as e:
        return [f"❌ Erreur lecture base.html: {str(e)}"]

def check_base_structure(filepath, base_name):
    """Vérifie la structure d'une base d'application"""
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier l'extension de base.html
        if '{% extends "base.html" %}' not in content:
            issues.append(f"⚠️  {base_name}: n'étend pas base.html")
        else:
            print(f"   ✅ {base_name} étend correctement base.html")
        
        return issues
        
    except Exception as e:
        return [f"❌ Erreur lecture {base_name}: {str(e)}"]

def check_home_compatibility(filepath):
    """Vérifie la compatibilité de home.html"""
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier si home.html utilise la nouvelle structure
        if '{% extends "base_home.html" %}' in content:
            print("✅ home.html utilise base_home.html")
        elif '{% extends "base.html" %}' in content:
            print("ℹ️  home.html utilise base.html (ancienne structure)")
            issues.append("💡 home.html: pourrait être migré vers base_home.html")
        else:
            issues.append("⚠️  home.html: structure d'extension non identifiée")
        
        return issues
        
    except Exception as e:
        return [f"❌ Erreur lecture home.html: {str(e)}"]

def generate_migration_guide(issues):
    """Génère un guide de migration basé sur les problèmes identifiés"""
    print("\n📋 GUIDE DE MIGRATION")
    print("=" * 50)
    
    if not issues:
        print("✅ Aucun problème critique détecté!")
        print("Vos templates sont compatibles avec la nouvelle structure.")
        return
    
    critical_issues = [issue for issue in issues if '❌' in issue or '⚠️' in issue]
    suggestions = [issue for issue in issues if 'ℹ️' in issue or '💡' in issue]
    
    if critical_issues:
        print("🚨 PROBLÈMES CRITIQUES:")
        for issue in critical_issues:
            print(f"   {issue}")
    
    if suggestions:
        print("\n💡 SUGGESTIONS D'AMÉLIORATION:")
        for suggestion in suggestions:
            print(f"   {suggestion}")
    
    print("\n🔧 ACTIONS RECOMMANDÉES:")
    
    if any("bloc" in issue for issue in critical_issues):
        print("""
1. Ajoutez les blocs manquants dans base.html:
   {% block title %}{% endblock %}
   {% block content %}{% endblock %}
   {% block extra_css %}{% endblock %}
   {% block extra_js %}{% endblock %}
        """)
    
    if any("home.html" in issue for issue in issues):
        print("""
2. Pour migrer home.html vers base_home.html:
   - Remplacez {% extends "base.html" %} par {% extends "base_home.html" %}
   - Vérifiez que votre contenu est dans {% block content %}
        """)

def create_compatibility_patch():
    """Crée un patch de compatibilité si nécessaire"""
    print("\n🔧 CRÉATION DE PATCH DE COMPATIBILITÉ")
    print("=" * 50)
    
    patch_content = """{# Patch de compatibilité pour base.html #}
{% comment %}
BLOCS REQUIS POUR LA NOUVELLE STRUCTURE
Ajoutez ces blocs dans votre base.html existant si manquants
{% endcomment %}

{# Bloc titre de la page #}
{% block title %}{% endblock %}

{# Bloc contenu principal #}
{% block content %}{% endblock %}

{# Bloc pour CSS supplémentaires #}
{% block extra_css %}{% endblock %}

{# Bloc pour JavaScript supplémentaires #}
{% block extra_js %}{% endblock %}
"""
    
    patch_path = "templates/compatibility_patch.html"
    with open(patch_path, 'w', encoding='utf-8') as f:
        f.write(patch_content)
    
    print(f"✅ Patch créé: {patch_path}")
    print("💡 Incluez ce contenu dans votre base.html si des blocs manquent")

def main():
    """Fonction principale"""
    print("🔄 VÉRIFICATION DE LA COMPATIBILITÉ DES TEMPLATES")
    print("=" * 60)
    
    # Vérifier la compatibilité
    issues = check_template_compatibility()
    
    # Générer le guide de migration
    generate_migration_guide(issues)
    
    # Créer un patch si nécessaire
    if any('bloc' in issue for issue in issues):
        create_compatibility_patch()
    
    print("\n🎉 VÉRIFICATION TERMINÉE!")
    print("\n📚 PROCHAINES ÉTAPES:")
    print("1. Vérifiez les problèmes identifiés ci-dessus")
    print("2. Appliquez les corrections nécessaires")
    print("3. Testez vos templates avec les nouvelles bases")
    print("4. Utilisez base_app.html pour les applications")
    print("5. Utilisez base_home.html pour la page d'accueil")

if __name__ == "__main__":
    main()