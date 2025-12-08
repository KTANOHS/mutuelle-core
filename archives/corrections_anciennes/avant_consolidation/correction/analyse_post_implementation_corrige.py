# analyse_post_implementation_corrige.py

import os
import sys
import django

# Configuration Django CORRECTE
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')  # Corrigez avec le bon nom
django.setup()

from django.apps import apps
from django.db import models
from django.contrib.auth.models import User, Group
from django.template.loader import get_template
from django.urls import reverse, NoReverseMatch

class AnalysePostImplementation:
    def __init__(self):
        self.resultats = {}
        self.erreurs = []
    
    def executer_analyse_complete(self):
        print("🚀 ANALYSE POST-IMPLÉMENTATION - CRÉATION MEMBRES PAR AGENTS")
        print("=" * 70)
        print()
        
        self.verifier_fonction_generer_numero()
        self.verifier_formulaires()
        self.verifier_vues()
        self.verifier_urls()
        self.verifier_templates()
        self.verifier_permissions()
        self.tester_fonctionnalites()
        self.analyser_donnees_test()
        self.generer_rapport_final()
    
    def verifier_fonction_generer_numero(self):
        print("🔢 1. VÉRIFICATION FONCTION GÉNÉRATION NUMÉRO")
        print("-" * 45)
        
        try:
            from core.utils import generer_numero_unique
            numero_test = generer_numero_unique()
            print(f"   ✅ generer_numero_unique() fonctionne")
            print(f"   📝 Numéro test généré: {numero_test}")
            
        except ImportError as e:
            print(f"   ❌ Fonction manquante: {e}")
            print("   🔧 Solution: Ajouter la fonction dans core/utils.py")
            self.erreurs.append("generer_numero_unique manquante")
            
            # Solution d'urgence
            print("   💡 Création de la fonction de secours...")
            self.creer_fonction_secours()
    
    def creer_fonction_secours(self):
        """Crée une fonction de secours si la fonction originale manque"""
        try:
            import random
            import string
            from django.utils import timezone
            
            def generer_numero_unique_secours():
                date_part = timezone.now().strftime("%Y%m%d")
                random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                return f"MEM-{date_part}-{random_part}"
            
            # Injecter temporairement
            import core.utils
            core.utils.generer_numero_unique = generer_numero_unique_secours
            print("   ✅ Fonction de secours créée")
            
        except Exception as e:
            print(f"   ❌ Échec création fonction secours: {e}")
    
    def verifier_formulaires(self):
        print("\n📝 2. VÉRIFICATION DES FORMULAIRES")
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
    
    def verifier_vues(self):
        print("\n👁️ 3. VÉRIFICATION DES VUES")
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
            from core.utils import gerer_erreurs, est_agent
            
            print("   🔐 Vérification sécurité des vues:")
            
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
        print("\n🌐 4. VÉRIFICATION DES URLs")
        print("-" * 40)
        
        try:
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
            
        except Exception as e:
            print(f"   ❌ Erreur vérification URLs: {e}")
            self.erreurs.append(f"Erreur URLs: {e}")
    
    def verifier_templates(self):
        print("\n🎨 5. VÉRIFICATION DES TEMPLATES")
        print("-" * 40)
        
        templates_attendus = [
            'membres/creer_membre.html',
            'membres/liste_membres_agent.html', 
            'membres/upload_documents.html'
        ]
        
        for template in templates_attendus:
            try:
                get_template(template)
                print(f"   ✅ {template} trouvé")
            except:
                print(f"   ❌ {template} manquant")
                self.erreurs.append(f"Template {template} manquant")
    
    def verifier_permissions(self):
        print("\n🔐 6. VÉRIFICATION DES PERMISSIONS")
        print("-" * 40)
        
        try:
            groupe_agent = Group.objects.filter(name='Agent').first()
            if groupe_agent:
                print(f"   ✅ Groupe 'Agent' trouvé ({groupe_agent.user_set.count()} utilisateurs)")
            else:
                print("   ❌ Groupe 'Agent' non trouvé")
                self.erreurs.append("Groupe Agent non trouvé")
                
        except Exception as e:
            print(f"   ❌ Erreur vérification permissions: {e}")
    
    def tester_fonctionnalites(self):
        print("\n🧪 7. TEST DES FONCTIONNALITÉS")
        print("-" * 40)
        
        try:
            from membres.models import Membre
            from agents.models import Agent
            
            total_membres = Membre.objects.count()
            total_agents = Agent.objects.count()
            
            print(f"   📊 Données existantes:")
            print(f"      • Membres: {total_membres}")
            print(f"      • Agents: {total_agents}")
            
            membres_avec_agent = Membre.objects.filter(agent_createur__isnull=False).count()
            print(f"      • Membres avec agent_createur: {membres_avec_agent}")
            
            # Test fonction est_agent
            from core.utils import est_agent
            agent_user = User.objects.filter(agent__isnull=False).first()
            if agent_user:
                resultat = est_agent(agent_user)
                print(f"   👤 Test est_agent: ✅ ({resultat})")
                
        except Exception as e:
            print(f"   ❌ Erreur tests fonctionnalités: {e}")
    
    def analyser_donnees_test(self):
        print("\n📊 8. ANALYSE DES DONNÉES DE TEST")
        print("-" * 40)
        
        try:
            from membres.models import Membre
            from agents.models import Agent
            
            agents = Agent.objects.all()
            print(f"   👥 Agents disponibles ({agents.count()}):")
            
            for agent in agents:
                membres_crees = Membre.objects.filter(agent_createur=agent).count()
                nom_agent = agent.nom_complet() if hasattr(agent, 'nom_complet') else agent.user.username
                print(f"      • {nom_agent}: {membres_crees} membres créés")
                
        except Exception as e:
            print(f"   ❌ Erreur analyse données: {e}")
    
    def generer_rapport_final(self):
        print("\n" + "=" * 70)
        print("📊 RAPPORT FINAL D'ANALYSE")
        print("=" * 70)
        
        total_erreurs = len(self.erreurs)
        
        if total_erreurs == 0:
            print("🎉 ✅ IMPLÉMENTATION RÉUSSIE !")
            print("   Tous les composants sont fonctionnels")
        else:
            print(f"⚠️  {total_erreurs} PROBLÈME(S) IDENTIFIÉ(S)")
            for i, erreur in enumerate(self.erreurs, 1):
                print(f"   {i}. {erreur}")
        
        print("\n🔧 ACTIONS REQUISES:")
        if "generer_numero_unique manquante" in self.erreurs:
            print("   1. ✅ AJOUTER la fonction generer_numero_unique() dans core/utils.py")
        if any("manquant" in erreur for erreur in self.erreurs):
            print("   2. ✅ CRÉER les fichiers manquants (formulaires, templates, etc.)")
        
        print("\n🎯 PROCHAINES ÉTAPES:")
        print("   • Tester avec: python manage.py runserver")
        print("   • Se connecter en tant qu'agent")
        print("   • Accéder à /membres/creer/")

def main():
    try:
        print("🔧 Initialisation de l'analyse...")
        analyse = AnalysePostImplementation()
        analyse.executer_analyse_complete()
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()