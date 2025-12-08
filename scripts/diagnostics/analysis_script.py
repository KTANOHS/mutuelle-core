# analysis_script.py
import os
import sys
import django
from pathlib import Path
from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import models

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

User = get_user_model()

class ApplicationAnalyzer:
    """Analyseur des applications Django et de leurs acteurs"""
    
    def __init__(self):
        self.apps_data = {}
        self.actors_data = {}
        
    def analyze_all_apps(self):
        """Analyse toutes les applications installées"""
        print("🔍 ANALYSE DES APPLICATIONS ET ACTEURS")
        print("=" * 80)
        
        installed_apps = [
            'membres', 'inscription', 'paiements', 'soins', 'api', 
            'assureur', 'medecin', 'pharmacien', 'core', 'agents', 'communication'
        ]
        
        for app_name in installed_apps:
            self.analyze_app(app_name)
        
        self.generate_report()
    
    def analyze_app(self, app_name):
        """Analyse une application spécifique"""
        try:
            app_config = apps.get_app_config(app_name)
            models_list = app_config.get_models()
            
            app_info = {
                'name': app_name,
                'verbose_name': getattr(app_config, 'verbose_name', app_name),
                'models': [],
                'actors': set(),
                'permissions': []
            }
            
            # Analyse des modèles
            for model in models_list:
                model_info = self.analyze_model(model)
                app_info['models'].append(model_info)
                
                # Extraction des acteurs depuis les relations ForeignKey
                self.extract_actors_from_model(model, app_info)
            
            self.apps_data[app_name] = app_info
            print(f"✅ Application analysée: {app_name}")
            
        except LookupError:
            print(f"❌ Application non trouvée: {app_name}")
    
    def analyze_model(self, model):
        """Analyse un modèle Django"""
        model_info = {
            'name': model.__name__,
            'verbose_name': getattr(model._meta, 'verbose_name', model.__name__),
            'fields': [],
            'foreign_keys': [],
            'many_to_many': [],
            'permissions': getattr(model._meta, 'permissions', [])
        }
        
        for field in model._meta.get_fields():
            field_info = {
                'name': field.name,
                'type': type(field).__name__,
                'verbose_name': getattr(field, 'verbose_name', field.name),
            }
            
            if isinstance(field, models.ForeignKey):
                field_info['related_model'] = field.related_model.__name__
                model_info['foreign_keys'].append(field_info)
                
            elif isinstance(field, models.ManyToManyField):
                field_info['related_model'] = field.related_model.__name__
                model_info['many_to_many'].append(field_info)
            
            model_info['fields'].append(field_info)
        
        return model_info
    
    def extract_actors_from_model(self, model, app_info):
        """Extrait les acteurs depuis les relations du modèle"""
        actors_mapping = {
            'User': 'utilisateur',
            'Agent': 'agent',
            'Medecin': 'médecin', 
            'Membre': 'membre',
            'Pharmacien': 'pharmacien',
            'Assureur': 'assureur',
            'Patient': 'patient'
        }
        
        for field in model._meta.get_fields():
            if hasattr(field, 'related_model') and field.related_model:
                related_model_name = field.related_model.__name__
                if related_model_name in actors_mapping:
                    actor = actors_mapping[related_model_name]
                    app_info['actors'].add(actor)
                    
                    # Stocker les informations d'acteur
                    if actor not in self.actors_data:
                        self.actors_data[actor] = {
                            'models': [],
                            'apps': set(),
                            'relations': []
                        }
                    
                    self.actors_data[actor]['models'].append(model.__name__)
                    self.actors_data[actor]['apps'].add(app_info['name'])
                    self.actors_data[actor]['relations'].append({
                        'model': model.__name__,
                        'field': field.name,
                        'relation_type': type(field).__name__
                    })
    
    def generate_report(self):
        """Génère un rapport complet"""
        print("\n" + "=" * 80)
        print("📊 RAPPORT D'ANALYSE COMPLET")
        print("=" * 80)
        
        self.print_apps_summary()
        self.print_actors_analysis()
        self.print_detailed_apps_analysis()
        self.print_permissions_analysis()
        self.print_recommendations()
    
    def print_apps_summary(self):
        """Affiche le résumé des applications"""
        print("\n🏗️  RÉSUMÉ DES APPLICATIONS")
        print("-" * 50)
        
        for app_name, app_info in self.apps_data.items():
            print(f"\n📁 {app_info['verbose_name']} ({app_name})")
            print(f"   📊 Modèles: {len(app_info['models'])}")
            print(f"   👥 Acteurs: {', '.join(sorted(app_info['actors'])) if app_info['actors'] else 'Aucun'}")
    
    def print_actors_analysis(self):
        """Analyse détaillée des acteurs"""
        print("\n👥 ANALYSE DES ACTEURS")
        print("-" * 50)
        
        for actor, data in self.actors_data.items():
            print(f"\n🎯 {actor.upper()}")
            print(f"   📍 Applications: {', '.join(sorted(data['apps']))}")
            print(f"   📋 Modèles concernés: {len(data['models'])}")
            print(f"   🔗 Relations:")
            for rel in data['relations'][:5]:  # Affiche les 5 premières relations
                print(f"      - {rel['model']}.{rel['field']} ({rel['relation_type']})")
            if len(data['relations']) > 5:
                print(f"      ... et {len(data['relations']) - 5} autres relations")
    
    def print_detailed_apps_analysis(self):
        """Analyse détaillée par application"""
        print("\n🔍 ANALYSE DÉTAILLÉE PAR APPLICATION")
        print("-" * 50)
        
        for app_name, app_info in self.apps_data.items():
            print(f"\n📁 {app_info['verbose_name']} ({app_name})")
            
            for model_info in app_info['models']:
                print(f"\n   📋 {model_info['verbose_name']} ({model_info['name']})")
                
                # Champs importants
                important_fields = []
                for field in model_info['fields']:
                    if field['type'] in ['ForeignKey', 'ManyToManyField']:
                        important_fields.append(field)
                
                if important_fields:
                    print("      🔗 Relations:")
                    for field in important_fields[:3]:
                        related = field.get('related_model', '?')
                        print(f"         - {field['name']} → {related} ({field['type']})")
    
    def print_permissions_analysis(self):
        """Analyse des permissions"""
        print("\n🔐 ANALYSE DES PERMISSIONS")
        print("-" * 50)
        
        all_permissions = {}
        
        for app_name, app_info in self.apps_data.items():
            for model_info in app_info['models']:
                if model_info['permissions']:
                    all_permissions[model_info['name']] = model_info['permissions']
        
        if all_permissions:
            for model, perms in all_permissions.items():
                print(f"\n📋 {model}:")
                for codename, name in perms:
                    print(f"   ✅ {codename}: {name}")
        else:
            print("Aucune permission personnalisée trouvée.")
    
    def print_recommendations(self):
        """Affiche des recommandations"""
        print("\n💡 RECOMMANDATIONS")
        print("-" * 50)
        
        # Vérification de la couverture des acteurs
        expected_actors = ['agent', 'médecin', 'membre', 'pharmacien', 'assureur']
        missing_actors = [actor for actor in expected_actors if actor not in self.actors_data]
        
        if missing_actors:
            print(f"⚠️  Acteurs manquants: {', '.join(missing_actors)}")
        
        # Recommandations par application
        app_recommendations = {
            'membres': "Vérifier la gestion des profils membres et leurs relations",
            'agents': "S'assurer des permissions des agents sur les autres modules",
            'medecin': "Vérifier l'intégration avec les soins et prescriptions",
            'pharmacien': "S'assurer de la gestion des ordonnances et stocks",
            'communication': "Vérifier les canaux de communication entre acteurs"
        }
        
        for app, recommendation in app_recommendations.items():
            if app in self.apps_data:
                print(f"📌 {app}: {recommendation}")

