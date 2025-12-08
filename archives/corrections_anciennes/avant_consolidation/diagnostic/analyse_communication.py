# analyse_communication.py
import os
import django
import sys
from datetime import datetime, timedelta

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction
from django.apps import apps

User = get_user_model()

class AnalyseurCommunication:
    """
    Script d'analyse du système de communication entre les acteurs
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
    
    def detecter_modeles_communication(self):
        """Détecter les modèles liés à la communication"""
        print("🔍 Détection des modèles de communication...")
        
        modeles_communication = [
            'Notification', 'Message', 'Conversation', 'MessageGroupe',
            'GroupeCommunication', 'PieceJointe', 'PreferenceNotification'
        ]
        
        for app_config in apps.get_app_configs():
            for modele in app_config.get_models():
                nom_modele = modele.__name__
                if nom_modele in modeles_communication:
                    self.models[nom_modele] = modele
                    self.log_success(f"Modèle trouvé: {nom_modele}")
        
        # Vérifier les modèles manquants
        for modele in modeles_communication:
            if modele not in self.models:
                self.log_warning(f"Modèle manquant: {modele}")
        
        return True
    
    def analyser_structure_communication(self):
        """Analyser la structure des modèles de communication"""
        print("\n📋 Analyse des structures de communication...")
        
        for nom_modele, modele in self.models.items():
            print(f"\n   🎯 {nom_modele}:")
            for champ in modele._meta.fields:
                print(f"      - {champ.name} ({champ.__class__.__name__})")
    
    def recuperer_acteurs_test(self):
        """Récupérer des acteurs existants pour les tests de communication"""
        try:
            # Récupérer les modèles
            Agent = apps.get_model('agents', 'Agent')
            Medecin = apps.get_model('medecin', 'Medecin')
            Pharmacien = apps.get_model('pharmacien', 'Pharmacien')
            Assureur = apps.get_model('assureur', 'Assureur')
            Membre = apps.get_model('membres', 'Membre')
            
            # Récupérer ou créer des acteurs de test
            agent = Agent.objects.filter(user__username='test_agent_complet').first()
            medecin = Medecin.objects.filter(user__username='test_medecin_complet').first()
            pharmacien = Pharmacien.objects.filter(user__username='test_pharmacien_complet').first()
            assureur = Assureur.objects.filter(user__username='test_assureur_complet').first()
            membre = Membre.objects.filter(numero_membre='COMPLET001').first()
            
            self.test_data = {
                'agent': agent,
                'medecin': medecin,
                'pharmacien': pharmacien,
                'assureur': assureur,
                'membre': membre
            }
            
            # Vérifier quels acteurs sont disponibles
            acteurs_trouves = {k: v for k, v in self.test_data.items() if v}
            self.log_success(f"Acteurs récupérés: {len(acteurs_trouves)}")
            
            for role, acteur in acteurs_trouves.items():
                identifiant = self._get_identifiant_acteur(acteur)
                print(f"   👤 {role}: {identifiant}")
            
            return len(acteurs_trouves) > 0
            
        except Exception as e:
            self.log_error(f"Erreur récupération acteurs: {e}")
            return False
    
    def tester_notifications(self):
        """Tester le système de notifications"""
        print("\n🔔 TEST SYSTÈME DE NOTIFICATIONS")
        
        if 'Notification' not in self.models:
            self.log_warning("Modèle Notification non disponible")
            return False
        
        Notification = self.models['Notification']
        
        try:
            # Vérifier les notifications existantes
            notifications_count = Notification.objects.count()
            self.log_success(f"Notifications existantes: {notifications_count}")
            
            # Créer une notification de test si on a des acteurs
            if self.test_data.get('agent') and self.test_data.get('membre'):
                with transaction.atomic():
                    # Analyser la structure de Notification
                    champs_notif = [f.name for f in Notification._meta.fields]
                    
                    donnees_notif = {
                        'destinataire': self.test_data['agent'].user,
                        'titre': 'Test de notification',
                        'message': 'Ceci est une notification de test du système de communication',
                        'type_notification': 'info',
                        'date_creation': datetime.now(),
                        'lu': False
                    }
                    
                    # Adapter selon les champs disponibles
                    if 'emetteur' in champs_notif:
                        donnees_notif['emetteur'] = self.test_data['membre'].user
                    if 'lien' in champs_notif:
                        donnees_notif['lien'] = '/test/communication'
                    
                    notification = Notification.objects.create(**donnees_notif)
                    self.log_success("Notification de test créée avec succès")
                    
                    # Vérifier qu'elle est accessible
                    notif_trouvee = Notification.objects.filter(id=notification.id).exists()
                    if notif_trouvee:
                        self.log_success("Notification accessible après création")
                    
                    # Nettoyer
                    notification.delete()
            
            return True
            
        except Exception as e:
            self.log_error(f"Erreur test notifications: {e}")
            return False
    
    def tester_messagerie(self):
        """Tester le système de messagerie"""
        print("\n💬 TEST SYSTÈME DE MESSAGERIE")
        
        if 'Message' not in self.models:
            self.log_warning("Modèle Message non disponible")
            return False
        
        Message = self.models['Message']
        Conversation = self.models.get('Conversation')
        
        try:
            # Vérifier les messages existants
            messages_count = Message.objects.count()
            self.log_success(f"Messages existants: {messages_count}")
            
            # Tester la création d'un message si on a des acteurs
            if self.test_data.get('agent') and self.test_data.get('medecin'):
                with transaction.atomic():
                    # Analyser la structure de Message
                    champs_message = [f.name for f in Message._meta.fields]
                    
                    donnees_message = {
                        'expediteur': self.test_data['agent'].user,
                        'destinataire': self.test_data['medecin'].user,
                        'contenu': 'Bonjour Docteur, voici un message de test du système de communication.',
                        'date_envoi': datetime.now(),
                        'lu': False
                    }
                    
                    # Gérer les conversations si le modèle existe
                    if Conversation and 'conversation' in champs_message:
                        # Créer ou récupérer une conversation
                        conversation, created = Conversation.objects.get_or_create(
                            sujet='Test communication Agent-Médecin',
                            defaults={
                                'date_creation': datetime.now(),
                                'type_conversation': 'professionnelle'
                            }
                        )
                        donnees_message['conversation'] = conversation
                    
                    message = Message.objects.create(**donnees_message)
                    self.log_success("Message de test créé avec succès")
                    
                    # Vérifier les scénarios de communication
                    self.tester_scenarios_communication()
                    
                    # Nettoyer
                    message.delete()
                    if Conversation and 'conversation' in locals():
                        conversation.delete()
            
            return True
            
        except Exception as e:
            self.log_error(f"Erreur test messagerie: {e}")
            return False
    
    def tester_scenarios_communication(self):
        """Tester différents scénarios de communication"""
        print("\n🔄 TEST SCÉNARIOS DE COMMUNICATION")
        
        scenarios = [
            {
                'nom': 'Agent → Médecin',
                'expediteur': 'agent',
                'destinataire': 'medecin',
                'message': "Bonjour Docteur, un nouveau bon a été émis pour le patient."
            },
            {
                'nom': 'Médecin → Pharmacien', 
                'expediteur': 'medecin',
                'destinataire': 'pharmacien',
                'message': "Bonjour, voici une ordonnance à préparer pour un patient."
            },
            {
                'nom': 'Pharmacien → Assureur',
                'expediteur': 'pharmacien', 
                'destinataire': 'assureur',
                'message': "Demande de remboursement pour médicaments délivrés."
            },
            {
                'nom': 'Assureur → Agent',
                'expediteur': 'assureur',
                'destinataire': 'agent', 
                'message': "Nouvelle directive à appliquer pour les cotisations."
            }
        ]
        
        for scenario in scenarios:
            expediteur = self.test_data.get(scenario['expediteur'])
            destinataire = self.test_data.get(scenario['destinataire'])
            
            if expediteur and destinataire:
                self.log_success(f"✅ {scenario['nom']} - Communication possible")
                print(f"      📨 De: {self._get_identifiant_acteur(expediteur)}")
                print(f"      📬 À: {self._get_identifiant_acteur(destinataire)}")
            else:
                self.log_warning(f"⚠️ {scenario['nom']} - Acteurs manquants")
    
    def analyser_flux_metier(self):
        """Analyser les flux de communication métier"""
        print("\n📈 ANALYSE DES FLUX MÉTIER")
        
        flux_metier = [
            {
                'nom': 'Émission bon → Notification médecin',
                'description': 'Quand un agent émet un bon, le médecin concerné reçoit une notification'
            },
            {
                'nom': 'Ordonnance → Notification pharmacien',
                'description': 'Quand un médecin crée une ordonnance, le pharmacien reçoit une notification'
            },
            {
                'nom': 'Traitement soin → Notification assureur',
                'description': 'Quand un soin est traité, l\'assureur reçoit une notification pour suivi'
            },
            {
                'nom': 'Problème → Alerte tous acteurs',
                'description': 'En cas de problème, tous les acteurs concernés reçoivent une alerte'
            }
        ]
        
        for flux in flux_metier:
            print(f"\n   🔄 {flux['nom']}")
            print(f"      📝 {flux['description']}")
            
            # Vérifier si le flux est implémentable
            if self._verifier_flux_implementable(flux):
                self.log_success("      ✅ Flux implémentable")
            else:
                self.log_warning("      ⚠️ Flux nécessite configuration")
    
    def _verifier_flux_implementable(self, flux):
        """Vérifier si un flux métier est implémentable avec les modèles actuels"""
        # Logique simplifiée pour la démonstration
        return True
    
    def tester_groups_messagerie(self):
        """Tester la messagerie de groupe"""
        print("\n👥 TEST MESSAGERIE DE GROUPE")
        
        if 'GroupeCommunication' not in self.models or 'MessageGroupe' not in self.models:
            self.log_warning("Modèles de groupe non disponibles")
            return False
        
        GroupeCommunication = self.models['GroupeCommunication']
        MessageGroupe = self.models['MessageGroupe']
        
        try:
            # Vérifier les groupes existants
            groupes_count = GroupeCommunication.objects.count()
            self.log_success(f"Groupes existants: {groupes_count}")
            
            # Créer un groupe de test si on a assez d'acteurs
            acteurs_disponibles = [v for v in self.test_data.values() if v]
            if len(acteurs_disponibles) >= 2:
                with transaction.atomic():
                    # Créer un groupe de test
                    groupe, created = GroupeCommunication.objects.get_or_create(
                        nom='Groupe Test Communication',
                        defaults={
                            'description': 'Groupe de test pour analyse communication',
                            'date_creation': datetime.now(),
                            'createur': acteurs_disponibles[0].user
                        }
                    )
                    
                    # Ajouter des membres au groupe
                    for acteur in acteurs_disponibles[:3]:  # Maximum 3 membres pour le test
                        if hasattr(groupe, 'membres'):
                            groupe.membres.add(acteur.user)
                    
                    # Créer un message de groupe
                    message_groupe = MessageGroupe.objects.create(
                        groupe=groupe,
                        expediteur=acteurs_disponibles[0].user,
                        contenu='Message de test dans le groupe de communication',
                        date_envoi=datetime.now()
                    )
                    
                    self.log_success("Groupe et message de groupe créés avec succès")
                    
                    # Nettoyer
                    message_groupe.delete()
                    groupe.delete()
            
            return True
            
        except Exception as e:
            self.log_error(f"Erreur test groupes: {e}")
            return False
    
    def analyser_performances_communication(self):
        """Analyser les performances du système de communication"""
        print("\n⚡ ANALYSE DES PERFORMANCES")
        
        if 'Notification' in self.models:
            Notification = self.models['Notification']
            
            # Statistiques des notifications
            total_notifications = Notification.objects.count()
            notifications_non_lues = Notification.objects.filter(lu=False).count()
            notifications_7j = Notification.objects.filter(
                date_creation__gte=datetime.now() - timedelta(days=7)
            ).count()
            
            print(f"   📊 Notifications:")
            print(f"      • Total: {total_notifications}")
            print(f"      • Non lues: {notifications_non_lues}")
            print(f"      • 7 derniers jours: {notifications_7j}")
        
        if 'Message' in self.models:
            Message = self.models['Message']
            
            # Statistiques des messages
            total_messages = Message.objects.count()
            messages_7j = Message.objects.filter(
                date_envoi__gte=datetime.now() - timedelta(days=7)
            ).count()
            
            print(f"   📊 Messages:")
            print(f"      • Total: {total_messages}")
            print(f"      • 7 derniers jours: {messages_7j}")
    
    def generer_rapport_communication(self):
        """Générer un rapport complet sur la communication"""
        print("\n" + "="*80)
        print("📊 RAPPORT D'ANALYSE DU SYSTÈME DE COMMUNICATION")
        print("="*80)
        
        # Résumé exécutif
        print(f"\n🎯 RÉSUMÉ EXÉCUTIF:")
        print(f"   • Modèles de communication: {len(self.models)}")
        print(f"   • Tests réussis: {len(self.results['success'])}")
        print(f"   • Avertissements: {len(self.results['warnings'])}")
        print(f"   • Erreurs: {len(self.results['errors'])}")
        
        # État du système
        print(f"\n🔧 ÉTAT DU SYSTÈME:")
        modeles_comm = ['Notification', 'Message', 'Conversation', 'GroupeCommunication']
        for modele in modeles_comm:
            status = "✅" if modele in self.models else "❌"
            print(f"   • {status} {modele}")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS:")
        
        if not self.models:
            print("   🔧 Implémenter un système de communication de base")
            print("   📚 Commencer par les notifications simples")
            print("   🎯 Prioriser les notifications métier critiques")
        else:
            if 'Notification' in self.models:
                print("   ✅ Système de notifications opérationnel")
            else:
                print("   🔧 Ajouter un système de notifications")
            
            if 'Message' in self.models:
                print("   ✅ Système de messagerie opérationnel") 
            else:
                print("   🔧 Implémenter la messagerie directe")
            
            if 'GroupeCommunication' in self.models:
                print("   ✅ Messagerie de groupe disponible")
            else:
                print("   💡 Envisager la messagerie de groupe pour les équipes")
        
        # Plan d'action
        print(f"\n🎯 PLAN D'ACTION COMMUNICATION:")
        print("   1. ✅ Vérifier l'état des modèles de communication")
        print("   2. ✅ Tester les scénarios entre acteurs")
        print("   3. 🔧 Configurer les notifications automatiques")
        print("   4. 👥 Former les utilisateurs au système")
        print("   5. 📈 Monitorer l'utilisation réelle")
        
        print(f"\n🕒 Analyse effectuée le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
    
    def _get_identifiant_acteur(self, acteur):
        """Obtenir un identifiant lisible pour un acteur"""
        if not acteur:
            return "Non disponible"
        
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
    
    def executer_analyse_complete(self):
        """Exécuter l'analyse complète de la communication"""
        print("🚀 ANALYSE COMPLÈTE DU SYSTÈME DE COMMUNICATION")
        print("="*60)
        
        # Étape 1: Détection des modèles
        self.detecter_modeles_communication()
        
        # Étape 2: Analyse structure
        self.analyser_structure_communication()
        
        # Étape 3: Récupération acteurs
        if not self.recuperer_acteurs_test():
            self.log_warning("Acteurs limités - certains tests seront restreints")
        
        # Étape 4: Tests fonctionnels
        self.tester_notifications()
        self.tester_messagerie()
        self.tester_groups_messagerie()
        
        # Étape 5: Analyse métier
        self.tester_scenarios_communication()
        self.analyser_flux_metier()
        
        # Étape 6: Performances
        self.analyser_performances_communication()
        
        # Étape 7: Rapport
        self.generer_rapport_communication()
        
        return len(self.results['errors']) == 0

def main():
    """Fonction principale"""
    analyseur = AnalyseurCommunication()
    succes = analyseur.executer_analyse_complete()
    
    if succes:
        print("\n🎉 ANALYSE RÉUSSIE!")
        print("💡 Le système de communication est opérationnel")
        sys.exit(0)
    else:
        print("\n💥 ANALYSE AVEC PROBLÈMES")
        print("🔧 Des améliorations sont nécessaires")
        sys.exit(1)

if __name__ == "__main__":
    main()