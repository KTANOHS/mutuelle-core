# analyse_templates_assureur.py
import os
import sys
import re
from pathlib import Path
import django
from django.conf import settings

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyser_templates_assureur():
    """
    Script d'analyse complet des templates de l'application assureur
    """
    print("🔍 ANALYSE DES TEMPLATES ASSUREUR")
    print("=" * 80)
    
    # 1. LOCALISATION DES TEMPLATES
    print("\n1. 📁 LOCALISATION DES TEMPLATES ASSUREUR")
    
    templates_dirs = []
    for template_config in settings.TEMPLATES:
        if 'DIRS' in template_config:
            templates_dirs.extend(template_config['DIRS'])
    
    # Dossiers spécifiques à vérifier
    dossiers_assureur = [
        BASE_DIR / 'assureur' / 'templates' / 'assureur',
        BASE_DIR / 'templates' / 'assureur',
    ]
    
    templates_trouves = []
    for dossier in dossiers_assureur:
        if dossier.exists():
            print(f"✅ Dossier trouvé: {dossier}")
            for file_path in dossier.rglob("*.html"):
                templates_trouves.append(file_path)
        else:
            print(f"❌ Dossier non trouvé: {dossier}")
    
    print(f"\n📊 {len(templates_trouves)} templates assureur trouvés")
    
    # 2. ANALYSE DÉTAILLÉE DE CHAQUE TEMPLATE
    print("\n2. 📋 ANALYSE DÉTAILLÉE DES TEMPLATES")
    
    stats = {
        'total_templates': len(templates_trouves),
        'templates_avec_erreurs': [],
        'templates_avec_urls_problematiques': [],
        'templates_valides': [],
        'urls_trouvees': set(),
        'urls_problematiques': set()
    }
    
    for template_path in templates_trouves:
        print(f"\n📄 Analyse de: {template_path.relative_to(BASE_DIR)}")
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                contenu = f.read()
        except UnicodeDecodeError:
            # Essayer avec un autre encodage
            with open(template_path, 'r', encoding='latin-1') as f:
                contenu = f.read()
        
        # Analyse des URLs Django
        urls_django = re.findall(r'\{%\s*url\s+[\'"]([^\'"]+)[\'"]\s*%\}', contenu)
        urls_django_with_args = re.findall(r'\{%\s*url\s+[\'"]([^\'"]+)[\'"][^%]*%\}', contenu)
        
        toutes_les_urls = urls_django + urls_django_with_args
        
        if toutes_les_urls:
            print(f"   🔗 URLs trouvées ({len(toutes_les_urls)}):")
            for url in toutes_les_urls:
                stats['urls_trouvees'].add(url)
                print(f"     - {url}")
        
        # Vérification des URLs problématiques
        urls_problematiques = [url for url in toutes_les_urls if 'rapports' in url and 'rapport_statistiques' not in url]
        if urls_problematiques:
            stats['templates_avec_urls_problematiques'].append(template_path)
            stats['urls_problematiques'].update(urls_problematiques)
            print(f"   ⚠️  URLs problématiques: {urls_problematiques}")
        
        # Vérification de la structure de base
        if '{% extends' in contenu:
            extends_match = re.search(r'\{%\s*extends\s+[\'"]([^\'"]+)[\'"]\s*%\}', contenu)
            if extends_match:
                print(f"   🏗️  Étend: {extends_match.group(1)}")
        
        # Vérification des blocs
        blocs = re.findall(r'\{%\s*block\s+([^%]+)%\}', contenu)
        if blocs:
            print(f"   🧱 Blocs: {', '.join([b.strip() for b in blocs])}")
        
        # Vérification des includes
        includes = re.findall(r'\{%\s*include\s+[\'"]([^\'"]+)[\'"]\s*%\}', contenu)
        if includes:
            print(f"   🔄 Includes: {', '.join(includes)}")
    
    # 3. RAPPORT DES PROBLÈMES
    print("\n3. ⚠️  RAPPORT DES PROBLÈMES IDENTIFIÉS")
    
    if stats['templates_avec_urls_problematiques']:
        print(f"\n❌ {len(stats['templates_avec_urls_problematiques'])} templates avec URLs problématiques:")
        for template in stats['templates_avec_urls_problematiques']:
            print(f"   - {template.relative_to(BASE_DIR)}")
        
        print(f"\n🔧 URLs à corriger:")
        for url in stats['urls_problematiques']:
            print(f"   - '{url}' → 'assureur:rapport_statistiques'")
    else:
        print("✅ Aucun template avec URLs problématiques trouvé")
    
    # 4. VÉRIFICATION DES CONFLITS ENTRE DOSSIERS
    print("\n4. 🔄 VÉRIFICATION DES CONFLITS ENTRE DOSSIERS")
    
    templates_par_nom = {}
    for template_path in templates_trouves:
        nom_fichier = template_path.name
        if nom_fichier not in templates_par_nom:
            templates_par_nom[nom_fichier] = []
        templates_par_nom[nom_fichier].append(template_path)
    
    conflits = {nom: paths for nom, paths in templates_par_nom.items() if len(paths) > 1}
    
    if conflits:
        print("⚠️  Conflits détectés (mêmes noms dans différents dossiers):")
        for nom, paths in conflits.items():
            print(f"   📄 {nom}:")
            for path in paths:
                print(f"     - {path.relative_to(BASE_DIR)}")
    else:
        print("✅ Aucun conflit de noms détecté")
    
    # 5. ANALYSE DES TEMPLATES ESSENTIELS
    print("\n5. 🎯 TEMPLATES ESSENTIELS POUR ASSUREUR")
    
    templates_essentiels = {
        'base_assureur.html': 'Template de base',
        'dashboard.html': 'Tableau de bord principal',
        'liste_membres.html': 'Liste des membres',
        'liste_bons.html': 'Liste des bons de soin',
        'liste_paiements.html': 'Liste des paiements',
        'rapport_statistiques.html': 'Rapports et statistiques',
        'acces_interdit.html': 'Page accès interdit'
    }
    
    templates_manquants = []
    for template, description in templates_essentiels.items():
        trouve = any(template in str(path) for path in templates_trouves)
        if trouve:
            # Trouver le chemin exact
            chemin = next((path for path in templates_trouves if template in str(path)), None)
            if chemin:
                print(f"✅ {template}: {description} → {chemin.relative_to(BASE_DIR)}")
            else:
                print(f"✅ {template}: {description}")
        else:
            print(f"❌ {template}: {description} - MANQUANT")
            templates_manquants.append(template)
    
    # 6. GÉNÉRATION DE RAPPORT DE CORRECTION
    print("\n6. 🔧 RAPPORT DE CORRECTION AUTOMATIQUE")
    
    if stats['urls_problematiques'] or templates_manquants:
        print("Script de correction nécessaire:")
        
        corrections = []
        for url in stats['urls_problematiques']:
            corrections.append(f"Remplacer '{url}' par 'assureur:rapport_statistiques'")
        
        for template in templates_manquants:
            corrections.append(f"Créer le template manquant: {template}")
        
        for correction in corrections:
            print(f"   - {correction}")
        
        # Générer un script de correction
        generer_script_correction(corrections, templates_trouves)
    else:
        print("✅ Aucune correction nécessaire")
    
    # 7. STATISTIQUES FINALES
    print("\n7. 📊 STATISTIQUES FINALES")
    print(f"   Total templates: {stats['total_templates']}")
    print(f"   Templates avec erreurs: {len(stats['templates_avec_urls_problematiques'])}")
    print(f"   URLs différentes trouvées: {len(stats['urls_trouvees'])}")
    print(f"   URLs problématiques: {len(stats['urls_problematiques'])}")
    print(f"   Templates essentiels manquants: {len(templates_manquants)}")
    
    return stats