def analyze_user_roles():
    """Analyse spécifique des rôles utilisateur"""
    print("\n🎭 ANALYSE DES RÔLES UTILISATEUR")
    print("-" * 50)
    
    User = get_user_model()
    
    # Compter les utilisateurs par type (basé sur les groupes ou champs personnalisés)
    try:
        total_users = User.objects.count()
        print(f"👥 Total utilisateurs: {total_users}")
        
        # Essayer de détecter les types d'utilisateurs
        user_types = {}
        
        # Vérifier les groupes
        from django.contrib.auth.models import Group
        groups = Group.objects.all()
        
        if groups.exists():
            print("\n🏷️  Groupes existants:")
            for group in groups:
                count = group.user_set.count()
                print(f"   📊 {group.name}: {count} utilisateurs")
                user_types[group.name.lower()] = count
        
        # Vérifier les champs personnalisés
        user_fields = [f.name for f in User._meta.get_fields()]
        role_fields = [f for f in user_fields if 'role' in f.lower() or 'type' in f.lower()]
        
        if role_fields:
            print(f"\n🔍 Champs de rôle détectés: {', '.join(role_fields)}")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse des utilisateurs: {e}")

def analyze_database_relations():
    """Analyse les relations entre les modèles"""
    print("\n🔗 ANALYSE DES RELATIONS ENTRE MODÈLES")
    print("-" * 50)
    
    try:
        from membres.models import Membre
        from agents.models import Agent
        from medecin.models import Medecin
        from pharmacien.models import Pharmacien
        
        models_to_check = [
            ('Membre', Membre),
            ('Agent', Agent), 
            ('Médecin', Medecin),
            ('Pharmacien', Pharmacien)
        ]
        
        for name, model in models_to_check:
            try:
                count = model.objects.count()
                print(f"📊 {name}: {count} enregistrements")
            except Exception as e:
                print(f"❌ {name}: Non accessible - {e}")
                
    except ImportError as e:
        print(f"⚠️  Impossible d'importer certains modèles: {e}")

