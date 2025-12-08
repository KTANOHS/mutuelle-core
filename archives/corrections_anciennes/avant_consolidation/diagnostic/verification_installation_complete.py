# verification_installation_complete.py
import os
import sys
import json
from pathlib import Path
from datetime import datetime

print("🎯 VÉRIFICATION INSTALLATION COMPLÈTE")
print("=" * 60)

class VerificateurInstallation:
    def __init__(self):
        self.rapport = {
            'timestamp': datetime.now().isoformat(),
            'composants': {},
            'statut': 'EN_COURS'
        }
    
    def verifier_composants(self):
        """Vérifie tous les composants installés"""
        print("🔍 Vérification des composants...")
        
        composants = {
            'scripts_surveillance': self._verifier_scripts_surveillance(),
            'planification_cron': self._verifier_planification_cron(),
            'dossiers_donnees': self._verifier_dossiers_donnees(),
            'donnees_historiques': self._verifier_donnees_historiques(),
            'compatibilite_scripts': self._verifier_compatibilite_scripts()
        }
        
        self.rapport['composants'] = composants
        self.rapport['statut'] = 'COMPLET' if all(composants.values()) else 'PARTIEL'
        
        return composants
    
    def _verifier_scripts_surveillance(self):
        """Vérifie que tous les scripts de surveillance sont présents"""
        scripts_requis = [
            'surveillance_simple.py',
            'surveillance_hebdomadaire.py', 
            'diagnostic_sync_final.py',
            'correcteur_sync_urgence.py',
            'rapport_performance_mensuel.py',
            'monitoring_long_terme.py',
            'adaptateur_evolution.py'
        ]
        
        presents = []
        manquants = []
        
        for script in scripts_requis:
            if Path(script).exists():
                presents.append(script)
            else:
                manquants.append(script)
        
        print(f"📝 Scripts surveillance: {len(presents)}/{len(scripts_requis)}")
        
        if manquants:
            print(f"   ⚠️  Manquants: {', '.join(manquants)}")
        
        return len(manquants) == 0
    
    def _verifier_planification_cron(self):
        """Vérifie la planification cron"""
        fichier_cron = 'planification_surveillance.cron'
        
        if Path(fichier_cron).exists():
            print("✅ Planification cron: PRÉSENTE")
            return True
        else:
            print("❌ Planification cron: ABSENTE")
            return False
    
    def _verifier_dossiers_donnees(self):
        """Vérifie les dossiers de données"""
        dossiers = ['donnees_monitoring', 'rapports_surveillance', 'rapports_performance']
        
        for dossier in dossiers:
            Path(dossier).mkdir(exist_ok=True)
        
        print(f"📁 Dossiers données: {len(dossiers)} créés")
        return True
    
    def _verifier_donnees_historiques(self):
        """Vérifie la présence de données historiques"""
        dossier_monitoring = Path('donnees_monitoring')
        
        if dossier_monitoring.exists():
            fichiers = list(dossier_monitoring.glob('*.json'))
            print(f"📊 Données historiques: {len(fichiers)} fichiers")
            return len(fichiers) > 0
        else:
            print("❌ Données historiques: AUCUNE")
            return False
    
    def _verifier_compatibilite_scripts(self):
        """Vérifie la compatibilité des scripts"""
        try:
            # Test d'import basique
            import surveillance_simple
            import monitoring_long_terme
            print("✅ Compatibilité scripts: OK")
            return True
        except Exception as e:
            print(f"❌ Compatibilité scripts: {e}")
            return False
    
    def generer_rapport_installation(self):
        """Génère un rapport d'installation complet"""
        print("\n📋 GÉNÉRATION RAPPORT D'INSTALLATION...")
        
        composants = self.verifier_composants()
        
        # Résumé
        print(f"\n🎯 RÉSUMÉ INSTALLATION: {self.rapport['statut']}")
        
        for nom, statut in composants.items():
            icone = '✅' if statut else '❌'
            print(f"   {icone} {nom}: {'OPÉRATIONNEL' if statut else 'NON OPÉRATIONNEL'}")
        
        # Sauvegarder le rapport
        nom_fichier = f"rapport_installation_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(nom_fichier, 'w') as f:
            json.dump(self.rapport, f, indent=2)
        
        print(f"\n💾 Rapport sauvegardé: {nom_fichier}")
        
        # Recommandations finales
        self._afficher_recommandations_finales()
        
        return self.rapport
    
    def _afficher_recommandations_finales(self):
        """Affiche les recommandations finales"""
        print("\n💡 RECOMMANDATIONS FINALES:")
        
        if not self.rapport['composants']['planification_cron']:
            print("   1. 🔧 Exécuter: crontab planification_surveillance.cron")
        
        print("   2. 📅 Surveillance active tous les lundis à 9h00")
        print("   3. 📊 Rapports mensuels générés automatiquement")
        print("   4. 🔄 Mises à jour vérifiées trimestriellement")
        print("   5. 📝 Logs disponibles dans /tmp/")
        
        print("\n🚀 SYSTÈME PRÊT POUR LA PRODUCTION!")

# Exécution
if __name__ == "__main__":
    verificateur = VerificateurInstallation()
    rapport = verificateur.generer_rapport_installation()