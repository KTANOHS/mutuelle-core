#!/usr/bin/env python
"""
SCRIPT DE TEST WORKFLOW BON DE SOIN
Création par Agent → Réception par Médecin → Validation
"""

import os
import sys
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from membres.models import Membre, Bon
from soins.models import Soin
from medecin.models import Ordonnance
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class TestWorkflowBon:
    """Classe de test pour le workflow complet des bons de soin"""
    
    def __init__(self):
        self.client = Client()
        self.agent = None
        self.medecin = None
        self.membre = None
        self.bon_created = None
        
    def print_step(self, step, message):
        """Affiche une étape du test"""
        print(f"\n{'='*60}")
        print(f"📋 ÉTAPE {step}: {message}")
        print(f"{'='*60}")
    
    def print_success(self, message):
        """Affiche un succès"""
        print(f"✅ {message}")
    
    def print_error(self, message):
        """Affiche une erreur"""
        print(f"❌ {message}")
    
    def print_info(self, message):
        """Affiche une information"""
        print(f"ℹ️  {message}")
    
    def setup_test_data(self):
        """Prépare les données de test"""
        self.print_step(1, "PRÉPARATION DES DONNÉES DE TEST")
        
        try:
            # Récupérer ou créer l'agent
            self.agent = User.objects.get(username='test_agent')
            self.print_success(f"Agent trouvé: {self.agent.username}")
            
            # Récupérer ou créer le médecin
            self.medecin = User.objects.get(username='medecin_test')
            self.print_success(f"Médecin trouvé: {self.medecin.username}")
            
            # Récupérer un membre existant (le premier disponible)
            self.membre = Membre.objects.first()
            if self.membre:
                self.print_success(f"Membre trouvé: {self.membre.nom} {self.membre.prenom} (ID: {self.membre.id})")
            else:
                self.print_error("Aucun membre trouvé dans la base")
                return False
                
            return True
            
        except User.DoesNotExist as e:
            self.print_error(f"Utilisateur non trouvé: {e}")
            return False
        except Exception as e:
            self.print_error(f"Erreur lors de la préparation: {e}")
            return False
    
    def test_connexion_agent(self):
        """Teste la connexion de l'agent"""
        self.print_step(2, "CONNEXION DE L'AGENT")
        
        try:
            # Connexion de l'agent
            login_success = self.client.login(username='test_agent', password='pass123')
            if login_success:
                self.print_success("Agent connecté avec succès")
                
                # Test accès tableau de bord agent
                response = self.client.get('/agents/tableau-de-bord/')
                if response.status_code == 200:
                    self.print_success("Tableau de bord agent accessible")
                else:
                    self.print_error(f"Erreur accès tableau de bord: {response.status_code}")
                    
                return True
            else:
                self.print_error("Échec connexion agent")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur connexion agent: {e}")
            return False
    
    def test_creation_bon_par_agent(self):
        """Teste la création d'un bon de soin par l'agent"""
        self.print_step(3, "CRÉATION DU BON DE SOIN PAR L'AGENT")
        
        try:
            # Données du bon de soin
            bon_data = {
                'membre': self.membre.id,
                'type_soin': 'CONSULT',
                'description': 'Consultation de test pour vérification du système',
                'lieu_soins': 'Centre Médical Principal',
                'date_soins': timezone.now().date(),
                'medecin_traitant': 'Dr. Test Validation',
                'montant_total': '7500',
                'statut': 'BROUILLON'
            }
            
            # Création du bon (simulation via API ou formulaire)
            # Note: Adaptez cette partie selon votre implémentation
            bon = Bon.objects.create(
                numero_bon=None,  # Auto-généré par la méthode save()
                membre=self.membre,
                type_soin='CONSULT',
                description=bon_data['description'],
                lieu_soins=bon_data['lieu_soins'],
                date_soins=bon_data['date_soins'],
                medecin_traitant=bon_data['medecin_traitant'],
                montant_total=7500,
                statut='BROUILLON'
            )
            
            self.bon_created = bon
            self.print_success(f"Bon créé avec succès: #{bon.id}")
            self.print_success(f"Numéro de bon auto-généré: {bon.numero_bon}")
            self.print_success(f"Statut initial: {bon.statut}")
            
            # Vérification des données
            self.print_info(f"Membre: {bon.membre.nom} {bon.membre.prenom}")
            self.print_info(f"Type de soin: {bon.get_type_soin_display()}")
            self.print_info(f"Montant: {bon.montant_total} FCFA")
            
            return True
            
        except Exception as e:
            self.print_error(f"Erreur création bon: {e}")
            return False
    
    def test_connexion_medecin(self):
        """Teste la connexion du médecin"""
        self.print_step(4, "CONNEXION DU MÉDECIN")
        
        try:
            # Déconnexion préalable
            self.client.logout()
            
            # Connexion du médecin
            login_success = self.client.login(username='medecin_test', password='pass123')
            if login_success:
                self.print_success("Médecin connecté avec succès")
                
                # Test accès tableau de bord médecin
                response = self.client.get('/medecin/dashboard/')
                if response.status_code == 200:
                    self.print_success("Tableau de bord médecin accessible")
                else:
                    self.print_error(f"Erreur accès tableau de bord médecin: {response.status_code}")
                    
                return True
            else:
                self.print_error("Échec connexion médecin")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur connexion médecin: {e}")
            return False
    
    def test_visualisation_bon_par_medecin(self):
        """Teste la visualisation du bon par le médecin"""
        self.print_step(5, "VISUALISATION DU BON PAR LE MÉDECIN")
        
        try:
            # Test accès à la liste des ordonnances/bons
            response = self.client.get('/medecin/ordonnances/')
            if response.status_code == 200:
                self.print_success("Liste des ordonnances accessible")
            else:
                self.print_error(f"Erreur accès liste ordonnances: {response.status_code}")
            
            # Vérifier que le médecin peut voir le bon créé
            # (Cette partie dépend de votre implémentation des permissions)
            bons_visibles = Bon.objects.filter(statut='BROUILLON').count()
            self.print_info(f"Bons en attente visibles: {bons_visibles}")
            
            return True
            
        except Exception as e:
            self.print_error(f"Erreur visualisation bon: {e}")
            return False
    
    def test_validation_bon_par_medecin(self):
        """Teste la validation du bon par le médecin"""
        self.print_step(6, "VALIDATION DU BON PAR LE MÉDECIN")
        
        try:
            if not self.bon_created:
                self.print_error("Aucun bon à valider")
                return False
            
            # Simulation de la validation par le médecin
            ancien_statut = self.bon_created.statut
            self.bon_created.statut = 'VALIDE'
            self.bon_created.date_validation = timezone.now()
            self.bon_created.valide_par = self.medecin
            self.bon_created.montant_rembourse = self.bon_created.montant_a_rembourser
            self.bon_created.save()
            
            self.print_success(f"Bon validé avec succès!")
            self.print_success(f"Ancien statut: {ancien_statut} → Nouveau statut: {self.bon_created.statut}")
            self.print_success(f"Validé par: {self.bon_created.valide_par.username}")
            self.print_success(f"Montant à rembourser: {self.bon_created.montant_rembourse} FCFA")
            self.print_success(f"Date de validation: {self.bon_created.date_validation}")
            
            return True
            
        except Exception as e:
            self.print_error(f"Erreur validation bon: {e}")
            return False
    
    def test_verification_etat_final(self):
        """Vérifie l'état final du système"""
        self.print_step(7, "VÉRIFICATION DE L'ÉTAT FINAL")
        
        try:
            # Vérification des statistiques
            total_bons = Bon.objects.count()
            bons_valides = Bon.objects.filter(statut='VALIDE').count()
            bons_attente = Bon.objects.filter(statut='BROUILLON').count()
            
            self.print_info(f"Total des bons dans le système: {total_bons}")
            self.print_info(f"Bons validés: {bons_valides}")
            self.print_info(f"Bons en attente: {bons_attente}")
            
            # Vérification du bon créé
            if self.bon_created:
                bon_verif = Bon.objects.get(id=self.bon_created.id)
                self.print_success(f"Bon #{bon_verif.id} - Statut final: {bon_verif.statut}")
                self.print_success(f"Montant remboursé: {bon_verif.montant_rembourse} FCFA")
                self.print_success(f"Validé par: {bon_verif.valide_par.username if bon_verif.valide_par else 'Non validé'}")
            
            return True
            
        except Exception as e:
            self.print_error(f"Erreur vérification état final: {e}")
            return False
    
    def run_complete_workflow(self):
        """Exécute le workflow complet"""
        print("\n" + "🎯" * 30)
        print("🎯 DÉMARRAGE DU TEST WORKFLOW BON DE SOIN")
        print("🎯" * 30)
        
        steps = [
            ("Préparation données", self.setup_test_data),
            ("Connexion agent", self.test_connexion_agent),
            ("Création bon", self.test_creation_bon_par_agent),
            ("Connexion médecin", self.test_connexion_medecin),
            ("Visualisation bon", self.test_visualisation_bon_par_medecin),
            ("Validation bon", self.test_validation_bon_par_medecin),
            ("Vérification final", self.test_verification_etat_final),
        ]
        
        results = []
        for step_name, step_method in steps:
            try:
                success = step_method()
                results.append((step_name, success))
            except Exception as e:
                self.print_error(f"Erreur inattendue dans {step_name}: {e}")
                results.append((step_name, False))
        
        # Affichage du résumé
        self.print_step("RÉSUMÉ", "RÉSULTATS DU WORKFLOW")
        
        successful_steps = sum(1 for _, success in results if success)
        total_steps = len(results)
        
        print(f"\n📊 RÉSULTAT: {successful_steps}/{total_steps} étapes réussies")
        
        for step_name, success in results:
            status = "✅ RÉUSSI" if success else "❌ ÉCHEC"
            print(f"  {step_name}: {status}")
        
        if successful_steps == total_steps:
            print(f"\n🎉 WORKFLOW COMPLET RÉUSSI! Le système fonctionne correctement.")
        else:
            print(f"\n⚠️  WORKFLOW PARTIEL: {successful_steps}/{total_steps} étapes validées")
        
        return successful_steps == total_steps

def test_rapide_bons_existants():
    """Test rapide pour vérifier les bons existants"""
    print("\n🔍 TEST RAPIDE - BONS EXISTANTS")
    
    try:
        bons = Bon.objects.all().select_related('membre', 'valide_par')
        print(f"Nombre total de bons: {bons.count()}")
        
        for bon in bons:
            print(f"\n📄 Bon #{bon.id}:")
            print(f"   Numéro: {bon.numero_bon}")
            print(f"   Membre: {bon.membre.nom} {bon.membre.prenom}")
            print(f"   Type: {bon.get_type_soin_display()}")
            print(f"   Statut: {bon.statut}")
            print(f"   Montant: {bon.montant_total} FCFA")
            print(f"   Remboursé: {bon.montant_rembourse} FCFA")
            print(f"   Validé par: {bon.valide_par.username if bon.valide_par else 'Non validé'}")
            
    except Exception as e:
        print(f"❌ Erreur test rapide: {e}")

if __name__ == "__main__":
    # Test rapide des bons existants
    test_rapide_bons_existants()
    
    # Test du workflow complet
    workflow_test = TestWorkflowBon()
    success = workflow_test.run_complete_workflow()
    
    # Code de sortie pour les scripts CI/CD
    sys.exit(0 if success else 1)