def generate_architecture_diagram():
    """Génère un diagramme d'architecture simplifié"""
    print("\n🏗️  DIAGRAMME D'ARCHITECTURE SIMPLIFIÉ")
    print("-" * 50)
    
    diagram = """
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │     MEMBRES     │    │     AGENTS      │    │    MÉDECINS     │
    │                 │    │                 │    │                 │
    │ • Profils       │◄───┤ • Gestion       │◄───┤ • Consultations │
    │ • Cotisations   │    │ • Validation    │    │ • Ordonnances   │
    │ • Historique    │    │ • Support       │    │ • Certificats   │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
          ▲                      ▲                       ▲
          │                      │                       │
          └──────────────────────┼───────────────────────┘
                                 │
    ┌─────────────────┐    ┌─────┴─────┐    ┌─────────────────┐
    │  PHARMACIENS    │    │ COMMUNI-  │    │     SOINS       │
    │                 │    │  CATION   │    │                 │
    │ • Médicaments   │◄───┤ • Messages│◄───┤ • Traitements   │
    │ • Ordonnances   │    │ • Notifs  │    │ • Rendez-vous   │
    │ • Stocks        │    │ • Groupes │    │ • Suivi         │
    └─────────────────┘    └───────────┘    └─────────────────┘
    """
    
    print(diagram)

if __name__ == "__main__":
    print("🚀 LANCEMENT DE L'ANALYSE DU SYSTÈME MUTUELLE")
    print("=" * 80)
    
    # Analyse principale
    analyzer = ApplicationAnalyzer()
    analyzer.analyze_all_apps()
    
    # Analyses supplémentaires
    analyze_user_roles()
    analyze_database_relations() 
    generate_architecture_diagram()
    
    print("\n" + "=" * 80)
    print("✅ ANALYSE TERMINÉE AVEC SUCCÈS")
    print("=" * 80)