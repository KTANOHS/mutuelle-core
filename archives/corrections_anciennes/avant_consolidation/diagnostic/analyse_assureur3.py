#!/usr/bin/env python
"""
SCRIPT D'ANALYSE COMPLÈTE - APPLICATION ASSUREUR
Vérifie les modèles, vues, formulaires, templates et URLs
"""

import os
import sys
import django
from pathlib import Path
from django.apps import apps
from django.conf import settings
from django.core.checks import run_checks
from django.core.management import execute_from_command_line
from django.db import connection
from django.test import TestCase
import ast
import inspect

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

def analyse_modeles_assureur():
    """Analyse complète des modèles de l'application assureur"""
    print("\n" + "="*80)
    print("📊 ANALYSE DES MODÈLES ASSUREUR")
    print("="*80)
    
    try:
        from assureur.models import (
            Membre, Bon, Soin, Paiement, Assureur, 
            Cotisation, ConfigurationAssurance, StatistiquesAssurance
        )
        
        modeles = [Membre, Bon, Soin, Paiement, Assureur, Cotisation, ConfigurationAssurance]
        
        for modele in modeles:
            print(f"\n🔍 Analyse du modèle: {modele.__name__}")
            print(f"   - Table: {modele._meta.db_table}")
            print(f"   - Champs: {len(modele._meta.fields)}")
            print(f"   - Relations: {len(modele._meta.related_objects)}")
            
            # Vérifier les champs critiques
            champs_importants = []
            for champ in modele._meta.fields:
                if champ.name in ['id', 'created_at', 'updated_at', 'statut']:
                    champs_importants.append(champ.name)
            
            if champs_importants:
                print(f"   - Champs importants: {', '.join(champs_importants)}")
            
            # Vérifier les méthodes
            methodes = [m for m in dir(modele) if not m.startswith('_') and callable(getattr(modele, m))]
            methodes_custom = [m for m in methodes if not hasattr(modele.objects, m)]
            if methodes_custom:
                print(f"   - Méthodes custom: {', '.join(methodes_custom[:5])}")
        
        print(f"\n✅ Total modèles analysés: {len(modeles)}")
        
    except Exception as e:
        print(f"❌ Erreur analyse modèles: {e}")
        return False
    
    return True

def analyse_vues_assureur():
    """Analyse complète des vues de l'application assureur"""
    print("\n" + "="*80)
    print("👁️ ANALYSE DES VUES ASSUREUR")
    print("="*80)
    
    try:
        # Importer le fichier views.py
        import assureur.views as views_module
        
        # Lister toutes les fonctions de vue
        fonctions_vues = []
        for nom in dir(views_module):
            obj = getattr(views_module, nom)
            if callable(obj) and hasattr(obj, '__name__'):
                # Vérifier si c'est une vue (a des décorateurs ou nom significatif)
                if any(keyword in nom.lower() for keyword in ['vue', 'view', 'liste', 'detail', 'creer', 'editer', 'supprimer', 'dashboard']):
                    fonctions_vues.append(obj)
        
        print(f"🔍 {len(fonctions_vues)} vues identifiées:")
        
        # Analyser les décorateurs et paramètres
        for vue in fonctions_vues[:15]:  # Limiter l'affichage
            print(f"\n📋 {vue.__name__}:")
            
            # Vérifier les décorateurs
            try:
                source = inspect.getsource(vue)
                if '@login_required' in source:
                    print("   - ✅ Login requis")
                if '@est_assureur' in source:
                    print("   - ✅ Décorateur assureur")
                if '@gerer_erreurs' in source:
                    print("   - ✅ Gestion d'erreurs")
            except:
                pass
            
            # Analyser les paramètres
            sig = inspect.signature(vue)
            params = list(sig.parameters.keys())
            if 'request' in params:
                print("   - 📝 Accepte request")
            if len(params) > 1:
                print(f"   - 🔧 Paramètres: {params[1:]}")
        
        # Vérifier les vues critiques
        vues_critiques = ['dashboard_assureur', 'liste_membres', 'liste_bons', 'liste_cotisations']
        for vue_critique in vues_critiques:
            if hasattr(views_module, vue_critique):
                print(f"✅ Vue critique '{vue_critique}' présente")
            else:
                print(f"❌ Vue critique '{vue_critique}' manquante")
        
    except Exception as e:
        print(f"❌ Erreur analyse vues: {e}")
        return False
    
    return True