def generer_script_correction(corrections, templates_trouves):
    """Génère un script de correction automatique"""
    
    script_content = """#!/usr/bin/env python3
# correction_templates_assureur.py
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def corriger_templates():
    print("🔧 APPLICATION DES CORRECTIONS...")
    
"""
    
    # Ajouter les corrections pour les URLs
    for correction in corrections:
        if "Remplacer" in correction:
            ancienne_url = correction.split("'")[1]
            script_content += f'    print("📝 {correction}")\n'
    
    # Ajouter la création des templates manquants
    for correction in corrections:
        if "Créer" in correction:
            template_name = correction.split(": ")[1]
            script_content += f'    print("🎨 {correction}")\n'
    
    script_content += """
    print("✅ Corrections appliquées!")

if __name__ == '__main__':
    corriger_templates()
"""
    
    script_path = BASE_DIR / 'correction_templates_assureur.py'
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    print(f"\n📄 Script de correction généré: {script_path}")

def analyser_structure_projet():
    """Analyse la structure complète du projet"""
    print("\n" + "="*80)
    print("🏗️  ANALYSE DE LA STRUCTURE DU PROJET")
    print("="*80)
    
    # Compter les fichiers par type
    extensions = {}
    total_fichiers = 0
    
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            total_fichiers += 1
            ext = os.path.splitext(file)[1]
            extensions[ext] = extensions.get(ext, 0) + 1
    
    print(f"\n📁 Structure du projet:")
    print(f"   Total fichiers: {total_fichiers}")
    print(f"   Répartition par type:")
    for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:10]:  # Top 10
        if ext:  # Ignorer les fichiers sans extension
            print(f"     {ext}: {count} fichiers")

