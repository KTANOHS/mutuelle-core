# lanceur_rapide_corrige.py
import os
import sys
import subprocess
import threading
from pathlib import Path

print("⚡ LANCEUR RAPIDE CORRIGÉ - SURVEILLANCE MUTUELLE CORE")
print("=" * 50)

class LanceurRapideCorrige:
    def __init__(self):
        self.scripts = {
            '1': {'nom': '🚀 Surveillance Express', 'cmd': 'surveillance_simple.py', 'args': '--mode auto'},
            '2': {'nom': '🔍 Diagnostic Flash', 'cmd': 'diagnostic_sync_final.py', 'args': ''},
            '3': {'nom': '📊 Stats Rapides', 'cmd': 'verification_post_correction.py', 'args': ''},
            '4': {'nom': '📈 Monitoring 30s', 'cmd': 'monitoring_long_terme.py', 'args': '1'},
            '5': {'nom': '🔄 Correcteur Auto', 'cmd': 'correcteur_sync_urgence.py', 'args': '--test'},
            '6': {'nom': '📋 Rapport Instantané', 'cmd': 'synthese_finale.py', 'args': ''}
        }
    
    def afficher_menu(self):
        print("\n⚡ ACTIONS RAPIDES (macOS Optimisé)")
        print("=" * 40)
        for key, script in self.scripts.items():
            print(f"{key}. {script['nom']}")
        print("0. 🔙 Retour")
        print("=" * 40)
    
    def executer_avec_timeout_macos(self, commande, args="", timeout=30):
        """Exécute une commande avec timeout compatible macOS"""
        try:
            full_cmd = f"python {commande} {args}".strip()
            
            # Méthode compatible macOS
            process = subprocess.Popen(
                full_cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            try:
                stdout, stderr = process.communicate(timeout=timeout)
                returncode = process.returncode
                
                if returncode == 0:
                    print("✅ Terminé avec succès!")
                    # Afficher les premières lignes
                    lines = stdout.split('\n')[:8]
                    for line in lines:
                        if line.strip() and not line.startswith('🛑'):
                            print(f"   {line}")
                else:
                    print("⚠️  Achevé avec avertissements")
                    if stderr:
                        error_lines = stderr.split('\n')[:3]
                        for line in error_lines:
                            if line.strip():
                                print(f"   ⚠️  {line}")
                                
            except subprocess.TimeoutExpired:
                process.kill()
                print("⏰ Timeout - Processus arrêté après 30s")
                return
                
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
                self.executer_avec_timeout_macos(script['cmd'], script['args'])
                input("\n↵ Appuyez sur Entrée pour continuer...")
            else:
                print("❌ Option invalide")

if __name__ == "__main__":
    lanceur = LanceurRapideCorrige()
    lanceur.demarrer()