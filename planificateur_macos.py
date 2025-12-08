# planificateur_macos.py
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

print("🍎 PLANIFICATEUR macOS - SURVEILLANCE AUTOMATIQUE")
print("=" * 60)

class PlanificateurMacOS:
    def __init__(self):
        self.scripts_dir = Path(__file__).parent
        self.launch_agents_dir = Path.home() / "Library" / "LaunchAgents"
        self.launch_agents_dir.mkdir(exist_ok=True)
    
    def creer_plist_surveillance(self):
        """Crée un fichier plist pour launchd (alternative à cron sur macOS)"""
        plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.mutuelle-core.surveillance</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{self.scripts_dir / "surveillance_hebdomadaire.py"}</string>
    </array>
    
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
        <key>Weekday</key>
        <integer>1</integer>
    </dict>
    
    <key>StandardOutPath</key>
    <string>/tmp/mutuelle_surveillance.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/mutuelle_surveillance_error.log</string>
    
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>'''
        
        plist_file = self.launch_agents_dir / "com.mutuelle-core.surveillance.plist"
        
        with open(plist_file, 'w') as f:
            f.write(plist_content)
        
        print(f"✅ Fichier plist créé: {plist_file}")
        return plist_file
    
    def creer_script_automation_macos(self):
        """Crée un script d'automatisation pour macOS"""
        script_content = f'''#!/bin/bash
# automation_surveillance_macos.sh
# Script d'automatisation pour macOS - Surveillance Mutuelle Core

SCRIPT_DIR="{self.scripts_dir}"
VENV_PYTHON="{sys.executable}"
LOG_DIR="/tmp/mutuelle_logs"

mkdir -p "$LOG_DIR"

echo "🤖 Démarrage automatique surveillance - $(date)"

# Surveillance quotidienne (8h00)
if [ "$1" = "quotidien" ] || [ -z "$1" ]; then
    echo "🔍 Surveillance quotidienne..."
    "$VENV_PYTHON" "$SCRIPT_DIR/surveillance_simple.py" --mode auto >> "$LOG_DIR/surveillance_quotidienne.log" 2>&1
fi

# Diagnostic hebdomadaire (lundi 9h00)
if [ "$1" = "hebdomadaire" ] || [ -z "$1" ]; then
    echo "📊 Diagnostic hebdomadaire..."
    "$VENV_PYTHON" "$SCRIPT_DIR/surveillance_hebdomadaire.py" >> "$LOG_DIR/diagnostic_hebdo.log" 2>&1
fi

# Rapport mensuel (1er du mois)
if [ "$1" = "mensuel" ] || [ -z "$1" ]; then
    echo "📈 Rapport mensuel..."
    "$VENV_PYTHON" "$SCRIPT_DIR/rapport_performance_mensuel.py" >> "$LOG_DIR/rapport_mensuel.log" 2>&1
fi

echo "✅ Automatisation terminée - $(date)"
'''
        
        script_file = "automation_surveillance_macos.sh"
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        # Rendre exécutable
        os.chmod(script_file, 0o755)
        print(f"✅ Script d'automatisation créé: {script_file}")
        return script_file
    
    def creer_raccourci_ical(self):
        """Crée des instructions pour planifier avec iCal (Apple Calendar)"""
        instructions = f'''
📅 PLANIFICATION AVEC iCAL (CALENDRIER APPLE)

Pour une surveillance automatique sur macOS, vous pouvez utiliser le Calendrier :

1. 🗓️ Ouvrez l'application "Calendrier"
2. ➕ Créez un nouveau calendrier "Surveillance Mutuelle"
3. 📅 Ajoutez les événements récurrents :

   🔸 QUOTIDIEN (8h00)
   - Ouvrir le Terminal
   - Commande: cd "{self.scripts_dir}" && {sys.executable} surveillance_simple.py --mode auto

   🔸 HEBDOMADAIRE (Lundi 9h00)  
   - Ouvrir le Terminal
   - Commande: cd "{self.scripts_dir}" && {sys.executable} surveillance_hebdomadaire.py

   🔸 MENSUEL (1er du mois 10h00)
   - Ouvrir le Terminal
   - Commande: cd "{self.scripts_dir}" && {sys.executable} rapport_performance_mensuel.py

4. 🔔 Configurez des alertes pour recevoir des notifications
'''
        
        with open('instructions_ical_surveillance.txt', 'w') as f:
            f.write(instructions)
        
        print("✅ Instructions iCal créées: instructions_ical_surveillance.txt")
        return instructions
    
    def installer_automation(self):
        """Installe le système d'automatisation macOS"""
        print("🍎 Installation automatisation macOS...")
        
        # 1. Créer le plist pour launchd
        plist_file = self.creer_plist_surveillance()
        
        # 2. Créer le script d'automatisation
        script_auto = self.creer_script_automation_macos()
        
        # 3. Créer les instructions iCal
        instructions = self.creer_raccourci_ical()
        
        print("\n🎯 AUTOMATISATION macOS CONFIGURÉE!")
        print("💡 Options disponibles:")
        print("   1. LaunchAgent (Recommandé):")
        print(f"      launchctl load {plist_file}")
        print("   2. Script shell:")
        print(f"      ./{script_auto} quotidien")
        print("   3. Calendrier iCal:")
        print("      Voir instructions_ical_surveillance.txt")
        
        return True

# Exécution
if __name__ == "__main__":
    planificateur = PlanificateurMacOS()
    planificateur.installer_automation()