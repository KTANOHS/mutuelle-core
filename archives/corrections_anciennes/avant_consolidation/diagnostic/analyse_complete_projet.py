# analyse_complete_projet.py

import os
import sys
import django
import subprocess
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.core.management import call_command
from django.urls import get_resolver, reverse, NoReverseMatch
from django.template.loader import get_template
import importlib
import inspect

class AnalyseCompleteProjet:
    def __init__(self):
        self.resultats = {
            'applications': {},
            'modeles': {},
            'vues': {},
            'urls': {},
            'templates': {},
            'permissions': {},
            'donnees': {},
            'problemes': [],
            'recommandations': []
        }
    
    def executer_analyse_complete(self):
        """Exécute l'analyse complète du projet"""
        print("🚀 ANALYSE COMPLÈTE DU PROJET DJANGO")
        print("=" * 70)
        print()
        
        self.analyser_structure_projet()
        self.analyser_applications()
        self.analyser_modeles()
        self.analyser_vues()
        self.analyser_urls()
        self.analyser_templates()
        self.analyser_permissions()
        self.analyser_donnees()
        self.verifier_integrations()
        self.generer_rapport_complet()
    
    def analyser_structure_projet(self):
        """Analyse la structure globale du projet"""
        print("📁 1. STRUCTURE DU PROJET")
        print("-" * 40)
        
        # Dossier racine
        racine = Path('.')
        dossiers_projet = [d for d in racine.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        print("   📂 Dossiers principaux:")
        for dossier in sorted(dossiers_projet):
            if dossier.name in ['venv', '__pycache__', '.git', 'logs', 'media', 'static', 'staticfiles']:
                continue
            nb_fichiers = len(list(dossier.rglob('*.py')))
            print(f"      • {dossier.name}/ ({nb_fichiers} fichiers Python)")
        
        # Fichiers principaux
        fichiers_importants = ['manage.py', 'requirements.txt']
        print("\n   📄 Fichiers importants:")
        for fichier in fichiers_importants:
            if racine.joinpath(fichier).exists():
                print(f"      ✅ {fichier}")
            else:
                print(f"      ❌ {fichier} manquant")
                self.resultats['problemes'].append(f"Fichier {fichier} manquant")
    
    def analyser_applications(self):
        """Analyse toutes les applications Django"""
        print("\n📦 2. APPLICATIONS DJANGO")
        print("-" * 40)
        
        applications = apps.get_app_configs()
        applications_custom = [app for app in applications if not app.name.startswith('django.')]
        
        print(f"   📊 {len(applications_custom)} applications personnalisées:")
        
        for app in sorted(applications_custom, key=lambda x: x.name):
            # CORRECTION: Convertir le générateur en liste
            modeles_list = list(app.get_models())
            modeles_count = len(modeles_list)
            migrations_count = len(self.compter_migrations(app.name))
            
            statut = "✅" if modeles_count > 0 else "⚠️"
            print(f"      {statut} {app.name}")
            print(f"          📋 Modèles: {modeles_count}")
            print(f"          🚚 Migrations: {migrations_count}")
            print(f"          📁 Chemin: {app.path}")
            
            self.resultats['applications'][app.name] = {
                'modeles': modeles_count,
                'migrations': migrations_count,
                'chemin': str(app.path)
            }
    
    def compter_migrations(self, app_name):
        """Compte les migrations d'une application"""
        try:
            migrations_dir = Path(apps.get_app_config(app_name).path) / 'migrations'
            if migrations_dir.exists():
                return [f for f in migrations_dir.iterdir() if f.is_file() and f.name.endswith('.py') and f.name != '__init__.py']
            return []
        except:
            return []
    
    def analyser_modeles(self):
        """Analyse détaillée de tous les modèles"""
        print("\n🗄️ 3. ANALYSE DES MODÈLES")
        print("-" * 40)
        
        total_modeles = 0
        total_champs = 0
        
        for app in apps.get_app_configs():
            if app.name.startswith('django.'):
                continue
                
            # CORRECTION: Convertir le générateur en liste
            modeles_app = list(app.get_models())
            if not modeles_app:
                continue
                
            print(f"   📋 {app.name}:")
            
            for modele in modeles_app:
                total_modeles += 1
                champs = modele._meta.get_fields()
                nb_champs = len([f for f in champs if not f.auto_created])
                
                # Relations
                relations = {
                    'ForeignKey': len([f for f in champs if isinstance(f, models.ForeignKey)]),
                    'OneToOne': len([f for f in champs if isinstance(f, models.OneToOneField)]),
                    'ManyToMany': len([f for f in champs if isinstance(f, models.ManyToManyField)])
                }
                
                total_champs += nb_champs
                
                print(f"      • {modele.__name__}")
                print(f"          📊 Champs: {nb_champs}")
                if any(relations.values()):
                    print(f"          🔗 Relations: {relations}")
                
                # Sauvegarder les données
                self.resultats['modeles'][f"{app.name}.{modele.__name__}"] = {
                    'champs': nb_champs,
                    'relations': relations,
                    'app': app.name
                }
        
        print(f"\n   📈 TOTAL: {total_modeles} modèles, {total_champs} champs")
    
    def analyser_vues(self):
        """Analyse toutes les vues du projet"""
        print("\n👁️ 4. ANALYSE DES VUES")
        print("-" * 40)
        
        # Analyser les fichiers views.py de chaque app
        for app in apps.get_app_configs():
            if app.name.startswith('django.'):
                continue
                
            try:
                views_module = importlib.import_module(f"{app.name}.views")
                fonctions_vues = []
                classes_vues = []
                
                for nom, obj in inspect.getmembers(views_module):
                    if inspect.isfunction(obj) and not nom.startswith('_'):
                        fonctions_vues.append(nom)
                    elif inspect.isclass(obj):
                        classes_vues.append(nom)
                
                if fonctions_vues or classes_vues:
                    print(f"   📋 {app.name}:")
                    if fonctions_vues:
                        print(f"      • Fonctions: {', '.join(sorted(fonctions_vues)[:5])}" + 
                              ("..." if len(fonctions_vues) > 5 else ""))
                    if classes_vues:
                        print(f"      • Classes: {', '.join(sorted(classes_vues)[:5])}" + 
                              ("..." if len(classes_vues) > 5 else ""))
                    
                    self.resultats['vues'][app.name] = {
                        'fonctions': len(fonctions_vues),
                        'classes': len(classes_vues),
                        'total': len(fonctions_vues) + len(classes_vues)
                    }
                    
            except ImportError:
                print(f"   ⚠️  {app.name}: Aucun fichier views.py")
            except Exception as e:
                print(f"   ❌ {app.name}: Erreur analyse vues - {e}")
    
    def analyser_urls(self):
        """Analyse la configuration des URLs"""
        print("\n🌐 5. ANALYSE DES URLs")
        print("-" * 40)
        
        try:
            resolver = get_resolver()
            urls_patterns = []
            
            def extraire_urls(urlpatterns, prefix=''):
                for pattern in urlpatterns:
                    if hasattr(pattern, 'url_patterns'):
                        # Include - namespace
                        extraire_urls(pattern.url_patterns, prefix + str(pattern.pattern))
                    else:
                        urls_patterns.append({
                            'pattern': prefix + str(pattern.pattern),
                            'name': getattr(pattern, 'name', None),
                            'callback': getattr(pattern, 'callback', None)
                        })
            
            extraire_urls(resolver.url_patterns)
            
            # Grouper par application
            urls_par_app = {}
            for url in urls_patterns:
                if url['callback'] and hasattr(url['callback'], '__module__'):
                    app_name = url['callback'].__module__.split('.')[0]
                    if app_name not in urls_par_app:
                        urls_par_app[app_name] = []
                    urls_par_app[app_name].append(url)
            
            for app_name, urls in urls_par_app.items():
                if app_name.startswith('django.'):
                    continue
                    
                print(f"   📋 {app_name}: {len(urls)} URLs")
                for url in urls[:3]:  # Afficher les 3 premières
                    nom = url['name'] or 'Sans nom'
                    print(f"      • {url['pattern']} → {nom}")
                if len(urls) > 3:
                    print(f"      ... et {len(urls) - 3} autres")
            
            self.resultats['urls'] = {
                'total': len(urls_patterns),
                'par_app': {app: len(urls) for app, urls in urls_par_app.items() 
                           if not app.startswith('django.')}
            }
            
        except Exception as e:
            print(f"   ❌ Erreur analyse URLs: {e}")
    
    def analyser_templates(self):
        """Analyse les templates du projet"""
        print("\n🎨 6. ANALYSE DES TEMPLATES")
        print("-" * 40)
        
        templates_dir = BASE_DIR / 'templates'
        if not templates_dir.exists():
            print("   ❌ Dossier templates/ non trouvé")
            return
        
        # Compter les templates par application
        templates_par_app = {}
        total_templates = 0
        
        for template_file in templates_dir.rglob('*.html'):
            total_templates += 1
            app_name = template_file.parent.name
            
            if app_name not in templates_par_app:
                templates_par_app[app_name] = []
            templates_par_app[app_name].append(template_file.name)
        
        print(f"   📊 {total_templates} templates trouvés:")
        
        for app_name, templates in sorted(templates_par_app.items()):
            print(f"      • {app_name}/: {len(templates)} templates")
            # Afficher quelques templates importants
            templates_importants = [t for t in templates if any(x in t for x in ['base', 'dashboard', 'liste', 'creer'])]
            for template in templates_importants[:2]:
                print(f"          📄 {template}")
        
        self.resultats['templates'] = {
            'total': total_templates,
            'par_app': {app: len(templates) for app, templates in templates_par_app.items()}
        }
    
    def analyser_permissions(self):
        """Analyse le système de permissions"""
        print("\n🔐 7. ANALYSE DES PERMISSIONS")
        print("-" * 40)
        
        # Groupes
        groupes = Group.objects.all()
        print(f"   👥 Groupes ({len(groupes)}):")
        for groupe in groupes:
            nb_utilisateurs = groupe.user_set.count()
            nb_permissions = groupe.permissions.count()
            print(f"      • {groupe.name} ({nb_utilisateurs} users, {nb_permissions} permissions)")
        
        # Permissions
        permissions_total = Permission.objects.count()
        print(f"   🔧 Permissions totales: {permissions_total}")
        
        # Utilisateurs par type
        try:
            from core.utils import get_user_primary_group
            users_par_type = {}
            for user in User.objects.all():
                user_type = get_user_primary_group(user)
                users_par_type[user_type] = users_par_type.get(user_type, 0) + 1
            
            print(f"   👤 Utilisateurs par type:")
            for user_type, count in users_par_type.items():
                print(f"      • {user_type}: {count}")
                
        except Exception as e:
            print(f"   ⚠️  Impossible d'analyser les types d'utilisateurs: {e}")
        
        self.resultats['permissions'] = {
            'groupes': len(groupes),
            'permissions_total': permissions_total,
            'utilisateurs': User.objects.count()
        }
    
    def analyser_donnees(self):
        """Analyse les données existantes dans la base"""
        print("\n📊 8. ANALYSE DES DONNÉES")
        print("-" * 40)
        
        try:
            # Modèles principaux à analyser
            modeles_principaux = [
                ('membres.Membre', 'Membres'),
                ('agents.Agent', 'Agents'),
                ('medecin.Medecin', 'Médecins'),
                ('pharmacien.Pharmacien', 'Pharmaciens'),
                ('soins.BonSoin', 'Bons de soin'),
                ('paiements.Paiement', 'Paiements'),
            ]
            
            for modele_path, nom_affichage in modeles_principaux:
                try:
                    modele = apps.get_model(modele_path)
                    count = modele.objects.count()
                    statut = "✅" if count > 0 else "⚠️"
                    print(f"   {statut} {nom_affichage}: {count}")
                    
                    # Statistiques supplémentaires pour certains modèles
                    if modele_path == 'membres.Membre':
                        membres_avec_agent = modele.objects.filter(agent_createur__isnull=False).count()
                        if membres_avec_agent > 0:
                            print(f"          👥 Membres avec agent: {membres_avec_agent}")
                    
                    self.resultats['donnees'][modele_path] = count
                    
                except LookupError:
                    print(f"   ❌ {nom_affichage}: Modèle non trouvé")
                except Exception as e:
                    print(f"   ❌ {nom_affichage}: Erreur - {e}")
        
        except Exception as e:
            print(f"   ❌ Erreur analyse données: {e}")
    
    def verifier_integrations(self):
        """Vérifie les intégrations entre composants"""
        print("\n🔗 9. VÉRIFICATION DES INTÉGRATIONS")
        print("-" * 40)
        
        # Vérifier la création membres par agents
        try:
            from membres.models import Membre
            from agents.models import Agent
            
            agents_actifs = Agent.objects.filter(est_actif=True)
            membres_crees_par_agents = Membre.objects.filter(agent_createur__isnull=False)
            
            print(f"   👥 Intégration Agents-Membres:")
            print(f"      • Agents actifs: {agents_actifs.count()}")
            print(f"      • Membres créés par agents: {membres_crees_par_agents.count()}")
            
            if agents_actifs.count() > 0 and membres_crees_par_agents.count() == 0:
                self.resultats['recommandations'].append(
                    "Aucun membre créé par les agents - Vérifier les permissions"
                )
                
        except Exception as e:
            print(f"   ⚠️  Impossible de vérifier l'intégration agents-membres: {e}")
        
        # Vérifier les URLs critiques
        urls_critiques = [
            ('membres:creer_membre', 'Création membre par agent'),
            ('agents:dashboard', 'Dashboard agent'),
            ('membres:dashboard', 'Dashboard membre'),
            ('admin:index', 'Admin Django'),
        ]
        
        print(f"   🌐 URLs critiques:")
        for url_name, description in urls_critiques:
            try:
                reverse(url_name)
                print(f"      ✅ {description}: Configurée")
            except NoReverseMatch:
                print(f"      ❌ {description}: Non configurée")
                self.resultats['problemes'].append(f"URL manquante: {url_name}")
    
    def generer_rapport_complet(self):
        """Génère un rapport complet d'analyse"""
        print("\n" + "=" * 70)
        print("📊 RAPPORT COMPLÈT D'ANALYSE")
        print("=" * 70)
        
        # Résumé statistique
        total_apps = len(self.resultats['applications'])
        total_modeles = len(self.resultats['modeles'])
        total_vues = sum(app['total'] for app in self.resultats['vues'].values())
        total_urls = self.resultats['urls'].get('total', 0)
        total_templates = self.resultats['templates'].get('total', 0)
        
        print(f"\n📈 STATISTIQUES GLOBALES:")
        print(f"   • Applications: {total_apps}")
        print(f"   • Modèles: {total_modeles}")
        print(f"   • Vues: {total_vues}")
        print(f"   • URLs: {total_urls}")
        print(f"   • Templates: {total_templates}")
        print(f"   • Utilisateurs: {self.resultats['permissions'].get('utilisateurs', 0)}")
        print(f"   • Groupes: {self.resultats['permissions'].get('groupes', 0)}")
        
        # Problèmes identifiés
        if self.resultats['problemes']:
            print(f"\n⚠️  PROBLÈMES IDENTIFIÉS ({len(self.resultats['problemes'])}):")
            for i, probleme in enumerate(self.resultats['problemes'], 1):
                print(f"   {i}. {probleme}")
        else:
            print(f"\n✅ AUCUN PROBLÈME MAJEUR IDENTIFIÉ")
        
        # Recommandations
        if self.resultats['recommandations']:
            print(f"\n💡 RECOMMANDATIONS ({len(self.resultats['recommandations'])}):")
            for i, recommandation in enumerate(self.resultats['recommandations'], 1):
                print(f"   {i}. {recommandation}")
        
        # Points forts
        points_forts = []
        if total_modeles > 10:
            points_forts.append("Architecture modèle riche et structurée")
        if total_vues > 20:
            points_forts.append("Interface utilisateur complète")
        if any('agent' in app.lower() for app in self.resultats['applications']):
            points_forts.append("Système agent-membre bien intégré")
        if self.resultats['donnees'].get('membres.Membre', 0) > 0:
            points_forts.append("Données existantes de test")
        
        if points_forts:
            print(f"\n🌟 POINTS FORTS:")
            for point in points_forts:
                print(f"   • {point}")
        
        # Prochaines étapes
        print(f"\n🎯 PROCHAINES ÉTAPES SUGGÉRÉES:")
        print(f"   1. Tester le flux complet création membre par agent")
        print(f"   2. Vérifier les permissions des différents groupes")
        print(f"   3. Tester l'upload de documents")
        print(f"   4. Valider les intégrations entre applications")
        print(f"   5. Documenter les APIs et workflows")
        
        print(f"\n⏱️  Analyse terminée!")

def analyser_requirements():
    """Analyse les dépendances du projet"""
    print("\n📦 ANALYSE DES DÉPENDANCES")
    print("-" * 40)
    
    requirements_file = BASE_DIR / 'requirements.txt'
    if requirements_file.exists():
        try:
            with open(requirements_file, 'r') as f:
                dependances = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            print(f"   📋 {len(dependances)} dépendances trouvées:")
            for dep in dependances[:10]:  # Afficher les 10 premières
                print(f"      • {dep}")
            if len(dependances) > 10:
                print(f"      ... et {len(dependances) - 10} autres")
                
        except Exception as e:
            print(f"   ❌ Erreur lecture requirements.txt: {e}")
    else:
        print("   ⚠️  Fichier requirements.txt non trouvé")

def verifier_sante_systeme():
    """Vérifie la santé générale du système Django"""
    print("\n🏥 VÉRIFICATION SANTÉ SYSTÈME")
    print("-" * 40)
    
    try:
        # Vérifier les migrations
        result = subprocess.run(['python', 'manage.py', 'check'], 
                              capture_output=True, text=True, cwd=BASE_DIR)
        
        if result.returncode == 0:
            print("   ✅ Vérification système: OK")
        else:
            print("   ❌ Problèmes détectés:")
            print(f"      {result.stderr}")
        
        # Vérifier les migrations en attente
        result = subprocess.run(['python', 'manage.py', 'makemigrations', '--check'], 
                              capture_output=True, text=True, cwd=BASE_DIR)
        
        if result.returncode == 0:
            print("   ✅ Migrations: À jour")
        else:
            print("   ⚠️  Migrations: Des migrations sont en attente")
            
    except Exception as e:
        print(f"   ❌ Erreur vérification santé: {e}")

def main():
    """Fonction principale"""
    try:
        print("🔍 LANCEMENT DE L'ANALYSE COMPLÈTE...")
        print()
        
        # Analyses système
        analyser_requirements()
        verifier_sante_systeme()
        
        # Analyse Django
        analyseur = AnalyseCompleteProjet()
        analyseur.executer_analyse_complete()
        
        print("\n" + "=" * 70)
        print("🎉 ANALYSE TERMINÉE AVEC SUCCÈS!")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()