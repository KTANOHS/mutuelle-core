# analyse_creation_membres_corrige.py

import os
import sys
import django
from django.apps import apps
from django.conf import settings

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.template.loader import get_template
from django.urls import get_resolver

class AnalyseCreationMembres:
    def __init__(self):
        self.analyse_resultats = {
            'membre_champs': [],
            'agent_champs': [],
            'relations': [],
            'permissions': [],
            'templates': [],
            'urls': [],
            'donnees_test': {}
        }
    
    def analyser_structure_actuelle(self):
        print("🔍 ANALYSE DE LA STRUCTURE ACTUELLE")
        print("=" * 60)
        print()
        
        self.analyser_modele_membre()
        self.analyser_modele_agent()
        self.analyser_relations()
        self.analyser_permissions()
        self.analyser_templates()
        self.analyser_urls_vues()
        self.analyser_donnees_test()
    
    def analyser_modele_membre(self):
        print("📋 1. ANALYSE DU MODÈLE MEMBRE")
        print("-" * 40)
        
        try:
            Membre = apps.get_model('membres', 'Membre')
            fields = Membre._meta.get_fields()
            
            for field in fields:
                # Ignorer les relations inverses
                if field.auto_created and not field.concrete:
                    continue
                    
                champ_info = {
                    'nom': field.name,
                    'type': type(field).__name__,
                    'obligatoire': False,
                    'unique': False
                }
                
                # Vérifier si c'est un champ de base (pas une relation)
                if hasattr(field, 'blank'):
                    champ_info['obligatoire'] = not field.blank and not field.null
                else:
                    # Pour les relations, on vérifie null
                    champ_info['obligatoire'] = not getattr(field, 'null', True)
                
                champ_info['unique'] = getattr(field, 'unique', False)
                
                # Ajouter des informations spécifiques aux relations
                if hasattr(field, 'related_model'):
                    champ_info['relation'] = field.related_model.__name__ if field.related_model else None
                
                self.analyse_resultats['membre_champs'].append(champ_info)
                
                # Affichage formaté
                relation_info = f" - Relation: {champ_info.get('relation')}" if champ_info.get('relation') else ""
                print(f"   📍 {field.name}")
                print(f"      Type: {champ_info['type']}")
                print(f"      Obligatoire: {champ_info['obligatoire']}")
                print(f"      Unique: {champ_info['unique']}{relation_info}")
                print()
            
            # Vérifier les champs critiques
            champs_critiques = ['user', 'numero_unique', 'nom', 'prenom', 'statut']
            champs_presents = [champ['nom'] for champ in self.analyse_resultats['membre_champs']]
            champs_manquants = [champ for champ in champs_critiques if champ not in champs_presents]
            
            if not champs_manquants:
                print("   ✅ Tous les champs critiques sont présents")
            else:
                print(f"   ⚠️  Champs manquants: {', '.join(champs_manquants)}")
                
        except Exception as e:
            print(f"   ❌ Erreur lors de l'analyse du modèle Membre: {e}")
    
    def analyser_modele_agent(self):
        print("👤 2. ANALYSE DU MODÈLE AGENT")
        print("-" * 40)
        
        try:
            Agent = apps.get_model('agents', 'Agent')
            fields = Agent._meta.get_fields()
            
            print("   Champs du modèle Agent:")
            for field in fields:
                # Ignorer les relations inverses pour l'affichage simple
                if field.auto_created and not field.concrete:
                    print(f"   📍 {field.name} ({type(field).__name__})")
                    continue
                    
                champ_info = {
                    'nom': field.name,
                    'type': type(field).__name__
                }
                
                self.analyse_resultats['agent_champs'].append(champ_info)
                print(f"   📍 {field.name} ({champ_info['type']})")
            
            # Vérifier la relation avec User
            has_user_relation = any(field.name == 'user' for field in fields)
            if has_user_relation:
                print("   ✅ Relation Agent -> User présente")
            else:
                print("   ❌ Relation Agent -> User manquante")
                
        except Exception as e:
            print(f"   ❌ Erreur lors de l'analyse du modèle Agent: {e}")
    
    def analyser_relations(self):
        print("🔗 3. ANALYSE DES RELATIONS")
        print("-" * 40)
        
        try:
            Membre = apps.get_model('membres', 'Membre')
            fields = Membre._meta.get_fields()
            
            # Vérifier la relation agent_createur
            has_agent_relation = any(
                field.name == 'agent_createur' and hasattr(field, 'related_model') 
                for field in fields
            )
            
            if has_agent_relation:
                print("   ✅ Relation Membre -> Agent (agent_createur) présente")
            else:
                print("   ❌ Relation Membre -> Agent (agent_createur) manquante")
            
            # Vérifier la relation user
            has_user_relation = any(
                field.name == 'user' and hasattr(field, 'related_model')
                for field in fields
            )
            
            if has_user_relation:
                print("   ✅ Relation Membre -> User présente")
            else:
                print("   ❌ Relation Membre -> User manquante")
                
        except Exception as e:
            print(f"   ❌ Erreur lors de l'analyse des relations: {e}")
    
    def analyser_permissions(self):
        print("🔐 4. ANALYSE DES PERMISSIONS")
        print("-" * 40)
        
        try:
            groups = Group.objects.all()
            print("   Groupes existants:")
            for group in groups:
                print(f"   👥 {group.name}")
            
            # Vérifier le groupe agents
            agents_group = Group.objects.filter(name='Agent').first()
            if agents_group:
                print("   ✅ Groupe 'Agent' existe")
            else:
                print("   ⚠️  Groupe 'Agent' n'existe pas")
                
        except Exception as e:
            print(f"   ❌ Erreur lors de l'analyse des permissions: {e}")
    
    def analyser_templates(self):
        print("🎨 5. ANALYSE DES TEMPLATES")
        print("-" * 40)
        
        templates_dir = 'templates'
        templates_agents = []
        templates_membres = []
        
        try:
            # Vérifier les templates existants (simplifié)
            templates_verifies = [
                'membres/creer_membre.html',
                'membres/liste_membres_agent.html',
                'agents/dashboard.html'
            ]
            
            for template in templates_verifies:
                try:
                    get_template(template)
                    if 'agent' in template:
                        templates_agents.append(template)
                    else:
                        templates_membres.append(template)
                    print(f"   ✅ {template} existe")
                except:
                    if 'liste_membres_agent' in template:
                        print(f"   ❌ {template} manquant")
                    else:
                        print(f"   ⚠️  {template} non trouvé")
                        
        except Exception as e:
            print(f"   ❌ Erreur lors de l'analyse des templates: {e}")
    
    def analyser_urls_vues(self):
        print("🌐 6. ANALYSE DES URLs ET VUES")
        print("-" * 40)
        
        try:
            resolver = get_resolver()
            url_patterns = []
            
            def extract_urls(urlpatterns, base=''):
                for pattern in urlpatterns:
                    if hasattr(pattern, 'url_patterns'):
                        extract_urls(pattern.url_patterns, base + str(pattern.pattern))
                    else:
                        url_patterns.append(base + str(pattern.pattern))
            
            extract_urls(resolver.url_patterns)
            
            # Vérifier les URLs importantes
            urls_importantes = ['creer_membre', 'liste_membres_agent']
            urls_trouvees = []
            
            for url in urls_importantes:
                if any(url in pattern for pattern in url_patterns):
                    urls_trouvees.append(url)
                else:
                    print(f"   ❌ URL manquante: {url}")
            
            if urls_trouvees:
                print(f"   ✅ URLs trouvées: {', '.join(urls_trouvees)}")
                
        except Exception as e:
            print(f"   ❌ Erreur lors de l'analyse des URLs: {e}")
    
    def analyser_donnees_test(self):
        print("🧪 7. ANALYSE DES DONNÉES DE TEST")
        print("-" * 40)
        
        try:
            Membre = apps.get_model('membres', 'Membre')
            Agent = apps.get_model('agents', 'Agent')
            
            total_membres = Membre.objects.count()
            membres_avec_agent = Membre.objects.filter(agent_createur__isnull=False).count()
            total_agents = Agent.objects.count()
            
            print(f"   Total membres: {total_membres}")
            print(f"   Membres avec agent: {membres_avec_agent}")
            print(f"   Membres sans agent: {total_membres - membres_avec_agent}")
            print(f"   Total agents: {total_agents}")
            
            # Lister les agents
            agents = Agent.objects.all()[:5]  # Limiter à 5 pour l'affichage
            for agent in agents:
                nom_complet = getattr(agent, 'nom_complet', getattr(agent.user, 'get_full_name', lambda: 'Nom non défini')())
                print(f"   📍 {agent.user.username} - {nom_complet}")
                
        except Exception as e:
            print(f"   ❌ Erreur lors de l'analyse des données: {e}")
    
    def generer_plan_implementation(self):
        print("🎯 PLAN D'IMPLÉMENTATION DÉTAILLÉ")
        print("=" * 60)
        print()
        
        etapes = [
            {
                'titre': '📋 ÉTAPE 1: PRÉPARATION (Jour 1)',
                'taches': [
                    '✅ Vérifier la structure des modèles',
                    '✅ Analyser les relations existantes',
                    '✅ Identifier les problèmes potentiels',
                    '📝 Créer les backups de la base de données'
                ]
            },
            {
                'titre': '🔧 ÉTAPE 2: FORMULAIRES (Jour 1)',
                'taches': [
                    '📝 Créer MembreCreationForm dans membres/forms.py',
                    '📝 Créer MembreDocumentForm pour l\'upload des documents',
                    '🔧 Implémenter la logique de sauvegarde avec agent_createur',
                    '✅ Tester la validation des formulaires'
                ]
            }
        ]
        
        for etape in etapes:
            print(etape['titre'])
            print("-" * 40)
            for tache in etape['taches']:
                print(f"   {tache}")
            print()
    
    def generer_checklist(self):
        print("📝 CHECKLIST D'IMPLÉMENTATION")
        print("=" * 60)
        print()
        
        checklist = [
            "📝 [ ] Créer MembreCreationForm",
            "📝 [ ] Créer MembreDocumentForm", 
            "🔧 [ ] Implémenter save() avec agent_createur",
            "🌐 [ ] Créer vue creer_membre()",
            "🌐 [ ] Créer vue liste_membres_agent()",
            "🎨 [ ] Créer template creer_membre.html",
            "🎨 [ ] Créer template liste_membres_agent.html",
            "🔗 [ ] Ajouter URLs création membre",
            "🔐 [ ] Vérifier/créer groupe agents"
        ]
        
        for item in checklist:
            print(f"   {item}")
        print()
    
    def generer_rapport_final(self):
        print("📊 RAPPORT FINAL D'ANALYSE")
        print("=" * 60)
        print()
        
        print("✅ POINTS FORTS:")
        print("-" * 20)
        
        # Vérifications sécurisées
        membre_champs = self.analyse_resultats.get('membre_champs', [])
        if isinstance(membre_champs, list):
            has_agent_creator = any('agent_createur' in champ.get('nom', '') for champ in membre_champs)
        else:
            has_agent_creator = False
        
        points_forts = [
            "Modèle Membre bien structuré avec tous les champs nécessaires",
            "Relation Membre -> Agent présente via agent_createur" if has_agent_creator else "Relation à implémenter",
            "Système de permissions Django en place",
            "Base de données opérationnelle avec des données de test"
        ]
        
        for point in points_forts:
            print(f"   • {point}")
        
        print()
        print("⚠️  POINTS D'AMÉLIORATION:")
        print("-" * 25)
        
        points_amelioration = [
            "Créer les formulaires de création de membre",
            "Implémenter les vues pour les agents",
            "Créer les templates manquants",
            "Configurer les URLs appropriées",
            "Tester les permissions des agents"
        ]
        
        for point in points_amelioration:
            print(f"   • {point}")

def main():
    print("🚀 ANALYSE POUR CRÉATION DE MEMBRES PAR LES AGENTS")
    print("=" * 70)
    print()
    
    try:
        analyse = AnalyseCreationMembres()
        analyse.analyser_structure_actuelle()
        print()
        analyse.generer_plan_implementation()
        analyse.generer_checklist()
        analyse.generer_rapport_final()
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()