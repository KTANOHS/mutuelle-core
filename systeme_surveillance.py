# systeme_surveillance.py
import os
import sys
from pathlib import Path

print("🎯 SYSTÈME DE SURVEILLANCE COMPLET - MUTUELLE CORE")
print("=" * 60)

class SystemeSurveillance:
    def __init__(self):
        self.modules = {
            '1': {'nom': '🔍 Surveillance Simple', 'script': 'surveillance_simple.py'},
            '2': {'nom': '📊 Diagnostic Complet', 'script': 'diagnostic_sync_final.py'},
            '3': {'nom': '🔄 Correcteur Urgence', 'script': 'correcteur_sync_urgence.py'},
            '4': {'nom': '📈 Monitoring Long Terme', 'script': 'monitoring_long_terme.py'},
            '5': {'nom': '📅 Surveillance Hebdomadaire', 'script': 'surveillance_hebdomadaire.py'},
            '6': {'nom': '📋 Rapport Performance', 'script': 'rapport_performance_mensuel.py'},
            '7': {'nom': '🔧 Adaptateur Évolution', 'script': 'adaptateur_evolution.py'},
            '8': {'nom': '✅ Vérification Installation', 'script': 'verification_installation_complete.py'},
            '9': {'nom': '🛠️ Planificateur', 'script': 'planificateur_surveillance.py'}
        }
    
    def afficher_menu(self):
        """Affiche le menu principal"""
        print("\n📋 MENU PRINCIPAL - SYSTÈME DE SURVEILLANCE")
        print("=" * 50)
        
        for key, module in self.modules.items():
            print(f"{key}. {module['nom']}")
        
        print("0. 🚪 Quitter")
        print("=" * 50)
    
    def lancer_module(self, choix):
        """Lance le module sélectionné"""
        if choix == '0':
            print("👋 Au revoir!")
            return False
        
        if choix in self.modules:
            module = self.modules[choix]
            script = module['script']
            
            if Path(script).exists():
                print(f"\n🚀 Lancement: {module['nom']}...")
                os.system(f'python {script}')
            else:
                print(f"❌ Script non trouvé: {script}")
        else:
            print("❌ Option invalide")
        
        input("\n↵ Appuyez sur Entrée pour continuer...")
        return True
    
    def demarrer(self):
        """Démarre le système de surveillance"""
        print("🎯 Bienvenue dans le système de surveillance Mutuelle Core!")
        print("💡 Tous les outils de diagnostic et maintenance sont regroupés ici.")
        
        while True:
            self.afficher_menu()
            choix = input("\nChoisir une option (0-9): ").strip()
            
            if not self.lancer_module(choix):
                break

# Exécution
if __name__ == "__main__":
    systeme = SystemeSurveillance()
    systeme.demarrer()