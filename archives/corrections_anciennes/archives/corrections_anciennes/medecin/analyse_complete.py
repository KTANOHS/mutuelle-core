# medecin/analyse_complete.py - VERSION CORRIGÉE
import os
import re
import inspect
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse, NoReverseMatch
from django.core.exceptions import ObjectDoesNotExist

def analyser_templates_corrige():
    """Version corrigée de l'analyse des templates"""
    print("\n📋 3. ANALYSE DES TEMPLATES ET BOUTONS")
    print("-" * 50)
    
    # CORRECTION : Chemin correct pour vos templates
    templates_dir = 'medecin/templates'
    
    if not os.path.exists(templates_dir):
        print(f"❌ Répertoire templates non trouvé: {templates_dir}")
        return None, None
    
    print(f"✅ Répertoire templates trouvé: {templates_dir}")
    
    templates_analyses = []
    problemes_csrf = []
    
    for fichier in os.listdir(templates_dir):
        if fichier.endswith('.html'):
            chemin = os.path.join(templates_dir, fichier)
            
            try:
                with open(chemin, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Analyser les formulaires POST
                forms_post = re.findall(r'<form[^>]*method=["\']post["\'][^>]*>', content, re.IGNORECASE)
                
                # Analyser les boutons et liens
                buttons = len(re.findall(r'<button', content))
                links = len(re.findall(r'<a href=', content))
                url_links = len(re.findall(r'{% url', content))
                
                print(f"📄 {fichier:25}")
                print(f"     ├─ Formulaires POST: {len(forms_post)}")
                
                # Vérifier CSRF tokens
                has_csrf = '{% csrf_token %}' in content
                
                if forms_post:
                    print(f"     ├─ CSRF Token: {'✅' if has_csrf else '❌'}")
                    if not has_csrf:
                        problemes_csrf.append(fichier)
                        print(f"     ├─ ⚠️  FORMULAIRES SANS CSRF!")
                
                print(f"     ├─ Boutons: {buttons}")
                print(f"     ├─ Liens: {links}")
                print(f"     └─ URLs Django: {url_links}")
                
                templates_analyses.append(fichier)
                
            except Exception as e:
                print(f"❌ Erreur lecture {fichier}: {e}")
    
    return templates_analyses, problemes_csrf

def analyser_application_medecin_corrige():
    """
    🎯 ANALYSE COMPLÈTE CORRIGÉE
    """
    print("🔍" * 60)
    print("🎯 ANALYSE COMPLÈTE CORRIGÉE - APPLICATION MÉDECIN")
    print("🔍" * 60)
    
    # 1. Analyse des URLs
    analyser_urls()
    
    print("\n" + "="*80)
    
    # 2. Analyse des vues et décorateurs
    analyser_vues()
    
    print("\n" + "="*80)
    
    # 3. Analyse CORRIGÉE des templates
    templates_analyses, problemes_csrf = analyser_templates_corrige()
    
    print("\n" + "="*80)
    
    # 4. Test fonctionnel
    tester_boutons_fonctionnels()
    
    print("\n" + "="*80)
    
    # 5. Rapport final
    generer_rapport_final_corrige(templates_analyses, problemes_csrf)

def generer_rapport_final_corrige(templates_analyses, problemes_csrf):
    """Rapport final corrigé"""
    print("\n📋 5. RAPPORT FINAL CORRIGÉ")
    print("-" * 50)
    
    urls_valides, urls_erreur = analyser_urls()
    vues_correctes, vues_problemes = analyser_vues()
    
    print(f"\n📊 STATISTIQUES GLOBALES:")
    print(f"   ├─ URLs valides: {len(urls_valides)}")
    print(f"   ├─ URLs en erreur: {len(urls_erreur)}")
    print(f"   ├─ Vues correctes: {len(vues_correctes)}")
    print(f"   ├─ Vues problématiques: {len(vues_problemes)}")
    print(f"   ├─ Templates analysés: {len(templates_analyses) if templates_analyses else 0}")
    print(f"   └─ Problèmes CSRF: {len(problemes_csrf) if problemes_csrf else 0}")
    
    print(f"\n🚨 PROBLÈMES IDENTIFIÉS:")
    
    if urls_erreur:
        print(f"   ❌ URLs non trouvées ({len(urls_erreur)}):")
        for url_name, description in urls_erreur:
            print(f"      - {description}")
    
    if vues_problemes:
        print(f"   ❌ Vues sans décorateurs ({len(vues_problemes)}):")
        for vue in vues_problemes:
            print(f"      - {vue}")
    
    if problemes_csrf:
        print(f"   ❌ Templates sans CSRF ({len(problemes_csrf)}):")
        for template in problemes_csrf:
            print(f"      - {template}")
    
    print(f"\n💡 RECOMMANDATIONS:")
    
    if urls_erreur:
        print("   1. 🔧 Ajouter dans medecin/urls.py:")
        print("      path('bon/<int:bon_id>/', views.detail_bon, name='detail_bon')")
        print("      path('bon/<int:bon_id>/ordonnance/', views.creer_ordonnance, name='creer_ordonnance')")
        print("      path('rendez-vous/<int:rdv_id>/statut/', views.modifier_statut_rdv, name='modifier_statut_rdv')")
    
    if problemes_csrf:
        print("   2. 🔧 Ajouter {% csrf_token %} dans les templates problématiques")
    
    if not urls_erreur and not vues_problemes and not problemes_csrf:
        print("   🎉 Tous les composants semblent corrects!")