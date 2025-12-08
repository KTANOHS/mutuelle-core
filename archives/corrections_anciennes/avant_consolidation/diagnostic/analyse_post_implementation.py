# analyse_post_implementation.py

import os
import sys
import django
from django.apps import apps
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, Group
from django.core.management import call_command

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

class AnalysePostImplementation:
    def __init__(self):
        self.resultats = {}
        self.erreurs = []
    
    def executer_analyse_complete(self):
        print("🚀 ANALYSE POST-IMPLÉMENTATION - CRÉATION MEMBRES PAR AGENTS")
        print("=" * 70)
        print()
        
        self.verifier_formulaires()
        self.verifier_vues()
        self.verifier_urls()
        self.verifier_templates()
        self.verifier_permissions()
        self.tester_fonctionnalites()
        self.analyser_donnees_test()
        self.generer_rapport_final()
    
    def verifier_formulaires(self):
        print("📝 1. VÉRIFICATION DES FORMULAIRES")
        print("-" * 40)
        
        try:
            from membres.forms import MembreCreationForm, MembreDocumentForm
            
            # Test MembreCreationForm
            form_creation = MembreCreationForm()
            champs_attendus = ['username', 'password', 'email', 'nom', 'prenom', 'telephone']
            champs_trouves = [field.name for field in form_creation]
            
            print("   ✅ MembreCreationForm importé avec succès")
            print(f"   📋 Champs trouvés: {len(champs_trouves)}")
            
            for champ in champs_attendus:
                if champ in champs_trouves:
                    print(f"      ✅ {champ}")
                else:
                    print(f"      ❌ {champ} manquant")
                    self.erreurs.append(f"Champ {champ} manquant dans MembreCreationForm")
            
            # Test MembreDocumentForm
            form_document = MembreDocumentForm()
            champs_documents = ['piece_identite_recto', 'piece_identite_verso', 'photo_identite']
            champs_docs_trouves = [field.name for field in form_document]
            
            print("   ✅ MembreDocumentForm importé avec succès")
            for champ in champs_documents:
                if champ in champs_docs_trouves:
                    print(f"      ✅ {champ}")
                else:
                    print(f"      ❌ {champ} manquant")
                    self.erreurs.append(f"Champ {champ} manquant dans MembreDocumentForm")
                    
        except ImportError as e:
            print(f"   ❌ Erreur d'import: {e}")
            self.erreurs.append(f"Erreur import formulaires: {e}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            self.erreurs.append(f"Erreur vérification formulaires: {e}")
    
    def verifier_vues(self):
        print("\n👁️ 2. VÉRIFICATION DES VUES")
        print("-" * 40)
        
        try:
            from membres.views import creer_membre, liste_membres_agent, upload_documents_membre
            
            vues_attendues = [
                'creer_membre', 
                'liste_membres_agent', 
                'upload_documents_membre'
            ]
            
            for vue in vues_attendues:
                try:
                    globals()[vue]  # Vérifie que la vue existe
                    print(f"   ✅ {vue} importée avec succès")
                except:
                    print(f"   ❌ {vue} non trouvée")
                    self.erreurs.append(f"Vue {vue} manquante")
            
            # Vérifier les décorateurs de sécurité
            from django.contrib.auth.decorators import login_required
            from core.utils import gerer_erreurs, est_agent
            
            print("   🔐 Vérification sécurité des vues:")
            
            # Test symbolique des décorateurs
            try:
                est_agent_func = est_agent
                gerer_erreurs_func = gerer_erreurs
                print("      ✅ Décorateurs de sécurité présents")
            except Exception as e:
                print(f"      ❌ Décorateurs manquants: {e}")
                self.erreurs.append("Décorateurs de sécurité manquants")
                
        except ImportError as e:
            print(f"   ❌ Erreur d'import vues: {e}")
            self.erreurs.append(f"Erreur import vues: {e}")
    
    def verifier_urls(self):
        print("\n🌐 3. VÉRIFICATION DES URLs")
        print("-" * 40)
        
        try:
            from django.urls import get_resolver, reverse, NoReverseMatch
            
            urls_attendues = [
                'membres:creer_membre',
                'membres:liste_membres_agent', 
                'membres:upload_documents'
            ]
            
            for url_name in urls_attendues:
                try:
                    reverse(url_name)
                    print(f"   ✅ {url_name} configurée")
                except NoReverseMatch:
                    print(f"   ❌ {url_name} non configurée")
                    self.erreurs.append(f"URL {url_name} non configurée")
            
            # Vérifier le namespace
            try:
                reverse('membres:creer_membre')
                print("   ✅ Namespace 'membres' actif")
            except:
                print("   ❌ Problème avec le namespace 'membres'")
                self.erreurs.append("Namespace 'membres' problématique")
                
        except Exception as e:
            print(f"   ❌ Erreur vérification URLs: {e}")
            self.erreurs.append(f"Erreur URLs: {e}")
    
    def verifier_templates(self):
        print("\n🎨 4. VÉRIFICATION DES TEMPLATES")
        print("-" * 40)
        
        from django.template.loader import get_template
        
        templates_attendus = [
            'membres/creer_membre.html',
            'membres/liste_membres_agent.html', 
            'membres/upload_documents.html',
            'agents/base_agent.html'  # Template de base nécessaire
        ]
        
        for template in templates_attendus:
            try:
                get_template(template)
                print(f"   ✅ {template} trouvé")
            except:
                print(f"   ❌ {template} manquant")
                self.erreurs.append(f"Template {template} manquant")
    
    def verifier_permissions(self):
        print("\n🔐 5. VÉRIFICATION DES PERMISSIONS")
        print("-" * 40)
        
        try:
            # Vérifier le groupe Agent
            groupe_agent = Group.objects.filter(name='Agent').first()
            if groupe_agent:
                print(f"   ✅ Groupe 'Agent' trouvé ({groupe_agent.user_set.count()} utilisateurs)")
            else:
                print("   ❌ Groupe 'Agent' non trouvé")
                self.erreurs.append("Groupe Agent non trouvé")
            
            # Vérifier les permissions nécessaires
            from django.contrib.auth.models import Permission
            from django.contrib.contenttypes.models import ContentType
            
            # Permissions de base pour les membres
            content_type_membre = ContentType.objects.get_for_model(apps.get_model('membres', 'Membre'))
            permissions_membre = Permission.objects.filter(content_type=content_type_membre)
            
            print(f"   📋 Permissions Membre disponibles: {permissions_membre.count()}")
            
            # Vérifier si les agents ont des permissions
            if groupe_agent:
                permissions_agent = groupe_agent.permissions.all()
                print(f"   🔧 Permissions du groupe Agent: {permissions_agent.count()}")
                
        except Exception as e:
            print(f"   ❌ Erreur vérification permissions: {e}")
            self.erreurs.append(f"Erreur permissions: {e}")
    
    def tester_fonctionnalites(self):
        print("\n🧪 6. TEST DES FONCTIONNALITÉS")
        print("-" * 40)
        
        try:
            from membres.models import Membre
            from agents.models import Agent
            from django.contrib.auth.models import User
            
            # Test 1: Données existantes
            total_membres = Membre.objects.count()
            total_agents = Agent.objects.count()
            
            print(f"   📊 Données existantes:")
            print(f"      • Membres: {total_membres}")
            print(f"      • Agents: {total_agents}")
            
            # Test 2: Vérifier agent_createur
            membres_avec_agent = Membre.objects.filter(agent_createur__isnull=False).count()
            print(f"      • Membres avec agent_createur: {membres_avec_agent}")
            
            # Test 3: Vérifier génération numéro unique
            from core.utils import generer_numero_unique
            try:
                numero_test = generer_numero_unique()
                print(f"   🔢 Génération numéro unique: ✅ ({numero_test})")
            except Exception as e:
                print(f"   🔢 Génération numéro unique: ❌ ({e})")
                self.erreurs.append(f"Génération numéro unique échouée: {e}")
            
            # Test 4: Vérifier fonction est_agent
            from core.utils import est_agent
            try:
                # Tester avec un utilisateur non-agent
                user_normal = User.objects.filter(agent__isnull=True).first()
                if user_normal:
                    resultat = est_agent(user_normal)
                    print(f"   👤 Test est_agent (non-agent): ✅ ({resultat})")
                
                # Tester avec un agent
                agent_user = User.objects.filter(agent__isnull=False).first()
                if agent_user:
                    resultat = est_agent(agent_user)
                    print(f"   👤 Test est_agent (agent): ✅ ({resultat})")
                    
            except Exception as e:
                print(f"   👤 Test est_agent: ❌ ({e})")
                self.erreurs.append(f"Fonction est_agent échouée: {e}")
                
        except Exception as e:
            print(f"   ❌ Erreur tests fonctionnalités: {e}")
            self.erreurs.append(f"Erreur tests: {e}")
    
    def analyser_donnees_test(self):
        print("\n📊 7. ANALYSE DES DONNÉES DE TEST")
        print("-" * 40)
        
        try:
            from membres.models import Membre
            from agents.models import Agent
            
            # Statistiques détaillées
            agents = Agent.objects.all()
            print(f"   👥 Agents disponibles ({agents.count()}):")
            
            for agent in agents:
                membres_crees = Membre.objects.filter(agent_createur=agent).count()
                nom_agent = agent.nom_complet() if hasattr(agent, 'nom_complet') else agent.user.username
                print(f"      • {nom_agent}: {membres_crees} membres créés")
            
            # Analyse des statuts
            statuts_membres = Membre.objects.values('statut').annotate(count=models.Count('id'))
            print(f"   📈 Répartition par statut:")
            for statut in statuts_membres:
                print(f"      • {statut['statut']}: {statut['count']} membres")
            
            # Analyse documents
            statuts_docs = Membre.objects.values('statut_documents').annotate(count=models.Count('id'))
            print(f"   📄 Statut des documents:")
            for statut in statuts_docs:
                print(f"      • {statut['statut_documents']}: {statut['count']} membres")
                
        except Exception as e:
            print(f"   ❌ Erreur analyse données: {e}")
    
    def simuler_creation_membre(self):
        print("\n🎯 8. SIMULATION CRÉATION MEMBRE")
        print("-" * 40)
        
        try:
            from membres.forms import MembreCreationForm
            from agents.models import Agent
            
            # Données de test
            donnees_test = {
                'username': 'test_membre_' + str(models.Value('NOW()')),
                'password': 'password123',
                'nom': 'Dupont',
                'prenom': 'Jean',
                'telephone': '0123456789',
                'categorie': 'standard',
                'type_piece_identite': 'cni',
                'cmu_option': False
            }
            
            form = MembreCreationForm(donnees_test)
            
            if form.is_valid():
                print("   ✅ Formulaire valide avec données de test")
                print("   📋 Champs validés:")
                for champ, valeur in form.cleaned_data.items():
                    if champ != 'password':  # Ne pas afficher le mot de passe
                        print(f"      • {champ}: {valeur}")
            else:
                print("   ❌ Formulaire invalide avec données de test")
                print("   📋 Erreurs:")
                for champ, erreurs in form.errors.items():
                    print(f"      • {champ}: {', '.join(erreurs)}")
                    self.erreurs.append(f"Erreur validation {champ}: {', '.join(erreurs)}")
                    
        except Exception as e:
            print(f"   ❌ Erreur simulation: {e}")
            self.erreurs.append(f"Erreur simulation: {e}")
    
    def generer_rapport_final(self):
        print("\n" + "=" * 70)
        print("📊 RAPPORT FINAL D'ANALYSE")
        print("=" * 70)
        
        # Résumé
        total_erreurs = len(self.erreurs)
        
        if total_erreurs == 0:
            print("🎉 ✅ IMPLÉMENTATION RÉUSSIE !")
            print("   Tous les composants sont fonctionnels")
        else:
            print(f"⚠️  {total_erreurs} PROBLÈME(S) IDENTIFIÉ(S)")
            for i, erreur in enumerate(self.erreurs, 1):
                print(f"   {i}. {erreur}")
        
        print("\n🔧 RECOMMANDATIONS:")
        
        if total_erreurs > 0:
            print("   1. Corriger les erreurs listées ci-dessus")
            print("   2. Tester la création manuelle d'un membre")
            print("   3. Vérifier les permissions du groupe Agent")
        else:
            print("   1. ✅ Tester la création manuelle d'un membre")
            print("   2. ✅ Vérifier l'upload des documents")
            print("   3. ✅ Former les agents à l'utilisation")
        
        print("\n🎯 PROCHAINES ÉTAPES:")
        print("   • Tester avec un compte agent connecté")
        print("   • Créer au moins un membre de test")
        print("   • Vérifier l'apparition dans 'Mes membres'")
        print("   • Tester l'upload de documents")
        print("   • Valider les emails de notification (si configurés)")
        
        print(f"\n⏱️  Analyse terminée à: {models.DateTimeField(auto_now=True).value_from_object(None)}")

def main():
    try:
        analyse = AnalysePostImplementation()
        analyse.executer_analyse_complete()
        
        # Demander si on veut tester la création
        print("\n" + "=" * 70)
        reponse = input("🧪 Voulez-vous tester la création d'un membre réel ? (o/n): ")
        
        if reponse.lower() in ['o', 'oui', 'y', 'yes']:
            print("\n🔧 TEST DE CRÉATION RÉELLE...")
            analyser_creation_reelle()
            
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()

def analyser_creation_reelle():
    """Test de création réelle d'un membre"""
    try:
        from membres.forms import MembreCreationForm
        from agents.models import Agent
        from django.contrib.auth.models import User
        
        # Trouver un agent existant pour le test
        agent_test = Agent.objects.first()
        if not agent_test:
            print("   ❌ Aucun agent trouvé pour le test")
            return
        
        print(f"   👤 Agent test: {agent_test.user.username}")
        
        # Données de test réalistes
        import random
        numero_test = random.randint(1000, 9999)
        
        donnees_test = {
            'username': f'test_membre_{numero_test}',
            'password': 'TestPassword123!',
            'email': f'test{numero_test}@example.com',
            'nom': 'TEST',
            'prenom': f'Utilisateur{numero_test}',
            'telephone': f'01{random.randint(1000, 9999)}{random.randint(1000, 9999)}',
            'numero_urgence': f'06{random.randint(1000, 9999)}{random.randint(1000, 9999)}',
            'date_naissance': '1990-01-01',
            'adresse': '123 Rue de Test, Ville Test',
            'profession': 'Testeur',
            'categorie': 'standard',
            'cmu_option': False,
            'type_piece_identite': 'cni',
            'numero_piece_identite': f'TEST{numero_test}',
            'date_expiration_piece': '2030-12-31'
        }
        
        form = MembreCreationForm(donnees_test)
        
        if form.is_valid():
            print("   ✅ Formulaire valide - Création en cours...")
            try:
                membre = form.save(agent_createur=agent_test)
                print(f"   🎉 MEMBRE CRÉÉ AVEC SUCCÈS !")
                print(f"      • Numéro unique: {membre.numero_unique}")
                print(f"      • Nom: {membre.prenom} {membre.nom}")
                print(f"      • Statut: {membre.statut}")
                print(f"      • Agent créateur: {membre.agent_createur}")
                
                # Nettoyer le test
                membre.user.delete()  # Supprime aussi le membre via CASCADE
                print("   🧹 Membre test supprimé")
                
            except Exception as e:
                print(f"   ❌ Erreur lors de la création: {e}")
        else:
            print("   ❌ Formulaire invalide:")
            for champ, erreurs in form.errors.items():
                print(f"      • {champ}: {', '.join(erreurs)}")
                
    except Exception as e:
        print(f"   ❌ Erreur test création: {e}")

if __name__ == "__main__":
    main()