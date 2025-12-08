#!/usr/bin/env python3
"""
SCRIPT D'ANALYSE ASSUREUR - Diagnostic complet de l'application
Usage: python analyse_assureur.py
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

# =============================================================================
# IMPORTS APRÈS CONFIGURATION DJANGO
# =============================================================================
from django.urls import reverse, NoReverseMatch, get_resolver
from django.apps import apps
from django.db import connection
from django.core.checks import run_checks
import inspect
from collections import defaultdict

class AnalyseurAssureur:
    """Classe pour analyser l'application assureur"""
    
    def __init__(self):
        self.resultats = {
            'erreurs': [],
            'avertissements': [],
            'succes': [],
            'statistiques': defaultdict(int)
        }
        self.app_config = apps.get_app_config('assureur')
    
    def analyser_structure(self):
        """Analyse la structure de l'application"""
        print("\n" + "="*60)
        print("📁 ANALYSE STRUCTURELLE")
        print("="*60)
        
        # Vérification des dossiers
        dossiers_requis = [
            'templates/assureur',
            'templates/assureur/communication',
            'templates/assureur/partials',
            'migrations'
        ]
        
        for dossier in dossiers_requis:
            chemin = BASE_DIR / 'assureur' / dossier
            if chemin.exists():
                self.resultats['succes'].append(f"✅ Dossier {dossier} existe")
                self.resultats['statistiques']['dossiers_existants'] += 1
            else:
                self.resultats['avertissements'].append(f"⚠️ Dossier manquant: {dossier}")
                self.resultats['statistiques']['dossiers_manquants'] += 1
    
    def analyser_modeles(self):
        """Analyse les modèles"""
        print("\n" + "="*60)
        print("🗄️ ANALYSE DES MODÈLES")
        print("="*60)
        
        try:
            from assureur import models
            
            # Lister tous les modèles
            modeles = [model for model in apps.get_models() 
                      if model._meta.app_label == 'assureur']
            
            if not modeles:
                self.resultats['avertissements'].append("⚠️ Aucun modèle trouvé dans assureur")
                return
            
            for modele in modeles:
                self.resultats['statistiques']['modeles_total'] += 1
                print(f"📊 Modèle: {modele.__name__}")
                
                # Vérifier si le modèle a des objets
                try:
                    count = modele.objects.count()
                    print(f"   📈 Instances: {count}")
                    self.resultats['statistiques']['modeles_avec_donnees'] += 1
                except Exception as e:
                    print(f"   ❌ Erreur accès données: {e}")
                    self.resultats['erreurs'].append(f"Erreur modèle {modele.__name__}: {e}")
            
            self.resultats['succes'].append(f"✅ {len(modeles)} modèles analysés")
            
        except ImportError as e:
            self.resultats['erreurs'].append(f"❌ Impossible d'importer les modèles: {e}")
    
    def analyser_vues(self):
        """Analyse les vues"""
        print("\n" + "="*60)
        print("🖥️ ANALYSE DES VUES")
        print("="*60)
        
        try:
            from assureur import views
            
            # Lister toutes les fonctions de vue
            fonctions_vues = []
            for nom, obj in inspect.getmembers(views):
                if (inspect.isfunction(obj) and 
                    not nom.startswith('_') and
                    hasattr(obj, '__module__') and 
                    obj.__module__ == 'assureur.views'):
                    fonctions_vues.append((nom, obj))
            
            print(f"📊 Vues trouvées: {len(fonctions_vues)}")
            
            # Analyser chaque vue
            for nom_vue, fonction in fonctions_vues:
                self.resultats['statistiques']['vues_total'] += 1
                
                # Vérifier les décorateurs
                decorateurs = []
                if hasattr(fonction, '__wrapped__'):
                    # Vue décorée
                    wrappee = fonction
                    while hasattr(wrappee, '__wrapped__'):
                        decorateur_nom = wrappee.__name__
                        if decorateur_nom != nom_vue:
                            decorateurs.append(decorateur_nom)
                        wrappee = wrappee.__wrapped__
                
                statut = "✅" if decorateurs else "⚠️"
                print(f"   {statut} {nom_vue} - Décorateurs: {decorateurs or 'Aucun'}")
                
                if not decorateurs:
                    self.resultats['avertissements'].append(f"Vue sans décorateur: {nom_vue}")
            
            self.resultats['succes'].append(f"✅ {len(fonctions_vues)} vues analysées")
            
        except ImportError as e:
            self.resultats['erreurs'].append(f"❌ Impossible d'importer les vues: {e}")
    
    def analyser_urls(self):
        """Analyse les URLs"""
        print("\n" + "="*60)
        print("🔗 ANALYSE DES URLs")
        print("="*60)
        
        try:
            from assureur import urls
            
            # Récupérer toutes les URLs de l'application
            resolver = get_resolver()
            urls_assureur = []
            
            for pattern in resolver.url_patterns:
                if hasattr(pattern, 'app_name') and pattern.app_name == 'assureur':
                    urls_assureur.extend(pattern.url_patterns)
            
            print(f"📊 URLs configurées: {len(urls_assureur)}")
            
            # Tester chaque URL
            urls_valides = 0
            urls_erreur = 0
            
            for pattern in urls_assureur:
                try:
                    if hasattr(pattern, 'name') and pattern.name:
                        # Tester la résolution de l'URL
                        url_name = f"assureur:{pattern.name}"
                        reverse(url_name)
                        print(f"   ✅ {url_name} -> {pattern.pattern}")
                        urls_valides += 1
                    else:
                        print(f"   ⚠️ URL sans nom: {pattern.pattern}")
                        urls_erreur += 1
                        
                except NoReverseMatch as e:
                    print(f"   ❌ ERREUR URL: {pattern.name} - {e}")
                    self.resultats['erreurs'].append(f"URL invalide: {pattern.name}")
                    urls_erreur += 1
                except Exception as e:
                    print(f"   ❌ ERREUR: {pattern.name} - {e}")
                    urls_erreur += 1
            
            self.resultats['statistiques']['urls_valides'] = urls_valides
            self.resultats['statistiques']['urls_erreur'] = urls_erreur
            
            if urls_valides > 0:
                self.resultats['succes'].append(f"✅ {urls_valides} URLs valides")
            if urls_erreur > 0:
                self.resultats['avertissements'].append(f"⚠️ {urls_erreur} URLs avec problèmes")
                
        except ImportError as e:
            self.resultats['erreurs'].append(f"❌ Impossible d'importer les URLs: {e}")
    
    def analyser_templates(self):
        """Analyse les templates"""
        print("\n" + "="*60)
        print("📄 ANALYSE DES TEMPLATES")
        print("="*60)
        
        templates_dir = BASE_DIR / 'assureur' / 'templates' / 'assureur'
        
        if not templates_dir.exists():
            self.resultats['erreurs'].append("❌ Dossier templates/assureur introuvable")
            return
        
        # Compter les templates
        templates_html = list(templates_dir.rglob('*.html'))
        templates_communication = list((templates_dir / 'communication').rglob('*.html')) if (templates_dir / 'communication').exists() else []
        templates_partials = list((templates_dir / 'partials').rglob('*.html')) if (templates_dir / 'partials').exists() else []
        
        print(f"📊 Templates totaux: {len(templates_html)}")
        print(f"📊 Templates communication: {len(templates_communication)}")
        print(f"📊 Templates partials: {len(templates_partials)}")
        
        # Vérifier les templates essentiels
        templates_essentiels = [
            'base_assureur.html',
            'dashboard.html',
            'liste_membres.html',
            'liste_bons.html',
            'liste_paiements.html',
            'communication/liste_messages.html',
            'communication/envoyer_message.html'
        ]
        
        for template in templates_essentiels:
            chemin = templates_dir / template
            if chemin.exists():
                print(f"   ✅ {template}")
                self.resultats['statistiques']['templates_existants'] += 1
            else:
                print(f"   ❌ {template} - MANQUANT")
                self.resultats['avertissements'].append(f"Template manquant: {template}")
                self.resultats['statistiques']['templates_manquants'] += 1
        
        self.resultats['succes'].append(f"✅ {len(templates_html)} templates analysés")
    
    def analyser_base_de_donnees(self):
        """Analyse la base de données"""
        print("\n" + "="*60)
        print("🗃️ ANALYSE BASE DE DONNÉES")
        print("="*60)
        
        try:
            with connection.cursor() as cursor:
                # Vérifier les tables de l'application
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name LIKE 'assureur_%'
                """)
                tables = cursor.fetchall()
                
                print(f"📊 Tables assureur trouvées: {len(tables)}")
                
                for table in tables:
                    table_name = table[0]
                    # Compter les lignes
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    print(f"   📈 {table_name}: {count} enregistrements")
                    self.resultats['statistiques']['tables_bd'] += 1
                    self.resultats['statistiques']['enregistrements_total'] += count
            
            if tables:
                self.resultats['succes'].append(f"✅ {len(tables)} tables analysées")
            else:
                self.resultats['avertissements'].append("⚠️ Aucune table assureur trouvée")
                
        except Exception as e:
            self.resultats['erreurs'].append(f"❌ Erreur base de données: {e}")
    
    def analyser_problemes_communs(self):
        """Vérifie les problèmes courants"""
        print("\n" + "="*60)
        print("🔍 PROBLÈMES COURANTS")
        print("="*60)
        
        # Vérifier les URLs problématiques
        urls_problematiques = [
            'liste_messages_assureur',
            'envoyer_message_assureur', 
            'repondre_message_assureur',
            'liste_notifications_assureur'
        ]
        
        for url_name in urls_problematiques:
            try:
                reverse(f'assureur:{url_name}')
                print(f"   ✅ URL {url_name} - CORRECTE (nouveau nom)")
            except NoReverseMatch:
                # Essayer l'ancien nom sans namespace
                try:
                    reverse(url_name)
                    print(f"   ⚠️ URL {url_name} - Utilise l'ancien nom (sans namespace)")
                    self.resultats['avertissements'].append(f"URL utilise ancien nom: {url_name}")
                except NoReverseMatch:
                    print(f"   ❌ URL {url_name} - INTROUVABLE")
                    self.resultats['erreurs'].append(f"URL introuvable: {url_name}")
        
        # Vérifier les imports de communication
        try:
            from communication.models import Message, Notification
            print("   ✅ Module communication - DISPONIBLE")
            self.resultats['statistiques']['communication_disponible'] = 1
        except ImportError:
            print("   ⚠️ Module communication - INDISPONIBLE")
            self.resultats['avertissements'].append("Module communication non disponible")
            self.resultats['statistiques']['communication_disponible'] = 0
    
    def executer_verifications_django(self):
        """Exécute les vérifications système de Django"""
        print("\n" + "="*60)
        print("⚙️ VÉRIFICATIONS DJANGO")
        print("="*60)
        
        try:
            resultats_verif = run_checks()
            if resultats_verif:
                for verif in resultats_verif:
                    niveau = "❌" if verif.level >= 40 else "⚠️"
                    print(f"   {niveau} {verif.msg}")
                    if verif.level >= 40:
                        self.resultats['erreurs'].append(f"Django: {verif.msg}")
                    else:
                        self.resultats['avertissements'].append(f"Django: {verif.msg}")
            else:
                print("   ✅ Aucune erreur système détectée")
                self.resultats['succes'].append("Vérifications Django passées")
                
        except Exception as e:
            self.resultats['erreurs'].append(f"Erreur vérifications Django: {e}")
    
    def generer_rapport(self):
        """Génère un rapport final"""
        print("\n" + "="*60)
        print("📊 RAPPORT FINAL")
        print("="*60)
        
        # Afficher les statistiques
        print("\n📈 STATISTIQUES:")
        for cle, valeur in self.resultats['statistiques'].items():
            print(f"   {cle}: {valeur}")
        
        # Afficher les succès
        if self.resultats['succes']:
            print(f"\n✅ SUCCÈS ({len(self.resultats['succes'])}):")
            for succes in self.resultats['succes']:
                print(f"   {succes}")
        
        # Afficher les avertissements
        if self.resultats['avertissements']:
            print(f"\n⚠️ AVERTISSEMENTS ({len(self.resultats['avertissements'])}):")
            for avertissement in self.resultats['avertissements']:
                print(f"   {avertissement}")
        
        # Afficher les erreurs
        if self.resultats['erreurs']:
            print(f"\n❌ ERREURS ({len(self.resultats['erreurs'])}):")
            for erreur in self.resultats['erreurs']:
                print(f"   {erreur}")
        
        # Score global
        total_problemes = len(self.resultats['erreurs']) + len(self.resultats['avertissements'])
        if total_problemes == 0:
            print(f"\n🎉 EXCELLENT! Aucun problème détecté!")
        elif len(self.resultats['erreurs']) == 0:
            print(f"\n👍 BON! {len(self.resultats['avertissements'])} avertissements à corriger")
        else:
            print(f"\n💥 ATTENTION! {len(self.resultats['erreurs'])} erreurs et {len(self.resultats['avertissements'])} avertissements")
    
    def analyser_complet(self):
        """Exécute l'analyse complète"""
        print("🔍 DÉMARRAGE DE L'ANALYSE ASSUREUR...")
        
        self.analyser_structure()
        self.analyser_modeles()
        self.analyser_vues()
        self.analyser_urls()
        self.analyser_templates()
        self.analyser_base_de_donnees()
        self.analyser_problemes_communs()
        self.executer_verifications_django()
        self.generer_rapport()
        
        return self.resultats

