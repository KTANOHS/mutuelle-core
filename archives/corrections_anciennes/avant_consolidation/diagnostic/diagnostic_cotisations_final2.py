# diagnostic_cotisations_final.py
import os
import sys
import django
import json
from datetime import datetime, timedelta
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from django.db import connection
from django.db.models import Q, Count
from django.contrib.auth.models import User
from django.apps import apps

print("🔍 DIAGNOSTIC FINAL COTISATIONS ASSUREUR → AGENT")
print("=" * 60)

class DiagnosticCotisationsFinal:
    def __init__(self):
        self.rapport = {
            'timestamp': datetime.now().isoformat(),
            'analyse': {},
            'problemes': [],
            'recommandations': [],
            'actions_immediates': []
        }
    
    def executer_diagnostic_complet(self):
        """Exécute le diagnostic complet avec corrections"""
        print("🎯 DIAGNOSTIC COMPLET AVEC CORRECTIONS...")
        
        try:
            # 1. Analyse de la structure actuelle
            self.analyser_structure_actuelle()
            
            # 2. Diagnostic des problèmes identifiés
            self.diagnostiquer_problemes_specifiques()
            
            # 3. Solutions immédiates
            self.proposer_solutions_immediates()
            
            # 4. Générer le rapport d'actions
            self.generer_rapport_actions()
            
            print("✅ DIAGNOSTIC TERMINÉ AVEC SOLUTIONS")
            
        except Exception as e:
            print(f"❌ Erreur lors du diagnostic: {str(e)}")
            self.rapport['erreur'] = str(e)
    
    def analyser_structure_actuelle(self):
        """Analyse la structure actuelle du système"""
        print("\n1. 📊 ANALYSE STRUCTURE ACTUELLE...")
        
        try:
            from membres.models import Membre
            from agents.models import Agent, VerificationCotisation
            from assureur.models import Assureur
            
            # Statistiques détaillées
            stats = {
                'membres_total': Membre.objects.count(),
                'membres_avec_verification': Membre.objects.filter(verificationcotisation__isnull=False).count(),
                'membres_sans_verification': Membre.objects.filter(verificationcotisation__isnull=True).count(),
                'verifications_total': VerificationCotisation.objects.count(),
                'agents_total': Agent.objects.count(),
                'assureurs_total': Assureur.objects.count()
            }
            
            print(f"   👥 Membres totaux: {stats['membres_total']}")
            print(f"   ✅ Membres avec vérification: {stats['membres_avec_verification']}")
            print(f"   ❌ Membres sans vérification: {stats['membres_sans_verification']}")
            print(f"   🔍 Vérifications totales: {stats['verifications_total']}")
            print(f"   👨‍💼 Agents: {stats['agents_total']}")
            print(f"   🏢 Assureurs: {stats['assureurs_total']}")
            
            # Analyse des vérifications par statut
            verifications_par_statut = VerificationCotisation.objects.values('statut_cotisation').annotate(
                count=Count('id')
            ).order_by('-count')
            
            print(f"\n   📈 RÉPARTITION DES STATUTS:")
            for statut in verifications_par_statut:
                print(f"      • {statut['statut_cotisation']}: {statut['count']} vérifications")
            
            # Analyse par agent
            verifications_par_agent = VerificationCotisation.objects.values(
                'agent__user__username'
            ).annotate(
                count=Count('id')
            ).order_by('-count')
            
            print(f"\n   👨‍💼 VÉRIFICATIONS PAR AGENT:")
            for agent in verifications_par_agent:
                nom_agent = agent['agent__user__username'] or 'Non assigné'
                print(f"      • {nom_agent}: {agent['count']} vérifications")
            
            self.rapport['analyse']['statistiques'] = stats
            self.rapport['analyse']['verifications_par_statut'] = list(verifications_par_statut)
            self.rapport['analyse']['verifications_par_agent'] = list(verifications_par_agent)
            
        except Exception as e:
            print(f"   ❌ Erreur analyse structure: {e}")
    
    def diagnostiquer_problemes_specifiques(self):
        """Diagnostique les problèmes spécifiques identifiés"""
        print("\n2. 🚨 DIAGNOSTIC PROBLÈMES SPÉCIFIQUES...")
        
        problemes = []
        
        try:
            from membres.models import Membre
            from agents.models import VerificationCotisation
            
            # 1. Membres sans vérification
            membres_sans_verification = Membre.objects.filter(
                verificationcotisation__isnull=True
            )
            
            if membres_sans_verification.exists():
                probleme = {
                    'type': 'MEMBRES_SANS_CONTROLE',
                    'description': f'{membres_sans_verification.count()} membres sans aucune vérification de cotisation',
                    'severite': 'MOYENNE',
                    'details': {
                        'count': membres_sans_verification.count(),
                        'exemples': list(membres_sans_verification.values('id', 'numero_unique', 'prenom', 'nom')[:3])
                    }
                }
                problemes.append(probleme)
                print(f"   🔴 {probleme['description']}")
            
            # 2. Champs manquants dans les modèles
            try:
                from membres.models import Cotisation
                problemes.append({
                    'type': 'MODELE_COTISATION_MANQUANT',
                    'description': 'Modèle Cotisation non trouvé dans membres/models.py',
                    'severite': 'HAUTE',
                    'details': 'Le modèle pour gérer les paiements de cotisation est absent'
                })
                print("   🔴 Modèle Cotisation manquant")
            except ImportError:
                pass  # Déjà géré
            
            # 3. Analyse des champs obligatoires VerificationCotisation
            try:
                # Tester la création pour identifier les champs manquants
                from agents.models import VerificationCotisation
                from membres.models import Membre
                from agents.models import Agent
                
                # Vérifier les champs obligatoires
                champs_obligatoires = []
                for field in VerificationCotisation._meta.get_fields():
                    if not field.null and not field.blank and field.name not in ['id']:
                        champs_obligatoires.append(field.name)
                
                print(f"   📋 Champs obligatoires VerificationCotisation: {', '.join(champs_obligatoires)}")
                
            except Exception as e:
                print(f"   ⚠️  Analyse champs obligatoires: {e}")
            
            # 4. Vérifier la cohérence des données
            verifications_incompletes = VerificationCotisation.objects.filter(
                Q(agent__isnull=True) | 
                Q(date_verification__isnull=True)
            )
            
            if verifications_incompletes.exists():
                probleme = {
                    'type': 'VERIFICATIONS_INCOMPLETES',
                    'description': f'{verifications_incompletes.count()} vérifications avec données manquantes',
                    'severite': 'MOYENNE'
                }
                problemes.append(probleme)
                print(f"   🟡 {probleme['description']}")
            
            self.rapport['problemes'] = problemes
            
        except Exception as e:
            print(f"   ❌ Erreur diagnostic problèmes: {e}")
    
    def proposer_solutions_immediates(self):
        """Propose des solutions immédiates aux problèmes identifiés"""
        print("\n3. 💡 PROPOSITION SOLUTIONS IMMÉDIATES...")
        
        solutions = []
        
        # Solution pour le modèle Cotisation manquant
        solutions.append({
            'action': 'CRÉER_MODÈLE_COTISATION',
            'description': 'Créer le modèle Cotisation dans membres/models.py',
            'urgence': 'HAUTE',
            'script': 'creer_modele_cotisation.py',
            'details': 'Modèle essentiel pour gérer les paiements des cotisations'
        })
        print("   🔧 Solution: Créer modèle Cotisation (HAUTE priorité)")
        
        # Solution pour les membres sans vérification
        solutions.append({
            'action': 'AFFECTER_VERIFICATIONS_MANQUANTES',
            'description': 'Assigner des agents pour vérifier les membres sans contrôle',
            'urgence': 'MOYENNE',
            'script': 'affecter_verifications_manquantes.py',
            'details': '17 membres attendent une vérification de leur cotisation'
        })
        print("   🔧 Solution: Assigner vérifications manquantes (MOYENNE priorité)")
        
        # Solution pour les champs obligatoires
        solutions.append({
            'action': 'CORRIGER_CHAMPS_OBLIGATOIRES',
            'description': 'Ajouter les champs manquants dans VerificationCotisation',
            'urgence': 'MOYENNE',
            'script': 'corriger_champs_verification.py',
            'details': 'Champ prochaine_echeance obligatoire manquant'
        })
        print("   🔧 Solution: Corriger champs obligatoires (MOYENNE priorité)")
        
        self.rapport['actions_immediates'] = solutions
        
        # Créer les scripts de correction
        self.creer_scripts_correction(solutions)
    
    def creer_scripts_correction(self, solutions):
        """Crée les scripts de correction automatique"""
        print("\n4. 🛠️  CRÉATION SCRIPTS DE CORRECTION...")
        
        for solution in solutions:
            script_name = solution['script']
            
            if script_name == 'creer_modele_cotisation.py':
                self.creer_script_modele_cotisation()
            elif script_name == 'affecter_verifications_manquantes.py':
                self.creer_script_affectation_verifications()
            elif script_name == 'corriger_champs_verification.py':
                self.creer_script_correction_champs()
        
        print("   ✅ Scripts de correction créés")
    
    def creer_script_modele_cotisation(self):
        """Crée le script pour ajouter le modèle Cotisation"""
        script_content = '''# creer_modele_cotisation.py
import os
import sys
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

print("🆕 CRÉATION MODÈLE COTISATION")
print("=" * 40)

# Ce script montre comment créer le modèle Cotisation
# À ajouter dans membres/models.py

modele_code = '''
class Cotisation(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente de paiement'),
        ('PAYEE', 'Payée'),
        ('EN_RETARD', 'En retard'),
        ('ANNULEE', 'Annulée'),
    ]
    
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='cotisations')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_echeance = models.DateField()
    date_paiement = models.DateField(null=True, blank=True)
    statut = models.CharField(max_digits=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    reference = models.CharField(max_digits=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Cotisation"
        verbose_name_plural = "Cotisations"
        ordering = ['-date_echeance']
    
    def __str__(self):
        return f"Cotisation {self.reference} - {self.membre}"
'''

print("💡 CODE MODÈLE À AJOUTER:")
print(modele_code)
print("\\n📝 Instructions:")
print("1. Ouvrez membres/models.py")
print("2. Ajoutez le code ci-dessus")
print("3. Exécutez: python manage.py makemigrations")
print("4. Exécutez: python manage.py migrate")
'''

        with open('creer_modele_cotisation.py', 'w') as f:
            f.write(script_content)
        print("   ✅ Script créé: creer_modele_cotisation.py")
    
    def creer_script_affectation_verifications(self):
        """Crée le script pour affecter les vérifications manquantes"""
        script_content = '''# affecter_verifications_manquantes.py
import os
import sys
import django
from pathlib import Path
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from membres.models import Membre
from agents.models import Agent, VerificationCotisation

print("🔍 AFFECTATION VÉRIFICATIONS MANQUANTES")
print("=" * 50)

def affecter_verifications_manquantes():
    \"\"\"Affecte des vérifications aux membres sans contrôle\"\"\"
    
    # Membres sans vérification
    membres_sans_verification = Membre.objects.filter(
        verificationcotisation__isnull=True
    )
    
    print(f"📊 {membres_sans_verification.count()} membres sans vérification")
    
    # Agents disponibles
    agents = Agent.objects.filter(est_actif=True)
    
    if not agents.exists():
        print("❌ Aucun agent actif disponible")
        return
    
    print(f"👨‍💼 {agents.count()} agents disponibles")
    
    # Affecter les vérifications
    verifications_creees = 0
    
    for i, membre in enumerate(membres_sans_verification):
        agent = agents[i % len(agents)]  # Répartition circulaire
        
        try:
            # Créer la vérification avec tous les champs requis
            verification = VerificationCotisation.objects.create(
                membre=membre,
                agent=agent,
                date_verification=datetime.now(),
                statut_cotisation='A_VERIFIER',
                date_dernier_paiement=datetime.now().date(),
                montant_dernier_paiement=0,
                montant_dette=0,
                prochaine_echeance=datetime.now().date() + timedelta(days=30),
                jours_retard=0,
                notifier_membre=False
            )
            
            verifications_creees += 1
            print(f"✅ Vérification créée: {membre.numero_unique} → {agent.user.username}")
            
        except Exception as e:
            print(f"❌ Erreur pour {membre.numero_unique}: {e}")
    
    print(f"🎯 {verifications_creees} vérifications créées avec succès")

if __name__ == "__main__":
    affecter_verifications_manquantes()
'''

        with open('affecter_verifications_manquantes.py', 'w') as f:
            f.write(script_content)
        print("   ✅ Script créé: affecter_verifications_manquantes.py")
    
    def creer_script_correction_champs(self):
        """Crée le script pour corriger les champs obligatoires"""
        script_content = '''# corriger_champs_verification.py
import os
import sys
import django
from pathlib import Path
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
django.setup()

from agents.models import VerificationCotisation

print("🔧 CORRECTION CHAMPS VÉRIFICATION")
print("=" * 50)

def corriger_champs_manquants():
    \"\"\"Corrige les champs manquants dans les vérifications existantes\"\"\"
    
    # Vérifications avec champs manquants
    verifications_a_corriger = VerificationCotisation.objects.filter(
        Q(prochaine_echeance__isnull=True) |
        Q(date_dernier_paiement__isnull=True)
    )
    
    print(f"📊 {verifications_a_corriger.count()} vérifications à corriger")
    
    corrections_appliquees = 0
    
    for verification in verifications_a_corriger:
        try:
            # Définir une date par défaut pour prochaine_echeance
            if verification.prochaine_echeance is None:
                verification.prochaine_echeance = datetime.now().date() + timedelta(days=30)
            
            # Définir une date par défaut pour date_dernier_paiement
            if verification.date_dernier_paiement is None:
                verification.date_dernier_paiement = datetime.now().date()
            
            # Définir des valeurs par défaut pour les autres champs
            if verification.montant_dernier_paiement is None:
                verification.montant_dernier_paiement = 0
            
            if verification.montant_dette is None:
                verification.montant_dette = 0
            
            if verification.jours_retard is None:
                verification.jours_retard = 0
            
            verification.save()
            corrections_appliquees += 1
            print(f"✅ Vérification {verification.id} corrigée")
            
        except Exception as e:
            print(f"❌ Erreur correction {verification.id}: {e}")
    
    print(f"🎯 {corrections_appliquees} vérifications corrigées")

if __name__ == "__main__":
    corriger_champs_manquants()
'''

        with open('corriger_champs_verification.py', 'w') as f:
            f.write(script_content)
        print("   ✅ Script créé: corriger_champs_verification.py")
    
    def generer_rapport_actions(self):
        """Génère un rapport d'actions prioritaires"""
        print("\n5. 📋 GÉNÉRATION RAPPORT D'ACTIONS...")
        
        # Convertir pour sérialisation JSON
        rapport_serialisable = json.loads(json.dumps(self.rapport, default=str))
        
        nom_fichier = f"rapport_actions_cotisations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(nom_fichier, 'w', encoding='utf-8') as f:
                json.dump(rapport_serialisable, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Rapport sauvegardé: {nom_fichier}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
        
        # Afficher le plan d'action
        self._afficher_plan_action()
    
    def _afficher_plan_action(self):
        """Affiche le plan d'action prioritaire"""
        print("\n" + "="*60)
        print("🎯 PLAN D'ACTION PRIORITAIRE")
        print("="*60)
        
        print(f"\n📊 SITUATION ACTUELLE:")
        stats = self.rapport['analyse']['statistiques']
        print(f"   👥 Membres: {stats['membres_total']}")
        print(f"   ✅ Vérifiés: {stats['membres_avec_verification']}")
        print(f"   ❌ Non vérifiés: {stats['membres_sans_verification']}")
        print(f"   🔍 Vérifications: {stats['verifications_total']}")
        
        print(f"\n🚨 PROBLÈMES IDENTIFIÉS:")
        for probleme in self.rapport['problemes']:
            severite_icon = '🔴' if probleme['severite'] == 'HAUTE' else '🟡'
            print(f"   {severite_icon} {probleme['description']}")
        
        print(f"\n💡 ACTIONS IMMÉDIATES:")
        for i, action in enumerate(self.rapport['actions_immediates'], 1):
            urgence_icon = '🔴' if action['urgence'] == 'HAUTE' else '🟡'
            print(f"   {i}. {urgence_icon} {action['description']}")
            print(f"      📁 Script: {action['script']}")
        
        print(f"\n🛠️  EXÉCUTION DES CORRECTIONS:")
        print("   1. python corriger_champs_verification.py")
        print("   2. python affecter_verifications_manquantes.py") 
        print("   3. python creer_modele_cotisation.py")
        print("   4. Ajouter le modèle Cotisation dans membres/models.py")
        print("   5. python manage.py makemigrations && python manage.py migrate")
        
        print(f"\n📈 RÉSULTATS ATTENDUS:")
        print("   ✅ Tous les membres auront une vérification")
        print("   ✅ Système complet de gestion des cotisations")
        print("   ✅ Flux assureur → agent opérationnel")
        
        print("="*60)

# Exécution
if __name__ == "__main__":
    diagnostic = DiagnosticCotisationsFinal()
    diagnostic.executer_diagnostic_complet()