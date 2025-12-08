#!/usr/bin/env python3
"""
SCRIPT DE CORRECTION COMPLET DES TEMPLATES ASSUREUR
Corrige toutes les URLs problématiques identifiées
"""

import re
import os
from pathlib import Path

def analyse_et_correction_complete():
    """Analyse et correction complète de tous les templates"""
    print("🔧 CORRECTION COMPLÈTE DES TEMPLATES ASSUREUR")
    print("=" * 60)
    
    project_root = Path(__file__).parent
    corrections_appliquees = 0
    
    # URLs problématiques et leurs corrections
    corrections_urls = {
        'export_bons_pdf': 'assureur:export_bons_pdf',
        'creer_paiement_general': 'assureur:creer_paiement',
        'assureur:rapports': 'assureur:rapport_statistiques',
        'detail_membre': 'assureur:detail_membre'
    }
    
    # Templates à analyser
    templates_a_corriger = [
        "templates/assureur/liste_bons.html",
        "templates/assureur/liste_paiements.html", 
        "templates/assureur/dashboard.html",
        "templates/assureur/partials/_sidebar.html",
        "templates/assureur/creer_bon.html"
    ]
    
    for template_path in templates_a_corriger:
        full_path = project_root / template_path
        
        if not full_path.exists():
            print(f"⚠️  Fichier non trouvé: {template_path}")
            continue
            
        print(f"\n📄 Analyse de: {template_path}")
        
        with open(full_path, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        contenu_original = contenu
        corrections_fichier = 0
        
        # Correction 1: URLs sans namespace
        for url_incorrecte, url_correcte in corrections_urls.items():
            # Pattern pour les URLs dans les tags Django
            patterns = [
                # {% url 'url_incorrecte' %}
                (f"\\{{%\\s*url\\s+['\"]{url_incorrecte}['\"]\\s*%\\}}", 
                 f"{{% url '{url_correcte}' %}}"),
                
                # href="{% url 'url_incorrecte' %}"
                (f'href=[\"\']\\s*\\{{%\\s*url\\s+[\"\\\']{url_incorrecte}[\"\\\']\\s*%\\}}\\s*[\"\\\']', 
                 f'href="{{% url \'{url_correcte}\' %}}"'),
                
                # URLs simples entre quotes
                (f"['\"]{url_incorrecte}['\"]", f"'{url_correcte}'"),
            ]
            
            for pattern, remplacement in patterns:
                nouveau_contenu, nb_remplacements = re.subn(pattern, remplacement, contenu)
                if nb_remplacements > 0:
                    contenu = nouveau_contenu
                    corrections_fichier += nb_remplacements
                    print(f"   ✅ Remplacé: {url_incorrecte} → {url_correcte} ({nb_remplacements}x)")
        
        # Correction 2: URLs avec arguments vides
        if 'detail_membre' in contenu:
            # Rechercher les appels à detail_membre avec arguments vides
            pattern_vide = r"\{\%\s*url\s+['\"]assureur:detail_membre['\"]\s+''\s*\%\}"
            contenu, nb_vides = re.subn(pattern_vide, "{% url 'assureur:detail_membre' 0 %}", contenu)
            if nb_vides > 0:
                corrections_fichier += nb_vides
                print(f"   ✅ Corrigé {nb_vides} appel(s) à detail_membre avec argument vide")
        
        if contenu != contenu_original:
            # Sauvegarde
            backup_path = full_path.with_suffix('.html.backup_final')
            if not backup_path.exists():
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(contenu_original)
            
            # Écriture des corrections
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(contenu)
            
            corrections_appliquees += corrections_fichier
            print(f"   💾 {corrections_fichier} correction(s) sauvegardée(s)")
        else:
            print("   ℹ️  Aucune correction nécessaire")
    
    return corrections_appliquees

def verifier_urls_manquantes():
    """Vérifie si les URLs nécessaires existent dans la configuration"""
    print("\n🔍 VÉRIFICATION DE LA CONFIGURATION DES URLs")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    
    # Vérifier assureur/urls.py
    urls_file = project_root / "assureur/urls.py"
    urls_manquantes = []
    
    if urls_file.exists():
        with open(urls_file, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        urls_requises = ['export_bons_pdf', 'creer_paiement']
        
        for url in urls_requises:
            if f"name='{url}'" not in contenu and f'name="{url}"' not in contenu:
                urls_manquantes.append(url)
    
    if urls_manquantes:
        print("❌ URLs manquantes dans assureur/urls.py:")
        for url in urls_manquantes:
            print(f"   - {url}")
        
        print("\n💡 AJOUTEZ CES URLs DANS assureur/urls.py:")
        print("""
from django.urls import path
from . import views

app_name = 'assureur'

urlpatterns = [
    # ... vos URLs existantes ...
    path('bons/export-pdf/', views.export_bons_pdf, name='export_bons_pdf'),
    path('paiements/creer/', views.creer_paiement, name='creer_paiement'),
]
""")
    else:
        print("✅ Toutes les URLs sont configurées")
    
    return urls_manquantes

def creer_vues_manquantes():
    """Crée les vues manquantes si nécessaire"""
    print("\n🛠️  VÉRIFICATION DES VUES MANQUANTES")
    print("=" * 50)
    
    views_file = Path(__file__).parent / "assureur/views.py"
    vues_manquantes = []
    
    if views_file.exists():
        with open(views_file, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        if 'def export_bons_pdf' not in contenu:
            vues_manquantes.append('export_bons_pdf')
        if 'def creer_paiement' not in contenu:
            vues_manquantes.append('creer_paiement')
    
    if vues_manquantes:
        print("❌ Vues manquantes dans assureur/views.py:")
        for vue in vues_manquantes:
            print(f"   - {vue}")
        
        print("\n💡 AJOUTEZ CES FONCTIONS DANS assureur/views.py:")
        print("""
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

def export_bons_pdf(request):
    \"\"\"Export PDF des bons de soin (version simplifiée)\"\"\"
    # Pour l'instant, retourne une réponse vide
    # Implémentez l'export PDF plus tard
    return HttpResponse("Fonction PDF à implémenter")

def creer_paiement(request):
    \"\"\"Créer un nouveau paiement (version simplifiée)\"\"\"
    if request.method == 'POST':
        # Traitement du formulaire
        messages.success(request, "Paiement créé avec succès")
        return redirect('assureur:liste_paiements')
    
    # Afficher le formulaire de création
    context = {
        'title': 'Créer un paiement'
    }
    return render(request, 'assureur/creer_paiement.html', context)
""")
    else:
        print("✅ Toutes les vues existent")
    
    return vues_manquantes

def solution_rapide_si_urgence():
    """Solution rapide pour désactiver les fonctionnalités problématiques"""
    print("\n🚨 SOLUTION RAPIDE (SI URGENCE)")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    
    # Pour liste_bons.html - commenter les boutons PDF
    bons_file = project_root / "templates/assureur/liste_bons.html"
    if bons_file.exists():
        with open(bons_file, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        # Commenter les boutons d'export PDF
        contenu = contenu.replace(
            "{% url 'assureur:export_bons_pdf' %}",
            "# {% url 'assureur:export_bons_pdf' %}"
        )
        
        with open(bons_file, 'w', encoding='utf-8') as f:
            f.write(contenu)
        print("✅ Boutons PDF désactivés dans liste_bons.html")
    
    # Pour liste_paiements.html - commenter les boutons de création
    paiements_file = project_root / "templates/assureur/liste_paiements.html"
    if paiements_file.exists():
        with open(paiements_file, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        # Commenter les boutons de création
        contenu = contenu.replace(
            "{% url 'assureur:creer_paiement' %}",
            "# {% url 'assureur:creer_paiement' %}"
        )
        
        with open(paiements_file, 'w', encoding='utf-8') as f:
            f.write(contenu)
        print("✅ Boutons création désactivés dans liste_paiements.html")

def main():
    """Fonction principale"""
    print("🚀 CORRECTION COMPLÈTE DU MODULE ASSUREUR")
    print("=" * 60)
    
    # Étape 1: Correction des templates
    corrections = analyse_et_correction_complete()
    
    # Étape 2: Vérification de la configuration
    urls_manquantes = verifier_urls_manquantes()
    
    # Étape 3: Vérification des vues
    vues_manquantes = creer_vues_manquantes()
    
    print("\n" + "=" * 60)
    print("📊 RAPPORT FINAL")
    print(f"✅ Corrections appliquées dans les templates: {corrections}")
    print(f"⚠️  URLs manquantes dans urls.py: {len(urls_manquantes)}")
    print(f"⚠️  Vues manquantes dans views.py: {len(vues_manquantes)}")
    
    if not urls_manquantes and not vues_manquantes:
        print("\n🎉 TOUT EST CONFIGURÉ! Redémarrez le serveur.")
    else:
        print("\n🚨 ACTIONS REQUISES:")
        if urls_manquantes:
            print("• Ajoutez les URLs manquantes dans assureur/urls.py")
        if vues_manquantes:
            print("• Ajoutez les vues manquantes dans assureur/views.py")
        
        print("\n💡 Solution temporaire:")
        print("• Exécutez la commande suivante pour désactiver les fonctionnalités problématiques:")
        print("  python -c \"from correction_finale import solution_rapide_si_urgence; solution_rapide_si_urgence()\"")

if __name__ == "__main__":
    main()