# =============================================================================
# EXÉCUTION DU SCRIPT
# =============================================================================
if __name__ == "__main__":
    try:
        analyseur = AnalyseurAssureur()
        resultats = analyseur.analyser_complet()
        
        # Sauvegarder le rapport dans un fichier
        with open('rapport_assureur.txt', 'w', encoding='utf-8') as f:
            f.write("RAPPORT D'ANALYSE ASSUREUR\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("STATISTIQUES:\n")
            for cle, valeur in resultats['statistiques'].items():
                f.write(f"  {cle}: {valeur}\n")
            
            f.write(f"\nSUCCÈS ({len(resultats['succes'])}):\n")
            for succes in resultats['succes']:
                f.write(f"  {succes}\n")
            
            f.write(f"\nAVERTISSEMENTS ({len(resultats['avertissements'])}):\n")
            for avertissement in resultats['avertissements']:
                f.write(f"  {avertissement}\n")
            
            f.write(f"\nERREURS ({len(resultats['erreurs'])}):\n")
            for erreur in resultats['erreurs']:
                f.write(f"  {erreur}\n")
        
        print(f"\n📄 Rapport sauvegardé dans: rapport_assureur.txt")
        
        # Code de sortie basé sur les erreurs
        if resultats['erreurs']:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        sys.exit(1)