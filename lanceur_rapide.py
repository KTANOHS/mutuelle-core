# lanceur_rapide.py
import os
import sys
import subprocess
from pathlib import Path

print("⚡ LANCEUR RAPIDE - SURVEILLANCE MUTUELLE CORE")
print("=" * 50)

class LanceurRapide:
    def __init__(self):
        self.scripts = {
            '1': {'nom': '🚀 Surveillance Express', 'cmd': 'surveillance_simple.py', 'args': ''},
            '2': {'nom': '🔍 Diagnostic Flash', 'cmd': 'diagnostic_sync_final.py', 'args': ''},
            '3': {'nom': '📊 Stats Rapides', 'cmd': 'verification_post_correction.py', 'args': ''},
            '4': {'nom': '📈 Monitoring 30s', 'cmd': 'monitoring_long_terme.py', 'args': '--rapide'},
            '5': {'nom': '🔄 Correcteur Auto', 'cmd': 'correcteur_sync_urgence.py', 'args': '--test'},
            '6': {'nom': '📋 Rapport Instantané', 'cmd': 'synthese_finale.py', 'args': ''}
        }
    
    def afficher_menu(self):
        print("\n⚡ ACTIONS RAPIDES (30 secondes max)")
        print("=" * 40)
        for key, script in self.scripts.items():
            print(f"{key}. {script['nom']}")
        print("0. 🔙 Retour")
        print("=" * 40)
    
    def executer_commande_rapide(self, commande, args=""):
        """Exécute une commande avec timeout"""
        try:
            cmd = f"timeout 30 python {commande} {args}".strip()
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Terminé avec succès!")
                # Afficher les 10 premières lignes du résultat
                lines = result.stdout.split('\n')[:10]
                for line in lines:
                    if line.strip():
                        print(f"   {line}")
            else:
                print("❌ Erreur d'exécution")
                if result.stderr:
                    print(f"   Erreur: {result.stderr[:100]}...")
                    
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    def demarrer(self):
        while True:
            self.afficher_menu()
            choix = input("\nChoisir une action (0-6): ").strip()
            
            if choix == '0':
                break
            elif choix in self.scripts:
                script = self.scripts[choix]
                print(f"\n🚀 Lancement: {script['nom']}...")
                self.executer_commande_rapide(script['cmd'], script['args'])
                input("\n↵ Appuyez sur Entrée pour continuer...")
            else:
                print("❌ Option invalide")

if __name__ == "__main__":
    lanceur = LanceurRapide()
    lanceur.demarrer()