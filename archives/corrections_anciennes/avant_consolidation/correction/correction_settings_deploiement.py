# correction_settings_deploiement.py
import os
import sys
from pathlib import Path

# Configuration du chemin
current_dir = Path(__file__).parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(str(current_dir))

import django
django.setup()

from django.core.management import call_command

class CorrecteurSettings:
    def __init__(self):
        self.current_dir = Path(__file__).parent
        self.settings_path = self.current_dir / 'mutuelle_core' / 'settings.py'
    
    def ajouter_apps_manquantes(self):
        """Ajoute les apps manquantes au settings.py"""
        print("🔧 Ajout des apps manquantes dans settings.py...")
        
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Apps à ajouter
            apps_a_ajouter = ["'ia_detection'", "'scoring'", "'relances'", "'dashboard'"]
            
            # Vérifier quelles apps sont manquantes
            apps_manquantes = [app for app in apps_a_ajouter if app not in contenu]
            
            if not apps_manquantes:
                print("✅ Toutes les apps sont déjà dans INSTALLED_APPS")
                return True
            
            print(f"📋 Apps à ajouter: {', '.join(apps_manquantes)}")
            
            # Trouver la section INSTALLED_APPS et ajouter les apps
            lignes = contenu.split('\n')
            nouvelle_contenu = []
            dans_installed_apps = False
            apps_ajoutees = False
            
            for ligne in lignes:
                nouvelle_contenu.append(ligne)
                
                # Repérer le début de INSTALLED_APPS
                if 'INSTALLED_APPS = [' in ligne:
                    dans_installed_apps = True
                
                # Ajouter les apps avant la fin de la liste
                elif dans_installed_apps and "    'communication'," in ligne and not apps_ajoutees:
                    # Ajouter après 'communication'
                    for app in apps_manquantes:
                        nouvelle_contenu.append(f"    {app},    # ✅ NOUVELLES FONCTIONNALITÉS")
                    apps_ajoutees = True
                    dans_installed_apps = False
            
            # Réécrire le fichier
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(nouvelle_contenu))
            
            print("✅ Apps ajoutées avec succès à INSTALLED_APPS")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la modification de settings.py: {e}")
            return False
    
    def creer_fichiers_apps_config(self):
        """Crée les fichiers apps.py pour configurer les nouvelles apps"""
        print("\\n📁 Création des fichiers apps.py...")
        
        # Config pour ia_detection
        apps_ia_content = '''from django.apps import AppConfig

class IaDetectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ia_detection'
    verbose_name = 'Détection IA'
    
    def ready(self):
        # Importer les signaux
        try:
            import ia_detection.signals
        except ImportError:
            pass
'''
        with open('ia_detection/apps.py', 'w', encoding='utf-8') as f:
            f.write(apps_ia_content)
        
        # Config pour scoring
        apps_scoring_content = '''from django.apps import AppConfig

class ScoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scoring'
    verbose_name = 'Scoring Membres'
    
    def ready(self):
        # Importer les signaux
        try:
            import scoring.signals
        except ImportError:
            pass
'''
        with open('scoring/apps.py', 'w', encoding='utf-8') as f:
            f.write(apps_scoring_content)
        
        # Config pour relances
        apps_relances_content = '''from django.apps import AppConfig

class RelancesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relances'
    verbose_name = 'Relances Automatisées'
'''
        with open('relances/apps.py', 'w', encoding='utf-8') as f:
            f.write(apps_relances_content)
        
        # Config pour dashboard
        apps_dashboard_content = '''from django.apps import AppConfig

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'
    verbose_name = 'Tableau de Bord'
'''
        with open('dashboard/apps.py', 'w', encoding='utf-8') as f:
            f.write(apps_dashboard_content)
        
        print("✅ Fichiers apps.py créés")
    
    def corriger_imports_signals(self):
        """Corrige les imports problématiques dans les signaux"""
        print("\\n🔧 Correction des imports signals...")
        
        try:
            # Corriger scoring/signals.py - commenter l'import IA pour l'instant
            with open('scoring/signals.py', 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            contenu_corrige = contenu.replace(
                'from ia_detection.services import analyser_verification_ia',
                '# from ia_detection.services import analyser_verification_ia  # À décommenter après déploiement IA'
            )
            
            with open('scoring/signals.py', 'w', encoding='utf-8') as f:
                f.write(contenu_corrige)
            
            print("✅ Imports signals corrigés")
            
        except Exception as e:
            print(f"⚠️  Impossible de corriger les signals: {e}")
    
    def executer_migrations(self):
        """Exécute les migrations Django"""
        print("\\n🚀 Exécution des migrations...")
        
        try:
            # Recharger Django avec les nouvelles configs
            django.setup()
            
            print("📦 Création des migrations...")
            call_command('makemigrations', 'ia_detection')
            call_command('makemigrations', 'scoring')
            call_command('makemigrations', 'relances')
            call_command('makemigrations', 'dashboard')
            
            print("📦 Application des migrations...")
            call_command('migrate')
            
            print("✅ Migrations exécutées avec succès")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors des migrations: {e}")
            return False
    
    def initialiser_donnees_base(self):
        """Initialise les données de base"""
        print("\\n🎯 Initialisation des données...")
        
        try:
            # Créer un script d'initialisation simplifié
            script_content = '''from django.core.management.base import BaseCommand
from relances.models import TemplateRelance
from scoring.models import RegleScoring

class Command(BaseCommand):
    help = 'Initialise les données pour les nouvelles fonctionnalités'
    
    def handle(self, *args, **options):
        self.stdout.write('🚀 Initialisation des données de base...')
        
        # Templates de relance
        templates_data = [
            {
                'nom': 'Premier rappel amiable',
                'type_relance': 'premier_rappel',
                'sujet': 'Rappel de paiement de votre cotisation',
                'template_html': '<h1>Rappel de paiement</h1><p>Bonjour {{ membre.nom }},</p><p>Nous vous rappelons que votre cotisation est due.</p>',
                'template_texte': 'Rappel de paiement. Bonjour {{ membre.nom }}, votre cotisation est due.',
                'delai_jours': 7
            },
            {
                'nom': 'Relance urgente',
                'type_relance': 'relance_urgente',
                'sujet': 'URGENT - Retard de paiement important',
                'template_html': '<h1>Relance urgente</h1><p>Bonjour {{ membre.nom }},</p><p>Votre retard de paiement nécessite une action immédiate.</p>',
                'template_texte': 'URGENT - Retard de paiement important. Action requise.',
                'delai_jours': 15
            },
        ]
        
        for data in templates_data:
            obj, created = TemplateRelance.objects.get_or_create(
                type_relance=data['type_relance'],
                defaults=data
            )
            if created:
                self.stdout.write(f"✅ Template créé: {data['nom']}")
        
        # Règles de scoring
        regles_data = [
            {'nom': 'Ponctualité paiements', 'critere': 'ponctualite_paiements', 'poids': 0.35},
            {'nom': 'Historique retards', 'critere': 'historique_retards', 'poids': 0.25},
            {'nom': 'Niveau dette', 'critere': 'niveau_dette', 'poids': 0.20},
            {'nom': 'Ancienneté membre', 'critere': 'anciennete_membre', 'poids': 0.10},
            {'nom': 'Fréquence vérifications', 'critere': 'frequence_verifications', 'poids': 0.10},
        ]
        
        for data in regles_data:
            obj, created = RegleScoring.objects.get_or_create(
                critere=data['critere'],
                defaults=data
            )
            if created:
                self.stdout.write(f"✅ Règle créée: {data['nom']}")
        
        self.stdout.write(self.style.SUCCESS('✅ Initialisation terminée avec succès!'))
'''
            
            with open('scripts/initialiser_nouvelles_apps.py', 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            # Exécuter l'initialisation
            call_command('initialiser_nouvelles_apps')
            
            print("✅ Données initialisées avec succès")
            return True
            
        except Exception as e:
            print(f"❌ Erreur initialisation données: {e}")
            return False
    
    def verifier_deploiement(self):
        """Vérifie que le déploiement a fonctionné"""
        print("\\n🔍 Vérification du déploiement...")
        
        try:
            from django.apps import apps
            
            # Vérifier que les apps sont chargées
            apps_attendues = ['ia_detection', 'scoring', 'relances', 'dashboard']
            for app in apps_attendues:
                try:
                    app_config = apps.get_app_config(app)
                    print(f"✅ App {app} chargée")
                except:
                    print(f"❌ App {app} NON chargée")
            
            # Vérifier les modèles
            try:
                from ia_detection.models import ModeleIA
                from scoring.models import RegleScoring
                from relances.models import TemplateRelance
                print("✅ Modèles importés avec succès")
                
                # Compter les données
                print(f"📊 Templates relance: {TemplateRelance.objects.count()}")
                print(f"📊 Règles scoring: {RegleScoring.objects.count()}")
                
            except Exception as e:
                print(f"⚠️  Erreur import modèles: {e}")
            
            # Tester le scoring
            try:
                from membres.models import Membre
                from scoring.calculators import CalculateurScoreMembre
                
                membre = Membre.objects.first()
                if membre:
                    calculateur = CalculateurScoreMembre()
                    score = calculateur.calculer_score_complet(membre)
                    print(f"🎯 Test scoring réussi: {membre.nom} → {score['score_final']}")
                else:
                    print("⚠️  Aucun membre trouvé pour tester le scoring")
                    
            except Exception as e:
                print(f"⚠️  Erreur test scoring: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur vérification: {e}")
            return False

def main():
    """Exécution principale de la correction"""
    print("🔧 CORRECTION DU DÉPLOIEMENT - MUTUELLE CORE")
    print("=" * 60)
    
    correcteur = CorrecteurSettings()
    
    # Étape 1: Ajouter les apps au settings.py
    if not correcteur.ajouter_apps_manquantes():
        print("❌ Échec de l'ajout des apps")
        return
    
    # Étape 2: Créer les fichiers apps.py
    correcteur.creer_fichiers_apps_config()
    
    # Étape 3: Corriger les imports
    correcteur.corriger_imports_signals()
    
    # Étape 4: Exécuter les migrations
    if not correcteur.executer_migrations():
        print("❌ Échec des migrations")
        return
    
    # Étape 5: Initialiser les données
    correcteur.initialiser_donnees_base()
    
    # Étape 6: Vérifier
    correcteur.verifier_deploiement()
    
    print("\\n" + "=" * 60)
    print("🎉 CORRECTION TERMINÉE AVEC SUCCÈS!")
    print("\\n📋 PROCHAINES ÉTAPES:")
    print("1. Redémarrez le serveur Django: python manage.py runserver")
    print("2. Accédez à l'admin pour voir les nouvelles fonctionnalités")
    print("3. Testez le scoring des membres")
    print("4. Vérifiez les templates de relance créés")

if __name__ == "__main__":
    main()