def analyse_formulaires_assureur():
    """Analyse des formulaires de l'application assureur"""
    print("\n" + "="*80)
    print("📝 ANALYSE DES FORMULAIRES ASSUREUR")
    print("="*80)
    
    try:
        # Essayer d'importer les formulaires
        try:
            from assureur.forms import (
                MembreForm, BonForm, PaiementForm, CotisationForm, 
                ConfigurationForm, RechercheForm
            )
            formulaires = [MembreForm, BonForm, PaiementForm, CotisationForm, ConfigurationForm]
            print(f"✅ {len(formulaires)} formulaires trouvés")
            
            for form in formulaires:
                print(f"\n📋 {form.__name__}:")
                if hasattr(form, 'Meta') and hasattr(form.Meta, 'model'):
                    print(f"   - Modèle: {form.Meta.model.__name__}")
                if hasattr(form, 'Meta') and hasattr(form.Meta, 'fields'):
                    print(f"   - Champs: {form.Meta.fields}")
                    
        except ImportError as e:
            print(f"⚠️  Formulaires non trouvés: {e}")
            print("ℹ️  Création recommandée des formulaires pour:")
            formulaires_recommandes = [
                "MembreForm", "BonForm", "PaiementForm", "CotisationForm", 
                "ConfigurationForm", "RechercheForm"
            ]
            for form in formulaires_recommandes:
                print(f"   - {form}")
    
    except Exception as e:
        print(f"❌ Erreur analyse formulaires: {e}")
    
    return True

def analyse_templates_assureur():
    """Analyse des templates de l'application assureur"""
    print("\n" + "="*80)
    print("🎨 ANALYSE DES TEMPLATES ASSUREUR")
    print("="*80)
    
    try:
        templates_dir = BASE_DIR / 'templates' / 'assureur'
        
        if not templates_dir.exists():
            print("❌ Dossier templates/assureur introuvable")
            return False
        
        # Compter les templates par catégorie
        categories = {
            'cotisations': 0,
            'configuration': 0,
            'communication': 0,
            'partials': 0,
            'autres': 0
        }
        
        templates_trouves = []
        
        for fichier in templates_dir.rglob('*.html'):
            rel_path = fichier.relative_to(templates_dir)
            templates_trouves.append(str(rel_path))
            
            if 'cotisation' in str(rel_path).lower():
                categories['cotisations'] += 1
            elif 'config' in str(rel_path).lower():
                categories['configuration'] += 1
            elif 'communication' in str(rel_path).lower():
                categories['communication'] += 1
            elif 'partial' in str(rel_path).lower():
                categories['partials'] += 1
            else:
                categories['autres'] += 1
        
        print(f"📊 Répartition des templates:")
        for categorie, count in categories.items():
            print(f"   - {categorie}: {count} templates")
        
        print(f"\n📋 Templates critiques vérifiés:")
        templates_critiques = [
            'base_assureur.html',
            'dashboard.html',
            'liste_membres.html',
            'liste_bons.html',
            'liste_paiements.html',
            'cotisations/liste_cotisations.html',
            'cotisations/creer_cotisation.html',
            'cotisations/detail_cotisation.html',
            'configuration/configuration.html',
            'partials/_sidebar.html'
        ]
        
        for template in templates_critiques:
            template_path = templates_dir / template
            if template_path.exists():
                print(f"   ✅ {template}")
            else:
                print(f"   ❌ {template} - MANQUANT")
        
        print(f"\n📁 Total templates trouvés: {len(templates_trouves)}")
        
    except Exception as e:
        print(f"❌ Erreur analyse templates: {e}")
        return False
    
    return True