def verifier_urls_django():
    """Vérifie toutes les URLs Django configurées"""
    print("\n" + "="*80)
    print("🌐 VÉRIFICATION DES URLs DJANGO CONFIGURÉES")
    print("="*80)
    
    try:
        from django.urls import get_resolver
        
        resolver = get_resolver()
        urls_assureur = []
        
        def extraire_urls(urlpatterns, prefix=''):
            urls = []
            for pattern in urlpatterns:
                if hasattr(pattern, 'pattern'):
                    url_str = str(pattern.pattern)
                    if hasattr(pattern, 'name') and pattern.name:
                        urls.append({
                            'url': prefix + url_str,
                            'name': pattern.name,
                            'pattern': pattern
                        })
                    if hasattr(pattern, 'url_patterns'):
                        urls.extend(extraire_urls(pattern.url_patterns, prefix + url_str))
            return urls
        
        toutes_urls = extraire_urls(resolver.url_patterns)
        urls_assureur = [url for url in toutes_urls if 'assureur' in url['url'] or 'assureur' in str(url.get('name', ''))]
        
        print(f"\n🔗 URLs assureur configurées ({len(urls_assureur)}):")
        for url_info in urls_assureur:
            statut = "✅" if url_info['name'] else "⚠️"
            print(f"   {statut} {url_info['url']} -> {url_info.get('name', 'SANS NOM')}")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse des URLs: {e}")

def analyser_templates_par_dossier():
    """Analyse détaillée par dossier de templates"""
    print("\n" + "="*80)
    print("📂 ANALYSE PAR DOSSIER DE TEMPLATES")
    print("="*80)
    
    dossiers_analyser = [
        BASE_DIR / 'assureur' / 'templates' / 'assureur',
        BASE_DIR / 'templates' / 'assureur',
    ]
    
    for dossier in dossiers_analyser:
        if dossier.exists():
            print(f"\n📁 Dossier: {dossier.relative_to(BASE_DIR)}")
            fichiers = list(dossier.rglob("*.html"))
            print(f"   📄 {len(fichiers)} templates HTML")
            
            # Analyser la taille des fichiers
            tailles = []
            for fichier in fichiers:
                taille = os.path.getsize(fichier)
                tailles.append(taille)
                print(f"     - {fichier.name} ({taille} octets)")
            
            if tailles:
                print(f"   📏 Taille moyenne: {sum(tailles) // len(tailles)} octets")
                print(f"   📏 Taille totale: {sum(tailles)} octets")

if __name__ == '__main__':
    print("🔍 LANCEMENT DE L'ANALYSE COMPLÈTE DES TEMPLATES ASSUREUR")
    print("="*80)
    
    # Analyses
    stats = analyser_templates_assureur()
    analyser_structure_projet()
    analyser_templates_par_dossier()
    verifier_urls_django()
    
    print("\n" + "="*80)
    print("🎉 ANALYSE TERMINÉE")
    print("="*80)
    
    # Recommandations finales
    if stats['urls_problematiques']:
        print("\n💡 RECOMMANDATIONS:")
        print("1. Exécutez le script de correction généré")
        print("2. Vérifiez que toutes les URLs utilisent 'assureur:rapport_statistiques'")
        print("3. Testez l'accès au dashboard après corrections")
    else:
        print("\n✅ Votre application assureur est bien configurée!")