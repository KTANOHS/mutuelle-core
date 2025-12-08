#!/usr/bin/env python3
"""
SCRIPT D'ANALYSE DE L'EXISTANT - Création de membres par les agents
Version corrigée
"""

import os
import sys
import django
from pathlib import Path
import logging

# Configuration Django
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps
from django.db import models
from django.contrib.auth.models import User, Group
from membres.models import Membre, Profile
from agents.models import Agent
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class AnalyseMembreCreation:
    """Classe d'analyse complète pour la création de membres par les agents"""
    
    def __init__(self):
        self.analyse_resultats = {}
        self.problemes = []
        self.recommandations = []
    
    def analyser_structure_actuelle(self):
        """Analyse la structure actuelle des modèles"""
        print("🔍 ANALYSE DE LA STRUCTURE ACTUELLE")
        print("=" * 60)
        
        # 1. Analyse du modèle Membre
        self.analyser_modele_membre()
        
        # 2. Analyse du modèle Agent
        self.analyser_modele_agent()
        
        # 3. Analyse des relations
        self.analyser_relations()
        
        # 4. Analyse des permissions
        self.analyser_permissions()
        
        # 5. Analyse des templates existants
        self.analyser_templates()
        
        # 6. Analyse des URLs et vues
        self.analyser_urls_vues()
    
    def analyser_modele_membre(self):
        """Analyse détaillée du modèle Membre - VERSION CORRIGÉE"""
        print("\n📋 1. ANALYSE DU MODÈLE MEMBRE")
        print("-" * 40)
        
        membre_fields = [f for f in Membre._meta.get_fields() if not f.is_relation or f.one_to_one or f.many_to_one]
        champ_analysis = []
        
        for field in membre_fields:
            try:
                champ_info = {
                    'nom': field.name,
                    'type': type(field).__name__,
                    'obligatoire': not getattr(field, 'blank', True) and not getattr(field, 'null', False),
                    'unique': getattr(field, 'unique', False),
                    'relation': field.is_relation,
                    'relation_modele': field.related_model.__name__ if field.is_relation else None
                }
                champ_analysis.append(champ_info)
                
                print(f"   📍 {field.name}")
                print(f"      Type: {type(field).__name__}")
                print(f"      Obligatoire: {champ_info['obligatoire']}")
                print(f"      Unique: {champ_info['unique']}")
                if field.is_relation:
                    print(f"      Relation: {field.related_model.__name__}")
                print()
                
            except AttributeError as e:
                print(f"   ⚠️  Erreur sur le champ {field.name}: {e}")
                continue
        
        # Vérification des champs critiques
        champs_critiques = ['user', 'nom', 'prenom', 'numero_unique']
        champs_presents = [f['nom'] for f in champ_analysis]
        champs_manquants = [c for c in champs_critiques if c not in champs_presents]
        
        if champs_manquants:
            self.problemes.append(f"Champs manquants dans Membre: {champs_manquants}")
        else:
            print("   ✅ Tous les champs critiques sont présents")
        
        self.analyse_resultats['membre_champs'] = champ_analysis
        self.analyse_resultats['membre_champs_critiques'] = champs_critiques
    
    def analyser_modele_agent(self):
        """Analyse du modèle Agent"""
        print("\n👤 2. ANALYSE DU MODÈLE AGENT")
        print("-" * 40)
        
        try:
            agent_model = apps.get_model('agents', 'Agent')
            agent_fields = [f for f in agent_model._meta.get_fields() if not f.is_relation or f.one_to_one or f.many_to_one]
            
            print("   Champs du modèle Agent:")
            for field in agent_fields:
                print(f"   📍 {field.name} ({type(field).__name__})")
                
            # Vérifier la relation avec User
            user_relation = any(field.name == 'user' for field in agent_fields)
            if user_relation:
                print("   ✅ Relation Agent -> User présente")
            else:
                self.problemes.append("Modèle Agent sans relation User")
                
        except LookupError:
            self.problemes.append("Modèle Agent non trouvé")
            print("   ❌ Modèle Agent non trouvé")
    
    def analyser_relations(self):
        """Analyse des relations entre modèles"""
        print("\n🔗 3. ANALYSE DES RELATIONS")
        print("-" * 40)
        
        # Relation Membre -> Agent (agent_createur)
        membre_fields = Membre._meta.get_fields()
        agent_relation = any(
            field.name == 'agent_createur' and hasattr(field, 'related_model') and field.related_model.__name__ == 'Agent' 
            for field in membre_fields if field.is_relation
        )
        
        if agent_relation:
            print("   ✅ Relation Membre -> Agent (agent_createur) présente")
        else:
            self.problemes.append("Relation Membre -> Agent manquante")
            print("   ❌ Relation Membre -> Agent manquante")
        
        # Relation Membre -> User
        user_relation = any(
            field.name == 'user' and hasattr(field, 'related_model') and field.related_model.__name__ == 'User'
            for field in membre_fields if field.is_relation
        )
        
        if user_relation:
            print("   ✅ Relation Membre -> User présente")
        else:
            self.problemes.append("Relation Membre -> User manquante")
    
    def analyser_permissions(self):
        """Analyse des permissions et groupes"""
        print("\n🔐 4. ANALYSE DES PERMISSIONS")
        print("-" * 40)
        
        # Vérifier les groupes existants
        groupes = Group.objects.all()
        print("   Groupes existants:")
        for groupe in groupes:
            print(f"   👥 {groupe.name}")
            
            # Permissions du groupe
            permissions = groupe.permissions.all()[:3]  # Premières 3 permissions
            if permissions:
                perm_names = [p.name.split('|')[0] for p in permissions]  # Simplifier l'affichage
                print(f"      Permissions: {', '.join(perm_names)}...")
        
        # Vérifier si le groupe "agents" existe
        groupe_agents = Group.objects.filter(name='agents').exists()
        if groupe_agents:
            print("   ✅ Groupe 'agents' existe")
        else:
            self.recommandations.append("Créer le groupe 'agents' avec les permissions appropriées")
            print("   ⚠️  Groupe 'agents' n'existe pas")
    
    def analyser_templates(self):
        """Analyse des templates existants"""
        print("\n🎨 5. ANALYSE DES TEMPLATES")
        print("-" * 40)
        
        templates_dir = project_root / 'templates'
        
        # Vérifier si le dossier templates existe
        if not templates_dir.exists():
            print("   ❌ Dossier templates non trouvé")
            self.problemes.append("Dossier templates manquant")
            return
        
        templates_agents = list(templates_dir.glob('**/*agent*'))
        templates_membres = list(templates_dir.glob('**/*membre*'))
        
        print("   Templates agents trouvés:")
        for template in templates_agents[:5]:  # Limiter l'affichage
            print(f"   📄 {template.relative_to(templates_dir)}")
        
        print("\n   Templates membres trouvés:")
        for template in templates_membres[:5]:
            print(f"   📄 {template.relative_to(templates_dir)}")
        
        # Vérifier les templates critiques
        templates_critiques = [
            'membres/creer_membre.html',
            'membres/liste_membres_agent.html',
            'agents/dashboard.html'
        ]
        
        templates_existants = 0
        for template in templates_critiques:
            template_path = templates_dir / template
            if template_path.exists():
                print(f"   ✅ {template} existe")
                templates_existants += 1
            else:
                print(f"   ❌ {template} manquant")
                self.recommandations.append(f"Créer le template: {template}")
        
        if templates_existants == 0:
            print("   ⚠️  Aucun template critique n'existe")
    
    def analyser_urls_vues(self):
        """Analyse des URLs et vues existantes"""
        print("\n🌐 6. ANALYSE DES URLs ET VUES")
        print("-" * 40)
        
        try:
            # Analyser le fichier urls.py de membres
            membres_urls = project_root / 'membres' / 'urls.py'
            if membres_urls.exists():
                with open(membres_urls, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                
                # Vérifier les URLs critiques
                urls_critiques = ['creer_membre', 'liste_membres_agent']
                urls_presentes = []
                urls_manquantes = []
                
                for url in urls_critiques:
                    if url in contenu:
                        urls_presentes.append(url)
                    else:
                        urls_manquantes.append(url)
                
                if urls_presentes:
                    print(f"   URLs présentes: {', '.join(urls_presentes)}")
                if urls_manquantes:
                    print(f"   URLs manquantes: {', '.join(urls_manquantes)}")
                    self.recommandations.extend([
                        f"Ajouter l'URL: {url}" for url in urls_manquantes
                    ])
            else:
                print("   ❌ Fichier membres/urls.py non trouvé")
                self.recommandations.append("Créer le fichier membres/urls.py")
                
        except Exception as e:
            print(f"   ⚠️  Erreur analyse URLs: {e}")
    
    def analyser_donnees_test(self):
        """Analyse des données de test existantes"""
        print("\n🧪 7. ANALYSE DES DONNÉES DE TEST")
        print("-" * 40)
        
        # Compter les membres existants
        total_membres = Membre.objects.count()
        membres_avec_agent = Membre.objects.filter(agent_createur__isnull=False).count()
        membres_sans_agent = Membre.objects.filter(agent_createur__isnull=True).count()
        
        print(f"   Total membres: {total_membres}")
        print(f"   Membres avec agent: {membres_avec_agent}")
        print(f"   Membres sans agent: {membres_sans_agent}")
        
        # Agents existants
        try:
            total_agents = Agent.objects.count()
            print(f"   Total agents: {total_agents}")
            
            if total_agents == 0:
                self.recommandations.append("Créer des données de test pour les agents")
            else:
                # Afficher les agents
                agents = Agent.objects.all()[:3]
                for agent in agents:
                    user = agent.user
                    print(f"   📍 {user.username} - {user.get_full_name() or 'Nom non défini'}")
                
        except Exception as e:
            print(f"   ⚠️  Erreur comptage agents: {e}")
    
    def generer_plan_implementation(self):
        """Génère un plan d'implémentation détaillé"""
        print("\n🎯 PLAN D'IMPLÉMENTATION DÉTAILLÉ")
        print("=" * 60)
        
        print("\n📋 ÉTAPE 1: PRÉPARATION (Jour 1)")
        print("-" * 40)
        print("""   1.1 ✅ Vérifier la structure des modèles
   1.2 ✅ Analyser les relations existantes  
   1.3 ✅ Identifier les problèmes potentiels
   1.4 📝 Créer les backups de la base de données""")
        
        print("\n🔧 ÉTAPE 2: FORMULAIRES (Jour 1)")
        print("-" * 40)
        print("""   2.1 📝 Créer MembreCreationForm dans membres/forms.py
   2.2 📝 Créer MembreDocumentForm pour l'upload des documents
   2.3 🔧 Implémenter la logique de sauvegarde avec agent_createur
   2.4 ✅ Tester la validation des formulaires""")
        
        print("\n👁️ ÉTAPE 3: VUES (Jour 2)")
        print("-" * 40)
        print("""   3.1 🌐 Créer vue creer_membre() avec permissions agents
   3.2 🌐 Créer vue liste_membres_agent() pour le suivi
   3.3 🌐 Créer vue upload_documents_membre() pour les documents
   3.4 🔐 Implémenter les décorateurs de permission
   3.5 ✅ Tester les vues avec différents utilisateurs""")
        
        print("\n🎨 ÉTAPE 4: TEMPLATES (Jour 2)")
        print("-" * 40)
        print("""   4.1 🎨 Créer templates/membres/creer_membre.html
   4.2 🎨 Créer templates/membres/liste_membres_agent.html  
   4.3 🎨 Créer templates/membres/upload_documents.html
   4.4 🎨 Modifier template agents/dashboard.html
   4.5 ✅ Tester le responsive design""")
        
        print("\n🌐 ÉTAPE 5: URLs ET NAVIGATION (Jour 3)")
        print("-" * 40)
        print("""   5.1 🔗 Ajouter les URLs dans membres/urls.py
   5.2 🔗 Mettre à jour la navigation des agents
   5.3 🔗 Configurer les redirections après création
   5.4 ✅ Tester tous les flux de navigation""")
        
        print("\n⚙️ ÉTAPE 6: PERMISSIONS ET SÉCURITÉ (Jour 3)")
        print("-" * 40)
        print("""   6.1 🔐 Vérifier/créer le groupe 'agents'
   6.2 🔐 Assigner les permissions appropriées
   6.3 🔐 Tester l'accès interdit pour les non-agents
   6.4 🔐 Implémenter la vérification agent_createur""")
        
        print("\n🧪 ÉTAPE 7: TESTS ET VALIDATION (Jour 4)")
        print("-" * 40)
        print("""   7.1 🧪 Créer des tests unitaires pour les formulaires
   7.2 🧪 Créer des tests d'intégration pour les vues
   7.3 🧪 Tester avec différents scénarios
   7.4 🧪 Valider les emails et notifications
   7.5 ✅ Tests de performance""")
    
    def generer_checklist_implementation(self):
        """Génère une checklist d'implémentation"""
        print("\n📝 CHECKLIST D'IMPLÉMENTATION")
        print("=" * 60)
        
        checklist = [
            # Formulaires
            ("📝", "Créer MembreCreationForm", "membres/forms.py"),
            ("📝", "Créer MembreDocumentForm", "membres/forms.py"),
            ("🔧", "Implémenter save() avec agent_createur", "membres/forms.py"),
            
            # Vues
            ("🌐", "Créer vue creer_membre()", "membres/views.py"),
            ("🌐", "Créer vue liste_membres_agent()", "membres/views.py"),
            ("🌐", "Créer vue upload_documents_membre()", "membres/views.py"),
            ("🔐", "Ajouter décorateurs permission", "membres/views.py"),
            
            # Templates
            ("🎨", "Créer template creer_membre.html", "templates/membres/"),
            ("🎨", "Créer template liste_membres_agent.html", "templates/membres/"),
            ("🎨", "Créer template upload_documents.html", "templates/membres/"),
            ("🎨", "Mettre à jour dashboard agent", "templates/agents/"),
            
            # URLs
            ("🔗", "Ajouter URLs création membre", "membres/urls.py"),
            ("🔗", "Configurer namespaces", "membres/urls.py"),
            
            # Permissions
            ("🔐", "Vérifier/créer groupe agents", "Admin Django"),
            ("🔐", "Assigner permissions", "Admin Django"),
        ]
        
        for emoji, task, location in checklist:
            print(f"   {emoji} [ ] {task}")
            print(f"      📍 {location}")
    
    def generer_rapport_final(self):
        """Génère le rapport final d'analyse"""
        print("\n📊 RAPPORT FINAL D'ANALYSE")
        print("=" * 60)
        
        print(f"\n✅ POINTS FORTS:")
        print("-" * 20)
        points_forts = []
        
        if Membre.objects.filter(agent_createur__isnull=False).exists():
            points_forts.append("Relation agent_createur déjà utilisée")
        
        if Agent.objects.count() > 0:
            points_forts.append("Agents existants dans la base")
            
        if any('agent_createur' in [f['nom'] for f in self.analyse_resultats.get('membre_champs', [])]):
            points_forts.append("Champ agent_createur présent dans Membre")
        
        for point in points_forts:
            print(f"   ✓ {point}")
        
        if not points_forts:
            print("   ℹ️  Aucun point fort spécifique identifié")
        
        print(f"\n❌ PROBLÈMES IDENTIFIÉS ({len(self.problemes)}):")
        print("-" * 35)
        for probleme in self.problemes:
            print(f"   ⚠️  {probleme}")
        
        if not self.problemes:
            print("   🎉 Aucun problème critique identifié!")
        
        print(f"\n💡 RECOMMANDATIONS ({len(self.recommandations)}):")
        print("-" * 30)
        for i, recommandation in enumerate(self.recommandations[:10], 1):  # Limiter à 10
            print(f"   {i}. 💡 {recommandation}")
        
        if len(self.recommandations) > 10:
            print(f"   ... et {len(self.recommandations) - 10} autres recommandations")
        
        print(f"\n🎯 RÉSUMÉ DE L'ÉTAT:")
        print("-" * 20)
        print(f"   📈 Complexité: MOYENNE")
        print(f"   ⏱️  Temps estimé: 3-4 jours")
        print(f"   🔧 Effort requis: MODÉRÉ")
        print(f"   🚀 Risque: FAIBLE")
        
        print(f"\n📊 DONNÉES EXISTANTES:")
        print("-" * 20)
        print(f"   👥 Utilisateurs: {User.objects.count()}")
        print(f"   👤 Membres: {Membre.objects.count()}")
        print(f"   🔧 Agents: {Agent.objects.count()}")

def main():
    """Fonction principale"""
    print("🚀 ANALYSE POUR CRÉATION DE MEMBRES PAR LES AGENTS")
    print("=" * 70)
    
    analyse = AnalyseMembreCreation()
    
    # Exécuter les analyses
    analyse.analyser_structure_actuelle()
    analyse.analyser_donnees_test()
    
    # Générer les rapports
    analyse.generer_plan_implementation()
    analyse.generer_checklist_implementation()
    analyse.generer_rapport_final()
    
    print("\n🎉 ANALYSE TERMINÉE!")
    print("=" * 30)
    print("💡 Utilisez les recommandations pour guider l'implémentation.")
    print("🚀 Bon développement!")

if __name__ == "__main__":
    main()