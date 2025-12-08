# diagnostic_cotisations_final.py - VERSION CORRIGÉE
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
            self.analyser_structure_actuelle()
            self.diagnostiquer_problemes_specifiques()
            self.proposer_solutions_immediates()
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
            
            self.rapport['analyse']['statistiques'] = stats
            
        except Exception as e:
            print(f"   ❌ Erreur analyse structure: {e}")
    
    def diagnostiquer_problemes_specifiques(self):
        """Diagnostique les problèmes spécifiques identifiés"""
        print("\n2. 🚨 DIAGNOSTIC PROBLÈMES SPÉCIFIQUES...")
        
        problemes = []
        
        try:
            from membres.models import Membre
            from agents.models import VerificationCotisation
            
            # Membres sans vérification
            membres_sans_verification = Membre.objects.filter(
                verificationcotisation__isnull=True
            )
            
            if membres_sans_verification.exists():
                probleme = {
                    'type': 'MEMBRES_SANS_CONTROLE',
                    'description': f'{membres_sans_verification.count()} membres sans vérification',
                    'severite': 'MOYENNE'
                }
                problemes.append(probleme)
                print(f"   🔴 {probleme['description']}")
            
            self.rapport['problemes'] = problemes
            
        except Exception as e:
            print(f"   ❌ Erreur diagnostic problèmes: {e}")
    
    def proposer_solutions_immediates(self):
        """Propose des solutions immédiates aux problèmes identifiés"""
        print("\n3. 💡 PROPOSITION SOLUTIONS IMMÉDIATES...")
        
        solutions = [
            {
                'action': 'CRÉER_MODÈLE_COTISATION',
                'description': 'Créer le modèle Cotisation dans membres/models.py',
                'urgence': 'HAUTE',
                'script': 'creer_modele_cotisation.py'
            },
            {
                'action': 'AFFECTER_VERIFICATIONS_MANQUANTES',
                'description': 'Assigner des agents pour vérifier les membres sans contrôle',
                'urgence': 'MOYENNE',
                'script': 'affecter_verifications_manquantes.py'
            }
        ]
        
        self.rapport['actions_immediates'] = solutions
        self.creer_scripts_correction(solutions)
    
    def creer_scripts_correction(self, solutions):
        """Crée les scripts de correction automatique"""
        print("\n4. 🛠️  CRÉATION SCRIPTS DE CORRECTION...")
        
        for solution in solutions:
            if solution['script'] == 'creer_modele_cotisation.py':
                self.creer_script_modele_cotisation()
            elif solution['script'] == 'affecter_verifications_manquantes.py':
                self.creer_script_affectation_verifications()
        
        print("   ✅ Scripts de correction créés")
    
    def creer_script_modele_cotisation(self):
        """Crée le script pour ajouter le modèle Cotisation"""
        script_content = '''# creer_modele_cotisation.py
print("🆕 CRÉATION MODÈLE COTISATION")
print("Ajouter le modèle Cotisation dans membres/models.py")
'''
        with open('creer_modele_cotisation.py', 'w') as f:
            f.write(script_content)
        print("   ✅ Script créé: creer_modele_cotisation.py")
    
    def creer_script_affectation_verifications(self):
        """Crée le script pour affecter les vérifications manquantes"""
        script_content = '''# affecter_verifications_manquantes.py
print("🔍 AFFECTATION VÉRIFICATIONS MANQUANTES")
print("Ce script affectera des agents aux membres sans vérification")
'''
        with open('affecter_verifications_manquantes.py', 'w') as f:
            f.write(script_content)
        print("   ✅ Script créé: affecter_verifications_manquantes.py")
    
    def generer_rapport_actions(self):
        """Génère un rapport d'actions prioritaires"""
        print("\n5. 📋 GÉNÉRATION RAPPORT D'ACTIONS...")
        
        nom_fichier = f"rapport_actions_cotisations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(nom_fichier, 'w', encoding='utf-8') as f:
                json.dump(self.rapport, f, indent=2, ensure_ascii=False, default=str)
            print(f"💾 Rapport sauvegardé: {nom_fichier}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
        
        self._afficher_plan_action()
    
    def _afficher_plan_action(self):
        """Affiche le plan d'action prioritaire"""
        print("\n" + "="*60)
        print("🎯 PLAN D'ACTION PRIORITAIRE")
        print("="*60)
        
        print("\n💡 ACTIONS IMMÉDIATES:")
        for i, action in enumerate(self.rapport['actions_immediates'], 1):
            urgence_icon = '🔴' if action['urgence'] == 'HAUTE' else '🟡'
            print(f"   {i}. {urgence_icon} {action['description']}")
            print(f"      📁 Script: {action['script']}")

# Exécution
if __name__ == "__main__":
    diagnostic = DiagnosticCotisationsFinal()
    diagnostic.executer_diagnostic_complet()
