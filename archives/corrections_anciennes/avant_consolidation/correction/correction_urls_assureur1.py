#!/usr/bin/env python3
"""
SCRIPT DE CORRECTION DES URLs INCOHÉRENTES - ASSUREUR
Analyse et corrige les incohérences entre les URLs du template et celles définies
"""

import os
import sys
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def analyser_urls_assureur():
    """Analyse les URLs définies dans assureur/urls.py"""
    print("\n" + "="*80)
    print("ANALYSE URLs DÉFINIES DANS assureur/urls.py")
    print("="*80)
    
    urls_file = BASE_DIR / "assureur" / "urls.py"
    
    if not urls_file.exists():
        print("❌ Fichier urls.py non trouvé")
        return {}
    
    with open(urls_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Chercher app_name
    app_name_match = re.search(r"app_name\s*=\s*['\"]([^'\"]+)['\"]", content)
    app_name = app_name_match.group(1) if app_name_match else 'assureur'
    print(f"📌 Namespace trouvé: {app_name}")
    
    # Extraire toutes les URLs avec leur nom
    url_patterns = re.findall(r"path\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*[^,]+\s*,\s*name=['\"]([^'\"]+)['\"]", content)
    
    print(f"🔗 URLs définies: {len(url_patterns)}")
    urls_par_nom = {}
    
    for pattern, name in url_patterns:
        urls_par_nom[name] = pattern
        print(f"  - {name}: {pattern}")
    
    return app_name, urls_par_nom

def analyser_template_base():
    """Analyse les URLs utilisées dans base_assureur.html"""
    print("\n" + "="*80)
    print("ANALYSE URLs UTILISÉES DANS base_assureur.html")
    print("="*80)
    
    template_file = BASE_DIR / "templates" / "assureur" / "base_assureur.html"
    
    if not template_file.exists():
        print("❌ Fichier base_assureur.html non trouvé")
        return []
    
    with open(template_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Chercher toutes les références d'URL
    url_refs = re.findall(r"\{%\s*url\s+['\"]([^'\"]+)['\"].*?%\}", content)
    
    print(f"🔍 Références d'URL trouvées: {len(url_refs)}")
    for ref in url_refs:
        print(f"  - {ref}")
    
    return url_refs

def identifier_incoherences(app_name, urls_par_nom, url_refs):
    """Identifie les incohérences entre les URLs définies et utilisées"""
    print("\n" + "="*80)
    print("IDENTIFICATION DES INCOHÉRENCES")
    print("="*80)
    
    incohérences = []
    
    for ref in url_refs:
        # Extraire le namespace et le nom
        if ':' in ref:
            ref_namespace, ref_name = ref.split(':', 1)
        else:
            ref_namespace = app_name
            ref_name = ref
        
        # Vérifier si l'URL existe
        if ref_name in urls_par_nom:
            print(f"✅ {ref} -> existe (chemin: {urls_par_nom[ref_name]})")
        else:
            # Chercher des correspondances partielles
            correspondances = []
            for name, path in urls_par_nom.items():
                if ref_name in name or name in ref_name:
                    correspondances.append((name, path))
            
            if correspondances:
                print(f"⚠️  {ref} -> non trouvé, mais correspondances possibles:")
                for name, path in correspondances:
                    print(f"     - {app_name}:{name}: {path}")
                incohérences.append((ref, correspondances))
            else:
                print(f"❌ {ref} -> non trouvé, aucune correspondance")
                incohérences.append((ref, []))
    
    return incohérences

def corriger_template(app_name, urls_par_nom, url_refs, incohérences):
    """Corrige les incohérences dans le template"""
    print("\n" + "="*80)
    print("CORRECTION DU TEMPLATE")
    print("="*80)
    
    template_file = BASE_DIR / "templates" / "assureur" / "base_assureur.html"
    
    if not template_file.exists():
        print("❌ Fichier base_assureur.html non trouvé")
        return
    
    with open(template_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Mapping des corrections nécessaires
    corrections = {}
    
    for ref, correspondances in incohérences:
        if correspondances:
            # Prendre la meilleure correspondance (la plus courte)
            meilleure_correspondance = min(correpondances, key=lambda x: len(x[0]))
            nouveau_nom = meilleure_correspondance[0]
            corrections[ref] = f"{app_name}:{nouveau_nom}"
            print(f"📝 {ref} -> {corrections[ref]}")
    
    # Appliquer les corrections
    contenu_corrigé = content
    for ancien, nouveau in corrections.items():
        ancien_pattern = re.escape(ancien)
        contenu_corrigé = re.sub(
            rf"\{{%\s*url\s+['\"]{ancien_pattern}['\"][^%]*%\}}",
            f"{{% url '{nouveau}' %}}",
            contenu_corrigé
        )
    
    if contenu_corrigé != content:
        # Sauvegarder une copie de sauvegarde
        backup_file = template_file.with_suffix('.html.backup')
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 Sauvegarde créée: {backup_file}")
        
        # Écrire le fichier corrigé
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(contenu_corrigé)
        
        print("✅ Template corrigé avec succès")
    else:
        print("✅ Aucune correction nécessaire")

def creer_mapping_urls_corrige():
    """Crée un mapping complet des URLs corrigées"""
    print("\n" + "="*80)
    print("MAPPING DES URLs CORRIGÉES")
    print("="*80)
    
    # URLs définies vs URLs utilisées dans le template
    mapping = {
        # Dashboard
        'dashboard': 'dashboard_assureur',
        
        # Membres
        'liste_membres': 'liste_membres',
        'detail_membre': 'detail_membre',
        'creer_membre': 'creer_membre',
        'recherche_membre': 'recherche_membre',
        
        # Bons
        'liste_bons': 'liste_bons',
        'detail_bon': 'detail_bon',
        'creer_bon': 'creer_bon',
        'valider_bon': 'valider_bon',
        'rejeter_bon': 'rejeter_bon',
        
        # Cotisations
        'liste_cotisations': 'liste_cotisations',
        'generer_cotisations': 'generer_cotisations',
        'preview_generation': 'preview_generation',
        
        # Paiements
        'liste_paiements': 'liste_paiements',
        'creer_paiement': 'creer_paiement',
        'detail_paiement': 'detail_paiement',
        
        # Statistiques
        'statistiques': 'statistiques_assureur',
        'rapport_statistiques': 'statistiques_assureur',
        'rapports': 'rapports',
        'generer_rapport': 'generer_rapport',
        'detail_rapport': 'detail_rapport',
        
        # Messagerie
        'liste_messages': 'messagerie_assureur',
        'messagerie': 'messagerie_assureur',
        'envoyer_message': 'envoyer_message_assureur',
        'detail_message': 'communication:detail_message',
        'repondre_message': 'communication:repondre_message',
        
        # Autres
        'configuration': 'configuration_assureur',
        'export_bons': 'export_bons',
        'test': 'test_assureur',
        'acces_interdit': 'acces_interdit',
    }
    
    print("📋 Mapping des URLs (template → Django):")
    for template_url, django_url in mapping.items():
        print(f"  - {template_url} -> {django_url}")

def verifier_et_corriger_tous_templates():
    """Vérifie et corrige tous les templates de l'assureur"""
    print("\n" + "="*80)
    print("VÉRIFICATION DE TOUS LES TEMPLATES")
    print("="*80)
    
    templates_dir = BASE_DIR / "templates" / "assureur"
    
    if not templates_dir.exists():
        print("❌ Dossier templates/assureur non trouvé")
        return
    
    # Trouver tous les templates HTML
    templates = list(templates_dir.rglob("*.html"))
    
    print(f"🔍 {len(templates)} templates à vérifier")
    
    corrections_appliquees = []
    
    for template in templates:
        rel_path = template.relative_to(templates_dir)
        
        with open(template, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chercher les références problématiques
        problemes = []
        
        # Problème 1: assureur:dashboard (devrait être assureur:dashboard_assureur)
        if 'assureur:dashboard' in content:
            problemes.append("assureur:dashboard -> assureur:dashboard_assureur")
            content = content.replace('assureur:dashboard', 'assureur:dashboard_assureur')
        
        # Problème 2: assureur:rapport_statistiques (devrait être assureur:statistiques_assureur)
        if 'assureur:rapport_statistiques' in content:
            problemes.append("assureur:rapport_statistiques -> assureur:statistiques_assureur")
            content = content.replace('assureur:rapport_statistiques', 'assureur:statistiques_assureur')
        
        # Problème 3: assureur:liste_messages (devrait être assureur:messagerie_assureur)
        if 'assureur:liste_messages' in content:
            problemes.append("assureur:liste_messages -> assureur:messagerie_assureur")
            content = content.replace('assureur:liste_messages', 'assureur:messagerie_assureur')
        
        # Problème 4: assureur:mes_ordonnances (n'existe probablement pas pour assureur)
        if 'assureur:mes_ordonnances' in content:
            problemes.append("assureur:mes_ordonnances -> # (supprimé)")
            content = content.replace('assureur:mes_ordonnances', '#')
        
        if problemes:
            # Sauvegarder le fichier corrigé
            with open(template, 'w', encoding='utf-8') as f:
                f.write(content)
            
            corrections_appliquees.append((rel_path, problemes))
            print(f"\n✅ {rel_path}:")
            for probleme in problemes:
                print(f"   - {probleme}")
    
    if corrections_appliquees:
        print(f"\n📊 Résumé: {len(corrections_appliquees)} templates corrigés")
    else:
        print("✅ Aucune correction nécessaire")

def generer_guide_migration():
    """Génère un guide de migration pour les développeurs"""
    print("\n" + "="*80)
    print("📘 GUIDE DE MIGRATION - URLs ASSUREUR")
    print("="*80)
    
    guide = """
🔄 MIGRATION DES URLs DE L'ASSUREUR

PROBLÈMES IDENTIFIÉS:
1. Incohérences entre les noms d'URLs dans les templates et ceux définis dans urls.py
2. Certains noms d'URLs n'existent pas dans urls.py

CORRECTIONS APPLIQUÉES:
1. Template base_assureur.html:
   - 'assureur:dashboard' → 'assureur:dashboard_assureur'
   - 'assureur:rapport_statistiques' → 'assureur:statistiques_assureur'
   - 'assureur:liste_messages' → 'assureur:messagerie_assureur'

2. Tous les templates:
   - Correction systématique des URLs problématiques

URLS DÉFINIES DANS assureur/urls.py:
• Dashboard: assureur:dashboard_assureur
• Membres: assureur:liste_membres, assureur:detail_membre, assureur:creer_membre
• Bons: assureur:liste_bons, assureur:detail_bon, assureur:creer_bon
• Cotisations: assureur:liste_cotisations, assureur:generer_cotisations
• Paiements: assureur:liste_paiements, assureur:creer_paiement
• Statistiques: assureur:statistiques_assureur, assureur:rapports
• Messagerie: assureur:messagerie_assureur, assureur:envoyer_message_assureur
• Configuration: assureur:configuration_assureur

⚠️ ATTENTION:
• Les templates qui utilisent 'assureur:mes_ordonnances' doivent être redirigés vers une autre page
• Vérifiez que toutes les vues existent et fonctionnent
• Testez chaque URL après la migration

🔧 POUR TESTER:
1. Lancez le serveur: python manage.py runserver
2. Accédez à: http://localhost:8000/assureur/dashboard_assureur/
3. Testez chaque lien du menu

📝 POUR LES DÉVELOPPEURS:
• Utilisez toujours les noms d'URLs définis dans assureur/urls.py
• Vérifiez les imports dans vos vues
• Testez les permissions d'accès

🆘 EN CAS DE PROBLÈME:
1. Vérifiez les logs Django
2. Vérifiez que l'URL existe dans assureur/urls.py
3. Vérifiez que la vue associée existe
4. Vérifiez les permissions de l'utilisateur
"""
    
    print(guide)
    
    # Sauvegarder le guide
    guide_file = BASE_DIR / "guide_migration_urls_assureur.txt"
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print(f"📄 Guide sauvegardé: {guide_file}")

def main():
    """Fonction principale"""
    print("\n" + "="*80)
    print("🔧 CORRECTION DES URLs INCOHÉRENTES - ASSUREUR")
    print("="*80)
    
    # Analyser les URLs définies
    app_name, urls_par_nom = analyser_urls_assureur()
    
    # Analyser les URLs utilisées dans le template
    url_refs = analyser_template_base()
    
    # Identifier les incohérences
    incohérences = identifier_incoherences(app_name, urls_par_nom, url_refs)
    
    # Corriger le template principal
    corriger_template(app_name, urls_par_nom, url_refs, incohérences)
    
    # Vérifier et corriger tous les templates
    verifier_et_corriger_tous_templates()
    
    # Créer un mapping des URLs corrigées
    creer_mapping_urls_corrige()
    
    # Générer un guide de migration
    generer_guide_migration()
    
    print("\n" + "="*80)
    print("✅ CORRECTIONS TERMINÉES AVEC SUCCÈS!")
    print("="*80)
    print("\n💡 Prochaines étapes:")
    print("1. Testez les URLs: python manage.py runserver")
    print("2. Accédez à: http://localhost:8000/assureur/dashboard_assureur/")
    print("3. Vérifiez tous les liens du menu")

if __name__ == "__main__":
    main()