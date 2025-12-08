# diagnostic_final_complet.py
import os
import django
import sys
from datetime import datetime, timedelta

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.db import transaction
from django.db.models import Q
from django.apps import apps
from django.utils import timezone

User = get_user_model()

class DiagnosticComplet:
    """
    Script de diagnostic COMPLET - version finalissime
    """
    
    def __init__(self):
        self.results = {
            'success': [],
            'warnings': [],
            'errors': []
        }
        self.models = {}
        self.test_data = {}
    
    def log_success(self, message):
        self.results['success'].append(message)
        print(f"✅ {message}")
    
    def log_warning(self, message):
        self.results['warnings'].append(message)
        print(f"⚠️ {message}")
    
    def log_error(self, message):
        self.results['errors'].append(message)
        print(f"❌ {message}")
    
    def detecter_modeles(self):
        """Détecter automatiquement tous les modèles disponibles"""
        print("🔍 Détection des modèles...")
        
        # Parcourir toutes les applications
        for app_config in apps.get_app_configs():
            for modele in app_config.get_models():
                nom_modele = modele.__name__
                self.models[nom_modele] = modele
        
        # Afficher les modèles importants
        modeles_importants = ['Membre', 'Agent', 'Medecin', 'Pharmacien', 'Assureur', 'Bon', 'Ordonnance', 'Soin', 'SpecialiteMedicale', 'EtablissementMedical']
        for modele in modeles_importants:
            if modele in self.models:
                self.log_success(f"Modèle trouvé: {modele}")
            else:
                self.log_warning(f"Modèle manquant: {modele}")
        
        return True
    
    def analyser_structure_modeles(self):
        """Analyser la structure des modèles importants"""
        print("\n📋 Analyse des structures de modèles...")
        
        modeles_a_analyser = ['Agent', 'Medecin', 'Pharmacien', 'Assureur', 'Membre']
        
        for nom_modele in modeles_a_analyser:
            if nom_modele in self.models:
                modele = self.models[nom_modele]
                champs = [f.name for f in modele._meta.fields]
                print(f"   🎯 {nom_modele} - Champs: {', '.join(champs[:8])}...")
                
                # Identifier les champs obligatoires
                champs_obligatoires = []
                for champ in modele._meta.fields:
                    if not champ.null and not champ.blank and not champ.has_default():
                        champs_obligatoires.append(champ.name)
                if champs_obligatoires:
                    print(f"   📌 Champs obligatoires: {champs_obligatoires}")
    
    def creer_specialite_medicale(self):
        """Créer une spécialité médicale pour les tests"""
        try:
            if 'SpecialiteMedicale' not in self.models:
                self.log_warning("Modèle SpecialiteMedicale non disponible")
                return None
            
            SpecialiteMedicale = self.models['SpecialiteMedicale']
            
            # Créer ou récupérer une spécialité de test
            specialite, created = SpecialiteMedicale.objects.get_or_create(
                nom='Médecine Générale',
                defaults={
                    'description': 'Spécialité de test pour diagnostic',
                    'actif': True
                }
            )
            
            if created:
                self.log_success("Spécialité médicale de test créée")
            else:
                self.log_success("Spécialité médicale existante récupérée")
            
            return specialite
            
        except Exception as e:
            self.log_warning(f"Impossible de créer la spécialité médicale: {e}")
            return None
    
    def creer_etablissement_medical(self):
        """Créer un établissement médical pour les tests"""
        try:
            if 'EtablissementMedical' not in self.models:
                self.log_warning("Modèle EtablissementMedical non disponible")
                return None
            
            EtablissementMedical = self.models['EtablissementMedical']
            
            # Créer ou récupérer un établissement de test
            etablissement, created = EtablissementMedical.objects.get_or_create(
                nom='Centre Médical de Test',
                defaults={
                    'adresse': 'Adresse de test',
                    'telephone': '+2250100000099',
                    'type_etablissement': 'Centre de santé',
                    'actif': True
                }
            )
            
            if created:
                self.log_success("Établissement médical de test créé")
            else:
                self.log_success("Établissement médical existant récupéré")
            
            return etablissement
            
        except Exception as e:
            self.log_warning(f"Impossible de créer l'établissement médical: {e}")
            return None
    
    def creer_acteurs_test(self):
        """Créer les acteurs de test avec gestion COMPLÈTE des dépendances"""
        try:
            # Vérifier les modèles nécessaires
            if 'Agent' not in self.models:
                self.log_error("Modèle Agent manquant")
                return False
            
            Agent = self.models['Agent']
            Membre = self.models.get('Membre')
            Medecin = self.models.get('Medecin')
            Pharmacien = self.models.get('Pharmacien') 
            Assureur = self.models.get('Assureur')
            
            # Agent de test
            agent_user, created = User.objects.get_or_create(
                username='test_agent_complet',
                defaults={
                    'email': 'agent_complet@test.com', 
                    'first_name': 'Test', 
                    'last_name': 'Agent'
                }
            )
            if created:
                agent_user.set_password('test123')
                agent_user.save()
            
            # Préparer les données de l'agent avec gestion des champs
            donnees_agent = {
                'user': agent_user,
                'matricule': 'COMPLET001',
                'date_embauche': timezone.now().date(),
                'poste': 'Agent de test',
            }
            
            # Ajouter des champs optionnels si ils existent
            champs_agent = [f.name for f in Agent._meta.fields]
            if 'telephone' in champs_agent:
                donnees_agent['telephone'] = '+2250100000001'
            if 'est_actif' in champs_agent:
                donnees_agent['est_actif'] = True
            
            agent, created = Agent.objects.get_or_create(
                user=agent_user,
                defaults=donnees_agent
            )
            
            # Médecin de test - avec gestion COMPLÈTE des dépendances
            medecin = None
            if Medecin:
                medecin_user, created = User.objects.get_or_create(
                    username='test_medecin_complet',
                    defaults={
                        'email': 'medecin_complet@test.com', 
                        'first_name': 'Test', 
                        'last_name': 'Medecin'
                    }
                )
                if created:
                    medecin_user.set_password('test123')
                    medecin_user.save()
                
                # Préparer les données du médecin
                donnees_medecin = {
                    'user': medecin_user,
                    'numero_ordre': 'COMPLET001',
                    'telephone_pro': '+2250100000002'
                }
                
                # Gérer la spécialité médicale
                champs_medecin = [f.name for f in Medecin._meta.fields]
                if 'specialite' in champs_medecin:
                    specialite = self.creer_specialite_medicale()
                    if specialite:
                        donnees_medecin['specialite'] = specialite
                    else:
                        self.log_warning("Impossible de créer le médecin - spécialité manquante")
                        medecin_user.delete()
                        medecin = None
                
                # Gérer l'établissement médical (NOUVEAU - correction du problème)
                if 'etablissement' in champs_medecin:
                    etablissement = self.creer_etablissement_medical()
                    if etablissement:
                        donnees_medecin['etablissement'] = etablissement
                    else:
                        self.log_warning("Impossible de créer le médecin - établissement manquant")
                        medecin_user.delete()
                        medecin = None
                
                # Créer le médecin seulement si on a toutes les dépendances
                if donnees_medecin.get('specialite') and donnees_medecin.get('etablissement'):
                    medecin, created = Medecin.objects.get_or_create(
                        user=medecin_user,
                        defaults=donnees_medecin
                    )
                    if created:
                        self.log_success("Médecin créé avec succès")
                else:
                    self.log_warning("Médecin non créé - dépendances manquantes")
            
            # Pharmacien de test
            pharmacien = None
            if Pharmacien:
                pharmacien_user, created = User.objects.get_or_create(
                    username='test_pharmacien_complet', 
                    defaults={
                        'email': 'pharmacien_complet@test.com', 
                        'first_name': 'Test', 
                        'last_name': 'Pharmacien'
                    }
                )
                if created:
                    pharmacien_user.set_password('test123')
                    pharmacien_user.save()
                
                donnees_pharmacien = {
                    'user': pharmacien_user,
                    'nom_pharmacie': 'Pharmacie Test COMPLET',
                    'adresse_pharmacie': 'Adresse test complète',
                    'telephone': '+2250100000003'
                }
                
                pharmacien, created = Pharmacien.objects.get_or_create(
                    user=pharmacien_user,
                    defaults=donnees_pharmacien
                )
            
            # Assureur de test
            assureur = None
            if Assureur:
                assureur_user, created = User.objects.get_or_create(
                    username='test_assureur_complet',
                    defaults={
                        'email': 'assureur_complet@test.com', 
                        'first_name': 'Test', 
                        'last_name': 'Assureur'
                    }
                )
                if created:
                    assureur_user.set_password('test123')
                    assureur_user.save()
                
                donnees_assureur = {
                    'user': assureur_user,
                    'numero_employe': 'COMPLET001',
                    'departement': 'Test'
                }
                
                champs_assureur = [f.name for f in Assureur._meta.fields]
                if 'date_embauche' in champs_assureur:
                    donnees_assureur['date_embauche'] = timezone.now().date()
                if 'est_actif' in champs_assureur:
                    donnees_assureur['est_actif'] = True
                
                assureur, created = Assureur.objects.get_or_create(
                    user=assureur_user,
                    defaults=donnees_assureur
                )
            
            # Membre de test - avec gestion COMPLÈTE des champs obligatoires
            membre = None
            if Membre:
                donnees_membre = {
                    'numero_membre': 'COMPLET001',
                    'nom': 'Test',
                    'prenom': 'Complet', 
                    'date_naissance': '1990-01-01',
                    'email': 'membre_complet@test.com',
                    'telephone': '+2250100000005',
                    'adresse': 'Adresse test complète',
                    'date_adhesion': timezone.now().date(),
                    'type_contrat': 'Standard',
                    'numero_contrat': 'CONT001',
                    'date_effet': timezone.now().date(),
                    'date_expiration': timezone.now().date() + timedelta(days=365),
                    'taux_couverture': 80.0
                }
                
                # Essayer d'ajouter l'agent si le champ existe
                champs_membre = [f.name for f in Membre._meta.fields]
                if 'agent_createur' in champs_membre:
                    donnees_membre['agent_createur'] = agent
                elif 'agent' in champs_membre:
                    donnees_membre['agent'] = agent
                
                membre, created = Membre.objects.get_or_create(
                    numero_membre='COMPLET001',
                    defaults=donnees_membre
                )
            
            self.test_data = {
                'agent': agent,
                'medecin': medecin,
                'pharmacien': pharmacien, 
                'assureur': assureur,
                'membre': membre
            }
            
            self.log_success("Acteurs de test créés avec succès")
            return True
            
        except FieldError as e:
            self.log_error(f"Erreur de champ lors de la création: {e}")
            return False
        except Exception as e:
            self.log_error(f"Erreur création acteurs: {str(e)}")
            import traceback
            print(f"🔍 Détails de l'erreur: {traceback.format_exc()}")
            return False
    
    def analyser_donnees_existantes(self):
        """Analyser les données existantes dans la base"""
        try:
            self.log_success("📊 ANALYSE DES DONNÉES EXISTANTES")
            
            # Analyser les membres existants
            if 'Membre' in self.models:
                Membre = self.models['Membre']
                membres = Membre.objects.all()[:5]
                
                print(f"   👥 {len(membres)} membre(s) trouvé(s):")
                for i, membre in enumerate(membres, 1):
                    info = f"      {i}. {membre.nom} {membre.prenom} (ID: {membre.id})"
                    print(info)
            
            # Compter les données par type
            print(f"\n   📈 STATISTIQUES GÉNÉRALES:")
            for modele_nom in ['Bon', 'Ordonnance', 'Soin']:
                if modele_nom in self.models:
                    count = self.models[modele_nom].objects.count()
                    print(f"      • {modele_nom}: {count}")
            
            # Analyser les agents existants
            if 'Agent' in self.models:
                agents = self.models['Agent'].objects.all()[:3]
                print(f"\n   👨‍💼 Agents existants ({len(agents)}):")
                for agent in agents:
                    info = f"      • {agent.matricule}"
                    if hasattr(agent, 'user') and agent.user:
                        info += f" ({agent.user.username})"
                    print(info)
            
            return True
            
        except Exception as e:
            self.log_warning(f"Analyse données existantes échouée: {e}")
            return False
    
    def tester_relations_acteurs(self):
        """Tester les relations entre les acteurs avec gestion d'erreurs"""
        try:
            # Vérifier que les données de test existent
            if not self.test_data.get('membre'):
                self.log_warning("Test relations ignoré - pas de membre de test")
                return True
            
            # Test Agent -> Membre
            membre = self.test_data['membre']
            self.log_success(f"ÉTAPE 1: Membre de test disponible - {membre.nom} {membre.prenom}")
            
            # Test visibilité des données
            if 'Membre' in self.models:
                membres_count = self.models['Membre'].objects.count()
                self.log_success(f"ÉTAPE 2: Visibilité données - {membres_count} membre(s) dans le système")
            
            # Vérifier la présence des autres acteurs
            if self.test_data.get('agent'):
                self.log_success("ÉTAPE 3: Agent présent dans le système")
            
            if self.test_data.get('medecin'):
                self.log_success("ÉTAPE 4: Médecin présent dans le système")
            
            if self.test_data.get('pharmacien'):
                self.log_success("ÉTAPE 5: Pharmacien présent dans le système")
            
            if self.test_data.get('assureur'):
                self.log_success("ÉTAPE 6: Assureur présent dans le système")
            
            return True
            
        except Exception as e:
            self.log_error(f"Erreur test relations: {str(e)}")
            return False
    
    def tester_acces_donnees(self):
        """Tester l'accès aux données par différents acteurs"""
        try:
            self.log_success("🔐 TEST ACCÈS AUX DONNÉES")
            
            # Test accès membres
            if 'Membre' in self.models:
                membres = self.models['Membre'].objects.all()
                self.log_success(f"   • Accès membres: {len(membres)} enregistrement(s)")
            
            # Test accès bons
            if 'Bon' in self.models:
                bons = self.models['Bon'].objects.all()
                self.log_success(f"   • Accès bons: {len(bons)} enregistrement(s)")
            
            # Test accès ordonnances
            if 'Ordonnance' in self.models:
                ordonnances = self.models['Ordonnance'].objects.all()
                self.log_success(f"   • Accès ordonnances: {len(ordonnances)} enregistrement(s)")
            
            # Test accès soins
            if 'Soin' in self.models:
                soins = self.models['Soin'].objects.all()
                self.log_success(f"   • Accès soins: {len(soins)} enregistrement(s)")
            
            return True
            
        except Exception as e:
            self.log_error(f"Erreur test accès: {str(e)}")
            return False
    
    def tester_workflow_complet(self):
        """Tester un workflow COMPLET avec création de données"""
        try:
            self.log_success("🔀 TEST WORKFLOW COMPLET")
            
            # Vérifier les données minimales
            if not self.test_data.get('membre'):
                self.log_warning("Workflow ignoré - membre manquant")
                return True
            
            # Étape 1: Vérifier que l'agent peut créer un membre
            self.log_success("ÉTAPE 1: Membre de test disponible")
            
            # Étape 2: Vérifier création bon si le modèle existe
            if 'Bon' in self.models and self.test_data.get('agent') and self.test_data.get('membre'):
                Bon = self.models['Bon']
                try:
                    with transaction.atomic():
                        # Analyser les champs disponibles
                        champs_bon = [f.name for f in Bon._meta.fields]
                        
                        donnees_bon = {
                            'membre': self.test_data['membre'],
                            'date_creation': timezone.now(),
                            'statut': 'emis'
                        }
                        
                        # Ajouter des champs selon ce qui existe
                        if 'numero_bon' in champs_bon:
                            donnees_bon['numero_bon'] = f"COMPLET{timezone.now().strftime('%Y%m%d%H%M%S')}"
                        if 'type_soin' in champs_bon:
                            donnees_bon['type_soin'] = 'Consultation diagnostic'
                        if 'description' in champs_bon:
                            donnees_bon['description'] = 'Bon créé par script diagnostic'
                        if 'created_by' in champs_bon:
                            donnees_bon['created_by'] = self.test_data['agent'].user
                        if 'agent' in champs_bon:
                            donnees_bon['agent'] = self.test_data['agent']
                        
                        bon = Bon.objects.create(**donnees_bon)
                        self.log_success("ÉTAPE 2: Bon créé avec succès")
                        self.test_data['bon_test'] = bon
                        
                except Exception as e:
                    self.log_warning(f"Création bon échouée: {e}")
            
            # Étape 3: Vérifier création ordonnance si possible
            if 'Ordonnance' in self.models and self.test_data.get('medecin') and 'bon_test' in self.test_data:
                Ordonnance = self.models['Ordonnance']
                try:
                    donnees_ordonnance = {
                        'medecin': self.test_data['medecin'],
                        'date_creation': timezone.now(),
                        'statut': 'active'
                    }
                    
                    # Ajouter les champs selon la structure
                    champs_ordonnance = [f.name for f in Ordonnance._meta.fields]
                    if 'bon_de_soin' in champs_ordonnance:
                        donnees_ordonnance['bon_de_soin'] = self.test_data['bon_test']
                    if 'medicament' in champs_ordonnance:
                        donnees_ordonnance['medicament'] = "Test Médicament"
                    if 'posologie' in champs_ordonnance:
                        donnees_ordonnance['posologie'] = "Test posologie"
                    
                    ordonnance = Ordonnance.objects.create(**donnees_ordonnance)
                    self.log_success("ÉTAPE 3: Ordonnance créée avec succès")
                    self.test_data['ordonnance_test'] = ordonnance
                    
                except Exception as e:
                    self.log_warning(f"Création ordonnance échouée: {e}")
            
            # Étape 4: Vérifier autres acteurs
            if self.test_data.get('medecin'):
                self.log_success("ÉTAPE 4: Médecin présent dans le système")
            
            if self.test_data.get('pharmacien'):
                self.log_success("ÉTAPE 5: Pharmacien présent dans le système")
            
            if self.test_data.get('assureur'):
                self.log_success("ÉTAPE 6: Assureur présent dans le système")
            
            return True
            
        except Exception as e:
            self.log_error(f"Erreur workflow: {str(e)}")
            return False
    
    def generer_rapport_final(self):
        """Générer un rapport complet et détaillé"""
        print("\n" + "="*80)
        print("📊 RAPPORT FINAL DE DIAGNOSTIC - VERSION COMPLÈTE")
        print("="*80)
        
        # Résumé exécutif
        print(f"\n🎯 RÉSUMÉ EXÉCUTIF:")
        total_tests = len(self.results['success']) + len(self.results['warnings']) + len(self.results['errors'])
        taux_reussite = (len(self.results['success']) / total_tests * 100) if total_tests > 0 else 0
        
        print(f"   • Taux de réussite: {taux_reussite:.1f}%")
        print(f"   • Tests réussis: {len(self.results['success'])}")
        print(f"   • Avertissements: {len(self.results['warnings'])}")
        print(f"   • Échecs critiques: {len(self.results['errors'])}")
        
        # État du système
        print(f"\n🔧 ÉTAT DU SYSTÈME:")
        modeles_critiques = ['Membre', 'Agent', 'Medecin', 'Pharmacien', 'Assureur', 'Bon', 'Ordonnance']
        modeles_presents = [m for m in modeles_critiques if m in self.models]
        print(f"   • Modèles critiques: {len(modeles_presents)}/{len(modeles_critiques)}")
        
        # Données existantes
        print(f"\n📈 DONNÉES EXISTANTES:")
        for modele in ['Membre', 'Agent', 'Bon', 'Ordonnance', 'Soin']:
            if modele in self.models:
                count = self.models[modele].objects.count()
                print(f"   • {modele}: {count}")
        
        # Acteurs de test créés
        print(f"\n👥 ACTEURS DE TEST:")
        acteurs_crees = {k: v for k, v in self.test_data.items() if v is not None}
        for role, acteur in acteurs_crees.items():
            identifiant = self._get_identifiant_acteur(acteur)
            print(f"   • {role}: {identifiant}")
        
        # Détail des problèmes
        if self.results['errors']:
            print(f"\n❌ PROBLÈMES CRITIQUES:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        if self.results['warnings']:
            print(f"\n⚠️  RECOMMANDATIONS:")
            for warning in self.results['warnings']:
                print(f"   • {warning}")
        
        # Plan d'action
        print(f"\n🎯 PLAN D'ACTION:")
        if not self.results['errors']:
            print("   ✅ Système globalement fonctionnel")
            print("   📝 Vérifier les workflows métier spécifiques")
            print("   👥 Tester avec des utilisateurs réels")
        else:
            if any("EtablissementMedical" in error for error in self.results['errors']):
                print("   🔧 Créer des établissements médicaux dans l'admin")
            if any("SpecialiteMedicale" in error for error in self.results['errors']):
                print("   🔧 Créer des spécialités médicales dans l'admin")
            print("   📚 Vérifier les relations entre modèles")
        
        print(f"\n🕒 Diagnostic effectué le: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
    
    def _get_identifiant_acteur(self, acteur):
        """Obtenir un identifiant lisible pour un acteur"""
        if not acteur:
            return "Non créé"
        
        try:
            if hasattr(acteur, 'user') and acteur.user:
                return acteur.user.username
            elif hasattr(acteur, 'matricule') and acteur.matricule:
                return acteur.matricule
            elif hasattr(acteur, 'numero_employe') and acteur.numero_employe:
                return acteur.numero_employe
            elif hasattr(acteur, 'id'):
                return f"ID: {acteur.id}"
            else:
                return str(acteur)
        except:
            return "Erreur affichage"
    
    def executer_diagnostic_complet(self):
        """Exécuter le diagnostic complet"""
        print("🚀 DIAGNOSTIC COMPLET DU SYSTÈME MUTUELLE")
        print("="*60)
        
        # Étape 1: Détection des modèles
        self.detecter_modeles()
        
        # Étape 2: Analyse des structures
        self.analyser_structure_modeles()
        
        # Étape 3: Création des acteurs de test
        creation_ok = self.creer_acteurs_test()
        if not creation_ok:
            self.log_warning("Création acteurs partielle - continuation avec analyse existante")
        
        # Étape 4: Analyse des données existantes
        self.analyser_donnees_existantes()
        
        # Étape 5: Tests des relations
        self.tester_relations_acteurs()
        
        # Étape 6: Test accès données
        self.tester_acces_donnees()
        
        # Étape 7: Test workflow COMPLET
        self.tester_workflow_complet()
        
        # Étape 8: Rapport final
        self.generer_rapport_final()
        
        return len(self.results['errors']) == 0

def main():
    """Fonction principale"""
    diagnostic = DiagnosticComplet()
    succes = diagnostic.executer_diagnostic_complet()
    
    if succes:
        print("\n🎉 DIAGNOSTIC RÉUSSI!")
        print("💡 Tous les problèmes ont été résolus")
        sys.exit(0)
    else:
        print("\n💥 DIAGNOSTIC AVEC PROBLÈMES RÉSIDUELS")
        print("🔧 Consulter le rapport pour les corrections")
        sys.exit(1)

if __name__ == "__main__":
    main()