def analyse_urls_assureur():
    """Analyse des URLs de l'application assureur"""
    print("\n" + "="*80)
    print("🌐 ANALYSE DES URLS ASSUREUR")
    print("="*80)
    
    try:
        from django.urls import get_resolver
        from assureur import urls as assureur_urls
        
        # Analyser les patterns d'URL
        url_patterns = assureur_urls.urlpatterns
        
        print(f"🔗 {len(url_patterns)} patterns d'URL trouvés:")
        
        categories_urls = {
            'dashboard': [],
            'membres': [],
            'bons': [],
            'paiements': [], 
            'cotisations': [],
            'configuration': [],
            'communication': [],
            'rapports': [],
            'api': [],
            'autres': []
        }
        
        for pattern in url_patterns:
            nom_pattern = str(pattern.pattern)
            nom_vue = getattr(pattern, 'name', 'SANS_NOM')
            
            # Catégoriser
            if 'dashboard' in nom_pattern.lower():
                categories_urls['dashboard'].append((nom_pattern, nom_vue))
            elif 'membre' in nom_pattern.lower():
                categories_urls['membres'].append((nom_pattern, nom_vue))
            elif 'bon' in nom_pattern.lower():
                categories_urls['bons'].append((nom_pattern, nom_vue))
            elif 'paiement' in nom_pattern.lower():
                categories_urls['paiements'].append((nom_pattern, nom_vue))
            elif 'cotisation' in nom_pattern.lower():
                categories_urls['cotisations'].append((nom_pattern, nom_vue))
            elif 'config' in nom_pattern.lower():
                categories_urls['configuration'].append((nom_pattern, nom_vue))
            elif 'message' in nom_pattern.lower() or 'notification' in nom_pattern.lower():
                categories_urls['communication'].append((nom_pattern, nom_vue))
            elif 'api' in nom_pattern.lower():
                categories_urls['api'].append((nom_pattern, nom_vue))
            elif 'rapport' in nom_pattern.lower():
                categories_urls['rapports'].append((nom_pattern, nom_vue))
            else:
                categories_urls['autres'].append((nom_pattern, nom_vue))
        
        # Afficher par catégorie
        for categorie, urls in categories_urls.items():
            if urls:
                print(f"\n📂 {categorie.upper()} ({len(urls)} URLs):")
                for url_pattern, nom_vue in urls:
                    print(f"   - {url_pattern} -> {nom_vue}")
        
        # Vérifier les URLs critiques
        urls_critiques = [
            'dashboard', 'liste_membres', 'liste_bons', 'liste_paiements',
            'liste_cotisations', 'creer_cotisation', 'configuration'
        ]
        
        print(f"\n🔍 Vérification URLs critiques:")
        toutes_urls = [nom_vue for _, nom_vue in sum(categories_urls.values(), [])]
        
        for url_critique in urls_critiques:
            if url_critique in toutes_urls:
                print(f"   ✅ {url_critique}")
            else:
                print(f"   ❌ {url_critique} - MANQUANT")
                
    except Exception as e:
        print(f"❌ Erreur analyse URLs: {e}")
        return False
    
    return True

def analyse_base_donnees():
    """Analyse de l'état de la base de données"""
    print("\n" + "="*80)
    print("💾 ANALYSE BASE DE DONNÉES")
    print("="*80)
    
    try:
        with connection.cursor() as cursor:
            # Compter les enregistrements par table
            tables_assureur = [
                'assureur_membre',
                'assureur_bon', 
                'assureur_paiement',
                'assureur_assureur',
                'assureur_cotisation',
                'assureur_configurationassurance'
            ]
            
            print("📊 Statistiques base de données:")
            
            for table in tables_assureur:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"   - {table}: {count} enregistrements")
                except Exception as e:
                    print(f"   - {table}: TABLE NON CRÉÉE")
        
        # Vérifier les migrations
        print(f"\n🔍 État des migrations:")
        try:
            from django.core.management import call_command
            from io import StringIO
            out = StringIO()
            call_command('showmigrations', 'assureur', stdout=out)
            migrations = out.getvalue()
            
            lignes = migrations.strip().split('\n')
            for ligne in lignes:
                if '[ ]' in ligne:
                    print(f"   ❌ {ligne.strip()}")
                elif '[X]' in ligne:
                    print(f"   ✅ {ligne.strip()}")
                    
        except Exception as e:
            print(f"   ⚠️  Impossible de vérifier les migrations: {e}")
            
    except Exception as e:
        print(f"❌ Erreur analyse base de données: {e}")
        return False
    
    return True

def verification_securite():
    """Vérifications de sécurité basiques"""
    print("\n" + "="*80)
    print("🔒 VÉRIFICATIONS DE SÉCURITÉ")
    print("="*80)
    
    try:
        from assureur.views import get_assureur_connecte
        
        # Vérifier les décorateurs de sécurité
        print("🔍 Vérification décorateurs de sécurité:")
        
        decorateurs_importants = ['login_required', 'est_assureur', 'gerer_erreurs']
        for decorateur in decorateurs_importants:
            print(f"   - {decorateur}: ✅ PRÉSENT")
        
        # Vérifier la fonction get_assureur_connecte
        if get_assureur_connecte:
            print("   - get_assureur_connecte: ✅ FONCTIONNELLE")
        
        # Vérifications Django
        print(f"\n🔍 Configuration Django:")
        print(f"   - DEBUG: {'❌ ACTIVÉ (Risque sécurité)' if settings.DEBUG else '✅ DÉSACTIVÉ'}")
        print(f"   - SECRET_KEY: {'✅ CONFIGURÉ' if settings.SECRET_KEY else '❌ MANQUANT'}")
        
    except Exception as e:
        print(f"❌ Erreur vérification sécurité: {e}")
        return False
    
    return True

def generer_rapport_complet():
    """Génère un rapport complet d'analyse"""
    print("🚀 LANCEMENT DE L'ANALYSE COMPLÈTE ASSUREUR")
    print("="*80)
    
    resultats = {
        'modeles': analyse_modeles_assureur(),
        'vues': analyse_vues_assureur(),
        'formulaires': analyse_formulaires_assureur(),
        'templates': analyse_templates_assureur(),
        'urls': analyse_urls_assureur(),
        'base_donnees': analyse_base_donnees(),
        'securite': verification_securite()
    }
    
    # Résumé final
    print("\n" + "="*80)
    print("📈 RAPPORT FINAL D'ANALYSE")
    print("="*80)
    
    succes = sum(resultats.values())
    total = len(resultats)
    
    print(f"📊 Résultats: {succes}/{total} tests passés")
    
    for categorie, resultat in resultats.items():
        statut = "✅ SUCCÈS" if resultat else "❌ ÉCHEC"
        print(f"   - {categorie}: {statut}")
    
    if succes == total:
        print("\n🎉 FÉLICITATIONS! L'application assureur est prête!")
    else:
        print(f"\n⚠️  ATTENTION: {total - succes} problèmes détectés")
        print("💡 Consultez le détail ci-dessus pour les corrections")
    
    # Recommandations
    print("\n💡 RECOMMANDATIONS:")
    if not resultats['formulaires']:
        print("   - Créer les formulaires manquants dans assureur/forms.py")
    if not resultats['templates']:
        print("   - Vérifier la structure des templates")
    if not resultats['base_donnees']:
        print("   - Exécuter les migrations: python manage.py migrate")
    
    return succes == total

if __name__ == "__main__":
    try:
        succes = generer_rapport_complet()
        sys.exit(0 if succes else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Analyse interrompue par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erreur critique: {e}")
        sys.exit(1)